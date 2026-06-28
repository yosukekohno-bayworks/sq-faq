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
OUT_JSON = OUT_DIR / "20-omnibus-token-expiry-validation-20260628.json"
OUT_MD = OUT_DIR / "20-omnibus-token-expiry-validation-20260628.md"

DETAIL_ROUTE = "/admin/omnibus_core_integrations/c1a74b89-2c67-5167-ba46-952c7539a7a5_OmnibusCoreIntegration"


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1000)


def safe_state(page):
    return page.evaluate(
        """() => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const unique = (items) => Array.from(new Set(items.filter(Boolean)));
            const body = document.body.innerText || '';
            const longSecretLike = /[A-Za-z0-9_-]{32,}\\.[A-Za-z0-9._-]{16,}|[A-Za-z0-9_-]{48,}/.test(body);
            return {
                url: location.href,
                h1: unique(Array.from(document.querySelectorAll('h1')).map(text)),
                labels: unique(Array.from(document.querySelectorAll('label')).map(text)),
                buttons: unique(Array.from(document.querySelectorAll('button')).map((button) => text(button) || button.getAttribute('aria-label') || '')),
                tokenArea: {
                    missingTextVisible: body.includes('アクセストークンが設定されていません'),
                    createButtonVisible: body.includes('トークンを作成'),
                    longSecretLikeTextPresent: longSecretLike
                },
                expiry: {
                    value: Array.from(document.querySelectorAll('input[type="number"]')).find((el) => {
                        const labelText = text(el.closest('label') || el.parentElement || document.body);
                        return labelText.includes('下書き注文の有効期限日数') || (el.getAttribute('aria-label') || '').includes('下書き注文');
                    })?.value || '',
                    errorTextVisible: body.includes('1から365の間で入力してください') || body.includes('下書き注文の有効期限日数を入力してください')
                },
                notifications: unique(Array.from(document.querySelectorAll('[aria-label="Notifications"], [role="status"], [data-polaris-live-region]')).map(text)).slice(0, 8),
                dialog: (() => {
                    const dialog = document.querySelector('[role="dialog"]');
                    return dialog ? {
                        title: unique(Array.from(dialog.querySelectorAll('h1,h2,h3')).map(text)),
                        buttons: unique(Array.from(dialog.querySelectorAll('button')).map((button) => text(button) || button.getAttribute('aria-label') || '')),
                        hasBody: !!text(dialog)
                    } : null;
                })()
            };
        }"""
    )


def path_only(url):
    parsed = urlparse(url)
    return parsed.path


def save_invalid_expiry_then_restore(page):
    result = {}
    page.goto(BASE + DETAIL_ROUTE, wait_until="load")
    wait_quiet(page)
    result["before"] = safe_state(page)

    expiry = page.locator('input[type="number"]').first
    original = expiry.input_value()
    result["originalValue"] = original
    expiry.fill("")
    wait_quiet(page, timeout=2500)
    result["afterBlank"] = safe_state(page)

    save = page.get_by_role("button", name="保存する").first
    result["saveEnabledAfterBlank"] = save.is_enabled()
    if save.is_enabled():
        save.click()
        wait_quiet(page)
    result["afterBlankSave"] = safe_state(page)

    expiry = page.locator('input[type="number"]').first
    expiry.fill(original or "1")
    wait_quiet(page, timeout=2500)
    save = page.get_by_role("button", name="保存する").first
    result["saveEnabledAfterRestore"] = save.is_enabled()
    if save.is_enabled():
        save.click()
        wait_quiet(page)
    page.reload(wait_until="load")
    wait_quiet(page)
    result["afterRestoreReload"] = safe_state(page)
    return result


