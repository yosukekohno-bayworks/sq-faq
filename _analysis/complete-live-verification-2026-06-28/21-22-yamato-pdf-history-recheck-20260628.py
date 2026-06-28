#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "21-22-yamato-pdf-history-recheck-20260628.json"
OUT_MD = OUT_DIR / "21-22-yamato-pdf-history-recheck-20260628.md"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
TOKEN_RE = re.compile(r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))")

ROUTES = [
    ("yamato_export_history", "/admin/csv_export/csv_export_operation_inventory_outbound_order_yamato_b2_clouds"),
    ("yamato_export_form", "/admin/inventory_outbound_orders/export/yamato_b2_cloud"),
    ("pdf_export_top", "/admin/pdf_export"),
    ("pdf_export_packing_slips", "/admin/pdf_export/pdf_export_operation_packing_slips"),
    ("pdf_export_packing_slips_create", "/admin/pdf_export/pdf_export_operation_packing_slips/create"),
]


def redact(value):
    if isinstance(value, str):
        return TOKEN_RE.sub("[REDACTED_LONG_VALUE]", value)
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items()}
    return value


def wait_quiet(page):
    try:
        page.wait_for_load_state("networkidle", timeout=7000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1000)


def inspect(page, route):
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    data = page.evaluate(
        """() => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const body = text(document.body);
            const links = Array.from(document.querySelectorAll('a[href]')).map((a) => ({
                text: text(a),
                href: a.getAttribute('href')
            })).filter((x) => x.text || x.href);
            const downloadLinks = links.filter((x) => {
                const haystack = `${x.text} ${x.href}`;
                return /ダウンロード|download|\\.csv(\\?|$)|\\.pdf(\\?|$)|packing[_-]?slip/i.test(haystack);
            });
            return {
                url: location.href,
                h1: Array.from(document.querySelectorAll('h1')).map(text).filter(Boolean),
                buttons: Array.from(document.querySelectorAll('button')).map(text).filter(Boolean),
                tableHeaders: Array.from(document.querySelectorAll('th')).map(text).filter(Boolean),
                links,
                downloadLinks,
                hasNoItems: body.includes('アイテムが見つかりませんでした'),
                hasNotFound: body.includes('このページは存在しないようです'),
                hasPackingSlipText: body.includes('同梱する納品書PDF') || body.includes('納品書'),
                hasMailNotice: body.includes('メール') || body.includes('ダウンロードリンク'),
                bodySample: body.slice(0, 3200)
            };
        }"""
    )
    return redact(data)


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "purpose": "Recheck whether Yamato B2 export history exposes downloadable CSV/PDF links and whether PDF packing-slip routes expose generation UI.",
        "pages": {},
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(25000)
        try:
            for name, route in ROUTES:
                payload["pages"][name] = inspect(page, route)
        finally:
            page.close()
            browser.close()

    payload["facts"] = {
        "yamatoHistoryEmpty": payload["pages"]["yamato_export_history"]["hasNoItems"],
        "yamatoHistoryDownloadLinks": payload["pages"]["yamato_export_history"]["downloadLinks"],
        "yamatoFormShowsPackingSlip": payload["pages"]["yamato_export_form"]["hasPackingSlipText"],
        "yamatoFormShowsMailNotice": payload["pages"]["yamato_export_form"]["hasMailNotice"],
        "pdfCategoryEmpty": payload["pages"]["pdf_export_packing_slips"]["hasNoItems"],
        "pdfCreateNotFound": payload["pages"]["pdf_export_packing_slips_create"]["hasNotFound"],
    }

    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 21/22 ヤマトB2・納品書PDF履歴再確認 2026-06-28",
        "",
        f"- 実行日時: {payload['generatedAt']}",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        "",
        "## 結果",
        "",
        f"- ヤマトB2 CSVエクスポート履歴は空状態: `{payload['facts']['yamatoHistoryEmpty']}`",
        f"- ヤマトB2 CSVエクスポート履歴のダウンロードリンク数: `{len(payload['facts']['yamatoHistoryDownloadLinks'])}`",
        f"- ヤマトB2条件指定フォームに納品書PDF表示あり: `{payload['facts']['yamatoFormShowsPackingSlip']}`",
        f"- ヤマトB2条件指定フォームにメール/ダウンロードリンク通知文言あり: `{payload['facts']['yamatoFormShowsMailNotice']}`",
        f"- PDF納品書カテゴリページは空状態: `{payload['facts']['pdfCategoryEmpty']}`",
        f"- PDF納品書 `/create` は存在しない画面: `{payload['facts']['pdfCreateNotFound']}`",
        "",
        "## 判断",
        "",
        "- 現環境では、ヤマトB2エクスポート履歴からCSV/PDFの実ファイルまたはダウンロードリンクを確認できない。",
        "- 画面上確認できる納品書PDFの入口はヤマトB2条件指定フォームの表示まで。PDFエクスポート画面単体には任意生成導線がない。",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
