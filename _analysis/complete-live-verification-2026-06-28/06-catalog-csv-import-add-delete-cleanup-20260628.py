#!/usr/bin/env python3
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "06-catalog-csv-import-add-delete-cleanup-20260628.json"
OUT_MD = OUT_DIR / "06-catalog-csv-import-add-delete-cleanup-20260628.md"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
PRODUCT_CODE = f"TEST_FAQ_CATCSV_{STAMP}"
PRODUCT_TITLE = f"TEST_FAQ_CATCSV_{STAMP}_商品"
CATALOG_TITLE = f"TEST_FAQ_CATCSV_{STAMP}_カタログ"
ADD_CSV = OUT_DIR / f"06-catalog-csv-import-add-{STAMP}.csv"
DELETE_CSV = OUT_DIR / f"06-catalog-csv-import-delete-{STAMP}.csv"


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def compact(text, limit=1800):
    return " ".join((text or "").split())[:limit]


def normalized(text):
    return " ".join((text or "").split())


def important(text, limit=90):
    patterns = (
        "CSV",
        "インポート",
        "カタログ",
        "商品",
        "検証",
        "実行",
        "成功",
        "失敗",
        "完了",
        "未実行",
        "処理中",
        "巻き戻すことができません",
        "削除",
        "該当する",
        PRODUCT_CODE,
        PRODUCT_TITLE,
        CATALOG_TITLE,
    )
    rows = []
    for line in (text or "").splitlines():
        line = line.strip()
        if line and any(pattern in line for pattern in patterns) and line not in rows:
            rows.append(line)
    return rows[:limit]


def write_outputs(payload):
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    md = [
        "# 06 カタログCSVインポート NEW/DELETE 実行確認 2026-06-28",
        "",
        "## 対象",
        "",
        f"- 商品コード: `{PRODUCT_CODE}`",
        f"- 商品名: `{PRODUCT_TITLE}`",
        f"- カタログ: `{CATALOG_TITLE}`",
        f"- ADD CSV: `{ADD_CSV.relative_to(ROOT)}`",
        f"- DELETE CSV: `{DELETE_CSV.relative_to(ROOT)}`",
        f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
        "",
        "## 結果",
        "",
        f"- NEW検証成功: `{'確認' if payload.get('add', {}).get('validationSuccess') else '未確認'}`",
        f"- NEW実行成功: `{'確認' if payload.get('add', {}).get('executionSuccess') else '未確認'}`",
        f"- NEW後のカタログ反映: `{'確認' if payload.get('catalogContainsAfterAdd') else '未確認'}`",
        f"- DELETE検証成功: `{'確認' if payload.get('delete', {}).get('validationSuccess') else '未確認'}`",
        f"- DELETE実行成功: `{'確認' if payload.get('delete', {}).get('executionSuccess') else '未確認'}`",
        f"- DELETE後のカタログ除外: `{'確認' if payload.get('catalogRemovedAfterDelete') else '未確認'}`",
        f"- 商品削除: `{'確認' if payload.get('cleanup', {}).get('productDeleted') else '未確認'}`",
        f"- カタログ削除: `{'確認' if payload.get('cleanup', {}).get('catalogDeleted') else '未確認'}`",
        "",
        "## 判定",
        "",
    ]
    if payload.get("complete"):
        md.extend([
            "- カタログ商品CSVは `product_code,command` の2列で、`NEW` により対象商品をカタログへ追加できる。",
            "- 同じ形式で `DELETE` を実行すると、対象商品をカタログから外せる。",
            "- NEW/DELETEとも検証成功後に確認ダイアログを経て実行され、実行ステータスは `成功 完了` になる。",
            "- 検証用の商品・カタログは削除済み。",
        ])
    else:
        md.append(f"- 未完了: `{payload.get('error') or '条件未達'}`")
    md.extend(["", "## ステップ", ""])
    for step in payload.get("steps", []):
        md.append(f"### {step['step']}")
        md.append("")
        md.append(f"- URL: `{step['url']}`")
        for line in step.get("importantLines", [])[:26]:
            md.append(f"- {line}")
        md.append("")
    OUT_MD.write_text("\n".join(md) + "\n")


