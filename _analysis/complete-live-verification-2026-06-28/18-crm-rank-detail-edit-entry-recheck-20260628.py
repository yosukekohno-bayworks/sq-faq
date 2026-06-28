#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "18-crm-rank-detail-edit-entry-recheck-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
RULE_NAME = "TEST_FAQ_会員ランク算出ルール"
RULE_ROUTE = "/admin/customer_rank_calculation_rules/37f5da19-1289-5ff2-99ac-1b39ed8dfeaa_CustomerRankCalculationRule"
UPDATE_ROUTE = f"{RULE_ROUTE}/update"


def compact(text, limit=1600):
    return " ".join((text or "").split())[:limit]


def wait_soft(page, ms=1000):
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(ms)


def visible_snapshot(page):
    return page.evaluate(
        """() => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const visible = (el) => {
                const box = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return box.width > 0 && box.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
            };
            return {
                url: location.href,
                title: document.title,
                h1: Array.from(document.querySelectorAll('h1')).map(text).filter(Boolean),
                labels: Array.from(document.querySelectorAll('label')).filter(visible).map(text).filter(Boolean),
                bodySample: text(document.body).slice(0, 5000),
                visibleLinks: Array.from(document.querySelectorAll('a[href]')).filter(visible).map((a) => ({
                    text: text(a),
                    href: a.href
                })).filter((x) => x.text || x.href.includes('customer_rank_calculation_rules')),
                visibleButtons: Array.from(document.querySelectorAll('button')).filter(visible).map((button) => ({
                    text: text(button),
                    ariaLabel: button.getAttribute('aria-label'),
                    disabled: !!button.disabled
                })).filter((x) => x.text || x.ariaLabel)
            };
        }"""
    )


def write_outputs(payload):
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    result = payload.get("result", {})
    lines = [
        "# CRM 会員ランク算出ルール 本体編集導線再確認 2026-06-28",
        "",
        f"- 対象ルール: `{RULE_NAME}`",
        f"- 詳細URL: `{BASE + RULE_ROUTE}`",
        f"- 直接更新URL: `{BASE + UPDATE_ROUTE}`",
        f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
        "",
        "## 結果",
        "",
        f"- 詳細画面に本体更新URL `/update` への可視リンクなし: `{'確認' if result.get('detailUpdateLinkAbsent') else '未確認'}`",
        f"- 詳細画面に本体削除ボタンなし: `{'確認' if result.get('detailDeleteControlAbsent') else '未確認'}`",
        f"- 詳細画面の `編集` はランク段階リンクのみ: `{'確認' if result.get('editLinksAreRankRulesOnly') else '未確認'}`",
        f"- 直接 `/update` URLは表示可能: `{'確認' if result.get('directUpdateAccessible') else '未確認'}`",
        "",
        "## 詳細画面の主な可視リンク",
        "",
    ]
    for link in payload.get("detail", {}).get("visibleLinks", []):
        href = link.get("href", "")
        if "customer_rank_calculation_rules" in href:
            lines.append(f"- `{link.get('text')}` -> `{href.replace(BASE, '')}`")
    lines.extend([
        "",
        "## 更新URLのラベル",
        "",
    ])
    for label in payload.get("update", {}).get("labels", []):
        lines.append(f"- `{label}`")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "ruleName": RULE_NAME,
        "detailRoute": RULE_ROUTE,
        "updateRoute": UPDATE_ROUTE,
        "steps": [],
        "result": {},
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(f"{BASE}/admin/customer_rank_calculation_rules", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["list"] = visible_snapshot(page)

            page.goto(f"{BASE}{RULE_ROUTE}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["detail"] = visible_snapshot(page)

            page.goto(f"{BASE}{UPDATE_ROUTE}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["update"] = visible_snapshot(page)

            detail_links = payload["detail"]["visibleLinks"]
            detail_buttons = payload["detail"]["visibleButtons"]
            update_links = [link for link in detail_links if link.get("href", "").rstrip("/").endswith("/update")]
            edit_links = [link for link in detail_links if link.get("text") == "編集"]
            rank_rule_edit_links = [
                link for link in edit_links
                if "/customer_rank_rules/" in link.get("href", "") and not link.get("href", "").endswith("/create")
            ]
            delete_controls = [
                item for item in detail_buttons
                if "削除" in f"{item.get('text') or ''} {item.get('ariaLabel') or ''}"
            ]
            payload["result"] = {
                "detailUpdateLinkAbsent": len(update_links) == 0,
                "detailDeleteControlAbsent": len(delete_controls) == 0,
                "editLinksAreRankRulesOnly": len(edit_links) > 0 and len(edit_links) == len(rank_rule_edit_links),
                "directUpdateAccessible": RULE_NAME in payload["update"]["bodySample"] and "タイトル" in payload["update"]["labels"],
            }
        finally:
            write_outputs(payload)
            if not page.is_closed():
                page.close()
    print(json.dumps(payload["result"], ensure_ascii=False, indent=2))
    if not all(payload["result"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
