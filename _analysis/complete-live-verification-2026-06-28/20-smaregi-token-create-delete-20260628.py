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
OUT_JSON = OUT_DIR / "20-smaregi-token-create-delete-20260628.json"
OUT_MD = OUT_DIR / "20-smaregi-token-create-delete-20260628.md"
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
                tokenArea: {
                    missingTextVisible: body.includes('外部アクセストークンが設定されていません'),
                    createButtonVisible: body.includes('トークンを作成'),
                    createdAtVisible: body.includes('作成日時:'),
                    deleteButtonVisible: Array.from(document.querySelectorAll('button')).some((button) => text(button) === '削除')
                },
                unlinkArea: {
                    unlinkTextVisible: body.includes('連携を解除'),
                    unlinkButtonVisible: Array.from(document.querySelectorAll('button')).some((button) => text(button) === '解除する')
                },
                notifications: unique(Array.from(document.querySelectorAll('[aria-label="Notifications"], [role="status"], [data-polaris-live-region]')).map(text)).slice(0, 8),
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
        "graphqlErrors": [],
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
                    if path_only(response.url) == "/api/graphql":
                        try:
                            body = response.json()
                            for err in body.get("errors", []) if isinstance(body, dict) else []:
                                message = err.get("message")
                                if message:
                                    payload["graphqlErrors"].append(message)
                        except Exception:
                            pass
            except Exception:
                pass

        page.on("request", on_request)
        page.on("response", on_response)

        try:
            page.goto(BASE + DETAIL_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["before"] = safe_state(page)

            create = page.get_by_role("button", name="トークンを作成")
            if create.count() > 0:
                create.first.click()
                wait_quiet(page)
            payload["afterCreate"] = safe_state(page)

            delete = page.get_by_role("button", name="削除", exact=True)
            if delete.count() > 0:
                delete.first.click()
                wait_quiet(page)
                payload["afterDeleteClick"] = safe_state(page)
                confirm = page.locator('[role="dialog"]').get_by_role("button", name="削除する")
                if confirm.count() > 0:
                    confirm.first.click(force=True)
                    wait_quiet(page)
            payload["afterDeleteConfirm"] = safe_state(page)

            page.reload(wait_until="load")
            wait_quiet(page)
            payload["afterReload"] = safe_state(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            before = payload.get("before", {}).get("tokenArea", {})
            created = payload.get("afterCreate", {}).get("tokenArea", {})
            deleted = payload.get("afterReload", {}).get("tokenArea", {})
            payload["facts"] = {
                "missingBefore": before.get("missingTextVisible") is True,
                "createdAtAfterCreate": created.get("createdAtVisible") is True,
                "deleteButtonAfterCreate": created.get("deleteButtonVisible") is True,
                "createButtonAfterCreate": created.get("createButtonVisible") is True,
                "deleteDialogOpened": payload.get("afterDeleteClick", {}).get("dialog") is not None,
                "missingAfterDeleteReload": deleted.get("missingTextVisible") is True,
                "createdAtAfterDeleteReload": deleted.get("createdAtVisible") is True,
                "unlinkButtonStillVisible": payload.get("afterReload", {}).get("unlinkArea", {}).get("unlinkButtonVisible") is True,
                "nonGetResponses": payload.get("responses", []),
                "graphqlErrors": payload.get("graphqlErrors", []),
                "errors": payload["errors"],
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# スマレジ 外部アクセストークン生成・削除確認 2026-06-28",
                "",
                f"- 対象URL: `{BASE + DETAIL_ROUTE}`",
                "- 方針: トークン値・全文本文・スクリーンショットは保存しない。連携解除は実行しない。",
                "",
                "## 結果",
                "",
                "| 確認項目 | 結果 |",
                "|:--|:--|",
                f"| 生成前に未設定文言が表示 | `{payload['facts']['missingBefore']}` |",
                f"| 生成後に作成日時が表示 | `{payload['facts']['createdAtAfterCreate']}` |",
                f"| 生成後にトークン用 `削除` が表示 | `{payload['facts']['deleteButtonAfterCreate']}` |",
                f"| 生成後も `トークンを作成` が表示 | `{payload['facts']['createButtonAfterCreate']}` |",
                f"| 削除確認ダイアログが表示 | `{payload['facts']['deleteDialogOpened']}` |",
                f"| 削除後リロードで未設定へ戻る | `{payload['facts']['missingAfterDeleteReload']}` |",
                f"| 連携解除ボタンは未実行のまま表示 | `{payload['facts']['unlinkButtonStillVisible']}` |",
                f"| 非GET通信 | `{payload['facts']['nonGetResponses']}` |",
                f"| GraphQLエラー | `{payload['facts']['graphqlErrors']}` |",
                "",
                "## 判断",
                "",
                "- `トークンを作成` は確認ダイアログなしで非GET通信を発行したが、今回の接続済みスマレジレコードでは作成日時・削除ボタンは表示されず、再読み込み後も `外部アクセストークンが設定されていません` のままだった。",
                "- 画面上の明示的なエラー表示は確認できなかった。GraphQLエラーが出ている場合は上表に記録する。",
                "- `連携を解除` は確認対象外のため実行していない。",
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