def record_step(payload, page, step):
    body = text_of(page)
    payload["steps"].append({
        "step": step,
        "url": page.url,
        "importantLines": important(body),
        "bodySample": compact(body, 2200),
    })
    write_outputs(payload)


def wait_soft(page, ms=1200):
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(ms)


def wait_text(page, text, timeout=30000):
    page.wait_for_function(
        "(expected) => document.body && document.body.innerText.includes(expected)",
        arg=text,
        timeout=timeout,
    )


def click_button(page, name, scope=None, exact=True, timeout=15000):
    (scope or page).get_by_role("button", name=name, exact=exact).first.click(timeout=timeout)


def make_csv(path, command):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_code", "command"])
        writer.writerow([PRODUCT_CODE, command])


def create_product(page, payload):
    page.goto(f"{BASE}/admin/products/create", wait_until="load", timeout=60000)
    wait_soft(page)
    page.locator('input[placeholder="7835152003XL180"]').fill(PRODUCT_CODE)
    page.locator('input[placeholder="半袖Tシャツ"]').first.fill(PRODUCT_TITLE)
    page.locator('input[placeholder="サイズ"]').fill("サイズ")
    page.locator("select").first.select_option("SIZE")
    page.locator('input[placeholder="S"]').fill("ONE")
    page.locator('input[placeholder="001"]').fill(f"{PRODUCT_CODE}_SKU")
    page.locator('input[placeholder="Tシャツ"]').fill("TEST_FAQ")
    page.locator('input[placeholder="ユニクロ"]').fill("TEST_FAQ")
    click_button(page, "保存する")
    wait_text(page, PRODUCT_TITLE)
    payload["productUrl"] = page.url
    record_step(payload, page, "product-created")


def create_catalog(page, payload):
    page.goto(f"{BASE}/admin/catalogs/create", wait_until="load", timeout=60000)
    wait_soft(page)
    page.locator('input[placeholder="渋谷店"]').fill(CATALOG_TITLE)
    click_button(page, "保存する")
    wait_text(page, CATALOG_TITLE)
    payload["catalogUrl"] = page.url
    record_step(payload, page, "catalog-created")


def status_finished(text, status_label):
    norm = normalized(text)
    return f"{status_label} 成功" in norm or f"{status_label} 失敗" in norm


def poll_status(page, status_label, attempts=24):
    body = text_of(page)
    for _ in range(attempts):
        if status_finished(body, status_label):
            return body
        page.wait_for_timeout(5000)
        page.reload(wait_until="domcontentloaded", timeout=60000)
        wait_soft(page, 800)
        body = text_of(page)
    return body