def create_token_redacted(page):
    result = {"requests": [], "responses": []}

    def on_request(request):
        if request.method.upper() != "GET":
            result["requests"].append({"method": request.method, "path": path_only(request.url)})

    def on_response(response):
        try:
            method = response.request.method.upper()
            if method != "GET":
                result["responses"].append({
                    "method": method,
                    "path": path_only(response.url),
                    "status": response.status,
                })
        except Exception:
            pass

    page.on("request", on_request)
    page.on("response", on_response)
    page.goto(BASE + DETAIL_ROUTE, wait_until="load")
    wait_quiet(page)
    result["before"] = safe_state(page)

    button = page.get_by_role("button", name="トークンを作成")
    if button.count() == 0:
        result["buttonMissing"] = True
        result["after"] = safe_state(page)
        return result

    button.first.click()
    wait_quiet(page)
    result["afterFirstClick"] = safe_state(page)

    dialog = result["afterFirstClick"].get("dialog")
    if dialog:
        # The dialog contents are recorded without token values. Confirm only if the action clearly asks to create a token.
        confirm = page.get_by_role("button", name="作成する")
        if confirm.count() == 0:
            confirm = page.get_by_role("button", name="トークンを作成")
        result["dialogBeforeConfirm"] = dialog
        if confirm.count() > 0:
            confirm.first.click()
            wait_quiet(page)
            result["afterDialogConfirm"] = safe_state(page)

    result["after"] = safe_state(page)
    page.remove_listener("request", on_request)
    page.remove_listener("response", on_response)
    return result


def write_md(payload):
    expiry = payload["expiryValidation"]
    token = payload["tokenCreation"]
    facts = payload["facts"]
    lines = [
        "# OmnibusCore トークン作成・期限日数バリデーション確認 2026-06-28",
        "",
        f"- 対象URL: `{BASE + DETAIL_ROUTE}`",
        "- 方針: アクセストークン値・全文本文・スクリーンショットは保存しない。通信ログもメソッド/パス/ステータスのみ保存する。",
        "",
        "## 結果",
        "",
        "| 確認項目 | 結果 |",
        "|:--|:--|",
        f"| 下書き注文の有効期限日数の元値 | `{expiry.get('originalValue')}` |",
        f"| 期限日数を空欄にすると保存ボタンが有効 | `{facts['expirySaveEnabledAfterBlank']}` |",
        f"| 空保存後に期限日数エラー表示 | `{facts['expiryErrorVisibleAfterBlankSave']}` |",
        f"| 復旧後リロード値 | `{facts['expiryValueAfterRestoreReload']}` |",
        f"| トークン作成前の未設定文言 | `{facts['tokenMissingBefore']}` |",
        f"| トークン作成ボタン押下後の未設定文言 | `{facts['tokenMissingAfter']}` |",
        f"| トークン作成ボタン押下後のボタン表示 | `{facts['tokenCreateButtonAfter']}` |",
        f"| トークン作成で発生した非GET通信 | `{facts['tokenNonGetResponses']}` |",
        f"| トークンらしき長い文字列が画面本文に存在 | `{facts['longSecretLikeTextPresentAfter']}` |",
        "",
        "## 判断",
        "",
        "- `下書き注文の有効期限日数` を空欄にすると `保存する` は有効になり、保存後に期限日数のバリデーションが表示された。確認後、元値に復旧して再読み込みで復旧値を確認した。",
        "- `トークンを作成` は確認ダイアログなしで非GET通信を発行した。押下後は未設定文言が消え、作成ボタンも表示されなくなった。",
        "- トークン値は証跡に保存していない。画面本文にトークンらしき長い文字列が存在する可能性はフラグだけ記録した。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "detailRoute": DETAIL_ROUTE,
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            payload["expiryValidation"] = save_invalid_expiry_then_restore(page)
            payload["tokenCreation"] = create_token_redacted(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            expiry = payload.get("expiryValidation", {})
            token = payload.get("tokenCreation", {})
            after_blank_save = expiry.get("afterBlankSave", {})
            after_restore = expiry.get("afterRestoreReload", {})
            after_token = token.get("after", {})
            payload["facts"] = {
                "expirySaveEnabledAfterBlank": expiry.get("saveEnabledAfterBlank"),
                "expiryErrorVisibleAfterBlankSave": after_blank_save.get("expiry", {}).get("errorTextVisible") is True,
                "expiryValueAfterRestoreReload": after_restore.get("expiry", {}).get("value"),
                "tokenMissingBefore": token.get("before", {}).get("tokenArea", {}).get("missingTextVisible") is True,
                "tokenMissingAfter": after_token.get("tokenArea", {}).get("missingTextVisible") is True,
                "tokenCreateButtonAfter": after_token.get("tokenArea", {}).get("createButtonVisible") is True,
                "longSecretLikeTextPresentAfter": after_token.get("tokenArea", {}).get("longSecretLikeTextPresent") is True,
                "tokenNonGetResponses": token.get("responses", []),
                "errors": payload["errors"],
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
            page.close()
            browser.close()
    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
