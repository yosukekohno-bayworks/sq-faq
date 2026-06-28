#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "07-local-pickup-variant-selection-20260628.json"
MD = OUT.with_suffix(".md")
ROUTE = "/admin/local_pickup_product_variants"
SEARCH_QUERY = "TEST_E2E"
SKU_RE = re.compile(r"(?:TEST_E2E_[A-Z0-9_]+|[0-9]{6}-[0-9A-Z]+-[0-9A-Z]+)")


def compact(text, limit=1600):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def rows(scope):
    data = scope.locator("tr, [role=row]").evaluate_all(
        r"""els => els.map((el, index) => ({
            index,
            text: (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim(),
            hasCheckbox: !!el.querySelector('input[type="checkbox"]')
        })).filter((row) => row.text && !row.text.startsWith('すべてのアイテムを選択する'))"""
    )
    out = []
    for row in data:
        sku_match = None
        for match in SKU_RE.finditer(row["text"]):
            sku_match = match.group(0)
        row["sku"] = sku_match
        out.append(row)
    return out


def sku_set(rows_):
    return {row["sku"] for row in rows_ if row.get("sku")}


def click_row_checkbox(page, sku, scope_selector=None):
    root = f"document.querySelector({json.dumps(scope_selector)})" if scope_selector else "document"
    return page.evaluate(
        rf"""(sku) => {{
            const root = {root};
            if (!root) return {{clicked: false, reason: 'scope not found'}};
            const rows = Array.from(root.querySelectorAll('tr, [role=row]'));
            const row = rows.find((candidate) => (candidate.innerText || candidate.textContent || '').includes(sku));
            if (!row) return {{clicked: false, reason: 'row not found'}};
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (!checkbox) return {{clicked: false, reason: 'checkbox not found', rowText: row.innerText}};
            checkbox.click();
            return {{clicked: true, rowText: (row.innerText || row.textContent || '').replace(/\s+/g, ' ').trim()}};
        }}""",
        sku,
    )


def button_state(locator):
    return locator.evaluate(
        """button => ({
            text: (button.innerText || button.textContent || '').replace(/\\s+/g, ' ').trim(),
            disabled: !!button.disabled,
            ariaDisabled: button.getAttribute('aria-disabled')
        })"""
    )


