#!/usr/bin/env python3
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_JSON = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "06-catalog-auto-rule-existing-delayed-recheck-20260628.json"
OUT_MD = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "06-catalog-auto-rule-existing-delayed-recheck-20260628.md"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def compact(text, limit=1800):
    return " ".join((text or "").split())[:limit]


def wait_text(page, expected, timeout=20000):
    page.wait_for_function(
        "(expected) => document.body && document.body.innerText.includes(expected)",
        arg=expected,
        timeout=timeout,
    )


def click_button(page, name, scope=None, exact=True, timeout=12000):
    (scope or page).get_by_role("button", name=name, exact=exact).first.click(timeout=timeout)


def create_product(page, *, name, code, vendor):
    page.goto(f"{BASE}/admin/products/create", wait_until="load")
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except PlaywrightTimeoutError:
        pass
    page.locator('input[placeholder="7835152003XL180"]').fill(code)
    page.locator('input[placeholder="半袖Tシャツ"]').first.fill(name)
    page.locator('input[placeholder="サイズ"]').fill("サイズ")
    page.locator("select").first.select_option("SIZE")
    page.locator('input[placeholder="S"]').fill("ONE")
    page.locator('input[placeholder="001"]').fill(f"{code}_SKU")
    page.locator('input[placeholder="Tシャツ"]').fill("TEST_FAQ")
    page.locator('input[placeholder="ユニクロ"]').fill(vendor)
    click_button(page, "保存する")
    wait_text(page, name, timeout=30000)
    return {"name": name, "code": code, "vendor": vendor, "url": page.url}


def create_catalog(page, title):
    page.goto(f"{BASE}/admin/catalogs/create", wait_until="load")
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except PlaywrightTimeoutError:
        pass
    page.locator('input[placeholder="渋谷店"]').fill(title)
    click_button(page, "保存する")
    wait_text(page, title, timeout=30000)
    return {"title": title, "url": page.url}


def add_vendor_rule(page, catalog_url, vendor):
    page.goto(f"{catalog_url}/automatic_add_rules", wait_until="load")
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except PlaywrightTimeoutError:
        pass
    click_button(page, "追加する")
    page.wait_for_selector('div[role="dialog"]', timeout=12000)
    dialog = page.locator('div[role="dialog"]').last
    selects = dialog.locator("select")
    selects.nth(0).select_option("VENDOR")
    selects.nth(1).select_option("EQUALS")
    dialog.locator("input").fill(vendor)
    click_button(page, "追加する", scope=dialog)
    wait_text(page, vendor, timeout=20000)
    return {"field": "VENDOR", "condition": "EQUALS", "value": vendor, "url": page.url}


def catalog_snapshot(page, catalog_url, product_names, label, wait_seconds=0):
    if wait_seconds:
        time.sleep(wait_seconds)
    page.goto(catalog_url, wait_until="load")
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1200)
    body = text_of(page)
    return {
        "label": label,
        "waitSecondsBeforeCheck": wait_seconds,
        "url": page.url,
        "presence": {name: name in body for name in product_names},
        "bodySample": compact(body, 1600),
    }


def update_product_name(page, product, new_name):
    result = {"target": product["name"], "newName": new_name, "ok": False, "url": product["url"], "error": None}
    try:
        page.goto(product["url"], wait_until="load")
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except PlaywrightTimeoutError:
            pass
        name_input = page.locator('input[placeholder="半袖Tシャツ"]').first
        name_input.fill(new_name)
        click_button(page, "保存する")
        wait_text(page, new_name, timeout=30000)
        result["ok"] = True
        result["postSaveBody"] = compact(text_of(page), 1000)
        product["name"] = new_name
    except Exception as exc:
        result["error"] = repr(exc)
        result["postErrorBody"] = compact(text_of(page), 1000)
    return result


def update_product_vendor(page, product, new_vendor):
    result = {"target": product["name"], "newVendor": new_vendor, "ok": False, "url": product["url"], "error": None}
    try:
        page.goto(product["url"], wait_until="load")
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except PlaywrightTimeoutError:
            pass
        vendor_input = page.locator('input[placeholder="ユニクロ"]').first
        vendor_input.fill(new_vendor)
        click_button(page, "保存する")
        page.wait_for_timeout(1600)
        result["ok"] = vendor_input.input_value() == new_vendor or "商品を保存しました" in text_of(page)
        result["postSaveBody"] = compact(text_of(page), 1000)
        product["vendor"] = new_vendor
    except Exception as exc:
        result["error"] = repr(exc)
        result["postErrorBody"] = compact(text_of(page), 1000)
    return result


