#!/usr/bin/env python3
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "22-product-csv-import-execute-cleanup-20260628.json"
OUT_MD = OUT_DIR / "22-product-csv-import-execute-cleanup-20260628.md"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
PRODUCT_CODE = f"TEST_FAQ_CSV_EXEC_{STAMP}"
PRODUCT_TITLE = f"TEST_FAQ_CSV_EXEC_{STAMP}_商品"
CSV_PATH = OUT_DIR / f"22-product-csv-import-execute-cleanup-{STAMP}.csv"


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def compact(text, limit=1800):
    return " ".join((text or "").split())[:limit]


def important(text, limit=80):
    patterns = (
        "CSV",
        "インポート",
        "商品",
        "検証",
        "実行",
        "成功",
        "失敗",
        "完了",
        "未実行",
        "処理中",
        "エラー",
        "ファイル",
        "保存",
        "作成日",
        "ステータス",
        "巻き戻すことができません",
        PRODUCT_CODE,
        PRODUCT_TITLE,
    )
    lines = []
    for line in (text or "").splitlines():
        line = line.strip()
        if line and any(pattern in line for pattern in patterns) and line not in lines:
            lines.append(line)
    return lines[:limit]


def wait_soft(page):
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1200)


def click_button(page, name, scope=None, exact=True, timeout=15000):
    (scope or page).get_by_role("button", name=name, exact=exact).first.click(timeout=timeout)


def record_step(payload, page, step):
    body = text_of(page)
    payload["steps"].append({
        "step": step,
        "url": page.url,
        "importantLines": important(body),
        "bodySample": compact(body, 2000),
    })
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def make_csv():
    headers = [
        "command",
        "product_code",
        "title",
        "description",
        "product_status",
        "brand_code",
        "product_vendor",
        "product_type",
        "tags",
        "option1_name",
        "option1_type",
        "option2_name",
        "option2_type",
        "option3_name",
        "option3_type",
        "seo_title",
        "seo_description",
        "is_outlet",
        "sale_start_date",
        "sale_end_date",
    ]
    row = [
        "NEW",
        PRODUCT_CODE,
        PRODUCT_TITLE,
        "CSV実行検証用。作成後に削除する。",
        "DRAFT",
        "",
        "TEST_FAQ",
        "TEST_FAQ_CSV",
        "TEST_FAQ_CSV_EXEC",
        "サイズ",
        "SIZE",
        "",
        "",
        "",
        "",
        "",
        "",
        "FALSE",
        "",
        "",
    ]
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(row)


def find_latest_import_detail(page):
    links = page.locator("a").evaluate_all(
        """els => els
          .map(a => ({text: (a.textContent || '').trim(), href: a.href || ''}))
          .filter(a => /CSVImportOperationProduct/.test(a.href))"""
    )
    return links[0]["href"] if links else None


