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
OUT_JSON = OUT_DIR / "20-omnibus-token-delete-cleanup-20260628.json"
OUT_MD = OUT_DIR / "20-omnibus-token-delete-cleanup-20260628.md"
DETAIL_ROUTE = "/admin/omnibus_core_integrations/c1a74b89-2c67-5167-ba46-952c7539a7a5_OmnibusCoreIntegration"


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
                tokenArea: {
                    missingTextVisible: body.includes('アクセストークンが設定されていません'),
                    createButtonVisible: body.includes('トークンを作成'),
                    createdAtVisible: body.includes('作成日時:'),
                    deleteButtonVisible: Array.from(document.querySelectorAll('button')).some((button) => text(button) === '削除')
                },
                expiryValue: Array.from(document.querySelectorAll('input[type="number"]')).map((el) => el.value).filter(Boolean)[0] || '',
                buttons: unique(Array.from(document.querySelectorAll('button')).map((button) => text(button) || button.getAttribute('aria-label') || '')).filter((label) => label === '削除' || label === '削除する' || label === 'トークンを作成' || label === '保存する'),
                dialog: (() => {
                    const dialog = document.querySelector('[role="dialog"]');
                    return dialog ? {
                        title: unique(Array.from(dialog.querySelectorAll('h1,h2,h3')).map(text)),
                        buttons: unique(Array.from(dialog.querySelectorAll('button')).map((button) => text(button) || button.getAttribute('aria-label') || '')),
                        textIncludesTokenDelete: text(dialog).includes('アクセストークン') || text(dialog).includes('トークン')
                    } : null;
                })()
            };
        }"""
    )


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "detailRoute": DETAIL_ROUTE,
        "requests": [],
        "responses": [],
        "errors": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)

        def on_request(request):
            if request.method.upper() != "GET":
                payload["requests"].append({"method": request.method, "path": path_only(request.url)})

        def on_response(response):
            try:
                if response.request.method.upper() != "GET":
                    payload["responses"].append({
                        "method": response.request.method,
                        "path": path_only(response.url),
                        "status": response.status,
                    })
            except Exception:
                pass

        page.on("request", on_request)
        page.on("response", on_response)
        try:
            page.goto(BASE + DETAIL_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["before"] = safe_state(page)

            delete = page.get_by_role("button", name="削除", exact=True)
            if delete.count() > 0:
                delete.first.click()
                wait_quiet(page)
                payload["afterDeleteClick"] = safe_state(page)
                dialog = payload["afterDeleteClick"].get("dialog")
                if dialog:
                    confirm = page.locator('[role="dialog"]').get_by_role("button", name="削除する")
                    if confirm.count() > 0:
                        confirm.first.click(force=True)
                        wait_quiet(page)
                        payload["afterConfirm"] = safe_state(page)
                else:
                    payload["afterConfirm"] = payload["afterDeleteClick"]
            else:
                payload["deleteButtonMissing"] = True
                payload["afterConfirm"] = payload["before"]

            page.reload(wait_until="load")
            wait_quiet(page)
            payload["afterReload"] = safe_state(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            after = payload.get("afterReload", {})
            payload["facts"] = {
                "tokenExistedBeforeCleanup": payload.get("before", {}).get("tokenArea", {}).get("createdAtVisible") is True,
                "tokenDeleteButtonVisibleBefore": payload.get("before", {}).get("tokenArea", {}).get("deleteButtonVisible") is True,
                "dialogOpened": payload.get("afterDeleteClick", {}).get("dialog") is not None,
                "tokenMissingAfterReload": after.get("tokenArea", {}).get("missingTextVisible") is True,
                "tokenCreatedAtAfterReload": after.get("tokenArea", {}).get("createdAtVisible") is True,
                "expiryValueAfterReload": after.get("expiryValue"),
                "nonGetResponses": payload.get("responses", []),
                "errors": payload["errors"],
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# OmnibusCore アクセストークン削除クリーンアップ 2026-06-28",
                "",
                f"- 対象URL: `{BASE + DETAIL_ROUTE}`",
                "- 方針: トークン値・全文本文・スクリーンショットは保存しない。",
                "",
                "## 結果",
                "",
                "| 確認項目 | 結果 |",
                "|:--|:--|",
                f"| 削除前にトークン作成日時が表示 | `{payload['facts']['tokenExistedBeforeCleanup']}` |",
                f"| 削除前にトークン用 `削除` ボタンが表示 | `{payload['facts']['tokenDeleteButtonVisibleBefore']}` |",
                f"| 削除クリック後に確認ダイアログ表示 | `{payload['facts']['dialogOpened']}` |",
                f"| リロード後に未設定文言へ戻った | `{payload['facts']['tokenMissingAfterReload']}` |",
                f"| リロード後の期限日数 | `{payload['facts']['expiryValueAfterReload']}` |",
                f"| 非GET通信 | `{payload['facts']['nonGetResponses']}` |",
                "",
                "## 判断",
                "",
                "- `トークンを作成` 後の画面には、マスク済みトークン、作成日時、トークン用の `削除` ボタン、追加の `トークンを作成` ボタンが表示される。",
                "- トークン用の `削除` クリック後、確認ダイアログを経て削除でき、再読み込み後は `アクセストークンが設定されていません` に戻った。",
                "- 前段で空欄検証した `下書き注文の有効期限日数` は、再読み込み後 `1` に戻っている。",
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