def run_catalog_import(page, payload, *, command, csv_path, key):
    result = {"command": command, "csv": str(csv_path.relative_to(ROOT)), "validationSuccess": False, "executionSuccess": False}
    payload[key] = result
    page.goto(f"{BASE}/admin/csv_import/csv_import_operation_catalog_products/create", wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    page.locator("select").first.select_option(label=CATALOG_TITLE)
    page.locator('input[type="file"]').set_input_files(str(csv_path))
    wait_soft(page)
    record_step(payload, page, f"{key}-form-filled")
    click_button(page, "保存する")
    wait_soft(page)
    record_step(payload, page, f"{key}-after-submit")
    if page.url.endswith("/create") and "ファイルを選択してください" in text_of(page):
        raise RuntimeError(f"{key} form rejected selected CSV file")

    validation_body = poll_status(page, "検証ステータス")
    record_step(payload, page, f"{key}-detail-after-validation")
    result["detailUrl"] = page.url
    result["validationSuccess"] = ("1個の商品" in validation_body or "1件の商品" in validation_body) and "成功" in validation_body
    if not result["validationSuccess"]:
        raise RuntimeError(f"{key} validation did not succeed")

    click_button(page, "実行する")
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    record_step(payload, page, f"{key}-execute-dialog")
    dialog = page.locator('div[role="dialog"]').last
    result["dialogText"] = compact(text_of(page), 1000)
    click_button(page, "実行する", scope=dialog)
    wait_soft(page)

    page.goto(result["detailUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    execution_body = poll_status(page, "実行ステータス")
    record_step(payload, page, f"{key}-detail-after-execution")
    result["executionSuccess"] = "成功" in execution_body and "完了" in execution_body
    if not result["executionSuccess"]:
        raise RuntimeError(f"{key} execution did not succeed")


def check_catalog_contains(page, payload, step, expected):
    page.goto(payload["catalogUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    body = text_of(page)
    contains = PRODUCT_TITLE in body
    record_step(payload, page, step)
    if expected:
        payload["catalogContainsAfterAdd"] = contains
    else:
        payload["catalogRemovedAfterDelete"] = not contains
    return contains


def delete_product(page, payload):
    if not payload.get("productUrl"):
        return
    page.goto(payload["productUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    click_button(page, "その他の操作")
    page.get_by_text("商品を削除する", exact=True).click(timeout=12000)
    page.wait_for_selector('div[role="dialog"]', timeout=12000)
    record_step(payload, page, "product-delete-dialog")
    dialog = page.locator('div[role="dialog"]').last
    click_button(page, "削除する", scope=dialog)
    wait_soft(page)
    page.goto(payload["productUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    body = text_of(page)
    payload["cleanup"]["productDeleted"] = "該当するProductが見つかりませんでした" in body
    record_step(payload, page, "product-after-delete")


def delete_catalog(page, payload):
    if not payload.get("catalogUrl"):
        return
    page.goto(payload["catalogUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    click_button(page, "その他の操作")
    page.get_by_text("カタログを削除する", exact=True).click(timeout=12000)
    page.wait_for_selector('div[role="dialog"]', timeout=12000)
    record_step(payload, page, "catalog-delete-dialog")
    dialog = page.locator('div[role="dialog"]').last
    click_button(page, "削除する", scope=dialog)
    wait_soft(page)
    page.goto(payload["catalogUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    body = text_of(page)
    payload["cleanup"]["catalogDeleted"] = "該当するCatalogが見つかりませんでした" in body
    record_step(payload, page, "catalog-after-delete")


def main():
    make_csv(ADD_CSV, "NEW")
    make_csv(DELETE_CSV, "DELETE")
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "productCode": PRODUCT_CODE,
        "productTitle": PRODUCT_TITLE,
        "catalogTitle": CATALOG_TITLE,
        "steps": [],
        "cleanup": {"productDeleted": False, "catalogDeleted": False},
        "complete": False,
        "error": None,
    }
    write_outputs(payload)
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(CDP)
            page = browser.contexts[0].new_page()
            page.set_default_timeout(20000)
            record_step(payload, page, "connected-cdp")
            try:
                create_product(page, payload)
                create_catalog(page, payload)
                run_catalog_import(page, payload, command="NEW", csv_path=ADD_CSV, key="add")
                if not check_catalog_contains(page, payload, "catalog-after-add", expected=True):
                    raise RuntimeError("catalog did not contain product after NEW import")
                run_catalog_import(page, payload, command="DELETE", csv_path=DELETE_CSV, key="delete")
                if check_catalog_contains(page, payload, "catalog-after-delete-import", expected=False):
                    raise RuntimeError("catalog still contained product after DELETE import")
                delete_product(page, payload)
                delete_catalog(page, payload)
                payload["complete"] = (
                    payload["add"]["validationSuccess"]
                    and payload["add"]["executionSuccess"]
                    and payload["delete"]["validationSuccess"]
                    and payload["delete"]["executionSuccess"]
                    and payload.get("catalogContainsAfterAdd")
                    and payload.get("catalogRemovedAfterDelete")
                    and payload["cleanup"].get("productDeleted")
                    and payload["cleanup"].get("catalogDeleted")
                )
            except Exception as exc:
                payload["error"] = repr(exc)
                try:
                    if not page.is_closed():
                        if payload.get("productUrl") and not payload["cleanup"].get("productDeleted"):
                            delete_product(page, payload)
                        if payload.get("catalogUrl") and not payload["cleanup"].get("catalogDeleted"):
                            delete_catalog(page, payload)
                except Exception as cleanup_exc:
                    payload["cleanupError"] = repr(cleanup_exc)
            finally:
                if not page.is_closed():
                    page.close()
    except Exception as exc:
        payload["error"] = repr(exc)
    write_outputs(payload)
    if not payload["complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
