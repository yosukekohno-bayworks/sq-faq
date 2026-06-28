#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "16-orders-returns-empty-state-recheck-20260628.json"
OUT_MD = OUT_DIR / "16-orders-returns-empty-state-recheck-20260628.md"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
TOKEN_RE = re.compile(r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))")


def redact(value):
    if isinstance(value, str):
        return TOKEN_RE.sub("[REDACTED_LONG_VALUE]", value)
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    return value


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snap(page):
    data = page.evaluate(
        """() => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const body = document.body ? document.body.innerText.replace(/\\s+/g, ' ').trim() : '';
            const buttons = Array.from(document.querySelectorAll('button, [role="button"], a.Polaris-Button')).map((el) => ({
                text: text(el) || el.getAttribute('aria-label') || '',
                tag: el.tagName.toLowerCase(),
                href: el.getAttribute('href'),
                disabled: !!el.disabled || el.className.toString().includes('disabled'),
                ariaDisabled: el.getAttribute('aria-disabled'),
                className: el.className.toString()
            })).filter((x) => x.text);
            return {
                url: location.href,
                title: document.title,
                h1: Array.from(document.querySelectorAll('h1')).map(text).filter(Boolean),
                buttons,
                links: Array.from(document.querySelectorAll('a[href]')).map((a) => ({
                    text: text(a),
                    href: a.getAttribute('href')
                })).filter((x) => x.text || x.href),
                tableHeaders: Array.from(document.querySelectorAll('th')).map(text).filter(Boolean),
                hasNoItems: body.includes('アイテムが見つかりませんでした'),
                hasNoOrders: body.includes('注文が見つかりませんでした'),
                hasFilterHint: body.includes('絞り込みや検索ワードを変更してみてください'),
                hasSearchResultTitle: body.includes('検索と絞り込みの結果'),
                hasSearchPlaceholder: body.includes('注文番号で検索する') || body.includes('キーワードで検索する'),
                hasAddFilter: body.includes('絞り込みを追加'),
                hasSaveView: body.includes('名前を付けて保存'),
                hasCancel: body.includes('キャンセル'),
                hasExchangeShipment: body.includes('交換出荷'),
                hasUnexpectedError: body.includes('予期せぬエラーが発生しました'),
                hasNotFound: body.includes('このページは存在しないようです'),
                bodySample: body.slice(0, 2400)
            };
        }"""
    )
    return redact(data)


def visit(page, route):
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    return snap(page)


def click_draft_create(page):
    before_url = page.url
    result = {
        "beforeUrl": before_url,
        "clicked": False,
        "afterUrl": before_url,
        "error": None,
    }
    try:
        link = page.get_by_text("注文を作成する", exact=True)
        if link.count() > 0:
            link.first.click(timeout=5000)
            wait_quiet(page, timeout=3000)
            result["clicked"] = True
            result["afterUrl"] = page.url
    except Exception as exc:
        result["error"] = repr(exc)
        result["afterUrl"] = page.url
    return result


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "errors": [],
        "pages": {},
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)

        for name, route in [
            ("orders", "/admin/orders"),
            ("ordersCreate", "/admin/orders/create"),
            ("draftOrders", "/admin/draft_orders"),
            ("draftOrdersCreate", "/admin/draft_orders/create"),
            ("orderReturns", "/admin/order_returns"),
            ("orderReturnsCreate", "/admin/order_returns/create"),
        ]:
            try:
                payload["pages"][name] = visit(page, route)
                if name == "draftOrders":
                    payload["draftCreateClick"] = click_draft_create(page)
                    payload["pages"]["draftOrdersAfterClick"] = snap(page)
            except Exception as exc:
                payload["errors"].append({name: repr(exc)})

        page.close()
        browser.close()

    payload["facts"] = {
        "orders": {
            "empty": payload["pages"].get("orders", {}).get("hasNoItems"),
            "hasSearchUi": any(payload["pages"].get("orders", {}).get(k) for k in ["hasSearchResultTitle", "hasSearchPlaceholder", "hasAddFilter", "hasSaveView"]),
            "createUnexpectedError": payload["pages"].get("ordersCreate", {}).get("hasUnexpectedError"),
        },
        "draftOrders": {
            "empty": payload["pages"].get("draftOrders", {}).get("hasNoOrders"),
            "createButton": [
                b for b in payload["pages"].get("draftOrders", {}).get("buttons", [])
                if "注文を作成する" in b.get("text", "")
            ],
            "clickResult": payload.get("draftCreateClick"),
            "directCreateUnexpectedError": payload["pages"].get("draftOrdersCreate", {}).get("hasUnexpectedError"),
        },
        "orderReturns": {
            "empty": payload["pages"].get("orderReturns", {}).get("hasNoItems"),
            "hasReturnActionUi": any(payload["pages"].get("orderReturns", {}).get(k) for k in ["hasSearchResultTitle", "hasSearchPlaceholder", "hasAddFilter", "hasCancel", "hasExchangeShipment"]),
            "createNotFound": payload["pages"].get("orderReturnsCreate", {}).get("hasNotFound"),
        },
    }

    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 16 注文・返品 空状態再確認 2026-06-28",
        "",
        f"- 実行日時: {payload['generatedAt']}",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        f"- エラー数: `{len(payload['errors'])}`",
        "",
        "## 結果",
        "",
        f"- 注文一覧は空状態: `{payload['facts']['orders']['empty']}`",
        f"- 注文一覧の検索/絞り込みUIあり: `{payload['facts']['orders']['hasSearchUi']}`",
        f"- `/admin/orders/create` は予期せぬエラー画面: `{payload['facts']['orders']['createUnexpectedError']}`",
        f"- 下書き一覧は空状態: `{payload['facts']['draftOrders']['empty']}`",
        f"- 下書き `注文を作成する` クリック後URL: `{payload['facts']['draftOrders']['clickResult']}`",
        f"- `/admin/draft_orders/create` は予期せぬエラー画面: `{payload['facts']['draftOrders']['directCreateUnexpectedError']}`",
        f"- 返品一覧は空状態: `{payload['facts']['orderReturns']['empty']}`",
        f"- 返品一覧の検索/絞り込み/キャンセル/交換出荷UIあり: `{payload['facts']['orderReturns']['hasReturnActionUi']}`",
        f"- `/admin/order_returns/create` は存在しない画面: `{payload['facts']['orderReturns']['createNotFound']}`",
        "",
        "## 判断",
        "",
        "- 現行の注文/下書き/返品一覧は、空状態と直URLエラーまで確認済み。",
        "- 注文データあり状態の列・検索/絞り込み・ステータス遷移・返品処理は、注文/返品データ投入または外部チャネル接続が必要。",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "json": str(OUT_JSON),
        "md": str(OUT_MD),
        "facts": payload["facts"],
        "errors": payload["errors"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
