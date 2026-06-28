#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "15-purchase-cancel-after-inbound-created-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

SUPPLIER = "TEST_E2E_20260622_取引先_1905"
TENANT = "ユニクロ"
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"
LOCATION = "TEST_E2E_20260622_GU倉庫_ON_1905"

LONG_TOKEN_RE = re.compile(r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))")


def redact(value):
    if isinstance(value, str):
        return LONG_TOKEN_RE.sub("[REDACTED_LONG_VALUE]", value)
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    return value


def compact(text, limit=4500):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def snapshot(page, limit=5000):
    data = page.evaluate(
        """() => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const attr = (el, name) => el.getAttribute(name);
            const nodes = (selector, limit = 120) => Array.from(document.querySelectorAll(selector)).slice(0, limit);
            const controls = nodes('button, a, input, textarea, select, [role="button"], [role="menuitem"]', 260)
                .map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    role: attr(el, 'role'),
                    text: textOf(el),
                    href: attr(el, 'href'),
                    type: attr(el, 'type'),
                    placeholder: attr(el, 'placeholder'),
                    ariaLabel: attr(el, 'aria-label'),
                    ariaDisabled: attr(el, 'aria-disabled'),
                    disabled: !!el.disabled,
                    value: el.tagName.toLowerCase() === 'input' || el.tagName.toLowerCase() === 'select' ? el.value : undefined
                }))
                .filter((x) => x.text || x.href || x.ariaLabel || x.placeholder || x.value);
            const rows = nodes('tr', 80).map(textOf).filter(Boolean);
            return {
                url: location.href,
                h1: nodes('h1', 10).map(textOf).filter(Boolean),
                h2: nodes('h2', 20).map(textOf).filter(Boolean),
                controls,
                rows,
                body: document.body ? document.body.innerText : ''
            };
        }"""
    )
    data["body"] = compact(data.get("body", ""), limit)
    return redact(data)


def select_option_by_label_or_index(page, label_text, option_text, fallback_index):
    result = {"label": label_text, "option": option_text, "method": None, "selected": False}
    try:
        target = page.get_by_label(label_text, exact=True)
        if target.count():
            target.first.select_option(label=option_text, timeout=5000)
            result["method"] = "label"
            result["selected"] = True
            page.wait_for_timeout(500)
            return result
    except Exception as exc:
        result["labelError"] = repr(exc)

    try:
        selected = page.evaluate(
            """({optionText, fallbackIndex}) => {
                const selects = Array.from(document.querySelectorAll('select'));
                const select = selects[fallbackIndex];
                if (!select) return {ok: false, reason: 'select not found', count: selects.length};
                const option = Array.from(select.options).find((o) => (o.innerText || o.textContent || '').trim() === optionText);
                if (!option) return {
                    ok: false,
                    reason: 'option not found',
                    options: Array.from(select.options).map((o) => (o.innerText || o.textContent || '').trim()).slice(0, 30)
                };
                select.value = option.value;
                select.dispatchEvent(new Event('input', {bubbles: true}));
                select.dispatchEvent(new Event('change', {bubbles: true}));
                return {ok: true, value: option.value};
            }""",
            {"optionText": option_text, "fallbackIndex": fallback_index},
        )
        result["method"] = "dom-select-index"
        result["domResult"] = selected
        result["selected"] = bool(selected.get("ok"))
        page.wait_for_timeout(700)
    except Exception as exc:
        result["domError"] = repr(exc)
    return redact(result)


def first_enabled_button(page, names, scope=None):
    root = scope or page
    for name in names:
        locator = root.get_by_role("button", name=name, exact=True)
        if locator.count():
            for i in range(locator.count()):
                item = locator.nth(i)
                try:
                    if item.is_enabled():
                        return name, item
                except Exception:
                    pass
    return None, None


