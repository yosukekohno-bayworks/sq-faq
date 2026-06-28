#!/usr/bin/env python3
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "06-catalog-auto-add-rule-matrix-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

STAMP = "20260628_013725"


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def short_body(page, limit=1200):
    return " ".join(text_of(page).split())[:limit]


def wait_text(page, expected, timeout=20000):
    page.wait_for_function(
        "(expected) => document.body && document.body.innerText.includes(expected)",
        arg=expected,
        timeout=timeout,
    )


def click_button(page, name, scope=None, exact=True, timeout=10000):
    locator = (scope or page).get_by_role("button", name=name, exact=exact)
    locator.first.click(timeout=timeout)


def set_selects_and_input(page, first_value, second_value, input_value):
    dialog = page.locator('div[role="dialog"]').last
    selects = dialog.locator("select")
    selects.nth(0).select_option(first_value)
    selects.nth(1).select_option(second_value)
    dialog.locator("input").fill(input_value)
    click_button(page, "追加する", scope=dialog)


def create_catalog(page, title):
    page.goto(f"{BASE}/admin/catalogs/create", wait_until="load")
    page.wait_for_load_state("networkidle", timeout=8000)
    page.locator('input[placeholder="渋谷店"]').fill(title)
    click_button(page, "保存する")
    wait_text(page, title)
    return {"title": title, "url": page.url}


def add_rule(page, catalog_url, field, value):
    page.goto(f"{catalog_url}/automatic_add_rules", wait_until="load")
    page.wait_for_load_state("networkidle", timeout=8000)
    click_button(page, "追加する")
    page.wait_for_selector('div[role="dialog"]', timeout=10000)
    set_selects_and_input(page, field, "EQUALS", value)
    wait_text(page, value)
    return {"field": field, "condition": "EQUALS", "value": value}


def select_brand(page, brand_code):
    click_button(page, "選択")
    page.wait_for_selector('div[role="dialog"] tr[id$="_Brand"]', timeout=10000)
    found = page.evaluate(
        """(brandCode) => {
            const rows = Array.from(document.querySelectorAll('div[role="dialog"] tr[id$="_Brand"]'));
            const row = rows.find((r) => Array.from(r.cells).some((c) => c.innerText.trim() === brandCode));
            if (!row) return false;
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox) checkbox.click();
            else row.click();
            return true;
        }""",
        brand_code,
    )
    if not found:
        raise RuntimeError(f"brand not found: {brand_code}")
    dialog = page.locator('div[role="dialog"]').last
    button = dialog.get_by_role("button", name="選択する")
    button.wait_for(state="visible", timeout=10000)
    for _ in range(20):
        if button.is_enabled():
            break
        page.wait_for_timeout(250)
    button.click()
    page.wait_for_selector('div[role="dialog"]', state="detached", timeout=10000)


def create_product(page, *, name, code, vendor, brand_code=None):
    page.goto(f"{BASE}/admin/products/create", wait_until="load")
    page.wait_for_load_state("networkidle", timeout=8000)
    page.locator('input[placeholder="7835152003XL180"]').fill(code)
    page.locator('input[placeholder="半袖Tシャツ"]').first.fill(name)
    page.locator('input[placeholder="サイズ"]').fill("サイズ")
    page.locator("select").first.select_option("SIZE")
    page.locator('input[placeholder="S"]').fill("ONE")
    page.locator('input[placeholder="001"]').fill(f"{code}_SKU")
    page.locator('input[placeholder="Tシャツ"]').fill("TEST_FAQ")
    page.locator('input[placeholder="ユニクロ"]').fill(vendor)
    if brand_code:
        select_brand(page, brand_code)
    click_button(page, "保存する")
    wait_text(page, name, timeout=30000)
    return {"name": name, "code": code, "vendor": vendor, "brand_code": brand_code, "url": page.url}


def catalog_presence(page, catalog_url, product_names, timeout_ms=16000):
    deadline = time.time() + timeout_ms / 1000
    last_body = ""
    while time.time() < deadline:
        page.goto(catalog_url, wait_until="load")
        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except PlaywrightTimeoutError:
            pass
        page.wait_for_timeout(1000)
        last_body = text_of(page)
        presence = {name: (name in last_body) for name in product_names}
        if any(presence.values()):
            return {"presence": presence, "bodySample": " ".join(last_body.split())[:1800]}
        time.sleep(0.7)
    return {"presence": {name: (name in last_body) for name in product_names}, "bodySample": " ".join(last_body.split())[:1800]}


def delete_product(page, product):
    result = {"url": product["url"], "name": product["name"], "deleted": False, "confirmText": None, "error": None}
    try:
        page.goto(product["url"], wait_until="load")
        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except PlaywrightTimeoutError:
            pass
        click_button(page, "その他の操作")
        page.get_by_text("商品を削除する", exact=True).click(timeout=10000)
        page.wait_for_selector('div[role="dialog"]', timeout=10000)
        result["confirmText"] = short_body(page, 600)
        dialog = page.locator('div[role="dialog"]').last
        click_button(page, "削除する", scope=dialog)
        page.wait_for_timeout(1600)
        page.goto(product["url"], wait_until="load")
        page.wait_for_timeout(1200)
        result["deleted"] = "該当するProductが見つかりませんでした" in text_of(page)
        result["postDeleteBody"] = short_body(page, 600)
    except Exception as exc:
        result["error"] = repr(exc)
    return result


