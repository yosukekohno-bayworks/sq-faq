#!/usr/bin/env python3
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
URL_INDEX = ROOT / "_analysis" / "04-notion-live-audit-url-index-2026-06-27.json"
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "route-crawl-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

TOKEN_RE = re.compile(r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))")


def redact(value):
    if value is None:
        return value
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
            const attr = (el, name) => el.getAttribute(name);
            const nodes = (selector, limit = 80) => Array.from(document.querySelectorAll(selector)).slice(0, limit);
            const controls = nodes('input, textarea', 120).map((el) => ({
                tag: el.tagName.toLowerCase(),
                type: attr(el, 'type'),
                name: attr(el, 'name'),
                id: attr(el, 'id'),
                placeholder: attr(el, 'placeholder'),
                ariaLabel: attr(el, 'aria-label'),
                disabled: !!el.disabled,
                required: !!el.required
            }));
            const selects = nodes('select, [role="combobox"]', 120).map((el) => ({
                tag: el.tagName.toLowerCase(),
                role: attr(el, 'role'),
                name: attr(el, 'name'),
                id: attr(el, 'id'),
                ariaLabel: attr(el, 'aria-label'),
                disabled: !!el.disabled,
                text: textOf(el).slice(0, 300),
                options: Array.from(el.querySelectorAll('option')).slice(0, 40).map((op) => ({
                    text: textOf(op),
                    value: op.getAttribute('value'),
                    disabled: !!op.disabled
                }))
            }));
            const buttons = nodes('button, [role="button"]', 160).map((el) => ({
                text: textOf(el),
                disabled: !!el.disabled,
                ariaDisabled: attr(el, 'aria-disabled')
            })).filter((x) => x.text);
            const links = nodes('a[href]', 160).map((el) => ({
                text: textOf(el),
                href: el.getAttribute('href')
            })).filter((x) => x.text || x.href);
            const body = document.body ? document.body.innerText.replace(/\\s+/g, ' ').trim() : '';
            return {
                h1: nodes('h1', 20).map(textOf).filter(Boolean),
                h2: nodes('h2', 40).map(textOf).filter(Boolean),
                h3: nodes('h3', 40).map(textOf).filter(Boolean),
                buttons,
                links,
                controls,
                selects,
                bodySample: body.slice(0, 2000),
                hasTodo: body.includes('TODO'),
                hasNotFound: body.includes('このページは存在しないようです'),
                hasUnexpectedError: body.includes('予期せぬエラーが発生しました')
            };
        }"""
    )
    return redact(data)


def main():
    index = json.loads(URL_INDEX.read_text())
    routes = sorted(url for url, meta in index.items() if meta.get("kind") == "concrete")
    results = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        for i, route in enumerate(routes, 1):
            requested = BASE + route
            error = None
            data = {}
            final_url = None
            title = None
            try:
                page.goto(requested, wait_until="load", timeout=35000)
                try:
                    page.wait_for_load_state("networkidle", timeout=6000)
                except Exception:
                    pass
                page.wait_for_timeout(2200)
                final_url = page.url
                title = page.title()
                data = extract(page)
            except Exception as exc:
                error = repr(exc)
            results.append({
                "route": route,
                "requestedUrl": requested,
                "finalUrl": final_url,
                "title": title,
                "error": error,
                **data,
            })
            if i % 20 == 0:
                OUT.write_text(json.dumps({
                    "generatedAt": datetime.now(timezone.utc).isoformat(),
                    "count": len(results),
                    "complete": False,
                    "results": results,
                }, ensure_ascii=False, indent=2))
            time.sleep(0.1)
        page.close()
        browser.close()
    OUT.write_text(json.dumps({
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "count": len(results),
        "complete": True,
        "results": results,
    }, ensure_ascii=False, indent=2))
    print(json.dumps({
        "count": len(results),
        "errors": sum(1 for r in results if r.get("error")),
        "notFound": [r["route"] for r in results if r.get("hasNotFound")],
        "unexpectedError": [r["route"] for r in results if r.get("hasUnexpectedError")],
        "todo": [r["route"] for r in results if r.get("hasTodo")],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
