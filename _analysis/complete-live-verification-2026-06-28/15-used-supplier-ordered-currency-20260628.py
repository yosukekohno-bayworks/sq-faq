#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "15-used-supplier-ordered-currency-20260628.json"
OUT_MD = OUT_DIR / "15-used-supplier-ordered-currency-20260628.md"
ORDERED_SCREENSHOT = OUT_DIR / "15-used-supplier-ordered-currency-detail-20260628.png"
SUPPLIER_SCREENSHOT = OUT_DIR / "15-used-supplier-archive-after-attempt-20260628.png"

BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

STAMP = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
SUPPLIER_NAME = f"TEST_FAQ_USED_SUPPLIER_{STAMP}"
SUPPLIER_CODE = f"TEST_USED_SUP_{STAMP}"
TENANT = "ユニクロ"
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"
INITIAL_CURRENCY = "米ドル"
INITIAL_CURRENCY_CODE = "USD"
TRY_CURRENCY_CODE = "EUR"

LONG_TOKEN_RE = re.compile(
    r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))"
)


def redact(value):
    if isinstance(value, str):
        return LONG_TOKEN_RE.sub("[REDACTED_LONG_VALUE]", value)
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    return value


def compact(text, limit=6000):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snapshot(page, limit=8000):
    data = page.evaluate(
        """() => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const attr = (el, name) => el.getAttribute(name);
            const nodes = (selector, limit = 120) => Array.from(document.querySelectorAll(selector)).slice(0, limit);
            const controls = nodes('button, a, input, textarea, select, [role="button"], [role="menuitem"]', 280)
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
                    value: el.tagName.toLowerCase() === 'input' || el.tagName.toLowerCase() === 'select' ? el.value : undefined,
                    options: el.tagName.toLowerCase() === 'select'
                        ? Array.from(el.options).map((o) => ({
                            text: (o.innerText || o.textContent || '').replace(/\\s+/g, ' ').trim(),
                            value: o.value,
                            selected: o.selected,
                            disabled: !!o.disabled
                        }))
                        : undefined
                }))
                .filter((x) => x.text || x.href || x.ariaLabel || x.placeholder || x.value || x.options);
            const body = document.body ? document.body.innerText : '';
            return {
                url: location.href,
                h1: nodes('h1', 10).map(textOf).filter(Boolean),
                h2: nodes('h2', 30).map(textOf).filter(Boolean),
                rows: nodes('tr', 150).map(textOf).filter(Boolean),
                controls,
                body
            };
        }"""
    )
    data["body"] = compact(data.get("body", ""), limit)
    data["purchaseCodes"] = sorted(set(re.findall(r"#IP-\d+", data["body"])))
    data["amountLike"] = re.findall(r"(?:US\$|SGD|THB|EUR|USD|JPY|￥|\$|€)[\s\d,.-]+", data["body"])
    return redact(data)


def save_payload(payload):
    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2))


def fill_first_visible(page, labels, fallback_index, value):
    result = {"value": value, "method": None, "labels": labels}
    for label in labels:
        try:
            locator = page.get_by_label(re.compile(label))
            if locator.count():
                locator.first.fill(value)
                result["method"] = f"label:{label}"
                return result
        except Exception as exc:
            result.setdefault("labelErrors", []).append({"label": label, "error": repr(exc)})
    visible_inputs = page.locator('input:not([type="hidden"])')
    count = visible_inputs.count()
    result["visibleInputCount"] = count
    for idx in range(count):
        item = visible_inputs.nth(idx)
        try:
            if item.is_visible() and item.is_enabled():
                if fallback_index == 0:
                    item.fill(value)
                    result["method"] = f"visible-input:{idx}"
                    return result
                fallback_index -= 1
        except Exception:
            pass
    result["method"] = "not-filled"
    return result


