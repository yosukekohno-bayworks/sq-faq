#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "19-retail-portal-user-dialog-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
DETAIL_ROUTE = "/admin/retail_portal_integrations/65104d5a-e12a-5c06-9716-48bf6cf4a67d_RetailPortalIntegration"


def compact(text, limit=2600):
    return " ".join((text or "").split())[:limit]


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snapshot(page, limit=3200):
    return {
        "url": page.url,
        "body": compact(text_of(page), limit),
        "buttons": page.evaluate(
            """() => Array.from(document.querySelectorAll('button')).map((b) => ({
                text: (b.innerText || b.textContent || '').replace(/\\s+/g, ' ').trim(),
                ariaLabel: b.getAttribute('aria-label'),
                disabled: !!b.disabled,
                ariaDisabled: b.getAttribute('aria-disabled')
            })).filter((b) => b.text || b.ariaLabel)"""
        ),
        "links": page.evaluate(
            """() => Array.from(document.querySelectorAll('a[href]')).map((a) => ({
                text: (a.innerText || a.textContent || '').replace(/\\s+/g, ' ').trim(),
                href: a.getAttribute('href')
            })).filter((a) => a.text || a.href)"""
        ),
    }


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "detailRoute": DETAIL_ROUTE,
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
            page.goto(BASE + DETAIL_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["steps"]["detailBefore"] = snapshot(page, limit=5000)
            selected_row = page.evaluate(
                """() => {
                    const row = Array.from(document.querySelectorAll('tr')).find((tr) => tr.innerText.includes('yosuke.kohno@bay-works.com'));
                    if (!row) return null;
                    const checkbox = row.querySelector('input[type="checkbox"]');
                    if (!checkbox) return {rowText: row.innerText, selected: false};
                    checkbox.click();
                    return {rowText: row.innerText, selected: true};
                }"""
            )
            page.wait_for_timeout(700)
            payload["steps"]["afterSelectingExistingUserRow"] = {
                "selectedRow": selected_row,
                **snapshot(page, limit=5000),
            }
            delete_button = page.get_by_role("button", name="削除する", exact=True).first
            if delete_button.count():
                delete_button.click()
                page.wait_for_selector('div[role="dialog"]', timeout=10000)
                delete_dialog = page.locator('div[role="dialog"]').last
                payload["steps"]["deleteDialogThenCancel"] = {
                    "text": compact(delete_dialog.inner_text(timeout=5000), 2200),
                    "buttons": page.evaluate(
                        """() => Array.from(document.querySelectorAll('div[role="dialog"] button')).map((b) => ({
                            text: (b.innerText || b.textContent || '').replace(/\\s+/g, ' ').trim(),
                            disabled: !!b.disabled,
                            ariaDisabled: b.getAttribute('aria-disabled')
                        }))"""
                    ),
                }
                cancel_delete = delete_dialog.get_by_role("button", name="キャンセル", exact=True)
                if cancel_delete.count():
                    cancel_delete.click()
                    page.wait_for_timeout(700)
            page.reload(wait_until="load")
            wait_quiet(page)

            add_button = page.get_by_role("button", name="ユーザーを追加する", exact=True)
            payload["steps"]["hasAddUserButton"] = add_button.count() > 0
            if add_button.count():
                add_button.click()
                page.wait_for_selector('div[role="dialog"]', timeout=15000)
                dialog = page.locator('div[role="dialog"]').last
                payload["steps"]["dialogInitial"] = {
                    "text": compact(dialog.inner_text(timeout=5000), 2600),
                    "inputs": page.evaluate(
                        """() => Array.from(document.querySelectorAll('div[role="dialog"] input')).map((i) => ({
                            type: i.getAttribute('type'),
                            placeholder: i.getAttribute('placeholder'),
                            ariaLabel: i.getAttribute('aria-label'),
                            value: i.value
                        }))"""
                    ),
                    "buttons": page.evaluate(
                        """() => Array.from(document.querySelectorAll('div[role="dialog"] button')).map((b) => ({
                            text: (b.innerText || b.textContent || '').replace(/\\s+/g, ' ').trim(),
                            disabled: !!b.disabled,
                            ariaDisabled: b.getAttribute('aria-disabled')
                        }))"""
                    ),
                }
                search = dialog.locator("input").first
                search.fill("kouno")
                search.press("Enter")
                page.wait_for_timeout(1600)
                payload["steps"]["dialogAfterSearchKouno"] = {
                    "text": compact(dialog.inner_text(timeout=5000), 3000),
                    "buttons": page.evaluate(
                        """() => Array.from(document.querySelectorAll('div[role="dialog"] button')).map((b) => ({
                            text: (b.innerText || b.textContent || '').replace(/\\s+/g, ' ').trim(),
                            disabled: !!b.disabled,
                            ariaDisabled: b.getAttribute('aria-disabled')
                        }))"""
                    ),
                }
                search.fill("yosuke.kohno@bay-works.com")
                search.press("Enter")
                page.wait_for_timeout(1600)
                payload["steps"]["dialogAfterSearchEmail"] = {
                    "text": compact(dialog.inner_text(timeout=5000), 3000),
                    "buttons": page.evaluate(
                        """() => Array.from(document.querySelectorAll('div[role="dialog"] button')).map((b) => ({
                            text: (b.innerText || b.textContent || '').replace(/\\s+/g, ' ').trim(),
                            disabled: !!b.disabled,
                            ariaDisabled: b.getAttribute('aria-disabled')
                        }))"""
                    ),
                }
                # Close without mutating the integration.
                cancel = dialog.get_by_role("button", name="キャンセル", exact=True)
                if cancel.count():
                    cancel.click()
                    page.wait_for_timeout(700)
                payload["steps"]["afterCancel"] = snapshot(page, limit=4200)
                page.reload(wait_until="load")
                wait_quiet(page)
                payload["steps"]["afterReload"] = snapshot(page, limit=4200)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            payload["steps"]["final"] = snapshot(page, limit=4200)
        finally:
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
            page.close()
            browser.close()
    print(json.dumps({
        "errors": payload["errors"],
        "hasAddUserButton": payload.get("steps", {}).get("hasAddUserButton"),
        "dialogText": payload.get("steps", {}).get("dialogInitial", {}).get("text"),
        "searchText": payload.get("steps", {}).get("dialogAfterSearchKouno", {}).get("text"),
        "emailSearchText": payload.get("steps", {}).get("dialogAfterSearchEmail", {}).get("text"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
