#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "14-allocation-request-close-reopen-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

TARGET_WAITING = "/admin/inventory_allocation_requests/726d9d8e-929b-533d-a875-a3a474cd18a0_InventoryAllocationRequest"
TARGET_CONFIRMED = "/admin/inventory_allocation_requests/396629c7-27d6-57af-b652-dcc9691eb4f6_InventoryAllocationRequest"
TARGET_MOVED = "/admin/inventory_allocation_requests/46fd468a-2570-5dc2-9f0d-a96471824d1e_InventoryAllocationRequest"
TARGET_LEFT_OPEN = "/admin/inventory_allocation_requests/7d388233-b643-5065-b17f-c3a1b9393226_InventoryAllocationRequest"

LONG_TOKEN_RE = re.compile(r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))")


def redact(value):
    if isinstance(value, str):
        return LONG_TOKEN_RE.sub("[REDACTED_LONG_VALUE]", value)
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    return value


def compact(text, limit=5000):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snapshot(page, limit=5000):
    data = page.evaluate(
        """() => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const attr = (el, name) => el.getAttribute(name);
            const nodes = (selector, limit = 120) => Array.from(document.querySelectorAll(selector)).slice(0, limit);
            const controls = nodes('button, a, input, textarea, [role="button"], [role="menuitem"]', 220)
                .map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    role: attr(el, 'role'),
                    text: textOf(el),
                    href: attr(el, 'href'),
                    type: attr(el, 'type'),
                    ariaLabel: attr(el, 'aria-label'),
                    ariaDisabled: attr(el, 'aria-disabled'),
                    disabled: !!el.disabled
                }))
                .filter((x) => x.text || x.href || x.ariaLabel);
            return {
                url: location.href,
                h1: nodes('h1', 10).map(textOf).filter(Boolean),
                h2: nodes('h2', 20).map(textOf).filter(Boolean),
                badgesAndStatus: nodes('[class*="Badge"], [class*="badge"], [data-testid*="badge"]', 80)
                    .map(textOf).filter(Boolean),
                controls,
                body: document.body ? document.body.innerText : ''
            };
        }"""
    )
    data["body"] = compact(data.get("body", ""), limit)
    return redact(data)


def click_other_menu_and_snapshot(page):
    result = {"clicked": False, "menuItems": [], "afterClick": None, "error": None}
    try:
        menu = page.get_by_role("button", name="その他の操作", exact=True)
        if not menu.count():
            result["error"] = "その他の操作 button not found"
            return result
        menu.first.click()
        page.wait_for_timeout(700)
        result["clicked"] = True
        result["afterClick"] = snapshot(page, limit=6500)
        result["menuItems"] = page.evaluate(
            """() => Array.from(document.querySelectorAll('[role="menuitem"], [role="option"], button, a'))
                .map((el) => ({
                    text: (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim(),
                    tag: el.tagName.toLowerCase(),
                    role: el.getAttribute('role'),
                    href: el.getAttribute('href'),
                    disabled: !!el.disabled,
                    ariaDisabled: el.getAttribute('aria-disabled')
                }))
                .filter((x) => x.text.includes('在庫依頼') || x.text.includes('クローズ') || x.text.includes('再開') || x.text.includes('再利用') || x.text.includes('キャンセル') || x.text.includes('引当'))"""
        )
    except Exception as exc:
        result["error"] = repr(exc)
    return redact(result)


def close_waiting_if_possible(page):
    result = {"attempted": False, "clickedCloseMenu": False, "dialog": None, "confirmClicked": None, "after": None, "error": None}
    try:
        menu = page.get_by_role("button", name="その他の操作", exact=True)
        if not menu.count():
            result["error"] = "その他の操作 button not found"
            return result
        menu.first.click()
        page.wait_for_timeout(700)
        close_item = page.get_by_text("在庫依頼をクローズする", exact=True)
        if not close_item.count():
            result["error"] = "在庫依頼をクローズする item not found"
            return result
        result["attempted"] = True
        close_item.first.click()
        result["clickedCloseMenu"] = True
        page.wait_for_timeout(900)
        dialog = page.locator('div[role="dialog"]').last
        if dialog.count():
            result["dialog"] = compact(dialog.inner_text(timeout=5000), 2500)
            candidates = ["在庫依頼をクローズする", "クローズする", "実行する", "削除する", "保存する"]
            for name in candidates:
                button = dialog.get_by_role("button", name=name, exact=True)
                if button.count():
                    disabled = button.first.evaluate("(el) => !!el.disabled || el.getAttribute('aria-disabled') === 'true'")
                    result["confirmClicked"] = {"name": name, "disabled": disabled}
                    if not disabled:
                        button.first.click()
                        break
            else:
                result["error"] = "confirm button not found"
                return result
        else:
            result["dialog"] = "dialog not found"
            return result
        wait_quiet(page)
        result["after"] = snapshot(page, limit=7000)
    except Exception as exc:
        result["error"] = repr(exc)
        result["after"] = snapshot(page, limit=7000)
    return redact(result)