def choose_modal_row(page, open_button_name, row_text, search_text=None):
    result = {"openButton": open_button_name, "rowText": row_text, "searchText": search_text or row_text}
    page.get_by_role("button", name=open_button_name, exact=True).first.click()
    page.wait_for_timeout(900)
    dialog = page.locator('div[role="dialog"]').last
    result["dialogBefore"] = compact(dialog.inner_text(timeout=8000), 2200) if dialog.count() else "dialog not found"

    search_inputs = dialog.locator('input[placeholder*="検索"], input[placeholder*="SKU"], input[placeholder*="キーワード"]')
    if search_inputs.count():
        search_inputs.first.fill(search_text or row_text)
        search_inputs.first.press("Enter")
        page.wait_for_timeout(1700)

    try:
        page.wait_for_function(
            """(needle) => Array.from(document.querySelectorAll('div[role="dialog"] tr')).some((tr) => (tr.innerText || '').includes(needle))""",
            arg=row_text,
            timeout=15000,
        )
    except PlaywrightTimeoutError:
        pass

    selected = page.evaluate(
        """(needle) => {
            const dialogs = Array.from(document.querySelectorAll('div[role="dialog"]'));
            const dialog = dialogs[dialogs.length - 1];
            if (!dialog) return {found: false, reason: 'dialog not found'};
            const row = Array.from(dialog.querySelectorAll('tr')).find((tr) => (tr.innerText || '').includes(needle));
            if (!row) {
                return {
                    found: false,
                    rows: Array.from(dialog.querySelectorAll('tr')).slice(0, 20).map((tr) => (tr.innerText || '').replace(/\\s+/g, ' ').trim())
                };
            }
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox) checkbox.click();
            else row.click();
            return {found: true, row: (row.innerText || '').replace(/\\s+/g, ' ').trim()};
        }""",
        row_text,
    )
    result["selected"] = selected
    page.wait_for_timeout(700)
    if selected.get("found"):
        button = dialog.get_by_role("button", name="選択する", exact=True)
        for _ in range(30):
            if button.count() and button.first.is_enabled():
                break
            page.wait_for_timeout(250)
        button.first.click()
        page.wait_for_timeout(1200)
    result["after"] = snapshot(page, limit=3000)
    return redact(result)


def set_purchase_line_values(page):
    result = {"attempts": []}
    for label, value in [("単価", "100"), ("数量", "1"), ("税率", "10")]:
        try:
            locator = page.get_by_label(label, exact=True)
            count = locator.count()
            result["attempts"].append({"label": label, "count": count})
            if count:
                locator.last.fill(value)
        except Exception as exc:
            result["attempts"].append({"label": label, "error": repr(exc)})
    page.wait_for_timeout(700)
    result["after"] = snapshot(page, limit=3000)
    return redact(result)


def get_purchase_route(page):
    if "/admin/inventory_purchase_orders/" in page.url:
        return page.url.replace(BASE, "")
    match = re.search(r"/admin/inventory_purchase_orders/[^\\s\"']+", text_of(page))
    return match.group(0) if match else None


def order_purchase(page):
    result = {"before": snapshot(page, limit=4200)}
    page.get_by_role("button", name="発注する", exact=True).click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    result["dialog"] = compact(dialog.inner_text(timeout=5000), 2200)
    name, button = first_enabled_button(page, ["発注する", "実行する", "保存する"], scope=dialog)
    result["confirmButton"] = name
    if not button:
        result["error"] = "confirm button not found"
        return result
    button.click()
    wait_quiet(page, timeout=9000)
    result["after"] = snapshot(page, limit=5200)
    return redact(result)


