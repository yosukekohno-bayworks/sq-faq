#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "02-user-create-exclude-readd-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
GROUP_NAME = "TEST_権限検証_20260620"


def compact(text, limit=2000):
    return " ".join((text or "").split())[:limit]


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def fill_user_form(page, family_name, given_name, email, select_group=False):
    page.goto(f"{BASE}/admin/settings/users/create", wait_until="load")
    wait_quiet(page)
    inputs = page.locator("input")
    inputs.nth(0).fill(family_name)
    inputs.nth(1).fill(given_name)
    inputs.nth(2).fill(email)
    if select_group:
        label = page.locator("label", has_text=GROUP_NAME).first
        if label.count():
            label.click()
        else:
            page.locator('input[type="radio"]').nth(1).check(force=True)


def save_form(page):
    page.get_by_role("button", name="保存する", exact=True).click()
    page.wait_for_timeout(2500)
    wait_quiet(page, timeout=4000)
    return {
        "url": page.url,
        "body": compact(text_of(page), 3000),
    }


def user_visible_in_list(page, email):
    page.goto(f"{BASE}/admin/settings/users", wait_until="load")
    wait_quiet(page)
    search = page.locator('input[placeholder="キーワードで検索する"]').first
    search.fill(email)
    search.press("Enter")
    page.wait_for_timeout(1800)
    body = text_of(page)
    return {
        "url": page.url,
        "containsEmail": email in body,
        "body": compact(body, 2200),
    }


def exclude_current_user(page):
    result = {
        "startUrl": page.url,
        "startBody": compact(text_of(page), 2200),
        "dialogText": None,
        "afterUrl": None,
        "afterBody": None,
    }
    page.get_by_role("button", name="組織から除外する", exact=True).click()
    page.wait_for_timeout(700)
    dialogs = page.locator('div[role="dialog"]')
    if dialogs.count():
        dialog = dialogs.last
        result["dialogText"] = compact(dialog.inner_text(timeout=5000), 1600)
        buttons = dialog.locator("button")
        clicked = False
        for i in range(buttons.count()):
            label = compact(buttons.nth(i).inner_text(timeout=2000), 200)
            if "除外" in label:
                buttons.nth(i).click()
                clicked = True
                break
        if not clicked:
            raise RuntimeError("exclude confirm button not found")
    page.wait_for_timeout(2500)
    wait_quiet(page, timeout=4000)
    result["afterUrl"] = page.url
    result["afterBody"] = compact(text_of(page), 2600)
    return result


def create_user(page, family_name, given_name, email, select_group):
    fill_user_form(page, family_name, given_name, email, select_group=select_group)
    before = compact(text_of(page), 2200)
    save = save_form(page)
    created = (
        "/admin/settings/users/create" not in save["url"]
        and "/admin/settings/users/" in save["url"]
        and "ユーザーを追加しました" in save["body"]
    )
    return {
        "selectGroup": select_group,
        "beforeSaveBody": before,
        "afterSave": save,
        "created": created,
    }


def main():
    now = datetime.now(timezone.utc)
    suffix = now.strftime("%Y%m%d%H%M%S")
    family_name = "FAQ検証"
    given_name = f"Member{suffix[-6:]}"
    email = f"sq-faq-member-{suffix}@example.com"
    payload = {
        "generatedAt": now.isoformat(),
        "email": email,
        "familyName": family_name,
        "givenName": given_name,
        "permissionGroupUsedForFallback": GROUP_NAME,
        "steps": {},
        "errors": [],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            payload["steps"]["createWithoutPermissionGroup"] = create_user(
                page, family_name, given_name, email, select_group=False
            )
            created_without_group = payload["steps"]["createWithoutPermissionGroup"]["created"]

            if created_without_group:
                payload["steps"]["createdUserDetail"] = {
                    "url": page.url,
                    "body": compact(text_of(page), 3000),
                }
            else:
                payload["steps"]["createWithPermissionGroup"] = create_user(
                    page, family_name, given_name, email, select_group=True
                )

            payload["steps"]["listAfterCreate"] = user_visible_in_list(page, email)

            # Open detail through the searched row if list contains it.
            if payload["steps"]["listAfterCreate"]["containsEmail"]:
                row_clicked = page.evaluate(
                    """(email) => {
                        const row = Array.from(document.querySelectorAll('tr')).find((tr) => tr.innerText.includes(email));
                        if (!row) return null;
                        row.click();
                        return row.innerText;
                    }""",
                    email,
                )
                page.wait_for_timeout(1600)
                wait_quiet(page, timeout=4000)
                payload["steps"]["openedDetailFromList"] = {
                    "rowText": compact(row_clicked, 1000),
                    "url": page.url,
                    "body": compact(text_of(page), 3000),
                }
                payload["steps"]["excludeFirstUser"] = exclude_current_user(page)
                payload["steps"]["listAfterFirstExclude"] = user_visible_in_list(page, email)

                payload["steps"]["readdSameEmail"] = create_user(
                    page, family_name, given_name, email, select_group=True
                )
                payload["steps"]["listAfterReadd"] = user_visible_in_list(page, email)
                if payload["steps"]["listAfterReadd"]["containsEmail"]:
                    row_clicked = page.evaluate(
                        """(email) => {
                            const row = Array.from(document.querySelectorAll('tr')).find((tr) => tr.innerText.includes(email));
                            if (!row) return null;
                            row.click();
                            return row.innerText;
                        }""",
                        email,
                    )
                    page.wait_for_timeout(1600)
                    wait_quiet(page, timeout=4000)
                    payload["steps"]["openedReaddedDetailFromList"] = {
                        "rowText": compact(row_clicked, 1000),
                        "url": page.url,
                        "body": compact(text_of(page), 2600),
                    }
                    payload["steps"]["excludeReaddedUser"] = exclude_current_user(page)
                    payload["steps"]["listAfterCleanup"] = user_visible_in_list(page, email)
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            payload["finalUrl"] = page.url
            payload["finalBody"] = compact(text_of(page), 2600)
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
            page.close()
            browser.close()
    print(json.dumps({
        "email": email,
        "errors": payload["errors"],
        "createdWithoutPermissionGroup": payload.get("steps", {}).get("createWithoutPermissionGroup", {}).get("created"),
        "readdCreated": payload.get("steps", {}).get("readdSameEmail", {}).get("created"),
        "cleanupContainsEmail": payload.get("steps", {}).get("listAfterCleanup", {}).get("containsEmail"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