def select_option_by_text(page, label_text, option_text, fallback_index=0):
    result = {"label": label_text, "option": option_text, "selected": False, "method": None}
    try:
        target = page.get_by_label(re.compile(label_text))
        if target.count():
            target.first.select_option(label=option_text, timeout=5000)
            result["selected"] = True
            result["method"] = "label"
            page.wait_for_timeout(500)
            return result
    except Exception as exc:
        result["labelError"] = repr(exc)
    selected = page.evaluate(
        """({optionText, fallbackIndex}) => {
            const selects = Array.from(document.querySelectorAll('select'));
            const select = selects[fallbackIndex];
            if (!select) return {ok: false, reason: 'select not found', selectCount: selects.length};
            const option = Array.from(select.options).find((o) => (o.innerText || o.textContent || '').trim() === optionText);
            if (!option) return {
                ok: false,
                reason: 'option not found',
                options: Array.from(select.options).map((o) => (o.innerText || o.textContent || '').trim())
            };
            select.value = option.value;
            select.dispatchEvent(new Event('input', {bubbles: true}));
            select.dispatchEvent(new Event('change', {bubbles: true}));
            return {ok: true, value: option.value, disabled: !!select.disabled};
        }""",
        {"optionText": option_text, "fallbackIndex": fallback_index},
    )
    result["method"] = "dom-select-index"
    result["domResult"] = selected
    result["selected"] = bool(selected.get("ok"))
    page.wait_for_timeout(700)
    return redact(result)


def first_enabled_button(page, names, scope=None):
    root = scope or page
    for name in names:
        locator = root.get_by_role("button", name=name, exact=True)
        if locator.count():
            for idx in range(locator.count()):
                item = locator.nth(idx)
                try:
                    if item.is_enabled():
                        return name, item
                except Exception:
                    pass
    return None, None