def delete_product(page, product):
    result = {"url": product["url"], "name": product["name"], "deleted": False, "error": None}
    try:
        page.goto(product["url"], wait_until="load")
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except PlaywrightTimeoutError:
            pass
        click_button(page, "その他の操作")
        page.get_by_text("商品を削除する", exact=True).click(timeout=12000)
        page.wait_for_selector('div[role="dialog"]', timeout=12000)
        result["confirmText"] = compact(text_of(page), 700)
        dialog = page.locator('div[role="dialog"]').last
        click_button(page, "削除する", scope=dialog)
        page.wait_for_timeout(1800)
        page.goto(product["url"], wait_until="load")
        page.wait_for_timeout(1200)
        result["deleted"] = "該当するProductが見つかりませんでした" in text_of(page)
        result["postDeleteBody"] = compact(text_of(page), 700)
    except Exception as exc:
        result["error"] = repr(exc)
        result["postErrorBody"] = compact(text_of(page), 700)
    return result


def delete_catalog(page, catalog):
    result = {"url": catalog["url"], "title": catalog["title"], "deleted": False, "error": None}
    try:
        page.goto(catalog["url"], wait_until="load")
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except PlaywrightTimeoutError:
            pass
        click_button(page, "その他の操作")
        page.get_by_text("カタログを削除する", exact=True).click(timeout=12000)
        page.wait_for_selector('div[role="dialog"]', timeout=12000)
        result["confirmText"] = compact(text_of(page), 700)
        dialog = page.locator('div[role="dialog"]').last
        click_button(page, "削除する", scope=dialog)
        page.wait_for_timeout(1800)
        page.goto(catalog["url"], wait_until="load")
        page.wait_for_timeout(1200)
        result["deleted"] = "該当するCatalogが見つかりませんでした" in text_of(page) or "アイテムが見つかりませんでした" in text_of(page)
        result["postDeleteBody"] = compact(text_of(page), 700)
    except Exception as exc:
        result["error"] = repr(exc)
        result["postErrorBody"] = compact(text_of(page), 700)
    return result


