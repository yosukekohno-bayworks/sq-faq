#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "21-dhl-import-format-recheck-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
LIST_ROUTE = "/admin/csv_import/csv_import_operation_fulfillment_by_dhls"
CREATE_ROUTE = "/admin/csv_import/csv_import_operation_fulfillment_by_dhls/create"


def compact(text, limit=3200):
    return " ".join((text or "").split())[:limit]


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snapshot(page, limit=4200):
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
        "inputs": page.evaluate(
            """() => Array.from(document.querySelectorAll('input')).map((i) => ({
                type: i.getAttribute('type'),
                placeholder: i.getAttribute('placeholder'),
                ariaLabel: i.getAttribute('aria-label'),
                name: i.getAttribute('name')
            }))"""
        ),
    }


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "routes": [LIST_ROUTE, CREATE_ROUTE],
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
            page.goto(BASE + LIST_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["steps"]["list"] = snapshot(page)
            payload["steps"]["listHasTemplateText"] = "テンプレート" in text_of(page)
            payload["steps"]["listHasNewImport"] = "新規インポート" in text_of(page)

            page.goto(BASE + CREATE_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["steps"]["createBeforeSave"] = snapshot(page)
            payload["steps"]["createHasTemplateText"] = "テンプレート" in text_of(page)

            save = page.get_by_role("button", name="保存する", exact=True)
            if save.count():
                save.click()
                page.wait_for_timeout(1800)
                wait_quiet(page, timeout=4000)
                payload["steps"]["createAfterEmptySave"] = snapshot(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            payload["steps"]["final"] = snapshot(page)
        finally:
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
            page.close()
            browser.close()
    print(json.dumps({
        "errors": payload["errors"],
        "listHasTemplateText": payload.get("steps", {}).get("listHasTemplateText"),
        "listHasNewImport": payload.get("steps", {}).get("listHasNewImport"),
        "createHasTemplateText": payload.get("steps", {}).get("createHasTemplateText"),
        "emptySaveHasFileError": "ファイルを選択してください" in payload.get("steps", {}).get("createAfterEmptySave", {}).get("body", ""),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