def poll_text(page, predicate, reload=False, attempts=12, wait_ms=5000):
    body = text_of(page)
    for _ in range(attempts):
        if predicate(body):
            return body
        page.wait_for_timeout(wait_ms)
        if reload:
            page.reload(wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
        body = text_of(page)
    return body


def normalized(text):
    return " ".join((text or "").split())


def validation_finished(text):
    norm = normalized(text)
    return (
        "1個の商品" in norm
        or "検証ステータス 成功" in norm
        or "検証ステータス 失敗" in norm
    )


def execution_finished(text):
    norm = normalized(text)
    return "実行ステータス 成功" in norm or "実行ステータス 失敗" in norm


def product_search_and_open(page, payload):
    page.goto(f"{BASE}/admin/products", wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    body = text_of(page)
    search = page.locator('input[type="search"], input[placeholder*="検索"], input[aria-label*="検索"]').first
    if (PRODUCT_CODE not in body and PRODUCT_TITLE not in body) and search.count():
        search.fill(PRODUCT_CODE)
        page.keyboard.press("Enter")
        wait_soft(page)
    record_step(payload, page, "products-search-after-execute")
    body = text_of(page)
    payload["productVisibleAfterExecution"] = PRODUCT_CODE in body or PRODUCT_TITLE in body
    hrefs = page.locator("a").evaluate_all(
        """(els, title) => els
          .map(a => ({text: (a.textContent || '').trim(), href: a.href || ''}))
          .filter(a => a.text.includes(title) && /\\/admin\\/products\\//.test(a.href))""",
        PRODUCT_TITLE,
    )
    if hrefs:
        payload["productUrl"] = hrefs[0]["href"]
        page.goto(payload["productUrl"], wait_until="domcontentloaded", timeout=60000)
        wait_soft(page)
        record_step(payload, page, "product-detail-before-delete")


def delete_product_if_open(page, payload):
    if not payload.get("productUrl"):
        return
    try:
        click_button(page, "その他の操作")
        page.get_by_text("商品を削除する", exact=True).click(timeout=12000)
        page.wait_for_selector('div[role="dialog"]', timeout=12000)
        record_step(payload, page, "delete-dialog")
        dialog = page.locator('div[role="dialog"]').last
        click_button(page, "削除する", scope=dialog)
        wait_soft(page)
        page.goto(payload["productUrl"], wait_until="domcontentloaded", timeout=60000)
        wait_soft(page)
        body = text_of(page)
        payload["cleanup"]["productDeleted"] = "該当するProductが見つかりませんでした" in body
        payload["cleanup"]["postDeleteBodySample"] = compact(body, 1000)
        record_step(payload, page, "product-detail-after-delete")
    except Exception as exc:
        payload["cleanup"]["deleteError"] = repr(exc)
        payload["cleanup"]["postErrorBodySample"] = compact(text_of(page), 1000)


def write_outputs(payload):
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    md = [
        "# 22 商品CSVインポート実行・削除確認 2026-06-28",
        "",
        "## 対象",
        "",
        f"- CSV: `{CSV_PATH.relative_to(ROOT)}`",
        f"- 商品コード: `{PRODUCT_CODE}`",
        f"- 商品名: `{PRODUCT_TITLE}`",
        f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
        "",
        "## 結果",
        "",
        f"- 検証成功件数: `{payload.get('validationSuccessText', '')}`",
        f"- 実行確認ダイアログ: `{'確認' if payload.get('executeDialogSeen') else '未確認'}`",
        f"- 実行ステータス: `{payload.get('executionSuccessText', '')}`",
        f"- 商品一覧反映: `{'確認' if payload.get('productVisibleAfterExecution') else '未確認'}`",
        f"- 商品削除: `{'確認' if payload.get('cleanup', {}).get('productDeleted') else '未確認'}`",
        "",
        "## 判定",
        "",
    ]
    if payload.get("complete"):
        md.extend([
            "- 商品CSVインポートは、CSVアップロード後に検証ステータスが成功完了となり、`実行する` で確認ダイアログを経て実行される。",
            "- 確認ダイアログには `この操作は巻き戻すことができません` が表示される。",
            "- 実行後、検証用商品は商品一覧に反映された。",
            "- 検証用商品は商品詳細から削除でき、削除後は該当Productなし表示になった。",
        ])
    else:
        md.append(f"- 未完了: `{payload.get('error') or payload.get('cleanup', {}).get('deleteError') or '条件未達'}`")
    md.extend(["", "## ステップ", ""])
    for step in payload.get("steps", []):
        md.append(f"### {step['step']}")
        md.append("")
        md.append(f"- URL: `{step['url']}`")
        for line in step.get("importantLines", [])[:20]:
            md.append(f"- {line}")
        md.append("")
    OUT_MD.write_text("\n".join(md) + "\n")


def main():
    make_csv()
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "csv": str(CSV_PATH.relative_to(ROOT)),
        "productCode": PRODUCT_CODE,
        "productTitle": PRODUCT_TITLE,
        "steps": [],
        "detailUrl": None,
        "productUrl": None,
        "executeDialogSeen": False,
        "productVisibleAfterExecution": False,
        "cleanup": {"productDeleted": False},
        "error": None,
        "complete": False,
    }
    write_outputs(payload)
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(CDP)
            context = browser.contexts[0]
            page = context.new_page()
            page.set_default_timeout(20000)
            payload["steps"].append({
                "step": "connected-cdp",
                "url": page.url,
                "importantLines": [],
                "bodySample": "",
            })
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

            page.goto(f"{BASE}/admin/csv_import/csv_import_operation_products/create", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            record_step(payload, page, "create-before-upload")

            page.locator('input[type="file"]').set_input_files(str(CSV_PATH))
            wait_soft(page)
            record_step(payload, page, "create-file-selected")

            click_button(page, "保存する")
            wait_soft(page)
            record_step(payload, page, "after-submit")

            body = poll_text(
                page,
                validation_finished,
                reload=True,
                attempts=24,
                wait_ms=5000,
            )
            record_step(payload, page, "detail-after-validation-poll")
            payload["validationSuccessText"] = "1個の商品" if "1個の商品" in body else ""
            payload["detailUrl"] = page.url
            if "1個の商品" not in body:
                raise RuntimeError("CSV validation did not succeed")

            click_button(page, "実行する")
            wait_soft(page)
            payload["executeDialogSeen"] = "CSVの取り込み処理を実行しますか？" in text_of(page)
            record_step(payload, page, "execute-dialog")
            dialog = page.locator('div[role="dialog"]').last
            click_button(page, "実行する", scope=dialog)
            wait_soft(page)
            record_step(payload, page, "after-confirm-execute")

            body = poll_text(
                page,
                execution_finished,
                reload=True,
                attempts=24,
                wait_ms=5000,
            )
            payload["executionSuccessText"] = "成功 完了" if "成功" in body and "完了" in body else ""
            record_step(payload, page, "detail-after-execution-poll")

            product_search_and_open(page, payload)
            delete_product_if_open(page, payload)
            payload["complete"] = (
                payload["executeDialogSeen"]
                and payload.get("executionSuccessText")
                and payload["productVisibleAfterExecution"]
                and payload["cleanup"].get("productDeleted")
            )
            page.close()
    except Exception as exc:
        payload["error"] = repr(exc)
    write_outputs(payload)
    if not payload["complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
