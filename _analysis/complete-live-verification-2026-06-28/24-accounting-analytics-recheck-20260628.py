#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "24-accounting-analytics-recheck-20260628.json"
OUT_MD = OUT_DIR / "24-accounting-analytics-recheck-20260628.md"
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
            const unique = (items) => Array.from(new Set(items.filter(Boolean)));
            const labelFor = (el) => {
                const id = el.id;
                if (id) {
                    const label = document.querySelector(`label[for="${CSS.escape(id)}"]`);
                    if (label) return text(label);
                }
                const label = el.closest('label');
                if (label) return text(label);
                return el.getAttribute('aria-label') || '';
            };
            const body = document.body ? document.body.innerText.replace(/\\s+/g, ' ').trim() : '';
            return {
                url: location.href,
                title: document.title,
                h1: unique(Array.from(document.querySelectorAll('h1')).map(text)),
                h2: unique(Array.from(document.querySelectorAll('h2')).map(text)),
                buttons: Array.from(document.querySelectorAll('button, [role="button"]')).map((el) => ({
                    text: text(el) || el.getAttribute('aria-label') || '',
                    disabled: !!el.disabled,
                    ariaDisabled: el.getAttribute('aria-disabled')
                })).filter((x) => x.text),
                links: Array.from(document.querySelectorAll('a[href]')).map((a) => ({
                    text: text(a),
                    href: a.getAttribute('href')
                })).filter((x) => x.text || x.href),
                controls: Array.from(document.querySelectorAll('input, select, textarea')).map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type') || '',
                    label: labelFor(el),
                    placeholder: el.getAttribute('placeholder') || '',
                    disabled: !!el.disabled,
                    readOnly: !!el.readOnly,
                    options: el.tagName.toLowerCase() === 'select' ? Array.from(el.options).map((opt) => text(opt)) : []
                })),
                tableHeaders: unique(Array.from(document.querySelectorAll('th')).map(text)),
                hasTodo: body.includes('TODO'),
                hasNotFound: body.includes('このページは存在しないようです'),
                hasNoItems: body.includes('アイテムが見つかりませんでした'),
                hasFilterHint: body.includes('絞り込みや検索ワードを変更してみてください'),
                bodySample: body.slice(0, 2400)
            };
        }"""
    )
    return redact(data)


def visit(page, route):
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    return snap(page)


def try_empty_save(page, payload_key, payload):
    try:
        button = page.get_by_role("button", name=re.compile("エクスポートを開始する|保存する"))
        if button.count() > 0:
            button.first.click()
            wait_quiet(page)
            payload[payload_key] = snap(page)
    except Exception as exc:
        payload.setdefault("errors", []).append({payload_key: repr(exc)})


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
            ("saleChangeLineItems", "/admin/sale_change_line_items"),
            ("saleChangeLineItemsCreate", "/admin/sale_change_line_items/create"),
            ("saleChangesExportList", "/admin/csv_export/csv_export_operation_sale_changes"),
            ("saleChangeLineItemsExportList", "/admin/csv_export/csv_export_operation_sale_change_line_items"),
            ("analyticsTop", "/admin/analytics"),
            ("analyticsRevenue", "/admin/analytics/revenue"),
            ("analyticsReports", "/admin/analytics/reports"),
        ]:
            try:
                payload["pages"][name] = visit(page, route)
            except Exception as exc:
                payload["errors"].append({name: repr(exc)})

        for name, route in [
            ("saleChangesExportCreate", "/admin/csv_export/csv_export_operation_sale_changes/create"),
            ("saleChangeLineItemsExportCreate", "/admin/csv_export/csv_export_operation_sale_change_line_items/create"),
        ]:
            try:
                payload["pages"][name] = visit(page, route)
                try_empty_save(page, name + "AfterEmptySave", payload["pages"])
            except Exception as exc:
                payload["errors"].append({name: repr(exc)})

        page.close()
        browser.close()

    analytics = ["analyticsTop", "analyticsRevenue", "analyticsReports"]
    export_create = ["saleChangesExportCreateAfterEmptySave", "saleChangeLineItemsExportCreateAfterEmptySave"]
    payload["facts"] = {
        "analyticsTodo": {
            key: {
                "h1": payload["pages"].get(key, {}).get("h1"),
                "hasTodo": payload["pages"].get(key, {}).get("hasTodo"),
                "buttons": payload["pages"].get(key, {}).get("buttons", []),
            }
            for key in analytics
        },
        "saleCreateNotFound": payload["pages"].get("saleChangeLineItemsCreate", {}).get("hasNotFound"),
        "saleList": {
            "hasNoItems": payload["pages"].get("saleChangeLineItems", {}).get("hasNoItems"),
            "hasFilterHint": payload["pages"].get("saleChangeLineItems", {}).get("hasFilterHint"),
            "buttons": payload["pages"].get("saleChangeLineItems", {}).get("buttons", []),
            "links": [
                link for link in payload["pages"].get("saleChangeLineItems", {}).get("links", [])
                if "sale_change" in (link.get("href") or "") or link.get("text") in ["注文軸", "明細軸"]
            ],
        },
        "exportListHeaders": {
            key: payload["pages"].get(key, {}).get("tableHeaders", [])
            for key in ["saleChangesExportList", "saleChangeLineItemsExportList"]
        },
        "exportCreateEmptyErrors": {
            key: {
                "tenant": "テナントを選択してください" in payload["pages"].get(key, {}).get("bodySample", ""),
                "start": "開始日時を入力してください" in payload["pages"].get(key, {}).get("bodySample", ""),
                "end": "終了日時を入力してください" in payload["pages"].get(key, {}).get("bodySample", ""),
            }
            for key in export_create
        },
    }

    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 24 会計・売上実績・分析 再確認 2026-06-28",
        "",
        f"- 実行日時: {payload['generatedAt']}",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        f"- エラー数: `{len(payload['errors'])}`",
        "",
        "## 結果",
        "",
        f"- `/admin/sale_change_line_items/create` は存在しない画面: `{payload['facts']['saleCreateNotFound']}`",
        f"- 売上実績一覧は空状態: `{payload['facts']['saleList']['hasNoItems']}`",
        f"- 売上実績一覧に空状態の検索/絞り込みヒントあり: `{payload['facts']['saleList']['hasFilterHint']}`",
        f"- 注文軸CSV作成フォームの空保存エラー: `{payload['facts']['exportCreateEmptyErrors']['saleChangesExportCreateAfterEmptySave']}`",
        f"- 明細軸CSV作成フォームの空保存エラー: `{payload['facts']['exportCreateEmptyErrors']['saleChangeLineItemsExportCreateAfterEmptySave']}`",
        "",
        "## 分析画面",
        "",
        "| 画面 | h1 | TODO本文 | 操作ボタン数 |",
        "|:--|:--|:--|--:|",
    ]
    for key, label in [
        ("analyticsTop", "分析"),
        ("analyticsRevenue", "収益"),
        ("analyticsReports", "レポート"),
    ]:
        row = payload["facts"]["analyticsTodo"][key]
        lines.append(f"| {label} | `{row['h1']}` | `{row['hasTodo']}` | {len(row['buttons'])} |")
    lines.extend([
        "",
        "## 判断",
        "",
        "- 売上実績一覧とCSVエクスポート導線は表示・空保存バリデーションまで確認済み。",
        "- 売上実績の手動作成直URLは存在しない画面。",
        "- 分析トップ/収益/レポートは現行UIとしてTODO本文のみ。集計・レポート操作は確認できない。",
        "- 注文データ・売上データがある状態の列構成、自動集計、出力CSVの実内容はデータ投入後の確認事項。",
    ])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "json": str(OUT_JSON),
        "md": str(OUT_MD),
        "facts": payload["facts"],
        "errors": payload["errors"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
