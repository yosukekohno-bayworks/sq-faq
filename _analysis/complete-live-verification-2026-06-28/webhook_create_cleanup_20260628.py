#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "23-webhook-create-cleanup-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
APP_ROUTE = "/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App"
APP_NAME = "TEST_FAQ_20260624_APP_113636"
TOKEN_RE = re.compile(r"(eyJ[A-Za-z0-9_.-]{20,}|[A-Za-z0-9_+/=-]{40,})")


def redact(text):
    return TOKEN_RE.sub("[REDACTED_SECRET]", text or "")


def compact(text, limit=2400):
    return redact(" ".join((text or "").split())[:limit])


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snapshot(page, limit=3000):
    buttons = page.evaluate(
        """() => Array.from(document.querySelectorAll('button')).map((b) => ({
            text: (b.innerText || b.textContent || '').replace(/\\s+/g, ' ').trim(),
            ariaLabel: b.getAttribute('aria-label'),
            disabled: !!b.disabled,
            ariaDisabled: b.getAttribute('aria-disabled')
        })).filter((b) => b.text || b.ariaLabel)"""
    )
    links = page.evaluate(
        """() => Array.from(document.querySelectorAll('a[href]')).map((a) => ({
            text: (a.innerText || a.textContent || '').replace(/\\s+/g, ' ').trim(),
            href: a.getAttribute('href')
        })).filter((a) => a.text || a.href)"""
    )
    return {
        "url": page.url,
        "body": compact(text_of(page), limit),
        "buttons": buttons[:80],
        "links": links[:80],
    }


def create_webhook(page, endpoint):
    page.goto(BASE + APP_ROUTE, wait_until="load")
    wait_quiet(page)
    before = snapshot(page)
    page.get_by_role("button", name="Webhookを作成する", exact=True).click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    before_save = {
        "dialogText": compact(dialog.inner_text(timeout=5000), 1800),
        "selectOptions": page.evaluate(
            """() => Array.from(document.querySelectorAll('div[role="dialog"] select option')).map((o) => ({
                value: o.value,
                text: (o.innerText || o.textContent || '').trim()
            }))"""
        ),
    }
    dialog.locator("select").first.select_option(label="注文の作成")
    dialog.locator('input[type="url"]').first.fill(endpoint)
    dialog.get_by_role("button", name="保存する", exact=True).click()
    page.wait_for_timeout(2500)
    wait_quiet(page, timeout=5000)
    return {
        "before": before,
        "beforeSave": before_save,
        "afterSave": snapshot(page, limit=4200),
    }


def try_cleanup(page, endpoint):
    result = {"attempted": False, "method": None, "before": snapshot(page, limit=4200)}
    body = text_of(page)
    if endpoint not in body:
        result["reason"] = "endpoint not visible after save"
        return result

    # Prefer row checkbox + bulk delete if the Webhook is rendered in a table.
    selected = page.evaluate(
        """(endpoint) => {
            const row = Array.from(document.querySelectorAll('tr')).find((tr) => tr.innerText.includes(endpoint));
            if (!row) return null;
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox) {
                checkbox.click();
                return row.innerText;
            }
            return null;
        }""",
        endpoint,
    )
    page.wait_for_timeout(700)
    if selected and page.get_by_role("button", name="削除する").count():
        result["attempted"] = True
        result["method"] = "row-checkbox-delete"
        result["selectedRow"] = compact(selected, 1000)
        page.get_by_role("button", name="削除する", exact=True).click()
        page.wait_for_selector('div[role="dialog"]', timeout=10000)
        dialog = page.locator('div[role="dialog"]').last
        result["confirmText"] = compact(dialog.inner_text(timeout=5000), 1400)
        dialog.get_by_role("button", name="削除する", exact=True).click()
        page.wait_for_timeout(2200)
        wait_quiet(page, timeout=4000)
        result["after"] = snapshot(page, limit=3600)
        result["endpointStillVisible"] = endpoint in text_of(page)
        return result

    # If there is no visible delete action, keep the evidence but avoid clicking
    # icon-only buttons whose purpose is not explicit.
    result["reason"] = "no explicit row checkbox + delete button found"
    result["after"] = snapshot(page, limit=4200)
    result["endpointStillVisible"] = endpoint in text_of(page)
    return result


def main():
    now = datetime.now(timezone.utc)
    suffix = now.strftime("%Y%m%d%H%M%S")
    endpoint = f"https://sq-faq-webhook.invalid/{suffix}"
    payload = {
        "generatedAt": now.isoformat(),
        "appRoute": APP_ROUTE,
        "appName": APP_NAME,
        "endpoint": endpoint,
        "errors": [],
        "steps": {},
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            payload["steps"]["create"] = create_webhook(page, endpoint)
            payload["steps"]["cleanup"] = try_cleanup(page, endpoint)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            payload["final"] = snapshot(page, limit=4200)
        finally:
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
            page.close()
            browser.close()
    print(json.dumps({
        "endpoint": endpoint,
        "errors": payload["errors"],
        "endpointVisibleAfterSave": endpoint in payload.get("steps", {}).get("create", {}).get("afterSave", {}).get("body", ""),
        "cleanupAttempted": payload.get("steps", {}).get("cleanup", {}).get("attempted"),
        "endpointStillVisible": payload.get("steps", {}).get("cleanup", {}).get("endpointStillVisible"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
