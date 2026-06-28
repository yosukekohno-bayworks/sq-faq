#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT = OUT_DIR / "20-smaregi-detail-tabs-20260628.json"
MD = OUT.with_suffix(".md")

DETAIL_ROUTE = "/admin/smaregi_integrations/a1ff4fd5-5636-571d-9c40-f222135d52ef_SmaregiIntegration"
TAB_ROUTES = {
    "店舗設定": DETAIL_ROUTE + "/location_links",
    "商品管理": DETAIL_ROUTE + "/products",
    "顧客管理": DETAIL_ROUTE + "/customers",
}


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1500)


def safe_state(page):
    return page.evaluate(
        """() => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const unique = (items) => Array.from(new Set(items.filter(Boolean)));
            return {
                url: location.href,
                h1: unique(Array.from(document.querySelectorAll('h1')).map(text)),
                h2: unique(Array.from(document.querySelectorAll('h2')).map(text)),
                labels: unique(Array.from(document.querySelectorAll('label')).map(text)),
                buttons: unique(Array.from(document.querySelectorAll('button')).map((button) => text(button) || button.getAttribute('aria-label') || '')),
                tableHeaders: unique(Array.from(document.querySelectorAll('th')).map(text)),
                links: Array.from(document.querySelectorAll('a[href]')).map((a) => ({ text: text(a), href: a.getAttribute('href') })).filter((x) => x.text || (x.href || '').includes('smaregi_integrations')),
                fields: Array.from(document.querySelectorAll('input, select, textarea')).map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type') || '',
                    placeholder: el.getAttribute('placeholder') || '',
                    disabled: !!el.disabled,
                    options: el.tagName.toLowerCase() === 'select' ? Array.from(el.options).map((opt) => text(opt)) : []
                })),
                includes: {
                    productSetting: document.body.innerText.includes('商品連携設定'),
                    inventorySetting: document.body.innerText.includes('在庫設定'),
                    transactionSetting: document.body.innerText.includes('取引連携設定'),
                    externalAccessToken: document.body.innerText.includes('外部アクセストークン'),
                    unlink: document.body.innerText.includes('連携を解除'),
                    tokenCreateButton: document.body.innerText.includes('トークンを作成'),
                    locationLinks: document.body.innerText.includes('店舗設定'),
                    products: document.body.innerText.includes('商品管理'),
                    customers: document.body.innerText.includes('顧客管理'),
                    stockDirection: document.body.innerText.includes('在庫同期の方向')
                }
            };
        }"""
    )


def write_md(payload):
    facts = payload["facts"]
    lines = [
        "# スマレジ接続済み詳細 実機確認 2026-06-28",
        "",
        f"- 対象URL: `{BASE + DETAIL_ROUTE}`",
        "- 方針: 外部アクセストークン領域があるため、トークン値・全文本文・入力値は保存しない。",
        "",
        "## 結果",
        "",
        "| 確認項目 | 結果 |",
        "|:--|:--|",
        f"| 詳細画面に商品連携設定 | `{facts['hasProductSetting']}` |",
        f"| 詳細画面に在庫設定 | `{facts['hasInventorySetting']}` |",
        f"| 詳細画面に取引連携設定 | `{facts['hasTransactionSetting']}` |",
        f"| 詳細画面に外部アクセストークン領域 | `{facts['hasExternalAccessToken']}` |",
        f"| 詳細画面に連携解除領域 | `{facts['hasUnlink']}` |",
        f"| タブリンク `店舗設定` | `{facts['hasLocationLinksTab']}` |",
        f"| タブリンク `商品管理` | `{facts['hasProductsTab']}` |",
        f"| タブリンク `顧客管理` | `{facts['hasCustomersTab']}` |",
        "",
        "## 基本設定のラベル",
        "",
    ]
    for label in payload.get("detail", {}).get("labels", []):
        lines.append(f"- `{label}`")
    lines.extend(["", "## タブURL", ""])
    for name, route in TAB_ROUTES.items():
        tab = payload.get("tabs", {}).get(name, {})
        lines.append(f"- `{name}`: `{tab.get('url', BASE + route)}`")
    lines.extend(
        [
            "",
            "## 判断",
            "",
            "- 接続済みスマレジ連携の詳細画面構成は確認済みとして扱う。",
            "- 実際の同期方向・頻度・スマレジ側アプリインストール導線・トークン作成後の挙動は未確認として残す。",
            "",
            "## 証跡",
            "",
            f"- JSON: `{OUT.relative_to(ROOT)}`",
            "",
        ]
    )
    MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "detailRoute": DETAIL_ROUTE,
        "errors": [],
        "tabs": {},
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(BASE + DETAIL_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["detail"] = safe_state(page)
            for name, route in TAB_ROUTES.items():
                page.goto(BASE + route, wait_until="load")
                wait_quiet(page)
                payload["tabs"][name] = safe_state(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            detail_inc = payload.get("detail", {}).get("includes", {})
            detail_links = payload.get("detail", {}).get("links", [])
            payload["facts"] = {
                "hasProductSetting": detail_inc.get("productSetting") is True,
                "hasInventorySetting": detail_inc.get("inventorySetting") is True,
                "hasTransactionSetting": detail_inc.get("transactionSetting") is True,
                "hasExternalAccessToken": detail_inc.get("externalAccessToken") is True,
                "hasUnlink": detail_inc.get("unlink") is True,
                "hasTokenCreateButton": detail_inc.get("tokenCreateButton") is True,
                "hasStockDirection": detail_inc.get("stockDirection") is True,
                "hasLocationLinksTab": any(link.get("text") == "店舗設定" for link in detail_links),
                "hasProductsTab": any(link.get("text") == "商品管理" and "/products" in (link.get("href") or "") for link in detail_links),
                "hasCustomersTab": any(link.get("text") == "顧客管理" for link in detail_links),
                "errors": payload["errors"],
            }
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
            page.close()
            browser.close()
    print(json.dumps({"json": str(OUT), "md": str(MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