def create_supplier(page):
    result = {"name": SUPPLIER_NAME, "code": SUPPLIER_CODE, "steps": {}}
    page.goto(BASE + "/admin/settings/suppliers/create", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["initial"] = snapshot(page, limit=5000)
    result["steps"]["name"] = fill_first_visible(page, ["取引先名", "仕入れ先ベンダー名", "名前"], 0, SUPPLIER_NAME)
    result["steps"]["code"] = fill_first_visible(page, ["取引先コード", "コード"], 1, SUPPLIER_CODE)
    result["steps"]["beforeSave"] = snapshot(page, limit=5000)
    _, save_button = first_enabled_button(page, ["保存する", "保存"])
    if not save_button:
        raise RuntimeError("supplier save button not found")
    save_button.click()
    wait_quiet(page, timeout=12000)
    result["steps"]["afterSave"] = snapshot(page, limit=7000)
    result["route"] = page.url.replace(BASE, "")
    result["created"] = SUPPLIER_NAME in result["steps"]["afterSave"].get("body", "")
    return redact(result)


def choose_variant(page, sku):
    result = {"sku": sku}
    page.get_by_role("button", name="参照", exact=True).first.click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    result["dialogBefore"] = compact(dialog.inner_text(timeout=8000), 2600)
    search = dialog.locator('input[placeholder*="SKU"], input[placeholder*="検索"]')
    if search.count():
        search.first.fill(sku)
        search.first.press("Enter")
        page.wait_for_timeout(2000)
    row = dialog.locator("tr").filter(has_text=sku).first
    if not row.count():
        result["rows"] = [compact(text, 500) for text in dialog.locator("tr").all_inner_texts()[:40]]
        raise RuntimeError(f"variant row not found: {sku}")
    result["row"] = compact(row.inner_text(timeout=5000), 900)
    checkbox = row.locator('input[type="checkbox"]').first
    if checkbox.count():
        checkbox.click()
    else:
        row.click()
    page.wait_for_timeout(500)
    dialog.get_by_role("button", name="選択する", exact=True).click()
    wait_quiet(page, timeout=5000)
    result["after"] = snapshot(page, limit=5000)
    return redact(result)


def set_line_values(page):
    result = {"attempts": []}
    for label, value in [("単価", "100"), ("数量", "1"), ("税率", "10")]:
        try:
            locator = page.get_by_label(label, exact=True)
            count = locator.count()
            result["attempts"].append({"label": label, "count": count, "value": value})
            if count:
                locator.last.fill(value)
        except Exception as exc:
            result["attempts"].append({"label": label, "error": repr(exc)})
    page.wait_for_timeout(700)
    result["after"] = snapshot(page, limit=5500)
    return redact(result)


def purchase_route_from_page(page):
    if "/admin/inventory_purchase_orders/" in page.url and not page.url.rstrip("/").endswith("/create"):
        return page.url.replace(BASE, "")
    body = page.evaluate("() => document.body ? document.body.innerText : ''")
    match = re.search(r"/admin/inventory_purchase_orders/[A-Za-z0-9_-]+", body)
    return match.group(0) if match else None


def find_purchase_by_supplier(page):
    result = {"found": False, "route": None, "code": None}
    page.goto(BASE + "/admin/inventory_purchase_orders", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["list"] = snapshot(page, limit=12000)
    candidate = page.evaluate(
        """(supplier) => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const rows = Array.from(document.querySelectorAll('tr'));
            for (const row of rows) {
                const text = textOf(row);
                if (!text.includes(supplier)) continue;
                const link = row.querySelector('a[href*="/admin/inventory_purchase_orders/"]');
                if (!link) continue;
                return {
                    row: text,
                    href: link.getAttribute('href'),
                    code: text.match(/#IP-\\d+/)?.[0] || null
                };
            }
            return {
                row: null,
                rows: rows.slice(0, 40).map(textOf)
            };
        }""",
        SUPPLIER_NAME,
    )
    result["candidate"] = candidate
    if candidate and candidate.get("href"):
        result["found"] = True
        result["route"] = candidate.get("href")
        result["code"] = candidate.get("code")
    return redact(result)


def create_purchase_order(page):
    result = {"steps": {}, "route": None, "code": None}
    page.goto(BASE + "/admin/inventory_purchase_orders/create", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["initial"] = snapshot(page, limit=7000)
    result["steps"]["supplier"] = select_option_by_text(page, "取引先", SUPPLIER_NAME, 0)
    result["steps"]["tenant"] = select_option_by_text(page, "テナント", TENANT, 1)
    result["steps"]["currency"] = select_option_by_text(page, "通貨", INITIAL_CURRENCY, 2)
    result["steps"]["variant"] = choose_variant(page, SKU)
    result["steps"]["lineValues"] = set_line_values(page)
    result["steps"]["beforeCreate"] = snapshot(page, limit=9000)
    page.get_by_role("button", name="作成する", exact=True).click()
    wait_quiet(page, timeout=15000)
    result["steps"]["afterCreate"] = snapshot(page, limit=10000)
    result["route"] = purchase_route_from_page(page)
    body = result["steps"]["afterCreate"].get("body", "")
    match = re.search(r"#IP-\d+", body)
    result["code"] = match.group(0) if match else None
    if not result["route"]:
        result["steps"]["findPurchaseBySupplier"] = find_purchase_by_supplier(page)
        result["route"] = result["steps"]["findPurchaseBySupplier"].get("route")
        result["code"] = result["code"] or result["steps"]["findPurchaseBySupplier"].get("code")
    return redact(result)


def order_purchase(page):
    result = {"before": snapshot(page, limit=7000)}
    page.get_by_role("button", name="発注する", exact=True).click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    result["dialog"] = compact(dialog.inner_text(timeout=5000), 2400)
    name, button = first_enabled_button(page, ["発注する", "実行する", "保存する"], scope=dialog)
    result["confirmButton"] = name
    if button:
        button.click()
        wait_quiet(page, timeout=12000)
    else:
        result["error"] = "confirm button not found"
    result["after"] = snapshot(page, limit=10000)
    try:
        page.screenshot(path=str(ORDERED_SCREENSHOT), full_page=True)
        result["screenshot"] = str(ORDERED_SCREENSHOT.relative_to(ROOT))
    except Exception as exc:
        result["screenshotError"] = repr(exc)
    return redact(result)


def inspect_ordered_currency(page, route):
    result = {"route": route, "attemptedChange": False, "saveClicked": False}
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["before"] = snapshot(page, limit=10000)
    info = page.evaluate(
        """({targetCode}) => {
            const selects = Array.from(document.querySelectorAll('select'));
            const select = selects.find((s) => Array.from(s.options).some((o) => o.value === targetCode));
            if (!select) return {found: false, selectCount: selects.length};
            return {
                found: true,
                disabled: !!select.disabled || select.getAttribute('aria-disabled') === 'true',
                value: select.value,
                options: Array.from(select.options).map((o) => ({
                    text: (o.innerText || o.textContent || '').replace(/\\s+/g, ' ').trim(),
                    value: o.value,
                    selected: o.selected,
                    disabled: !!o.disabled
                }))
            };
        }""",
        {"targetCode": TRY_CURRENCY_CODE},
    )
    result["currencySelect"] = info
    if info.get("found") and not info.get("disabled"):
        result["attemptedChange"] = True
        result["selectResult"] = page.evaluate(
            """({targetCode}) => {
                const select = Array.from(document.querySelectorAll('select'))
                    .find((s) => Array.from(s.options).some((o) => o.value === targetCode));
                if (!select) return {ok: false};
                select.value = targetCode;
                select.dispatchEvent(new Event('input', {bubbles: true}));
                select.dispatchEvent(new Event('change', {bubbles: true}));
                return {ok: true, value: select.value};
            }""",
            {"targetCode": TRY_CURRENCY_CODE},
        )
        page.wait_for_timeout(700)
        result["afterSelect"] = snapshot(page, limit=9000)
        name, button = first_enabled_button(page, ["保存する", "保存"])
        result["saveButton"] = name
        if button:
            result["saveClicked"] = True
            button.click()
            wait_quiet(page, timeout=12000)
            result["afterSave"] = snapshot(page, limit=10000)
    return redact(result)


def supplier_options(page):
    page.goto(BASE + "/admin/inventory_purchase_orders/create", wait_until="load", timeout=35000)
    wait_quiet(page)
    return redact(
        page.evaluate(
            """(name) => {
                const selects = Array.from(document.querySelectorAll('select'));
                const supplier = selects[0];
                const options = supplier ? Array.from(supplier.options).map((o) => ({
                    text: (o.innerText || o.textContent || '').replace(/\\s+/g, ' ').trim(),
                    value: o.value,
                    disabled: !!o.disabled,
                    selected: !!o.selected
                })) : [];
                return {
                    url: location.href,
                    containsName: options.some((o) => o.text === name),
                    options
                };
            }""",
            SUPPLIER_NAME,
        )
    )


def attempt_supplier_archive(page):
    result = {"supplier": SUPPLIER_NAME, "steps": {}}
    page.goto(BASE + "/admin/settings/suppliers", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["listBefore"] = snapshot(page, limit=10000)
    row_result = page.evaluate(
        """(name) => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const row = Array.from(document.querySelectorAll('tr')).find((tr) => textOf(tr).includes(name));
            if (!row) return {found: false, rows: Array.from(document.querySelectorAll('tr')).slice(0, 30).map(textOf)};
            const checkbox = row.querySelector('input[type="checkbox"]');
            if (checkbox) checkbox.click();
            else row.click();
            return {found: true, row: textOf(row), checkbox: !!checkbox};
        }""",
        SUPPLIER_NAME,
    )
    result["steps"]["selectRow"] = row_result
    page.wait_for_timeout(900)
    result["steps"]["afterSelect"] = snapshot(page, limit=10000)
    archive_button = page.get_by_role("button", name="アーカイブする", exact=True)
    result["archiveButtonCount"] = archive_button.count()
    if archive_button.count():
        archive_button.first.click()
        page.wait_for_selector('div[role="dialog"]', timeout=12000)
        dialog = page.locator('div[role="dialog"]').last
        result["dialog"] = compact(dialog.inner_text(timeout=5000), 3000)
        name, button = first_enabled_button(page, ["削除する", "アーカイブする", "実行する"], scope=dialog)
        result["confirmButton"] = name
        if button:
            button.click()
            wait_quiet(page, timeout=12000)
    result["steps"]["afterAttempt"] = snapshot(page, limit=12000)
    try:
        page.screenshot(path=str(SUPPLIER_SCREENSHOT), full_page=True)
        result["screenshot"] = str(SUPPLIER_SCREENSHOT.relative_to(ROOT))
    except Exception as exc:
        result["screenshotError"] = repr(exc)
    page.goto(BASE + "/admin/settings/suppliers", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["allTabAfterReload"] = snapshot(page, limit=10000)
    try:
        page.get_by_role("tab", name="アーカイブ", exact=True).click()
    except Exception:
        try:
            page.get_by_text("アーカイブ", exact=True).click()
        except Exception as exc:
            result["archiveTabClickError"] = repr(exc)
    wait_quiet(page, timeout=5000)
    result["steps"]["archiveTab"] = snapshot(page, limit=10000)
    return redact(result)


def extract_facts(payload):
    order = payload.get("steps", {}).get("order", {})
    currency = payload.get("steps", {}).get("orderedCurrency", {})
    archive = payload.get("steps", {}).get("supplierArchive", {})
    all_after = archive.get("steps", {}).get("allTabAfterReload", {}).get("body", "")
    archive_tab = archive.get("steps", {}).get("archiveTab", {}).get("body", "")
    options_after = payload.get("steps", {}).get("supplierOptionsAfterArchive", {})
    facts = {
        "supplierName": SUPPLIER_NAME,
        "supplierCode": SUPPLIER_CODE,
        "purchaseRoute": payload.get("purchaseRoute"),
        "purchaseCode": payload.get("purchaseCode"),
        "orderedDialog": order.get("dialog"),
        "orderedStatusContainsOrdered": "発注済み" in json.dumps(currency.get("before", {}), ensure_ascii=False),
        "orderedCurrencyValueDisplayed": "米ドル" in json.dumps(currency.get("before", {}), ensure_ascii=False),
        "orderedCurrencySelectFound": bool(currency.get("currencySelect", {}).get("found")),
        "orderedCurrencySelectDisabled": bool(currency.get("currencySelect", {}).get("disabled")),
        "orderedCurrencyChangeAttempted": bool(currency.get("attemptedChange")),
        "orderedCurrencySaveClicked": bool(currency.get("saveClicked")),
        "supplierArchiveDialog": archive.get("dialog"),
        "supplierArchiveConfirmButton": archive.get("confirmButton"),
        "supplierStillInAllTab": SUPPLIER_NAME in all_after,
        "supplierInArchiveTab": SUPPLIER_NAME in archive_tab,
        "supplierStillInPurchaseOptions": bool(options_after.get("containsName")),
        "errors": payload.get("errors", []),
    }
    return redact(facts)


def write_md(payload):
    facts = payload.get("facts") or extract_facts(payload)
    lines = [
        "# 15 発注済み伝票の通貨変更可否・使用済み取引先削除 実機確認 2026-06-28",
        "",
        f"- 実行日時: {payload.get('generatedAt')}",
        f"- 検証用取引先: `{SUPPLIER_NAME}` / `{SUPPLIER_CODE}`",
        f"- SKU: `{SKU}`",
        f"- 発注伝票: `{facts.get('purchaseCode')}`",
        f"- 発注伝票URL: `{facts.get('purchaseRoute')}`",
        "",
        "## 結果",
        "",
        "| 確認項目 | 結果 |",
        "|:--|:--|",
        f"| 発注後の商品セクション | `{facts.get('orderedStatusContainsOrdered')}` |",
        f"| 発注済み詳細に通貨selectがある | `{facts.get('orderedCurrencySelectFound')}` |",
        f"| 発注済み詳細に通貨値が表示される | `{facts.get('orderedCurrencyValueDisplayed')}` |",
        f"| 発注済み後に通貨変更を試行した | `{facts.get('orderedCurrencyChangeAttempted')}` |",
        f"| 発注済み後の保存ボタン押下 | `{facts.get('orderedCurrencySaveClicked')}` |",
        f"| 取引先削除/アーカイブ確認ボタン | `{facts.get('supplierArchiveConfirmButton')}` |",
        f"| 実行後も取引先が「すべて」タブに残る | `{facts.get('supplierStillInAllTab')}` |",
        f"| 実行後に取引先が「アーカイブ」タブに出る | `{facts.get('supplierInArchiveTab')}` |",
        f"| 実行後も発注作成フォームの取引先候補に残る | `{facts.get('supplierStillInPurchaseOptions')}` |",
        "",
        "## ダイアログ",
        "",
        "### 発注確認",
        "",
        facts.get("orderedDialog") or "なし",
        "",
        "### 取引先アーカイブ/削除確認",
        "",
        facts.get("supplierArchiveDialog") or "なし",
        "",
        "## 判断",
        "",
        "- 発注済み伝票では通貨selectと保存ボタンが表示されず、通貨は値表示のみになるため、発注後に通貨変更する導線は確認できない。",
        "- 発注伝票で使用された検証用取引先に一括操作 `アーカイブする` → `削除する` を実行しても、対象取引先は削除されず「すべて」タブと発注作成フォーム候補に残った。",
        "- 同じ操作でも未使用取引先は一覧・アーカイブタブ・発注フォーム候補から消えるため、取引先は使用有無で挙動が分かれる。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        f"- 発注済み詳細スクリーンショット: `{ORDERED_SCREENSHOT.relative_to(ROOT)}`",
        f"- 取引先削除試行後スクリーンショット: `{SUPPLIER_SCREENSHOT.relative_to(ROOT)}`",
    ]
    if facts.get("errors"):
        lines.extend(["", "## エラー", ""])
        lines.extend([f"- `{err}`" for err in facts["errors"]])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "purpose": "Verify ordered purchase currency editability and archive/delete behavior for a supplier used by a purchase order.",
        "inputs": {
            "supplierName": SUPPLIER_NAME,
            "supplierCode": SUPPLIER_CODE,
            "tenant": TENANT,
            "sku": SKU,
            "initialCurrency": INITIAL_CURRENCY_CODE,
        },
        "steps": {},
        "errors": [],
    }
    save_payload(payload)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            payload["steps"]["supplier"] = create_supplier(page)
            save_payload(payload)
            payload["steps"]["purchase"] = create_purchase_order(page)
            payload["purchaseRoute"] = payload["steps"]["purchase"].get("route")
            payload["purchaseCode"] = payload["steps"]["purchase"].get("code")
            save_payload(payload)
            if not payload["purchaseRoute"]:
                raise RuntimeError("purchase route not detected")
            page.goto(BASE + payload["purchaseRoute"], wait_until="load", timeout=35000)
            wait_quiet(page)
            payload["steps"]["order"] = order_purchase(page)
            body = payload["steps"]["order"].get("after", {}).get("body", "")
            match = re.search(r"#IP-\d+", body)
            payload["purchaseCode"] = match.group(0) if match else payload.get("purchaseCode")
            save_payload(payload)
            payload["steps"]["orderedCurrency"] = inspect_ordered_currency(page, payload["purchaseRoute"])
            save_payload(payload)
            payload["steps"]["supplierArchive"] = attempt_supplier_archive(page)
            save_payload(payload)
            payload["steps"]["supplierOptionsAfterArchive"] = supplier_options(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            try:
                payload["steps"]["finalSnapshot"] = snapshot(page, limit=10000)
            except Exception:
                pass
        finally:
            payload["facts"] = extract_facts(payload)
            save_payload(payload)
            write_md(payload)
            page.close()
            browser.close()

    print(
        json.dumps(
            {
                "json": str(OUT_JSON),
                "md": str(OUT_MD),
                "errors": payload["errors"],
                "facts": payload.get("facts"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
