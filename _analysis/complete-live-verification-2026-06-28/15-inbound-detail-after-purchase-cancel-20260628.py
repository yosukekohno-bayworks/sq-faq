#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "15-inbound-detail-after-purchase-cancel-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
ROUTE = "/admin/inventory_inbound_orders/3506bdef-629c-5ebd-98fd-ca256a1959c5_InventoryInboundOrder"
TOKEN_RE = re.compile(r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))")


def compact(text, limit=7000):
    return TOKEN_RE.sub("[REDACTED_LONG_VALUE]", " ".join((text or "").split())[:limit])


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snapshot(page):
    data = page.evaluate(
        """() => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const attr = (el, name) => el.getAttribute(name);
            const nodes = (selector, limit = 120) => Array.from(document.querySelectorAll(selector)).slice(0, limit);
            return {
                url: location.href,
                h1: nodes('h1', 10).map(textOf).filter(Boolean),
                h2: nodes('h2', 30).map(textOf).filter(Boolean),
                controls: nodes('button, a, input, [role="button"], [role="menuitem"]', 220)
                    .map((el) => ({
                        tag: el.tagName.toLowerCase(),
                        text: textOf(el),
                        href: attr(el, 'href'),
                        disabled: !!el.disabled,
                        ariaDisabled: attr(el, 'aria-disabled'),
                        ariaLabel: attr(el, 'aria-label')
                    }))
                    .filter((x) => x.text || x.href || x.ariaLabel),
                rows: nodes('tr', 60).map(textOf).filter(Boolean),
                body: document.body ? document.body.innerText : ''
            };
        }"""
    )
    data["body"] = compact(data.get("body", ""))
    return data


def main():
    payload = {"generatedAt": datetime.now(timezone.utc).isoformat(), "route": ROUTE, "snapshot": None, "errors": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(BASE + ROUTE, wait_until="load", timeout=35000)
            wait_quiet(page)
            payload["snapshot"] = snapshot(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
            page.close()
            browser.close()
    print(json.dumps({"out": str(OUT), "errors": payload["errors"], "h1": payload.get("snapshot", {}).get("h1")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
