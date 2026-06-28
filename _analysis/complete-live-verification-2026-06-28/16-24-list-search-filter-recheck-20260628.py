#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "16-24-list-search-filter-recheck-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")


def compact(text, limit=3000):
    return " ".join((text or "").split())[:limit]


def wait_soft(page, timeout=10000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(700)


def snapshot(page, label):
    return page.evaluate(
        """(label) => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const labelFor = (el) => {
                if (el.id) {
                    const label = document.querySelector(`label[for="${CSS.escape(el.id)}"]`);
                    if (label) return text(label);
                }
                const wrapped = el.closest('label');
                if (wrapped) return text(wrapped);
                return el.getAttribute('aria-label') || '';
            };
            const uniq = (arr) => Array.from(new Set(arr.filter(Boolean)));
            const body = document.body ? document.body.innerText.replace(/\\s+/g, ' ').trim() : '';
            return {
                label,
                url: location.href,
                h1: uniq(Array.from(document.querySelectorAll('h1')).map(text)),
                headers: uniq(Array.from(document.querySelectorAll('th')).map(text)),
                rows: Array.from(document.querySelectorAll('tr')).slice(0, 12).map(text).filter(Boolean),
                buttons: Array.from(document.querySelectorAll('button,[role="button"]')).map((el) => ({
                    text: text(el) || el.getAttribute('aria-label') || '',
                    ariaLabel: el.getAttribute('aria-label') || '',
                    disabled: !!el.disabled,
                    ariaDisabled: el.getAttribute('aria-disabled')
                })).filter((x) => x.text || x.ariaLabel),
                inputs: Array.from(document.querySelectorAll('input,select,textarea')).map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type') || '',
                    label: labelFor(el),
                    placeholder: el.getAttribute('placeholder') || '',
                    value: el.value || '',
                    options: el.tagName.toLowerCase() === 'select' ? Array.from(el.options).map(text) : []
                })),
                hasSearchResultButton: body.includes('検索と絞り込みの結果'),
                hasAddFilter: body.includes('絞り込みを追加'),
                hasSaveView: body.includes('名前を付けて保存'),
                bodySample: body.slice(0, 2500)
            };
        }""",
        label,
    )


def open_search_panel(page):
    opened = {"clicked": [], "pressedF": False}
    for name in ["検索と絞り込みの結果", "検索"]:
        loc = page.get_by_role("button", name=name, exact=True)
        if loc.count():
            try:
                loc.first.click(timeout=5000)
                wait_soft(page)
                opened["clicked"].append(name)
                break
            except Exception:
                pass
    page.keyboard.press("F")
    opened["pressedF"] = True
    wait_soft(page)
    return opened


def inspect_route(page, route):
    page.goto(BASE + route, wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    before = snapshot(page, "before-open-search")
    opened = open_search_panel(page)
    after = snapshot(page, "after-open-search")
    filter_menu = None
    add_filter = page.get_by_role("button", name="絞り込みを追加", exact=True)
    if add_filter.count():
        try:
            add_filter.first.click(timeout=5000)
            wait_soft(page)
            filter_menu = snapshot(page, "after-click-add-filter")
        except Exception as exc:
            filter_menu = {"error": repr(exc)}
    return {"route": route, "openSearch": opened, "before": before, "after": after, "filterMenu": filter_menu}


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "routes": {},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            for name, route in [
                ("orders", "/admin/orders"),
                ("orderReturns", "/admin/order_returns"),
                ("saleChangeLineItems", "/admin/sale_change_line_items"),
            ]:
                try:
                    payload["routes"][name] = inspect_route(page, route)
                except Exception as exc:
                    payload["errors"].append({name: repr(exc)})
        finally:
            page.close()

    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# 注文・返品・売上実績 検索/絞り込みUI再確認 2026-06-28", ""]
    for name, data in payload["routes"].items():
        after = data.get("after", {})
        menu = data.get("filterMenu") or {}
        lines.extend([
            f"## {name}",
            f"- URL: `{data.get('route')}`",
            f"- テーブル列: `{ ' / '.join(after.get('headers') or []) }`",
            f"- 検索パネル表示: `{after.get('hasSearchResultButton')}`",
            f"- 絞り込み追加表示: `{after.get('hasAddFilter')}`",
            f"- 名前を付けて保存表示: `{after.get('hasSaveView')}`",
            f"- 入力欄: `{json.dumps(after.get('inputs') or [], ensure_ascii=False)}`",
            f"- 絞り込みメニュー本文: `{compact((menu.get('bodySample') if isinstance(menu, dict) else '') or '', 1000)}`",
            "",
        ])
    if payload["errors"]:
        lines.append("## Errors")
        lines.append(json.dumps(payload["errors"], ensure_ascii=False, indent=2))
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"routes": list(payload["routes"]), "errors": payload["errors"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