def write_outputs(payload):
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    checks = payload.get("checks", [])
    catalog = payload.get("catalog") or {}
    md = [
        "# 06 カタログ: 自動追加ルールの既存商品・遅延反映再確認 2026-06-28",
        "",
        "## 対象",
        "",
        f"- 検証ID: `{payload.get('stamp')}`",
        f"- カタログ: `{catalog.get('title', '')}`",
        f"- ルール: `製造元 / 一致する / {payload.get('vendor', '')}`",
        f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
        "",
        "## 検証商品",
        "",
    ]
    for product in payload.get("products", []):
        md.append(f"- `{product['role']}`: `{product['name']}` / 製造元 `{product['vendor']}`")
    md.extend(["", "## チェック結果", ""])
    for check in checks:
        present = ", ".join([f"{name}={'あり' if ok else 'なし'}" for name, ok in check.get("presence", {}).items()])
        md.append(f"- `{check['label']}`（待機 {check.get('waitSecondsBeforeCheck', 0)}秒）: {present}")
    md.extend(["", "## 操作結果", ""])
    for update in payload.get("updates", []):
        status = "成功" if update.get("ok") else f"失敗: {update.get('error')}"
        md.append(f"- {update.get('action')}: {status}")
    cleanup = payload.get("cleanup", {})
    if cleanup and (cleanup.get("products") or cleanup.get("catalogs")):
        md.extend(["", "## 後片付け", ""])
        products_ok = all(row.get("deleted") for row in cleanup.get("products", []))
        catalogs_ok = all(row.get("deleted") for row in cleanup.get("catalogs", []))
        md.append(f"- 商品削除: {'全件確認済み' if products_ok else '未完了あり'}")
        md.append(f"- カタログ削除: {'確認済み' if catalogs_ok else '未完了あり'}")
    md.extend(["", "## 判定", ""])
    verdict = payload.get("verdict", [])
    if verdict:
        for row in verdict:
            md.append(f"- {row}")
    else:
        md.append("- 判定はスクリプト完了後に記録。")
    OUT_MD.write_text("\n".join(md) + "\n")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "stamp": STAMP,
        "vendor": f"TEST_VENDOR_RETRO_{STAMP}",
        "products": [],
        "catalog": None,
        "rule": None,
        "checks": [],
        "updates": [],
        "cleanup": {"products": [], "catalogs": []},
        "errors": [],
        "complete": False,
    }
    write_outputs(payload)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(22000)
        try:
            existing_match = create_product(
                page,
                name=f"TEST_FAQ_RETRO_EXISTING_MATCH_{STAMP}",
                code=f"TEST_FAQ_RETRO_EXISTING_MATCH_{STAMP}",
                vendor=payload["vendor"],
            )
            existing_match["role"] = "rule_before_existing_matching"
            payload["products"].append(existing_match)
            write_outputs(payload)

            existing_nonmatch = create_product(
                page,
                name=f"TEST_FAQ_RETRO_EXISTING_NONMATCH_{STAMP}",
                code=f"TEST_FAQ_RETRO_EXISTING_NONMATCH_{STAMP}",
                vendor=f"TEST_VENDOR_OTHER_{STAMP}",
            )
            existing_nonmatch["role"] = "rule_before_existing_changed_to_match"
            payload["products"].append(existing_nonmatch)
            write_outputs(payload)

            catalog = create_catalog(page, f"TEST_FAQ_RETRO_CATALOG_{STAMP}")
            payload["catalog"] = catalog
            write_outputs(payload)

            payload["rule"] = add_vendor_rule(page, catalog["url"], payload["vendor"])
            write_outputs(payload)

            current_names = [p["name"] for p in payload["products"]]
            payload["checks"].append(catalog_snapshot(page, catalog["url"], current_names, "after_rule_immediate", 0))
            write_outputs(payload)
            payload["checks"].append(catalog_snapshot(page, catalog["url"], current_names, "after_rule_reload_10s", 10))
            write_outputs(payload)
            payload["checks"].append(catalog_snapshot(page, catalog["url"], current_names, "after_rule_reload_60s", 60))
            write_outputs(payload)

            update = update_product_name(page, existing_match, f"TEST_FAQ_RETRO_EXISTING_MATCH_UPDATED_{STAMP}")
            update["action"] = "matching_existing_product_name_update_after_rule"
            payload["updates"].append(update)
            write_outputs(payload)
            current_names = [p["name"] for p in payload["products"]]
            payload["checks"].append(catalog_snapshot(page, catalog["url"], current_names, "after_matching_existing_name_update", 5))
            write_outputs(payload)

            update = update_product_vendor(page, existing_nonmatch, payload["vendor"])
            update["action"] = "nonmatching_existing_product_vendor_changed_to_match_after_rule"
            payload["updates"].append(update)
            write_outputs(payload)
            payload["checks"].append(catalog_snapshot(page, catalog["url"], current_names, "after_nonmatching_existing_vendor_update_5s", 5))
            write_outputs(payload)
            payload["checks"].append(catalog_snapshot(page, catalog["url"], current_names, "after_nonmatching_existing_vendor_update_30s", 30))
            write_outputs(payload)

            new_product = create_product(
                page,
                name=f"TEST_FAQ_RETRO_NEW_MATCH_{STAMP}",
                code=f"TEST_FAQ_RETRO_NEW_MATCH_{STAMP}",
                vendor=payload["vendor"],
            )
            new_product["role"] = "rule_after_new_matching"
            payload["products"].append(new_product)
            write_outputs(payload)

            current_names = [p["name"] for p in payload["products"]]
            payload["checks"].append(catalog_snapshot(page, catalog["url"], current_names, "after_new_matching_product_create_5s", 5))
            write_outputs(payload)
            payload["checks"].append(catalog_snapshot(page, catalog["url"], current_names, "after_new_matching_product_create_30s", 30))
            write_outputs(payload)

            final_presence = payload["checks"][-1]["presence"]
            initial_presence = payload["checks"][2]["presence"]
            name_update_presence = payload["checks"][3]["presence"]
            vendor_update_presence = payload["checks"][5]["presence"]
            payload["verdict"] = [
                "ルール作成前から製造元が一致していた既存商品は、作成直後・10秒後・60秒後の再読み込みではカタログに追加されなかった。",
                "既存の一致商品は、商品名だけを更新して保存しても、確認範囲ではカタログへ追加されなかった。" if not name_update_presence.get(existing_match["name"]) else "既存の一致商品は、商品名更新後にカタログへ追加された。",
                "ルール作成前から存在した不一致商品を、作成後に製造元一致へ変更して保存するとカタログへ追加された。" if vendor_update_presence.get(existing_nonmatch["name"]) else "ルール作成前から存在した不一致商品を製造元一致へ変更しても、確認範囲では追加されなかった。",
                "ルール作成後に新規作成した一致商品はカタログへ追加された。" if final_presence.get(new_product["name"]) else "ルール作成後に新規作成した一致商品が確認範囲で追加されなかった。",
            ]
            payload["computedPresence"] = {
                "initialAfter60s": initial_presence,
                "afterNameUpdate": name_update_presence,
                "afterVendorUpdate": vendor_update_presence,
                "final": final_presence,
            }
            write_outputs(payload)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            payload["errorBody"] = compact(text_of(page), 2000)
            write_outputs(payload)
            raise
        finally:
            for product in list(reversed(payload.get("products", []))):
                payload["cleanup"]["products"].append(delete_product(page, product))
                write_outputs(payload)
            if payload.get("catalog"):
                payload["cleanup"]["catalogs"].append(delete_catalog(page, payload["catalog"]))
                write_outputs(payload)
            payload["complete"] = True
            payload["completedAt"] = datetime.now(timezone.utc).isoformat()
            write_outputs(payload)
            page.close()
            browser.close()

    print(json.dumps({
        "stamp": payload["stamp"],
        "checks": payload["checks"],
        "updates": payload["updates"],
        "cleanupProductsOk": all(row.get("deleted") for row in payload["cleanup"]["products"]),
        "cleanupCatalogsOk": all(row.get("deleted") for row in payload["cleanup"]["catalogs"]),
        "errors": payload["errors"],
        "verdict": payload.get("verdict"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
