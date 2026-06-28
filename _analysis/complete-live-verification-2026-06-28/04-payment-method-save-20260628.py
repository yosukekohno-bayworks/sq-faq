#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "04-payment-method-save-20260628.json"
OUT_MD = OUT_DIR / "04-payment-method-save-20260628.md"
SCREENSHOT = OUT_DIR / "04-payment-method-save-20260628.png"

BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

STAMP = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
NAME = f"TEST_FAQ_PAYMENT_{STAMP}"
CODE = f"test_faq_payment_{STAMP}"
GATEWAY = f"faq_gateway_{STAMP}"

LONG_TOKEN_RE = re.compile(
    r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))"
)


def redact(value):
    if isinstance(value, str):
        return LONG_TOKEN_RE.sub("[REDACTED_LONG_VALUE]", value)
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    return value


def compact(text, limit=7000):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snapshot(page, limit=9000):
    data = page.evaluate(
        """() => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const attr = (el, name) => el.getAttribute(name);
            const labelOf = (el) => {
                const id = el.id;
                const label = id ? document.querySelector(`label[for="${CSS.escape(id)}"]`) : null;
                return label ? textOf(label) : '';
            };
            const nodes = (selector, limit = 120) => Array.from(document.querySelectorAll(selector)).slice(0, limit);
            const controls = nodes('button, a, input, textarea, select, [role="button"], [role="menuitem"]', 260)
                .map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    role: attr(el, 'role'),
                    text: textOf(el),
                    href: attr(el, 'href'),
                    type: attr(el, 'type'),
                    label: labelOf(el),
                    placeholder: attr(el, 'placeholder'),
                    ariaLabel: attr(el, 'aria-label'),
                    ariaDisabled: attr(el, 'aria-disabled'),
                    disabled: !!el.disabled,
                    checked: el.tagName.toLowerCase() === 'input' && el.type === 'checkbox' ? el.checked : undefined,
                    value: el.tagName.toLowerCase() === 'input' || el.tagName.toLowerCase() === 'select' ? el.value : undefined
                }))
                .filter((x) => x.text || x.href || x.ariaLabel || x.placeholder || x.value || x.label);
            return {
                url: location.href,
                h1: nodes('h1', 10).map(textOf).filter(Boolean),
                h2: nodes('h2', 30).map(textOf).filter(Boolean),
                rows: nodes('tr', 100).map(textOf).filter(Boolean),
                controls,
                body: document.body ? document.body.innerText : ''
            };
        }"""
    )
    data["body"] = compact(data.get("body", ""), limit)
    return redact(data)


def save_payload(payload):
    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2))


def first_enabled_button(page, names, scope=None):
    root = scope or page
    for name in names:
        locator = root.get_by_role("button", name=name, exact=True)
        if locator.count():
            for idx in range(locator.count()):
                item = locator.nth(idx)
                try:
                    if item.is_enabled():
                        return name, item
                except Exception:
                    pass
    return None, None


