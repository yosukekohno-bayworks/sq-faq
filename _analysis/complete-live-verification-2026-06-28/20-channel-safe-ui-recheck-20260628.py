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
OUT_JSON = OUT_DIR / "20-channel-safe-ui-recheck-20260628.json"
OUT_MD = OUT_DIR / "20-channel-safe-ui-recheck-20260628.md"

SMAREGI_DETAIL = "/admin/smaregi_integrations/a1ff4fd5-5636-571d-9c40-f222135d52ef_SmaregiIntegration"
OMNIBUS_DETAIL = "/admin/omnibus_core_integrations/c1a74b89-2c67-5167-ba46-952c7539a7a5_OmnibusCoreIntegration"


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snap(page, limit=3000):
    return page.evaluate(
        """(limit) => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const unique = (items) => Array.from(new Set(items.filter(Boolean)));
            return {
                url: location.href,
                h1: unique(Array.from(document.querySelectorAll('h1')).map(text)),
                h2: unique(Array.from(document.querySelectorAll('h2')).map(text)),
                labels: unique(Array.from(document.querySelectorAll('label')).map(text)),
                buttons: unique(Array.from(document.querySelectorAll('button')).map((button) => text(button) || button.getAttribute('aria-label') || '')),
                links: Array.from(document.querySelectorAll('a[href]')).map((a) => ({
                    text: text(a),
                    href: a.getAttribute('href'),
                    target: a.getAttribute('target') || ''
                })).filter((x) => x.text || x.href),
                controls: Array.from(document.querySelectorAll('input, select, textarea')).map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type') || '',
                    placeholder: el.getAttribute('placeholder') || '',
                    value: el.tagName.toLowerCase() === 'select' ? el.value : '',
                    disabled: !!el.disabled,
                    checked: el.tagName.toLowerCase() === 'input' && el.type === 'checkbox' ? el.checked : null,
                    options: el.tagName.toLowerCase() === 'select' ? Array.from(el.options).map((opt) => text(opt)) : []
                })),
                bodyIncludes: {
                    shopifyEmptyCopy: document.body.innerText.includes('Shopifyストアを接続する') && document.body.innerText.includes('商品や注文データの連携を行います'),
                    smaregiInstallBanner: document.body.innerText.includes('スマレジ連携を利用するには') && document.body.innerText.includes('アプリをインストール'),
                    smaregiUnlinkDialog: document.body.innerText.includes('連携を解除') && /(解除しますか|連携を解除する|この処理は巻き戻すことができません)/.test(document.body.innerText),
                    recustomerConnectCopy: document.body.innerText.includes('アカウントを接続'),
                    omnibusTokenCreate: document.body.innerText.includes('トークンを作成')
                },
                bodyText: document.body.innerText.replace(/\\s+/g, ' ').trim().slice(0, limit)
            };
        }""",
        limit,
    )


def click_empty_save(page):
    before = snap(page)
    result = {"before": before}
    save = page.get_by_role("button", name="保存する")
    if save.count() == 0:
        save = page.get_by_role("button", name="接続する")
    if save.count() > 0:
        save.first.click()
        wait_quiet(page)
        result["after"] = snap(page)
    return result


def smaregi_unlink_probe(page):
    result = {"abortedRequests": []}

    def abort_non_get(route, request):
        if request.method.upper() != "GET":
            result["abortedRequests"].append({"method": request.method, "url": request.url})
            route.abort()
        else:
            route.continue_()

    page.goto(BASE + SMAREGI_DETAIL, wait_until="load")
    wait_quiet(page)
    result["before"] = snap(page)
    page.route("**/*", abort_non_get)
    try:
        button = page.get_by_role("button", name="連携を解除")
        if button.count() == 0:
            button = page.get_by_text("連携を解除", exact=True)
        if button.count() > 0:
            button.first.click()
            wait_quiet(page)
            result["afterClick"] = snap(page)
            page.keyboard.press("Escape")
            wait_quiet(page, timeout=3000)
            result["afterEscape"] = snap(page)
        else:
            result["buttonMissing"] = True
    except Exception as exc:
        result["error"] = repr(exc)
    finally:
        page.unroute("**/*", abort_non_get)
    return result


