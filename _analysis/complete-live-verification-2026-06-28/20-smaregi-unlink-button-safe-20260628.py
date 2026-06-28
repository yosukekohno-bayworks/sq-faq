#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "20-smaregi-unlink-button-safe-20260628.json"
OUT_MD = OUT_DIR / "20-smaregi-unlink-button-safe-20260628.md"
DETAIL_ROUTE = "/admin/smaregi_integrations/a1ff4fd5-5636-571d-9c40-f222135d52ef_SmaregiIntegration"


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1000)


def path_only(url):
    parsed = urlparse(url)
    return parsed.path


def safe_state(page):
    return page.evaluate(
        """() => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const unique = (items) => Array.from(new Set(items.filter(Boolean)));
            const body = document.body.innerText || '';
            return {
                url: location.href,
                h1: unique(Array.from(document.querySelectorAll('h1')).map(text)),
                buttons: unique(Array.from(document.querySelectorAll('button')).map((button) => text(button) || button.getAttribute('aria-label') || '')),
                unlinkSectionVisible: body.includes('連携を解除'),
                unlinkButtonVisible: Array.from(document.querySelectorAll('button')).some((button) => text(button) === '解除する'),
                dialog: (() => {
                    const dialog = document.querySelector('[role="dialog"]');
                    return dialog ? {
                        title: unique(Array.from(dialog.querySelectorAll('h1,h2,h3')).map(text)),
                        buttons: unique(Array.from(dialog.querySelectorAll('button')).map((button) => text(button) || button.getAttribute('aria-label') || '')),
                        textIncludesUnlink: /解除|連携/.test(text(dialog))
                    } : null;
                })()
            };
        }"""
    )


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "detailRoute": DETAIL_ROUTE,
        "abortedRequests": [],
        "errors": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)

        def abort_non_get(route, request):
            if request.method.upper() != "GET":
                payload["abortedRequests"].append({"method": request.method, "path": path_only(request.url)})
                route.abort()
            else:
                route.continue_()

        try:
            page.goto(BASE + DETAIL_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["before"] = safe_state(page)
            page.route("**/*", abort_non_get)
            button = page.get_by_role("button", name="解除する")
            if button.count() > 0:
                button.first.click()
                wait_quiet(page)
            else:
                payload["unlinkButtonMissing"] = True
            payload["afterClick"] = safe_state(page)
            page.keyboard.press("Escape")
            wait_quiet(page, timeout=3000)
            payload["afterEscape"] = safe_state(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            try:
                page.unroute("**/*", abort_non_get)
            except Exception:
                pass
            payload["facts"] = {
                "unlinkButtonVisibleBefore": payload.get("before", {}).get("unlinkButtonVisible") is True,
                "dialogOpenedAfterClick": payload.get("afterClick", {}).get("dialog") is not None,
                "dialog": payload.get("afterClick", {}).get("dialog"),
                "abortedRequests": payload.get("abortedRequests", []),
                "urlAfterClick": payload.get("afterClick", {}).get("url"),
                "errors": payload["errors"],
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# スマレジ 解除するボタン安全確認 2026-06-28",
                "",
                f"- 対象URL: `{BASE + DETAIL_ROUTE}`",
                "- 方針: `解除する` 実ボタンをクリックするが、非GET通信は遮断して連携解除を実行しない。確認ダイアログが出た場合は確定しない。",
                "",
                "## 結果",
                "",
                "| 確認項目 | 結果 |",
                "|:--|:--|",
                f"| クリック前に `解除する` ボタンが表示 | `{payload['facts']['unlinkButtonVisibleBefore']}` |",
                f"| クリック後に確認ダイアログが表示 | `{payload['facts']['dialogOpenedAfterClick']}` |",
                f"| ダイアログ | `{payload['facts']['dialog']}` |",
                f"| 遮断した非GET通信 | `{payload['facts']['abortedRequests']}` |",
                f"| クリック後URL | `{payload['facts']['urlAfterClick']}` |",
                "",
                "## 判断",
                "",
                "- 見出し `連携を解除` ではなく、実ボタン `解除する` を対象に再確認した。",
                "- 非GET通信を遮断したため、連携解除の確定・データ変化は実行していない。",
                "",
                "## 証跡",
                "",
                f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
                "",
            ]
            OUT_MD.write_text("\n".join(lines), encoding="utf-8")
            page.close()
            browser.close()

    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