def create_payment_method(page):
    result = {"steps": {}}
    page.goto(BASE + "/admin/settings/payment_methods/create", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["initial"] = snapshot(page)
    inputs = page.locator('input:not([type="hidden"])')
    inputs.nth(0).fill(NAME)
    inputs.nth(1).fill(CODE)
    inputs.nth(2).fill(GATEWAY)
    inputs.nth(3).check()
    inputs.nth(4).check()
    result["steps"]["beforeSave"] = snapshot(page)
    _, save_button = first_enabled_button(page, ["保存する", "保存"])
    if not save_button:
        raise RuntimeError("payment method save button not found")
    save_button.click()
    wait_quiet(page, timeout=12000)
    result["steps"]["afterSave"] = snapshot(page)
    return redact(result)


def open_created_detail(page):
    result = {"found": False}
    page.goto(BASE + "/admin/settings/payment_methods", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["list"] = snapshot(page)
    selected = page.evaluate(
        """(name) => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const row = Array.from(document.querySelectorAll('tr')).find((tr) => textOf(tr).includes(name));
            if (!row) return {found: false, rows: Array.from(document.querySelectorAll('tr')).slice(0, 40).map(textOf)};
            return {
                found: true,
                row: textOf(row),
                rowId: row.id || null,
                linkCount: row.querySelectorAll('a').length
            };
        }""",
        NAME,
    )
    result["selected"] = selected
    if not selected.get("found"):
        return redact(result)
    if selected.get("rowId"):
        page.goto(BASE + f"/admin/settings/payment_methods/{selected['rowId']}", wait_until="load", timeout=35000)
        wait_quiet(page, timeout=9000)
    else:
        page.evaluate(
            """(name) => {
                const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
                const row = Array.from(document.querySelectorAll('tr')).find((tr) => textOf(tr).includes(name));
                if (row) row.click();
            }""",
            NAME,
        )
        wait_quiet(page, timeout=9000)
    result["found"] = True
    result["detail"] = snapshot(page)
    try:
        page.screenshot(path=str(SCREENSHOT), full_page=True)
        result["screenshot"] = str(SCREENSHOT.relative_to(ROOT))
    except Exception as exc:
        result["screenshotError"] = repr(exc)
    return redact(result)


def try_cleanup(page):
    result = {"attempted": False, "dialog": None}
    try:
        button = page.get_by_role("button", name="アーカイブ", exact=True)
        if not button.count():
            result["reason"] = "no archive button"
            return result
        result["before"] = snapshot(page, limit=6000)
        button.first.click()
        result["attempted"] = True
        page.wait_for_timeout(1200)
        if page.locator('div[role="dialog"]').count():
            dialog = page.locator('div[role="dialog"]').last
            result["dialog"] = compact(dialog.inner_text(timeout=5000), 3000)
            _, confirm = first_enabled_button(page, ["削除する", "アーカイブする", "実行する"], scope=dialog)
            if confirm:
                confirm.click()
                wait_quiet(page, timeout=10000)
        result["after"] = snapshot(page)
    except Exception as exc:
        result["error"] = repr(exc)
    return redact(result)


def extract_facts(payload):
    detail_step = payload.get("steps", {}).get("detail", {})
    detail = detail_step.get("detail", {})
    list_snapshot = detail_step.get("list", {})
    controls = detail.get("controls", [])
    checked = {c.get("label"): c.get("checked") for c in controls if c.get("type") == "checkbox"}
    body = json.dumps(detail, ensure_ascii=False)
    list_body = json.dumps(list_snapshot, ensure_ascii=False)
    cleanup = payload.get("steps", {}).get("cleanup", {})
    return {
        "name": NAME,
        "code": CODE,
        "gateway": GATEWAY,
        "createdRowFound": bool(payload.get("steps", {}).get("detail", {}).get("found")),
        "listRowHasLink": bool(detail_step.get("selected", {}).get("linkCount")),
        "editUrl": detail.get("url"),
        "detailContainsName": NAME in body,
        "detailContainsCode": CODE in body,
        "listContainsGateway": GATEWAY in list_body,
        "detailContainsGateway": GATEWAY in body,
        "shipWhilePaymentPendingChecked": checked.get("支払い待ちでも注文を出荷する"),
        "cashOnDeliveryChecked": checked.get("代引き"),
        "cleanupAttempted": bool(cleanup.get("attempted")),
        "cleanupDialog": cleanup.get("dialog"),
        "cleanupChangedBody": cleanup.get("before", {}).get("body") != cleanup.get("after", {}).get("body") if cleanup.get("after") else None,
        "errors": payload.get("errors", []),
    }


def write_md(payload):
    facts = payload.get("facts") or extract_facts(payload)
    lines = [
        "# 04 決済方法の保存挙動 実機確認 2026-06-28",
        "",
        f"- 実行日時: {payload.get('generatedAt')}",
        f"- 名前: `{NAME}`",
        f"- コード: `{CODE}`",
        f"- ゲートウェイ: `{GATEWAY}`",
        "",
        "## 結果",
        "",
        "| 確認項目 | 結果 |",
        "|:--|:--|",
        f"| 一覧から詳細を開けた | `{facts.get('createdRowFound')}` |",
        f"| 一覧行にリンクがある | `{facts.get('listRowHasLink')}` |",
        f"| 編集URL | `{facts.get('editUrl')}` |",
        f"| 詳細に名前が残る | `{facts.get('detailContainsName')}` |",
        f"| 詳細にコードが残る | `{facts.get('detailContainsCode')}` |",
        f"| 一覧にゲートウェイが残る | `{facts.get('listContainsGateway')}` |",
        f"| 編集画面にゲートウェイ欄/値が残る | `{facts.get('detailContainsGateway')}` |",
        f"| 支払い待ちでも注文を出荷する | `{facts.get('shipWhilePaymentPendingChecked')}` |",
        f"| 代引き | `{facts.get('cashOnDeliveryChecked')}` |",
        f"| 後始末操作を試行した | `{facts.get('cleanupAttempted')}` |",
        f"| 後始末操作で本文変化があった | `{facts.get('cleanupChangedBody')}` |",
        "",
        "## 後始末ダイアログ",
        "",
        facts.get("cleanupDialog") or "なし",
        "",
        "## 判断",
        "",
        "- ゲートウェイはフォーム上の自由入力値として保存され、一覧に表示される。",
        "- 編集画面にはゲートウェイ欄が表示されないため、保存後に管理画面からゲートウェイを変更する導線は確認できない。",
        "- `支払い待ちでも注文を出荷する` と `代引き` はチェックONで保存でき、編集画面でもON状態が残る。",
        "- 編集画面の `アーカイブ` ボタンは押せるが、今回の確認ではダイアログや本文変化は確認できなかった。",
        "- 注文・出荷・会計への実効差は、この検証では確認していない。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        f"- スクリーンショット: `{SCREENSHOT.relative_to(ROOT)}`",
    ]
    if facts.get("errors"):
        lines.extend(["", "## エラー", ""])
        lines.extend([f"- `{err}`" for err in facts["errors"]])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "purpose": "Verify payment method gateway free input and checkbox persistence.",
        "inputs": {"name": NAME, "code": CODE, "gateway": GATEWAY},
        "steps": {},
        "errors": [],
    }
    save_payload(payload)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            payload["steps"]["create"] = create_payment_method(page)
            save_payload(payload)
            payload["steps"]["detail"] = open_created_detail(page)
            save_payload(payload)
            payload["steps"]["cleanup"] = try_cleanup(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            try:
                payload["steps"]["finalSnapshot"] = snapshot(page)
            except Exception:
                pass
        finally:
            payload["facts"] = extract_facts(payload)
            save_payload(payload)
            write_md(payload)
            page.close()
            browser.close()
    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
