#!/usr/bin/env python3
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "11-price-tax-blank-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
RULE = "407b1402-6d11-5672-bc33-5de49d5ce9bc_ProductPriceRule"
RULE_NAME = "TEST_FAQ_DEEP_202606080340_販売価格ルール"
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def compact(text, limit=1600):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=6000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def click_button(page, name, scope=None, exact=True, timeout=15000):
    locator = (scope or page).get_by_role("button", name=name, exact=exact)
    locator.first.click(timeout=timeout)


def open_create_form(page, kind):
    page.goto(f"{BASE}/admin/product_price_rules/{RULE}/{kind}", wait_until="load")
    wait_quiet(page)
    click_button(page, "登録する")
    page.wait_for_timeout(600)


def choose_sku(page):
    click_button(page, "選択")
    page.wait_for_selector('div[role="dialog"] input[placeholder="SKUコードで検索する"]', timeout=15000)
    dialog_count = page.locator('div[role="dialog"]').count()
    search = page.locator('div[role="dialog"] input[placeholder="SKUコードで検索する"]').last
    search.fill(SKU)
    search.press("Enter")
    page.wait_for_function(
        """(sku) => Array.from(document.querySelectorAll('div[role="dialog"] tr')).some((tr) => tr.innerText.includes(sku))""",
        arg=SKU,
        timeout=15000,
    )
    row_text = page.evaluate(
        """(sku) => {
            const dialogs = Array.from(document.querySelectorAll('div[role="dialog"]'));
            const dialog = dialogs[dialogs.length - 1];
            const row = Array.from(dialog.querySelectorAll('tr')).find((tr) => tr.innerText.includes(sku));
            if (!row) return null;
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox) checkbox.click();
            else row.click();
            return row.innerText;
        }""",
        SKU,
    )
    dialog = page.locator('div[role="dialog"]').last
    button = dialog.get_by_role("button", name="選択する", exact=True)
    for _ in range(24):
        if button.is_enabled():
            break
        page.wait_for_timeout(250)
    button.click()
    page.wait_for_function(
        """(count) => document.querySelectorAll('div[role="dialog"]').length < count""",
        arg=dialog_count,
        timeout=15000,
    )
    page.wait_for_timeout(500)
    return compact(row_text, 700)


def fill_numbers(page, price):
    inputs = page.locator('input[type="number"]')
    if inputs.count() < 2:
        raise RuntimeError("number inputs not found")
    inputs.nth(0).fill(str(price))
    inputs.nth(1).fill("")


def fill_sale_dates(page, start_datetime):
    inputs = page.locator('input[type="datetime-local"]')
    if inputs.count() < 2:
        raise RuntimeError("datetime inputs not found")
    inputs.nth(0).fill(start_datetime)
    inputs.nth(1).fill("")


def search_list(page, kind):
    page.goto(f"{BASE}/admin/product_price_rules/{RULE}/{kind}", wait_until="load")
    wait_quiet(page)
    search = page.locator('input[placeholder="SKUコードで検索する"]').first
    search.fill(SKU)
    search.press("Enter")
    page.wait_for_timeout(2200)
    return compact(text_of(page), 2200)


def row_text(page, sku=SKU):
    rows = page.evaluate(
        """(sku) => Array.from(document.querySelectorAll('tr'))
            .filter((tr) => tr.innerText.includes(sku))
            .map((tr) => ({id: tr.id, text: tr.innerText}))""",
        sku,
    )
    return [{"id": r["id"], "text": compact(r["text"], 1000)} for r in rows]


def select_row_by_sku(page):
    selected = page.evaluate(
        """(sku) => {
            const row = Array.from(document.querySelectorAll('tr')).find((tr) => tr.innerText.includes(sku));
            if (!row) return null;
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox) checkbox.click();
            else row.click();
            return row.innerText;
        }""",
        SKU,
    )
    page.wait_for_timeout(900)
    return compact(selected, 1000)


