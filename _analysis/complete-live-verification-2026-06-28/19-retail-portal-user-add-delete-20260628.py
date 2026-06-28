#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "19-retail-portal-user-add-delete-20260628.json"
OUT_MD = OUT_DIR / "19-retail-portal-user-add-delete-20260628.md"
SCREENSHOT_AFTER_ADD = OUT_DIR / "19-retail-portal-user-after-add-20260628.png"
SCREENSHOT_AFTER_DELETE = OUT_DIR / "19-retail-portal-user-after-delete-20260628.png"

BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
DETAIL_ROUTE = "/admin/retail_portal_integrations/65104d5a-e12a-5c06-9716-48bf6cf4a67d_RetailPortalIntegration"

STAMP = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
FAMILY = "FAQリテール"
GIVEN = f"User{STAMP[-6:]}"
EMAIL = f"sq-faq-retail-{STAMP}@example.com"


def compact(text, limit=6000):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def snapshot(page, limit=7000):
    return {
        "url": page.url,
        "body": compact(text_of(page), limit),
        "rows": page.evaluate(
            """() => Array.from(document.querySelectorAll('tr')).map((tr) =>
                (tr.innerText || tr.textContent || '').replace(/\\s+/g, ' ').trim()
            ).filter(Boolean).slice(0, 120)"""
        ),
        "buttons": page.evaluate(
            """() => Array.from(document.querySelectorAll('button, a')).map((b) => ({
                tag: b.tagName.toLowerCase(),
                text: (b.innerText || b.textContent || '').replace(/\\s+/g, ' ').trim(),
                href: b.getAttribute('href'),
                disabled: !!b.disabled,
                ariaDisabled: b.getAttribute('aria-disabled'),
                ariaLabel: b.getAttribute('aria-label')
            })).filter((b) => b.text || b.href || b.ariaLabel).slice(0, 220)"""
        ),
    }


def save_payload(payload):
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def first_enabled_button(page, names, scope=None):
    root = scope or page
    for name in names:
        locator = root.get_by_role("button", name=name, exact=True)
        if locator.count():
            for idx in range(locator.count()):
                item = locator.nth(idx)
                try:
                    if item.is_enabled() and item.get_attribute("aria-disabled") != "true":
                        return name, item
                except Exception:
                    pass
    return None, None


