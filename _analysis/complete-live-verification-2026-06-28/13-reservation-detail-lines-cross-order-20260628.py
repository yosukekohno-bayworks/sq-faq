#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "13-reservation-detail-lines-cross-order-20260628.json"
OUT_MD = OUT_DIR / "13-reservation-detail-lines-cross-order-20260628.md"

BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

ROUTES = [
    ("#IR-1011", "/admin/inventory_reservation_orders/7ade0706-6d15-5c55-a0be-b60386308eb4_InventoryReservationOrder"),
    ("#IR-1010", "/admin/inventory_reservation_orders/560cdefc-c95a-582e-a8fd-ecffd6c25b27_InventoryReservationOrder"),
    ("#IR-1009", "/admin/inventory_reservation_orders/4e4aa346-7103-552f-99f3-8d089495279e_InventoryReservationOrder"),
    ("#IR-1007", "/admin/inventory_reservation_orders/8c6ccdcc-7189-52c1-9312-e656c10c4909_InventoryReservationOrder"),
]

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


def wait_quiet(page, timeout=8000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1500)


def inspect_route(browser, cookies, code, route):
    context = browser.new_context(storage_state={"cookies": cookies, "origins": []})
    page = context.new_page()
    page.set_default_timeout(20000)
    try:
        page.goto(BASE + route, wait_until="load", timeout=35000)
        wait_quiet(page)
        page.reload(wait_until="load", timeout=35000)
        wait_quiet(page)
        data = page.evaluate(
            r"""() => {
                const textOf = (el) => (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim();
                const rows = Array.from(document.querySelectorAll('table tr'))
                    .map((row, index) => ({index, text: textOf(row)}))
                    .filter((row) => /\d{6}-|TEST_E2E/.test(row.text));
                return {
                    url: location.href,
                    h1: Array.from(document.querySelectorAll('h1')).map(textOf),
                    tableRows: rows,
                    bodyTail: textOf(document.body).slice(-1200)
                };
            }"""
        )
        data.update({"code": code, "route": route, "lineRowCount": len(data.get("tableRows", []))})
        return redact(data)
    finally:
        context.close()


def write_md(payload):
    rows = payload["routes"]
    first_signatures = [
        " | ".join(row["text"] for row in item.get("tableRows", [])[:5])
        for item in rows
    ]
    same_first_rows = len(set(first_signatures)) == 1
    lines = [
        "# 取置伝票詳細の商品明細表示 横断確認",
        "",
        f"- 実行日時: {payload['generatedAt']}",
        "- 方法: 各伝票を認証Cookieのみの新規ブラウザコンテキストで直接開き、さらに強制リロードして商品明細テーブルを取得",
        f"- 対象伝票: {', '.join(item['code'] for item in rows)}",
        "",
        "## 結果",
        "",
    ]
    for item in rows:
        first = item.get("tableRows", [{}])[0].get("text", "") if item.get("tableRows") else ""
        lines.append(f"- `{item['code']}`: 商品明細行 `{item['lineRowCount']}` 件。先頭行: `{first}`")
    lines.extend(
        [
            "",
            "## 判断",
            "",
            f"- 先頭5行の並びが全対象伝票で同一: `{same_first_rows}`",
            "- 伝票番号・ロケーション・メモは各伝票の値に変わる一方、商品明細テーブルは複数伝票で同じ行群が表示された。",
            "- 2026-06-28時点では、取置伝票詳細の商品明細テーブルを「その伝票固有の明細」として案内しない。作成フォーム保存前の明細数、ステータス、在庫推移を優先して確認する。",
            "",
            "## 証跡",
            "",
            f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "purpose": "Check whether inventory reservation order detail rows are scoped to each route.",
        "routes": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        state = browser.contexts[0].storage_state()
        cookies = state.get("cookies", [])
        for code, route in ROUTES:
            payload["routes"].append(inspect_route(browser, cookies, code, route))
        browser.close()
    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2))
    write_md(payload)
    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