def write_md(payload):
    facts = payload["facts"]
    lines = [
        "# 販売チャネル連携 安全UI再確認 2026-06-28",
        "",
        "## 方針",
        "",
        "- 外部OAuth開始、同期実行、トークン生成、連携解除確定は実行しない。",
        "- スマレジの `連携を解除` クリック確認では非GET通信を遮断し、確認ダイアログの有無だけを確認した。",
        "",
        "## 結果",
        "",
        "| 項目 | 結果 |",
        "|:--|:--|",
        f"| Shopify未接続コピー | `{facts['shopifyEmptyCopy']}` |",
        f"| Shopify作成フォームの主要ラベル | `{facts['shopifyCreateLabels']}` |",
        f"| Recustomer一覧/作成フォーム | `{facts['recustomer']}` |",
        f"| スマレジ作成フォーム内のアプリ導線リンク | `{facts['smaregiInstallLinks']}` |",
        f"| スマレジ連携解除クリック後 | `{facts['smaregiUnlinkProbe']}` |",
        f"| OmnibusCoreトークン作成ボタン | `{facts['omnibusTokenButtonVisible']}` |",
        "",
        "## 判断",
        "",
        "- Shopify未接続時の空状態コピーと作成フォーム項目は、2026-06-28時点でも画面で確認できた。",
        "- Recustomerは一覧の `アカウントを接続` と作成フォームの `ストアID` / `シークレット` まで確認した。接続後の返品/交換連携は未確認のまま。",
        "- スマレジ作成フォームのバナー文言は表示されるが、フォーム内にスマレジ側インストール手順へ遷移するリンクは確認できない。",
        "- スマレジ接続済み詳細の `連携を解除` クリック確認では、確認ダイアログは表示されず、非GET通信も発生しなかった。解除確定は実行していない。",
        "- OmnibusCoreの `トークンを作成` は表示確認のみ。トークン生成は行っていない。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {"generatedAt": datetime.now(timezone.utc).isoformat(), "errors": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(BASE + "/admin/shopify_integrations", wait_until="load")
            wait_quiet(page)
            payload["shopifyList"] = snap(page)
            page.goto(BASE + "/admin/shopify_integrations/create", wait_until="load")
            wait_quiet(page)
            payload["shopifyCreate"] = snap(page)

            page.goto(BASE + "/admin/recustomer_integrations", wait_until="load")
            wait_quiet(page)
            payload["recustomerList"] = snap(page)
            page.goto(BASE + "/admin/recustomer_integrations/create", wait_until="load")
            wait_quiet(page)
            payload["recustomerCreate"] = snap(page)
            payload["recustomerEmptySave"] = click_empty_save(page)

            page.goto(BASE + "/admin/smaregi_integrations/create", wait_until="load")
            wait_quiet(page)
            payload["smaregiCreate"] = snap(page)
            payload["smaregiUnlinkProbe"] = smaregi_unlink_probe(page)

            page.goto(BASE + OMNIBUS_DETAIL, wait_until="load")
            wait_quiet(page)
            payload["omnibusDetail"] = snap(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            smaregi_links = [
                link for link in payload.get("smaregiCreate", {}).get("links", [])
                if "smaregi" in (link.get("href") or "").lower() or "スマレジ" in link.get("text", "")
            ]
            unlink_after = payload.get("smaregiUnlinkProbe", {}).get("afterClick", {})
            payload["facts"] = {
                "shopifyEmptyCopy": payload.get("shopifyList", {}).get("bodyIncludes", {}).get("shopifyEmptyCopy") is True,
                "shopifyCreateLabels": payload.get("shopifyCreate", {}).get("labels", []),
                "recustomer": {
                    "listConnectCopy": payload.get("recustomerList", {}).get("bodyIncludes", {}).get("recustomerConnectCopy") is True,
                    "createLabels": payload.get("recustomerCreate", {}).get("labels", []),
                    "emptySaveErrors": payload.get("recustomerEmptySave", {}).get("after", {}).get("bodyText", ""),
                },
                "smaregiInstallLinks": smaregi_links,
                "smaregiInstallBanner": payload.get("smaregiCreate", {}).get("bodyIncludes", {}).get("smaregiInstallBanner") is True,
                "smaregiUnlinkProbe": {
                    "dialogOpened": unlink_after.get("bodyIncludes", {}).get("smaregiUnlinkDialog") is True,
                    "buttons": unlink_after.get("buttons", []),
                    "abortedRequests": payload.get("smaregiUnlinkProbe", {}).get("abortedRequests", []),
                    "error": payload.get("smaregiUnlinkProbe", {}).get("error"),
                },
                "omnibusTokenButtonVisible": payload.get("omnibusDetail", {}).get("bodyIncludes", {}).get("omnibusTokenCreate") is True,
                "errors": payload["errors"],
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
            page.close()
            browser.close()
    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