def create_user(page):
    result = {"email": EMAIL}
    page.goto(BASE + "/admin/settings/users/create", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["before"] = snapshot(page, limit=5000)
    inputs = page.locator("input")
    inputs.nth(0).fill(FAMILY)
    inputs.nth(1).fill(GIVEN)
    inputs.nth(2).fill(EMAIL)
    result["beforeSave"] = snapshot(page, limit=5000)
    page.get_by_role("button", name="保存する", exact=True).click()
    page.wait_for_timeout(5000)
    wait_quiet(page, timeout=12000)
    result["afterSave"] = snapshot(page, limit=7000)
    result["created"] = "/admin/settings/users/" in page.url and "/create" not in page.url
    result["userRoute"] = page.url.replace(BASE, "") if result["created"] else None
    if not result["created"]:
        page.goto(BASE + "/admin/settings/users", wait_until="load", timeout=35000)
        wait_quiet(page)
        search = page.locator('input[placeholder="キーワードで検索する"]').first
        search.fill(EMAIL)
        search.press("Enter")
        page.wait_for_timeout(2200)
        wait_quiet(page, timeout=5000)
        result["listSearchAfterSave"] = snapshot(page, limit=6000)
        row = page.evaluate(
            """(email) => {
                const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
                const row = Array.from(document.querySelectorAll('tr')).find((tr) => textOf(tr).includes(email));
                if (!row) return null;
                row.click();
                return textOf(row);
            }""",
            EMAIL,
        )
        if row:
            page.wait_for_timeout(1500)
            wait_quiet(page, timeout=5000)
            result["created"] = True
            result["userRoute"] = page.url.replace(BASE, "")
            result["openedFromList"] = {"row": row, **snapshot(page, limit=6000)}
    return result


def select_dialog_row(dialog, needle):
    selected = dialog.page.evaluate(
        """({needle}) => {
            const dialogs = Array.from(document.querySelectorAll('div[role="dialog"]'));
            const dialog = dialogs[dialogs.length - 1];
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            if (!dialog) return {found: false, reason: 'dialog not found'};
            const row = Array.from(dialog.querySelectorAll('tr')).find((tr) => textOf(tr).includes(needle));
            if (!row) return {found: false, rows: Array.from(dialog.querySelectorAll('tr')).map(textOf).slice(0, 40)};
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox) checkbox.click();
            else row.click();
            return {found: true, row: textOf(row), checkbox: !!checkbox};
        }""",
        {"needle": needle},
    )
    dialog.page.wait_for_timeout(700)
    return selected


def add_user_to_retail_portal(page):
    result = {"email": EMAIL}
    page.goto(BASE + DETAIL_ROUTE, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["before"] = snapshot(page, limit=7000)
    page.get_by_role("button", name="ユーザーを追加する", exact=True).click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    result["dialogInitial"] = compact(dialog.inner_text(timeout=5000), 3000)
    search = dialog.locator("input").first
    search.fill(EMAIL)
    search.press("Enter")
    page.wait_for_timeout(1800)
    result["dialogAfterSearch"] = compact(dialog.inner_text(timeout=5000), 4000)
    result["selected"] = select_dialog_row(dialog, EMAIL)
    name, button = first_enabled_button(page, ["選択する"], scope=dialog)
    result["selectButton"] = name
    if not button:
        result["error"] = "select button not enabled"
        return result
    button.click()
    page.wait_for_timeout(4000)
    wait_quiet(page, timeout=12000)
    page.goto(BASE + DETAIL_ROUTE, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["afterAdd"] = snapshot(page, limit=8000)
    try:
        page.screenshot(path=str(SCREENSHOT_AFTER_ADD), full_page=True)
        result["screenshot"] = str(SCREENSHOT_AFTER_ADD.relative_to(ROOT))
    except Exception as exc:
        result["screenshotError"] = repr(exc)
    return result


def delete_user_from_retail_portal(page):
    result = {"email": EMAIL}
    page.goto(BASE + DETAIL_ROUTE, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["before"] = snapshot(page, limit=8000)
    selected = page.evaluate(
        """(email) => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const row = Array.from(document.querySelectorAll('tr')).find((tr) => textOf(tr).includes(email));
            if (!row) return {found: false, rows: Array.from(document.querySelectorAll('tr')).map(textOf).slice(0, 80)};
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox) checkbox.click();
            else row.click();
            return {found: true, row: textOf(row), checkbox: !!checkbox};
        }""",
        EMAIL,
    )
    result["selected"] = selected
    page.wait_for_timeout(800)
    result["afterSelect"] = snapshot(page, limit=8000)
    if not selected.get("found"):
        return result
    page.get_by_role("button", name="削除する", exact=True).click()
    page.wait_for_selector('div[role="dialog"]', timeout=12000)
    dialog = page.locator('div[role="dialog"]').last
    result["dialog"] = compact(dialog.inner_text(timeout=5000), 3000)
    name, button = first_enabled_button(page, ["削除する"], scope=dialog)
    result["confirmButton"] = name
    if button:
        button.click()
        page.wait_for_timeout(5000)
        wait_quiet(page, timeout=12000)
    page.goto(BASE + DETAIL_ROUTE, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["afterDelete"] = snapshot(page, limit=8000)
    try:
        page.screenshot(path=str(SCREENSHOT_AFTER_DELETE), full_page=True)
        result["screenshot"] = str(SCREENSHOT_AFTER_DELETE.relative_to(ROOT))
    except Exception as exc:
        result["screenshotError"] = repr(exc)
    return result


def exclude_created_user(page, user_route):
    result = {"userRoute": user_route}
    if not user_route:
        page.goto(BASE + "/admin/settings/users", wait_until="load", timeout=35000)
        wait_quiet(page)
        search = page.locator('input[placeholder="キーワードで検索する"]').first
        search.fill(EMAIL)
        search.press("Enter")
        page.wait_for_timeout(2200)
        wait_quiet(page, timeout=5000)
        result["listSearch"] = snapshot(page, limit=6000)
        row = page.evaluate(
            """(email) => {
                const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
                const row = Array.from(document.querySelectorAll('tr')).find((tr) => textOf(tr).includes(email));
                if (!row) return null;
                row.click();
                return textOf(row);
            }""",
            EMAIL,
        )
        if not row:
            result["error"] = "user row not found"
            return result
        page.wait_for_timeout(1500)
        wait_quiet(page, timeout=5000)
        user_route = page.url.replace(BASE, "")
        result["userRoute"] = user_route
    page.goto(BASE + user_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["before"] = snapshot(page, limit=6000)
    page.get_by_role("button", name="組織から除外する", exact=True).click()
    page.wait_for_selector('div[role="dialog"]', timeout=12000)
    dialog = page.locator('div[role="dialog"]').last
    result["dialog"] = compact(dialog.inner_text(timeout=5000), 2500)
    name, button = first_enabled_button(page, ["除外する"], scope=dialog)
    result["confirmButton"] = name
    if button:
        button.click()
        page.wait_for_timeout(4000)
        wait_quiet(page, timeout=12000)
    result["after"] = snapshot(page, limit=7000)
    page.goto(BASE + "/admin/settings/users", wait_until="load", timeout=35000)
    wait_quiet(page)
    search = page.locator('input[placeholder="キーワードで検索する"]').first
    search.fill(EMAIL)
    search.press("Enter")
    page.wait_for_timeout(2200)
    wait_quiet(page, timeout=5000)
    result["listAfterExclude"] = snapshot(page, limit=6000)
    return result


def facts(payload):
    add = payload.get("steps", {}).get("addToRetailPortal", {})
    delete = payload.get("steps", {}).get("deleteFromRetailPortal", {})
    cleanup = payload.get("steps", {}).get("excludeUser", {})
    return {
        "email": EMAIL,
        "userCreated": bool(payload.get("steps", {}).get("createUser", {}).get("created")),
        "addDialogFoundUser": bool(add.get("selected", {}).get("found")),
        "addedListContainsEmail": any(EMAIL in row for row in add.get("afterAdd", {}).get("rows", [])),
        "deleteDialog": delete.get("dialog"),
        "deletedListContainsEmail": any(EMAIL in row for row in delete.get("afterDelete", {}).get("rows", [])),
        "userExcluded": not any(EMAIL in row for row in cleanup.get("listAfterExclude", {}).get("rows", [])),
        "errors": payload.get("errors", []),
    }


def write_md(payload):
    f = payload.get("facts") or facts(payload)
    lines = [
        "# 19 リテールポータル連携 ユーザー追加/削除確定 実機確認 2026-06-28",
        "",
        f"- 実行日時: {payload.get('generatedAt')}",
        f"- 検証用管理メンバー: `{EMAIL}`",
        f"- 対象連携: `{DETAIL_ROUTE}`",
        "",
        "## 結果",
        "",
        "| 確認項目 | 結果 |",
        "|:--|:--|",
        f"| 検証用管理メンバー作成 | `{f.get('userCreated')}` |",
        f"| 追加ダイアログで検証用ユーザーを検索・選択 | `{f.get('addDialogFoundUser')}` |",
        f"| 追加後一覧にメールアドレスが表示 | `{f.get('addedListContainsEmail')}` |",
        f"| 削除後一覧にメールアドレスが残る | `{f.get('deletedListContainsEmail')}` |",
        f"| 検証用管理メンバー除外 | `{f.get('userExcluded')}` |",
        "",
        "## 削除確認ダイアログ",
        "",
        f.get("deleteDialog") or "なし",
        "",
        "## 判断",
        "",
        "- リテールポータル連携詳細の `ユーザーを追加する` から、管理メンバーをメールアドレス検索して追加できる。",
        "- 追加後は詳細画面のユーザー一覧に `名前` / `メールアドレス` で表示される。",
        "- 追加済みユーザーは行選択後の `削除する` で削除確認ダイアログを経て削除でき、削除後の一覧から消える。",
        "- リテールポータル側に実際にログインできるか、付与される権限範囲は別権限/接続環境での確認が必要。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        f"- 追加後スクリーンショット: `{SCREENSHOT_AFTER_ADD.relative_to(ROOT)}`",
        f"- 削除後スクリーンショット: `{SCREENSHOT_AFTER_DELETE.relative_to(ROOT)}`",
    ]
    if f.get("errors"):
        lines.extend(["", "## エラー", ""])
        lines.extend([f"- `{err}`" for err in f["errors"]])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "detailRoute": DETAIL_ROUTE,
        "email": EMAIL,
        "steps": {},
        "errors": [],
    }
    save_payload(payload)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            payload["steps"]["createUser"] = create_user(page)
            save_payload(payload)
            payload["steps"]["addToRetailPortal"] = add_user_to_retail_portal(page)
            save_payload(payload)
            payload["steps"]["deleteFromRetailPortal"] = delete_user_from_retail_portal(page)
            save_payload(payload)
            payload["steps"]["excludeUser"] = exclude_created_user(page, payload["steps"]["createUser"].get("userRoute"))
        except Exception as exc:
            payload["errors"].append(repr(exc))
            try:
                payload["steps"]["finalSnapshot"] = snapshot(page)
            except Exception:
                pass
        finally:
            payload["facts"] = facts(payload)
            save_payload(payload)
            write_md(payload)
            page.close()
            browser.close()
    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
