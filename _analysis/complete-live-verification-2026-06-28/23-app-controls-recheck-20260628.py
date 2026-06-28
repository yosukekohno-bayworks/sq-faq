#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "23-app-controls-recheck-20260628.json"
OUT_MD = OUT_DIR / "23-app-controls-recheck-20260628.md"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
APP_ROUTE = "/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App"
APP_NAME = "TEST_FAQ_20260624_APP_113636"


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def compact(text, limit=1800):
    return " ".join((text or "").split())[:limit]


def wait_soft(page, ms=1000):
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(ms)


def controls(page):
    return page.evaluate(
        """() => Array.from(document.querySelectorAll('button,a,[role="button"]')).filter((el) => {
            const box = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            return box.width > 0 && box.height > 0 && style.visibility !== 'hidden' && style.display !== 'none';
        }).map((el) => ({
            text: (el.innerText || el.textContent || '').trim(),
            ariaLabel: el.getAttribute('aria-label'),
            href: el.getAttribute('href'),
            disabled: el.disabled || el.getAttribute('aria-disabled') === 'true' || el.className.includes('disabled')
        })).filter((x) => x.text || x.ariaLabel || x.href)"""
    )


def select_options(page):
    return page.evaluate(
        """() => Array.from(document.querySelectorAll('select')).map((select) =>
            Array.from(select.options).map((option) => option.textContent.trim()).filter(Boolean)
        )"""
    )


def record(payload, page, step):
    body = text_of(page)
    payload["steps"].append({
        "step": step,
        "url": page.url,
        "bodySample": compact(body),
        "controls": controls(page),
        "selectOptions": select_options(page),
    })
    write_outputs(payload)


def has_control(payload, step, text):
    for row in payload["steps"]:
        if row["step"] != step:
            continue
        for control in row.get("controls", []):
            if control.get("text") == text or control.get("ariaLabel") == text:
                return True
    return False


def has_any_control(payload, step, words):
    for row in payload["steps"]:
        if row["step"] != step:
            continue
        for control in row.get("controls", []):
            text = f"{control.get('text') or ''} {control.get('ariaLabel') or ''}"
            if any(word in text for word in words):
                return True
    return False


def write_outputs(payload):
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    result = payload.get("result", {})
    md = [
        "# 23 API/Webhook アプリ操作導線再確認 2026-06-28",
        "",
        f"- 対象アプリ: `{APP_NAME}`",
        f"- 対象画面: `{APP_ROUTE}`",
        f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
        "",
        "## 結果",
        "",
        f"- アプリ詳細で削除/失効/再発行導線なし: `{'確認' if result.get('noDeleteReissueOnDetail') else '未確認'}`",
        f"- アプリ一覧カードで削除/失効/再発行導線なし: `{'確認' if result.get('noDeleteReissueOnList') else '未確認'}`",
        f"- Webhook作成後の編集/削除/停止導線なし: `{'確認' if result.get('noWebhookEditDeleteStop') else '未確認'}`",
        f"- リクエストログはTODO表示: `{'確認' if result.get('requestLogTodo') else '未確認'}`",
        f"- Storefrontトークン発行ボタンは表示のみ確認: `{'確認' if result.get('storefrontButtonVisible') else '未確認'}`",
        "",
        "## ステップ",
        "",
    ]
    for step in payload.get("steps", []):
        md.append(f"### {step['step']}")
        md.append("")
        md.append(f"- URL: `{step['url']}`")
        sample = step.get("bodySample", "")
        if sample:
            md.append(f"- 本文抜粋: {sample[:700]}")
        labels = []
        for control in step.get("controls", []):
            label = control.get("text") or control.get("ariaLabel") or control.get("href")
            if label and label not in labels:
                labels.append(label)
        if labels:
            md.append(f"- 操作要素: `{', '.join(labels[:30])}`")
        for opts in step.get("selectOptions", []):
            if opts:
                md.append(f"- select選択肢: `{', '.join(opts)}`")
        md.append("")
    OUT_MD.write_text("\n".join(md) + "\n")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "appRoute": APP_ROUTE,
        "appName": APP_NAME,
        "steps": [],
        "result": {},
    }
    write_outputs(payload)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(f"{BASE}{APP_ROUTE}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            record(payload, page, "app-detail")

            try:
                page.get_by_role("button", name="その他の操作", exact=True).click(timeout=5000)
                wait_soft(page, 500)
                record(payload, page, "app-detail-action-menu")
                page.keyboard.press("Escape")
                wait_soft(page, 300)
            except PlaywrightTimeoutError:
                payload["result"]["detailActionMenuAbsent"] = True

            page.get_by_role("button", name="Webhookを作成する", exact=True).click()
            page.wait_for_selector('div[role="dialog"]', timeout=15000)
            wait_soft(page, 500)
            record(payload, page, "webhook-create-dialog")
            page.keyboard.press("Escape")
            wait_soft(page, 500)

            page.goto(f"{BASE}/admin/settings/apps", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            record(payload, page, "app-list")

            page.goto(f"{BASE}{APP_ROUTE}/admin_api", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            record(payload, page, "request-log")

            forbidden_app = ["削除", "失効", "再発行"]
            forbidden_webhook = ["編集", "削除", "停止", "無効"]
            request_log_text = payload["steps"][-1]["bodySample"]
            no_detail = (
                not has_any_control(payload, "app-detail", forbidden_app)
                and not has_any_control(payload, "app-detail-action-menu", forbidden_app)
            )
            payload["result"] = {
                **payload.get("result", {}),
                "noDeleteReissueOnDetail": no_detail,
                "noDeleteReissueOnList": not has_any_control(payload, "app-list", forbidden_app),
                "noWebhookEditDeleteStop": not has_any_control(payload, "app-detail", forbidden_webhook),
                "requestLogTodo": "TODO" in request_log_text and "リクエストログ" in request_log_text,
                "storefrontButtonVisible": has_control(payload, "app-detail", "トークンを発行する"),
            }
        finally:
            write_outputs(payload)
            if not page.is_closed():
                page.close()
    if not all(payload["result"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
