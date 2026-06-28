#!/usr/bin/env python3
import json
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "06-catalog-csv-import-add-delete-cleanup-20260628.json"
OUT_MD = OUT_DIR / "06-catalog-csv-import-add-delete-cleanup-20260628.md"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def compact(text, limit=1800):
    return " ".join((text or "").split())[:limit]


def normalized(text):
    return " ".join((text or "").split())


def important(payload, text, limit=90):
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
        payload["productCode"],
        payload["productTitle"],
        payload["catalogTitle"],
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
        f"- 商品コード: `{payload['productCode']}`",
        f"- 商品名: `{payload['productTitle']}`",
        f"- カタログ: `{payload['catalogTitle']}`",
        f"- ADD CSV: `{payload.get('add', {}).get('csv')}`",
        f"- DELETE CSV: `{payload.get('delete', {}).get('csv')}`",
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
        "importantLines": important(payload, body),
        "bodySample": compact(body, 2200),
    })
    write_outputs(payload)


def wait_soft(page, ms=1200):
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(ms)


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


def click_button(page, name, scope=None, exact=True, timeout=15000):
    (scope or page).get_by_role("button", name=name, exact=exact).first.click(timeout=timeout)


def success_count_ok(body):
    return ("1個の商品" in body or "1件の商品" in body) and "成功" in body


def execute_existing_add(page, payload):
    page.goto(payload["add"]["detailUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    body = poll_status(page, "検証ステータス")
    payload["add"]["validationSuccess"] = success_count_ok(body)
    record_step(payload, page, "add-resume-detail-before-execution")
    if not payload["add"]["validationSuccess"]:
        raise RuntimeError("add validation did not succeed")
    if "実行ステータス 成功" not in normalized(body):
        click_button(page, "実行する")
        page.wait_for_selector('div[role="dialog"]', timeout=15000)
        record_step(payload, page, "add-resume-execute-dialog")
        dialog = page.locator('div[role="dialog"]').last
        payload["add"]["dialogText"] = compact(text_of(page), 1000)
        click_button(page, "実行する", scope=dialog)
        wait_soft(page)
    page.goto(payload["add"]["detailUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    body = poll_status(page, "実行ステータス")
    payload["add"]["executionSuccess"] = "成功" in body and "完了" in body
    record_step(payload, page, "add-resume-detail-after-execution")
    if not payload["add"]["executionSuccess"]:
        raise RuntimeError("add execution did not succeed")


def run_delete_import(page, payload):
    delete_csv = ROOT / payload["delete"]["csv"]
    page.goto(f"{BASE}/admin/csv_import/csv_import_operation_catalog_products/create", wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    page.locator("select").first.select_option(label=payload["catalogTitle"])
    page.locator('input[type="file"]').set_input_files(str(delete_csv))
    wait_soft(page)
    record_step(payload, page, "delete-form-filled")
    click_button(page, "保存する")
    wait_soft(page)
    record_step(payload, page, "delete-after-submit")
    body = poll_status(page, "検証ステータス")
    payload["delete"]["detailUrl"] = page.url
    payload["delete"]["validationSuccess"] = success_count_ok(body)
    record_step(payload, page, "delete-detail-after-validation")
    if not payload["delete"]["validationSuccess"]:
        raise RuntimeError("delete validation did not succeed")
    click_button(page, "実行する")
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    record_step(payload, page, "delete-execute-dialog")
    dialog = page.locator('div[role="dialog"]').last
    payload["delete"]["dialogText"] = compact(text_of(page), 1000)
    click_button(page, "実行する", scope=dialog)
    wait_soft(page)
    page.goto(payload["delete"]["detailUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    body = poll_status(page, "実行ステータス")
    payload["delete"]["executionSuccess"] = "成功" in body and "完了" in body
    record_step(payload, page, "delete-detail-after-execution")
    if not payload["delete"]["executionSuccess"]:
        raise RuntimeError("delete execution did not succeed")


def check_catalog(page, payload, step, expected):
    page.goto(payload["catalogUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    body = text_of(page)
    contains = payload["productTitle"] in body
    record_step(payload, page, step)
    if expected:
        payload["catalogContainsAfterAdd"] = contains
    else:
        payload["catalogRemovedAfterDelete"] = not contains
    return contains


def delete_product(page, payload):
    if not payload.get("productUrl") or payload["cleanup"].get("productDeleted"):
        return
    page.goto(payload["productUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    body = text_of(page)
    if "該当するProductが見つかりませんでした" in body:
        payload["cleanup"]["productDeleted"] = True
        record_step(payload, page, "product-already-deleted")
        return
    click_button(page, "その他の操作")
    page.get_by_text("商品を削除する", exact=True).click(timeout=12000)
    page.wait_for_selector('div[role="dialog"]', timeout=12000)
    record_step(payload, page, "product-delete-dialog")
    dialog = page.locator('div[role="dialog"]').last
    click_button(page, "削除する", scope=dialog)
    wait_soft(page)
    page.goto(payload["productUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    payload["cleanup"]["productDeleted"] = "該当するProductが見つかりませんでした" in text_of(page)
    record_step(payload, page, "product-after-delete")


def delete_catalog(page, payload):
    if not payload.get("catalogUrl"):
        return
    page.goto(payload["catalogUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    body = text_of(page)
    if "該当するCatalogが見つかりませんでした" in body:
        payload["cleanup"]["catalogDeleted"] = True
        record_step(payload, page, "catalog-already-deleted")
        return
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


def finalize(payload):
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
    write_outputs(payload)


def main():
    payload = json.loads(OUT_JSON.read_text())
    payload.setdefault("delete", {
        "command": "DELETE",
        "csv": "_analysis/complete-live-verification-2026-06-28/06-catalog-csv-import-delete-20260628_082508.csv",
        "validationSuccess": False,
        "executionSuccess": False,
    })
    payload.setdefault("cleanup", {"productDeleted": False, "catalogDeleted": False})
    payload["error"] = None
    payload.pop("cleanupError", None)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(20000)
        try:
            record_step(payload, page, "resume-connected-cdp")
            if not (payload.get("add", {}).get("validationSuccess") and payload.get("add", {}).get("executionSuccess")):
                execute_existing_add(page, payload)
            if not payload.get("catalogContainsAfterAdd"):
                if not check_catalog(page, payload, "catalog-after-add", expected=True):
                    raise RuntimeError("catalog did not contain product after NEW import")
            if not (payload.get("delete", {}).get("validationSuccess") and payload.get("delete", {}).get("executionSuccess")):
                run_delete_import(page, payload)
            if not payload.get("catalogRemovedAfterDelete"):
                if check_catalog(page, payload, "catalog-after-delete-import", expected=False):
                    raise RuntimeError("catalog still contained product after DELETE import")
            delete_product(page, payload)
            delete_catalog(page, payload)
        except Exception as exc:
            payload["error"] = repr(exc)
            try:
                delete_product(page, payload)
                delete_catalog(page, payload)
            except Exception as cleanup_exc:
                payload["cleanupError"] = repr(cleanup_exc)
        finally:
            finalize(payload)
            if not page.is_closed():
                page.close()
    if not payload["complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