def write_md(payload):
    result = payload["result"]
    lines = [
        "# 店舗受取SKU選択 実機確認 2026-06-28",
        "",
        f"- 対象: `{ROUTE}`",
        f"- 検索語: `{SEARCH_QUERY}`",
        f"- 追加前件数: {result['beforeCount']}",
        f"- 追加対象としてチェックしたSKU: `{result['selectedSku']}`",
        f"- 未チェックで残したSKU: `{result['unselectedSku']}`",
        f"- 追加後件数: {result['afterAddCount']}",
        f"- チェックしたSKUが追加された: {result['selectedAdded']}",
        f"- 未チェックSKUが追加されなかった: {result['unselectedStayedAbsent']}",
        f"- 削除後件数: {result['afterCleanupCount']}",
        f"- 追加分のクリーンアップ完了: {result['cleanupRemovedSelected']}",
        f"- 追加ダイアログ内にカタログ項目あり: {result['dialogHasCatalogMention']}",
        "",
        "## 候補行",
        "",
    ]
    for row in result["candidateRows"]:
        lines.append(f"- `{row.get('sku')}`: {row['text']}")
    lines.extend(
        [
            "",
            "## 結論",
            "",
            "- 商品管理 > 店舗受取の追加ダイアログでは、チェックしたSKUだけが店舗受取対象一覧に追加され、未チェックのSKUは追加されない。",
            "- この商品側UIはSKU直接指定であり、追加ダイアログ内にカタログ選択項目は表示されない。",
            "- カタログで束ねた商品集合との優先関係は、この画面単体では判定できない。リテールポータル/販売チャネル接続後の挙動として残す。",
            "",
        ]
    )
    MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "route": ROUTE,
        "searchQuery": SEARCH_QUERY,
        "errors": [],
        "result": {},
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(BASE + ROUTE, wait_until="load")
            wait_quiet(page)
            before_rows = rows(page)
            before_skus = sku_set(before_rows)

            page.get_by_role("button", name="バリエーションを追加する", exact=True).click()
            page.wait_for_selector('[role="dialog"]', timeout=15000)
            dialog = page.locator('[role="dialog"]').last
            dialog.locator("input").first.fill(SEARCH_QUERY)
            page.keyboard.press("Enter")
            wait_quiet(page)
            candidate_rows = rows(dialog)
            available = [row for row in candidate_rows if row.get("sku") and row["sku"] not in before_skus]
            if len(available) < 2:
                raise RuntimeError(f"Need at least 2 not-yet-selected candidates, got {len(available)}")
            selected_sku = available[0]["sku"]
            unselected_sku = available[1]["sku"]
            dialog_text_before_select = compact(dialog.inner_text(timeout=5000), 3000)
            select_click = click_row_checkbox(page, selected_sku, '[role="dialog"]')
            if not select_click.get("clicked"):
                raise RuntimeError(f"Could not click selected row: {select_click}")
            page.wait_for_timeout(500)
            select_button = dialog.get_by_role("button", name="選択する", exact=True)
            select_button_state = button_state(select_button)
            select_button.click()
            wait_quiet(page, timeout=10000)
            page.reload(wait_until="load")
            wait_quiet(page, timeout=10000)

            after_add_rows = rows(page)
            after_add_skus = sku_set(after_add_rows)
            selected_added = selected_sku in after_add_skus
            unselected_stayed_absent = unselected_sku not in after_add_skus

            cleanup_click = None
            cleanup_confirm_text = None
            if selected_added:
                cleanup_click = click_row_checkbox(page, selected_sku)
                if not cleanup_click.get("clicked"):
                    raise RuntimeError(f"Could not click cleanup row: {cleanup_click}")
                page.wait_for_timeout(500)
                page.get_by_role("button", name="削除する", exact=True).click()
                page.wait_for_selector('[role="dialog"]', timeout=15000)
                confirm = page.locator('[role="dialog"]').last
                cleanup_confirm_text = compact(confirm.inner_text(timeout=5000), 1200)
                confirm.get_by_role("button", name="削除する", exact=True).click()
                wait_quiet(page, timeout=10000)
                page.reload(wait_until="load")
                wait_quiet(page, timeout=10000)

            after_cleanup_rows = rows(page)
            after_cleanup_skus = sku_set(after_cleanup_rows)
            payload["result"] = {
                "beforeCount": len(before_rows),
                "beforeSample": before_rows[:8],
                "candidateRows": candidate_rows,
                "selectedSku": selected_sku,
                "unselectedSku": unselected_sku,
                "selectClick": select_click,
                "selectButtonStateBeforeClick": select_button_state,
                "dialogHasCatalogMention": "カタログ" in dialog_text_before_select,
                "afterAddCount": len(after_add_rows),
                "afterAddSample": after_add_rows[:8],
                "selectedAdded": selected_added,
                "unselectedStayedAbsent": unselected_stayed_absent,
                "cleanupClick": cleanup_click,
                "cleanupConfirmText": cleanup_confirm_text,
                "afterCleanupCount": len(after_cleanup_rows),
                "afterCleanupSample": after_cleanup_rows[:8],
                "cleanupRemovedSelected": selected_sku not in after_cleanup_skus,
                "unselectedStillAbsentAfterCleanup": unselected_sku not in after_cleanup_skus,
            }
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            if payload["result"]:
                write_md(payload)
            page.close()
            browser.close()

    print(
        json.dumps(
            {
                "errors": payload["errors"],
                "selectedSku": payload.get("result", {}).get("selectedSku"),
                "unselectedSku": payload.get("result", {}).get("unselectedSku"),
                "selectedAdded": payload.get("result", {}).get("selectedAdded"),
                "unselectedStayedAbsent": payload.get("result", {}).get("unselectedStayedAbsent"),
                "cleanupRemovedSelected": payload.get("result", {}).get("cleanupRemovedSelected"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
