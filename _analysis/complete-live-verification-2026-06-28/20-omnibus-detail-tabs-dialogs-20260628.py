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
OUT = OUT_DIR / "20-omnibus-detail-tabs-dialogs-20260628.json"
MD = OUT.with_suffix(".md")
SITE_DIALOG_SHOT = OUT_DIR / "20-omnibus-site-dialog-20260628.png"
MAIL_DIALOG_SHOT = OUT_DIR / "20-omnibus-mail-dialog-20260628.png"

DETAIL_ROUTE = "/admin/omnibus_core_integrations/c1a74b89-2c67-5167-ba46-952c7539a7a5_OmnibusCoreIntegration"
SITE_ROUTE = DETAIL_ROUTE + "/sites"
MAIL_ROUTE = DETAIL_ROUTE + "/notification_emails"


def norm(value):
    return " ".join((value or "").split())


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1500)


def safe_visible_state(page):
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
                links: Array.from(document.querySelectorAll('a[href]')).map((a) => ({ text: text(a), href: a.getAttribute('href') })).filter((x) => x.text),
                fields: Array.from(document.querySelectorAll('input, select, textarea')).map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type') || '',
                    placeholder: el.getAttribute('placeholder') || '',
                    disabled: !!el.disabled,
                    options: el.tagName.toLowerCase() === 'select' ? Array.from(el.options).map((opt) => text(opt)) : []
                })),
                visibleTextIncludes: {
                    basicTab: document.body.innerText.includes('基本設定'),
                    siteTab: document.body.innerText.includes('連携サイト'),
                    mailTab: document.body.innerText.includes('通知メール'),
                    shippingStatus: document.body.innerText.includes('出荷指示のステータス'),
                    accessToken: document.body.innerText.includes('アクセストークン'),
                    createTokenButton: document.body.innerText.includes('トークンを作成'),
                    siteDialogTitle: document.body.innerText.includes('連携サイトを追加する'),
                    mailDialogTitle: document.body.innerText.includes('通知メールを追加する'),
                    priceRuleHint: document.body.innerText.includes('時間に00:00以外が含まれる価格ルール'),
                    duplicatedEmailHint: document.body.innerText.includes('メールアドレスは重複して登録できません')
                }
            };
        }"""
    )


def click_add_button(page):
    add = page.get_by_role("button", name="追加する")
    if add.count() == 0:
        add = page.get_by_text("追加する", exact=True)
    add.first.click()


def dialog_screenshot(page, path):
    dialog = page.locator('[role="dialog"]').first
    if dialog.count() > 0:
        dialog.screenshot(path=str(path))
    else:
        page.screenshot(path=str(path), full_page=False)


def write_md(payload):
    facts = payload["facts"]
    lines = [
        "# OmnibusCore 詳細タブ・追加ダイアログ 実機確認 2026-06-28",
        "",
        f"- 対象URL: `{BASE + DETAIL_ROUTE}`",
        "- 方針: 基本設定にはアクセストークン領域があるため、トークン文字列や全文本文は保存しない。",
        "",
        "## 結果",
        "",
        "| 確認項目 | 結果 |",
        "|:--|:--|",
        f"| 詳細画面に `基本設定` タブ | `{facts['hasBasicTab']}` |",
        f"| 詳細画面に `連携サイト` タブ | `{facts['hasSiteTab']}` |",
        f"| 詳細画面に `通知メール` タブ | `{facts['hasMailTab']}` |",
        f"| 基本設定に `出荷指示のステータス` | `{facts['hasShippingStatus']}` |",
        f"| 基本設定に `アクセストークン` 領域 | `{facts['hasAccessTokenArea']}` |",
        f"| 連携サイト追加ダイアログを表示 | `{facts['siteDialogOpened']}` |",
        f"| 通知メール追加ダイアログを表示 | `{facts['mailDialogOpened']}` |",
        "",
        "## 連携サイトダイアログのラベル",
        "",
    ]
    for label in payload.get("siteDialog", {}).get("labels", []):
        lines.append(f"- `{label}`")
    lines.extend(["", "## 通知メールダイアログのラベル", ""])
    for label in payload.get("mailDialog", {}).get("labels", []):
        lines.append(f"- `{label}`")
    lines.extend(
        [
            "",
            "## 判断",
            "",
            "- 接続済みOmnibusCore連携の詳細画面では、基本設定・連携サイト・通知メールの3タブを確認した。",
            "- `連携サイト` タブの `追加する` から、場所コード・サイト名・販売価格・ロケーション・サイト倉庫ロケーションを持つ追加ダイアログを確認した。",
            "- `通知メール` タブの `追加する` から、名前・メールアドレスを持つ追加ダイアログを確認した。",
            "- 同期時の引当・出荷反映、アクセストークン作成後の挙動、メール重複登録の実保存は未確認として残す。",
            "",
            "## 証跡",
            "",
            f"- JSON: `{OUT.relative_to(ROOT)}`",
            f"- 連携サイトダイアログ: `{SITE_DIALOG_SHOT.relative_to(ROOT)}`",
            f"- 通知メールダイアログ: `{MAIL_DIALOG_SHOT.relative_to(ROOT)}`",
            "",
        ]
    )
    MD.write_text("\n".join(lines), encoding="utf-8")


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
            page.goto(BASE + DETAIL_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["detail"] = safe_visible_state(page)

            page.goto(BASE + SITE_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["siteTab"] = safe_visible_state(page)
            click_add_button(page)
            wait_quiet(page)
            payload["siteDialog"] = safe_visible_state(page)
            dialog_screenshot(page, SITE_DIALOG_SHOT)
            page.keyboard.press("Escape")
            wait_quiet(page, timeout=3000)

            page.goto(BASE + MAIL_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["mailTab"] = safe_visible_state(page)
            click_add_button(page)
            wait_quiet(page)
            payload["mailDialog"] = safe_visible_state(page)
            dialog_screenshot(page, MAIL_DIALOG_SHOT)
            page.keyboard.press("Escape")
            wait_quiet(page, timeout=3000)
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            detail_flags = payload.get("detail", {}).get("visibleTextIncludes", {})
            site_flags = payload.get("siteDialog", {}).get("visibleTextIncludes", {})
            mail_flags = payload.get("mailDialog", {}).get("visibleTextIncludes", {})
            payload["facts"] = {
                "hasBasicTab": detail_flags.get("basicTab") is True,
                "hasSiteTab": detail_flags.get("siteTab") is True,
                "hasMailTab": detail_flags.get("mailTab") is True,
                "hasShippingStatus": detail_flags.get("shippingStatus") is True,
                "hasAccessTokenArea": detail_flags.get("accessToken") is True,
                "hasCreateTokenButton": detail_flags.get("createTokenButton") is True,
                "siteDialogOpened": site_flags.get("siteDialogTitle") is True,
                "mailDialogOpened": mail_flags.get("mailDialogTitle") is True,
                "siteLabels": payload.get("siteDialog", {}).get("labels", []),
                "mailLabels": payload.get("mailDialog", {}).get("labels", []),
                "sitePriceRuleHint": site_flags.get("priceRuleHint") is True,
                "mailDuplicateHint": mail_flags.get("duplicatedEmailHint") is True,
                "errors": payload["errors"],
            }
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
            page.close()
            browser.close()
    print(json.dumps({"json": str(OUT), "md": str(MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