def create_purchase_order(page):
    result = {"steps": {}, "route": None, "error": None}
    try:
        page.goto(BASE + "/admin/inventory_purchase_orders/create", wait_until="load", timeout=35000)
        wait_quiet(page)
        result["steps"]["initial"] = snapshot(page, limit=4200)
        result["steps"]["supplier"] = select_option_by_label_or_index(page, "取引先*", SUPPLIER, 0)
        result["steps"]["tenant"] = select_option_by_label_or_index(page, "テナント*", TENANT, 1)
        result["steps"]["variant"] = choose_modal_row(page, "参照", SKU, SKU)
        result["steps"]["lineValues"] = set_purchase_line_values(page)
        result["steps"]["beforeCreate"] = snapshot(page, limit=5200)
        page.get_by_role("button", name="作成する", exact=True).click()
        wait_quiet(page, timeout=12000)
        result["steps"]["afterCreate"] = snapshot(page, limit=6200)
        result["route"] = get_purchase_route(page)
        if not result["route"]:
            result["error"] = "purchase route not detected after create"
            return result
        result["steps"]["order"] = order_purchase(page)
        result["route"] = get_purchase_route(page) or result["route"]
    except Exception as exc:
        result["error"] = repr(exc)
        try:
            result["steps"]["finalSnapshot"] = snapshot(page, limit=6200)
        except Exception:
            pass
    return redact(result)


def open_other_menu(page):
    result = {"clicked": False, "items": [], "snapshot": None, "error": None}
    try:
        page.get_by_role("button", name="その他の操作", exact=True).first.click()
        page.wait_for_timeout(700)
        result["clicked"] = True
        result["items"] = page.evaluate(
            """() => Array.from(document.querySelectorAll('[role="menuitem"], button, a'))
                .map((el) => ({
                    text: (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim(),
                    tag: el.tagName.toLowerCase(),
                    role: el.getAttribute('role'),
                    href: el.getAttribute('href'),
                    disabled: !!el.disabled,
                    ariaDisabled: el.getAttribute('aria-disabled')
                }))
                .filter((x) => x.text.includes('キャンセル') || x.text.includes('発注') || x.text.includes('入荷'))"""
        )
        result["snapshot"] = snapshot(page, limit=6200)
    except Exception as exc:
        result["error"] = repr(exc)
    return redact(result)


def cancel_item_state(page):
    return page.evaluate(
        """() => {
            const candidates = Array.from(document.querySelectorAll('[role="menuitem"], button, a, [cmdk-item]'))
                .filter((el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim() === 'キャンセルする');
            return candidates.map((el) => ({
                tag: el.tagName.toLowerCase(),
                role: el.getAttribute('role'),
                disabled: !!el.disabled,
                ariaDisabled: el.getAttribute('aria-disabled'),
                className: el.className,
                text: (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim()
            }));
        }"""
    )


def try_cancel_purchase(page):
    result = {"attempted": False, "stateBefore": cancel_item_state(page), "dialog": None, "after": None, "error": None}
    enabled = any(not item.get("disabled") and item.get("ariaDisabled") != "true" for item in result["stateBefore"])
    result["enabled"] = enabled
    if not enabled:
        result["after"] = snapshot(page, limit=6000)
        return redact(result)
    try:
        item = page.get_by_text("キャンセルする", exact=True).last
        result["attempted"] = True
        item.click()
        page.wait_for_timeout(900)
        dialog = page.locator('div[role="dialog"]').last
        if dialog.count():
            result["dialog"] = compact(dialog.inner_text(timeout=5000), 2200)
            name, button = first_enabled_button(page, ["キャンセルする", "実行する", "削除する"], scope=dialog)
            result["confirmButton"] = name
            if button:
                button.click()
                wait_quiet(page, timeout=9000)
            else:
                result["error"] = "confirm button not found"
        else:
            result["dialog"] = "dialog not found"
        result["after"] = snapshot(page, limit=7000)
    except Exception as exc:
        result["error"] = repr(exc)
        result["after"] = snapshot(page, limit=7000)
    return redact(result)