def select_row_containing(page, needle):
    selected = page.evaluate(
        """(needle) => {
            const row = Array.from(document.querySelectorAll('tr')).find((tr) => tr.innerText.includes(needle));
            if (!row) return null;
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox) checkbox.click();
            else row.click();
            return row.innerText;
        }""",
        needle,
    )
    page.wait_for_timeout(900)
    return compact(selected, 1000)


def cleanup_selected(page, action_name):
    before = compact(text_of(page), 1800)
    click_button(page, action_name)
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    confirm_text = compact(dialog.inner_text(timeout=5000), 1200)
    # Both delete and disable dialogs use the visible destructive action text.
    click_button(page, action_name, scope=dialog)
    page.wait_for_timeout(1800)
    return {"beforeActionBody": before, "confirmText": confirm_text, "postActionBody": compact(text_of(page), 1800)}


def create_regular(page):
    result = {"kind": "regular", "input": {"price": 1234, "priceTaxIncl": ""}}
    open_create_form(page, "product_variant_regulars")
    result["formBeforeSave"] = compact(text_of(page), 1600)
    result["selectedSkuRow"] = choose_sku(page)
    fill_numbers(page, result["input"]["price"])
    click_button(page, "保存する")
    page.wait_for_timeout(2500)
    result["afterSaveUrl"] = page.url
    result["afterSaveBody"] = compact(text_of(page), 2400)
    result["listBody"] = search_list(page, "product_variant_regulars")
    result["rows"] = row_text(page)
    result["selectedRow"] = select_row_by_sku(page)
    result["buttonsAfterSelect"] = page.evaluate(
        """() => Array.from(document.querySelectorAll('button')).map((b) => b.innerText.trim()).filter(Boolean)"""
    )
    result["cleanup"] = cleanup_selected(page, "削除する")
    result["afterCleanupListBody"] = search_list(page, "product_variant_regulars")
    result["afterCleanupRows"] = row_text(page)
    return result


def create_sale(page):
    result = {
        "kind": "sale",
        "input": {"price": 876, "priceTaxIncl": "", "startDatetime": "2026-06-28T10:45", "endDatetime": ""},
    }
    open_create_form(page, "product_variant_sales")
    result["formBeforeSave"] = compact(text_of(page), 1800)
    result["selectedSkuRow"] = choose_sku(page)
    fill_numbers(page, result["input"]["price"])
    fill_sale_dates(page, result["input"]["startDatetime"])
    click_button(page, "保存する")
    page.wait_for_timeout(2500)
    result["afterSaveUrl"] = page.url
    result["afterSaveBody"] = compact(text_of(page), 2600)
    result["listBody"] = search_list(page, "product_variant_sales")
    result["rows"] = row_text(page)
    result["selectedSkuRowForDetail"] = select_row_by_sku(page)
    page.wait_for_timeout(1200)
    result["detailBeforeCleanup"] = compact(text_of(page), 2400)
    result["selectedRow"] = select_row_containing(page, f"￥{result['input']['price']}")
    result["buttonsAfterSelect"] = page.evaluate(
        """() => Array.from(document.querySelectorAll('button')).map((b) => b.innerText.trim()).filter(Boolean)"""
    )
    result["cleanup"] = cleanup_selected(page, "無効化する")
    result["afterCleanupListBody"] = search_list(page, "product_variant_sales")
    result["afterCleanupRows"] = row_text(page)
    return result


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "rule": RULE_NAME,
        "ruleUrl": f"{BASE}/admin/product_price_rules/{RULE}",
        "sku": SKU,
        "results": [],
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            payload["results"].append(create_regular(page))
        except Exception as exc:
            payload["errors"].append({"step": "regular", "error": repr(exc), "body": compact(text_of(page), 2400), "url": page.url})
        try:
            payload["results"].append(create_sale(page))
        except Exception as exc:
            payload["errors"].append({"step": "sale", "error": repr(exc), "body": compact(text_of(page), 2400), "url": page.url})
        page.close()
        browser.close()
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(json.dumps({
        "out": str(OUT),
        "results": [r["kind"] for r in payload["results"]],
        "errors": payload["errors"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