def select_modal_row(page, open_button_index, row_text):
    page.get_by_role("button", name="選択", exact=True).nth(open_button_index).click()
    wait_expr = """(rowText) => Array.from(document.querySelectorAll('tr')).some((tr) => (tr.innerText || '').includes(rowText))"""
    try:
        page.wait_for_function(wait_expr, arg=row_text, timeout=12000)
    except PlaywrightTimeoutError:
        search_inputs = page.locator('input[placeholder*="検索"]')
        if search_inputs.count():
            search_inputs.first.fill(row_text)
            page.wait_for_timeout(1500)
            try:
                page.wait_for_function(wait_expr, arg=row_text, timeout=8000)
            except PlaywrightTimeoutError:
                pass
        if not page.evaluate(wait_expr, row_text):
            return redact({
                "found": False,
                "rowText": row_text,
                "rowSamples": page.evaluate(
                    """() => Array.from(document.querySelectorAll('tr')).slice(0, 12)
                        .map((tr) => (tr.innerText || '').replace(/\\s+/g, ' ').trim())"""
                ),
                "body": compact(page.evaluate("() => document.body ? document.body.innerText : ''"), 2500),
            })
    row_info = page.evaluate(
        """(rowText) => {
            const rows = Array.from(document.querySelectorAll('tr'));
            const row = rows.find((tr) => (tr.innerText || '').includes(rowText));
            if (!row) return {found: false, rowText};
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox) {
                checkbox.click();
            } else {
                row.click();
            }
            return {found: true, rowText: (row.innerText || '').replace(/\\s+/g, ' ').trim()};
        }""",
        row_text,
    )
    page.wait_for_timeout(500)
    page.get_by_role("button", name="選択する", exact=True).last.click()
    page.wait_for_timeout(900)
    return redact(row_info)


def create_waiting_request(page):
    result = {"steps": {}, "createdRoute": None, "error": None}
    try:
        page.goto(BASE + "/admin/inventory_allocation_requests/create", wait_until="load", timeout=35000)
        wait_quiet(page)
        result["steps"]["initialForm"] = snapshot(page, limit=3500)
        result["steps"]["productSelected"] = select_modal_row(page, 0, "482787-30-ONE")
        page.locator('input[type="number"]').first.fill("1")
        page.wait_for_timeout(300)
        result["steps"]["destinationSelected"] = select_modal_row(page, 0, "ユニクロEC")
        result["steps"]["requestSourceSelected"] = select_modal_row(page, 1, "ユニクロEC")
        result["steps"]["filledForm"] = snapshot(page, limit=4500)
        page.get_by_role("button", name="保存する", exact=True).last.click()
        wait_quiet(page, timeout=9000)
        result["steps"]["afterSave"] = snapshot(page, limit=7000)
        if "/admin/inventory_allocation_requests/" in page.url:
            result["createdRoute"] = page.url.replace(BASE, "")
    except Exception as exc:
        result["error"] = repr(exc)
        try:
            result["steps"]["finalSnapshot"] = snapshot(page, limit=7000)
        except Exception:
            pass
    return redact(result)


def create_close_and_inspect(page):
    item = {"label": "new-close", "steps": {}, "error": None}
    try:
        created = create_waiting_request(page)
        item["steps"]["create"] = created
        route = created.get("createdRoute")
        if not route:
            item["error"] = "created detail route not found"
            return item
        item["route"] = route
        page.goto(BASE + route, wait_until="load", timeout=35000)
        wait_quiet(page)
        item["steps"]["afterCreateReload"] = snapshot(page, limit=7000)
        item["steps"]["beforeCloseMenu"] = click_other_menu_and_snapshot(page)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        item["steps"]["closeAttempt"] = close_waiting_if_possible(page)
        item["steps"]["afterCloseImmediate"] = snapshot(page, limit=7000)
        page.goto(BASE + route, wait_until="load", timeout=35000)
        wait_quiet(page)
        item["steps"]["afterCloseReload"] = snapshot(page, limit=7000)
        item["steps"]["afterCloseMenu"] = click_other_menu_and_snapshot(page)
    except Exception as exc:
        item["error"] = repr(exc)
        try:
            item["steps"]["finalSnapshot"] = snapshot(page, limit=7000)
        except Exception:
            pass
    return redact(item)


def inspect_route(page, label, route, close=False):
    item = {"label": label, "route": route, "steps": {}, "error": None}
    try:
        page.goto(BASE + route, wait_until="load", timeout=35000)
        wait_quiet(page)
        item["steps"]["initial"] = snapshot(page, limit=7000)
        item["steps"]["menuBefore"] = click_other_menu_and_snapshot(page)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        if close:
            item["steps"]["closeAttempt"] = close_waiting_if_possible(page)
            page.goto(BASE + route, wait_until="load", timeout=35000)
            wait_quiet(page)
            item["steps"]["afterReload"] = snapshot(page, limit=7000)
            item["steps"]["menuAfterReload"] = click_other_menu_and_snapshot(page)
    except Exception as exc:
        item["error"] = repr(exc)
        try:
            item["steps"]["finalSnapshot"] = snapshot(page, limit=7000)
        except Exception:
            pass
    return redact(item)


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "targets": {
            "waitingClosedDuringTest": TARGET_WAITING,
            "confirmedExisting": TARGET_CONFIRMED,
            "movedExisting": TARGET_MOVED,
        },
        "results": [],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            payload["results"].append(create_close_and_inspect(page))
            payload["results"].append(inspect_route(page, "left-open-close", TARGET_LEFT_OPEN, close=True))
            payload["results"].append(inspect_route(page, "broken_waiting_request_reference", TARGET_WAITING, close=False))
            payload["results"].append(inspect_route(page, "confirmed_request_existing", TARGET_CONFIRMED, close=False))
            payload["results"].append(inspect_route(page, "moved_request_existing", TARGET_MOVED, close=False))
        finally:
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
            page.close()
            browser.close()
    print(json.dumps({
        "generatedAt": payload["generatedAt"],
        "labels": [r["label"] for r in payload["results"]],
        "errors": {r["label"]: r.get("error") or r.get("steps", {}).get("closeAttempt", {}).get("error") for r in payload["results"]},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