def create_inbound_from_purchase(page, purchase_route):
    result = {"steps": {}, "inboundRoute": None, "error": None}
    try:
        page.goto(BASE + purchase_route, wait_until="load", timeout=35000)
        wait_quiet(page)
        result["steps"]["purchaseBeforeInbound"] = snapshot(page, limit=6200)
        link = page.get_by_text("入荷指示を作成する", exact=True)
        if not link.count():
            result["error"] = "入荷指示を作成する link not found"
            return result
        link.first.click()
        wait_quiet(page, timeout=9000)
        result["steps"]["inboundFormInitial"] = snapshot(page, limit=5200)
        result["steps"]["location"] = choose_modal_row(page, "参照", LOCATION, LOCATION)
        result["steps"]["inboundFormFilled"] = snapshot(page, limit=5200)
        page.get_by_role("button", name="保存する", exact=True).last.click()
        wait_quiet(page, timeout=12000)
        result["steps"]["afterSave"] = snapshot(page, limit=7000)
        if "/admin/inventory_inbound_orders/" in page.url:
            result["inboundRoute"] = page.url.replace(BASE, "")
    except Exception as exc:
        result["error"] = repr(exc)
        try:
            result["steps"]["finalSnapshot"] = snapshot(page, limit=7000)
        except Exception:
            pass
    return redact(result)


def inspect_inbound_list(page):
    page.goto(BASE + "/admin/inventory_inbound_orders", wait_until="load", timeout=35000)
    wait_quiet(page)
    return snapshot(page, limit=7000)


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "purpose": "Verify whether a purchase order can be cancelled after a purchase-linked inbound order is created but before receiving.",
        "inputs": {"supplier": SUPPLIER, "tenant": TENANT, "sku": SKU, "location": LOCATION},
        "errors": [],
        "steps": {},
    }
    OUT.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2))

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(22000)
        try:
            payload["steps"]["purchaseListBefore"] = snapshot_open(page, "/admin/inventory_purchase_orders", 7000)
            payload["steps"]["inboundListBefore"] = snapshot_open(page, "/admin/inventory_inbound_orders", 7000)
            payload["steps"]["createPurchase"] = create_purchase_order(page)
            purchase_route = payload["steps"]["createPurchase"].get("route")
            if not purchase_route:
                raise RuntimeError("created purchase route not found")

            payload["purchaseRoute"] = purchase_route
            payload["steps"]["createInbound"] = create_inbound_from_purchase(page, purchase_route)
            inbound_route = payload["steps"]["createInbound"].get("inboundRoute")
            if inbound_route:
                payload["inboundRoute"] = inbound_route

            page.goto(BASE + purchase_route, wait_until="load", timeout=35000)
            wait_quiet(page)
            payload["steps"]["purchaseAfterInboundReload"] = snapshot(page, limit=7000)
            payload["steps"]["menuAfterInboundBeforeReceive"] = open_other_menu(page)
            payload["steps"]["cancelAttemptBeforeReceive"] = try_cancel_purchase(page)
            page.goto(BASE + purchase_route, wait_until="load", timeout=35000)
            wait_quiet(page)
            payload["steps"]["purchaseAfterCancelReload"] = snapshot(page, limit=7000)
            if inbound_route:
                page.goto(BASE + inbound_route, wait_until="load", timeout=35000)
                wait_quiet(page)
                payload["steps"]["inboundAfterPurchaseCancel"] = snapshot(page, limit=7000)
            payload["steps"]["inboundListAfter"] = inspect_inbound_list(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            try:
                payload["steps"]["finalSnapshot"] = snapshot(page, limit=7000)
            except Exception:
                pass
        finally:
            OUT.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2))
            page.close()
            browser.close()

    print(json.dumps({
        "out": str(OUT),
        "errors": payload["errors"],
        "purchaseRoute": payload.get("purchaseRoute"),
        "inboundRoute": payload.get("inboundRoute"),
        "cancelEnabled": payload.get("steps", {}).get("cancelAttemptBeforeReceive", {}).get("enabled"),
        "cancelAttempted": payload.get("steps", {}).get("cancelAttemptBeforeReceive", {}).get("attempted"),
    }, ensure_ascii=False, indent=2))


def snapshot_open(page, route, limit=5000):
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    return snapshot(page, limit=limit)


if __name__ == "__main__":
    main()