def delete_catalog(page, catalog):
    result = {"url": catalog["url"], "title": catalog["title"], "deleted": False, "confirmText": None, "error": None}
    try:
        page.goto(catalog["url"], wait_until="load")
        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except PlaywrightTimeoutError:
            pass
        click_button(page, "その他の操作")
        page.get_by_text("カタログを削除する", exact=True).click(timeout=10000)
        page.wait_for_selector('div[role="dialog"]', timeout=10000)
        result["confirmText"] = short_body(page, 600)
        dialog = page.locator('div[role="dialog"]').last
        click_button(page, "削除する", scope=dialog)
        page.wait_for_timeout(1600)
        page.goto(catalog["url"], wait_until="load")
        page.wait_for_timeout(1200)
        result["deleted"] = "該当するCatalogが見つかりませんでした" in text_of(page)
        result["postDeleteBody"] = short_body(page, 600)
    except Exception as exc:
        result["error"] = repr(exc)
    return result


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "stamp": STAMP,
        "catalogs": [],
        "rules": {},
        "products": [],
        "checks": {},
        "cleanup": {"products": [], "catalogs": []},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)

        try:
            mix_catalog = {"title": f"TEST_FAQ_RULE_MIX_{STAMP}", "url": f"{BASE}/admin/catalogs/2f4edd32-7e00-5bb8-b96d-a4f538b3bb6b_Catalog"}
            page.goto(mix_catalog["url"], wait_until="load")
            wait_text(page, mix_catalog["title"], timeout=10000)
        except Exception:
            mix_catalog = create_catalog(page, f"TEST_FAQ_RULE_MIX_{STAMP}")
        payload["catalogs"].append(mix_catalog)

        multi_catalog = create_catalog(page, f"TEST_FAQ_RULE_MULTI_{STAMP}")
        wildcard_catalog = create_catalog(page, f"TEST_FAQ_RULE_WILDCARD_{STAMP}")
        payload["catalogs"].extend([multi_catalog, wildcard_catalog])

        vendor_mix = f"TEST_VENDOR_MIX_{STAMP}"
        vendor_other = f"TEST_VENDOR_OTHER_{STAMP}"
        vendor_multi_a = f"TEST_MULTI_A_{STAMP}"
        vendor_multi_b = f"TEST_MULTI_B_{STAMP}"
        vendor_comma = f"{vendor_multi_a},{vendor_multi_b}"
        vendor_any = f"TEST_ANY_{STAMP}"

        payload["rules"]["mix"] = [
            add_rule(page, mix_catalog["url"], "VENDOR", vendor_mix),
            add_rule(page, mix_catalog["url"], "BRAND", "GU"),
        ]
        payload["rules"]["multi"] = [
            add_rule(page, multi_catalog["url"], "VENDOR", vendor_comma),
        ]
        payload["rules"]["wildcard"] = [
            add_rule(page, wildcard_catalog["url"], "VENDOR", "*"),
        ]

        product_specs = [
            {"name": f"TEST_FAQ_MIX_VENDOR_ONLY_{STAMP}", "code": f"TEST_FAQ_MIX_VENDOR_ONLY_{STAMP}", "vendor": vendor_mix, "brand_code": None},
            {"name": f"TEST_FAQ_MIX_BRAND_ONLY_{STAMP}", "code": f"TEST_FAQ_MIX_BRAND_ONLY_{STAMP}", "vendor": vendor_other, "brand_code": "GU"},
            {"name": f"TEST_FAQ_MIX_BOTH_{STAMP}", "code": f"TEST_FAQ_MIX_BOTH_{STAMP}", "vendor": vendor_mix, "brand_code": "GU"},
            {"name": f"TEST_FAQ_MULTI_A_ONLY_{STAMP}", "code": f"TEST_FAQ_MULTI_A_ONLY_{STAMP}", "vendor": vendor_multi_a, "brand_code": None},
            {"name": f"TEST_FAQ_MULTI_COMMA_EXACT_{STAMP}", "code": f"TEST_FAQ_MULTI_COMMA_EXACT_{STAMP}", "vendor": vendor_comma, "brand_code": None},
            {"name": f"TEST_FAQ_WILDCARD_ANY_{STAMP}", "code": f"TEST_FAQ_WILDCARD_ANY_{STAMP}", "vendor": vendor_any, "brand_code": None},
            {"name": f"TEST_FAQ_WILDCARD_LITERAL_{STAMP}", "code": f"TEST_FAQ_WILDCARD_LITERAL_{STAMP}", "vendor": "*", "brand_code": None},
        ]

        for spec in product_specs:
            product = create_product(page, **spec)
            payload["products"].append(product)
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

        mix_names = [p["name"] for p in payload["products"][:3]]
        multi_names = [p["name"] for p in payload["products"][3:5]]
        wildcard_names = [p["name"] for p in payload["products"][5:]]
        payload["checks"]["mix"] = catalog_presence(page, mix_catalog["url"], mix_names)
        payload["checks"]["multi"] = catalog_presence(page, multi_catalog["url"], multi_names)
        payload["checks"]["wildcard"] = catalog_presence(page, wildcard_catalog["url"], wildcard_names)

        for product in list(reversed(payload["products"])):
            payload["cleanup"]["products"].append(delete_product(page, product))
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
        for catalog in list(reversed(payload["catalogs"])):
            payload["cleanup"]["catalogs"].append(delete_catalog(page, catalog))
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

        page.close()
        browser.close()

    payload["complete"] = True
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(json.dumps({
        "checks": payload["checks"],
        "cleanupProductsOk": all(row.get("deleted") for row in payload["cleanup"]["products"]),
        "cleanupCatalogsOk": all(row.get("deleted") for row in payload["cleanup"]["catalogs"]),
        "errors": payload["errors"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
