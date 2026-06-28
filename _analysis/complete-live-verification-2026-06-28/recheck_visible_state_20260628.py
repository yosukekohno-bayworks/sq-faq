#!/usr/bin/env python3
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "visible-state-recheck-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

TOKEN_RE = re.compile(r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))")

ROUTES = [
    "/admin/analytics",
    "/admin/analytics/revenue",
    "/admin/analytics/reports",
    "/admin/b2b",
    "/admin/order_returns",
    "/admin/order_returns/create",
    "/admin/orders",
    "/admin/orders/create",
    "/admin/pdf_export",
    "/admin/pdf_export/pdf_export_operation_packing_slips/create",
    "/admin/settings/metafield_definitions",
    "/admin/settings/translation",
    "/admin/settings/translation/translation_rules",
    "/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App/admin_api",
    "/admin_api",
]


def redact(value):
    if isinstance(value, str):
        return TOKEN_RE.sub("[REDACTED_LONG_VALUE]", value)
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    return value


def extract(page):
    data = page.evaluate(
        """() => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const nodes = (selector, limit = 80) => Array.from(document.querySelectorAll(selector)).slice(0, limit);
            const body = document.body ? document.body.innerText.replace(/\\s+/g, ' ').trim() : '';
            return {
                h1: nodes('h1', 12).map(textOf).filter(Boolean),
                h2: nodes('h2', 30).map(textOf).filter(Boolean),
                buttons: nodes('button, [role="button"]', 80).map((el) => ({
                    text: textOf(el),
                    disabled: !!el.disabled,
                    ariaDisabled: el.getAttribute('aria-disabled')
                })).filter((x) => x.text),
                links: nodes('a[href]', 80).map((el) => ({
                    text: textOf(el),
                    href: el.getAttribute('href')
                })).filter((x) => x.text || x.href),
                bodySample: body.slice(0, 1600),
                hasTodo: body.includes('TODO'),
                hasNotFound: body.includes('このページは存在しないようです'),
                hasUnexpectedError: body.includes('予期せぬエラーが発生しました'),
                hasNoItems: body.includes('アイテムが見つかりませんでした')
            };
        }"""
    )
    return redact(data)


def main():
    results = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        for route in ROUTES:
            requested_url = BASE + route
            error = None
            data = {}
            final_url = None
            title = None
            try:
                page.goto(requested_url, wait_until="load", timeout=35000)
                try:
                    page.wait_for_load_state("networkidle", timeout=5000)
                except Exception:
                    pass
                page.wait_for_timeout(1200)
                final_url = page.url
                title = page.title()
                data = extract(page)
            except Exception as exc:
                error = repr(exc)
            results.append(redact({
                "route": route,
                "requestedUrl": requested_url,
                "finalUrl": final_url,
                "title": title,
                "error": error,
                **data,
            }))
            OUT.write_text(json.dumps({
                "generatedAt": datetime.now(timezone.utc).isoformat(),
                "count": len(results),
                "complete": False,
                "results": results,
            }, ensure_ascii=False, indent=2))
            time.sleep(0.1)
        page.close()
        browser.close()

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "count": len(results),
        "complete": True,
        "results": results,
        "summary": {
            "errors": sum(1 for row in results if row.get("error")),
            "todo": [row["route"] for row in results if row.get("hasTodo")],
            "notFound": [row["route"] for row in results if row.get("hasNotFound")],
            "unexpectedError": [row["route"] for row in results if row.get("hasUnexpectedError")],
            "noItems": [row["route"] for row in results if row.get("hasNoItems")],
        },
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
