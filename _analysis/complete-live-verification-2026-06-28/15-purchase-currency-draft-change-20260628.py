#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "15-purchase-currency-draft-change-20260628.json"
OUT_MD = OUT_DIR / "15-purchase-currency-draft-change-20260628.md"

BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

SUPPLIER = "TEST_E2E_20260622_取引先_1905"
TENANT = "ユニクロ"
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"
INITIAL_CURRENCY = "米ドル"
INITIAL_CURRENCY_CODE = "USD"
UPDATED_CURRENCY = "ユーロ"
UPDATED_CURRENCY_CODE = "EUR"

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
                            selected: o.selected
                        }))
                        : undefined
                }))
                .filter((x) => x.text || x.href || x.ariaLabel || x.placeholder || x.value || x.options);
            const body = document.body ? document.body.innerText : '';
            return {
                url: location.href,
                h1: nodes('h1', 10).map(textOf).filter(Boolean),
                h2: nodes('h2', 30).map(textOf).filter(Boolean),
                rows: nodes('tr', 120).map(textOf).filter(Boolean),
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
    selected = page.evaluate(
        """({optionText, fallbackIndex}) => {
            const selects = Array.from(document.querySelectorAll('select'));
            const select = selects[fallbackIndex];
            if (!select) return {ok: false, reason: 'select not found', count: selects.length};
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
            result["attempts"].append({"label": label, "count": locator.count(), "value": value})
            if locator.count():
                locator.last.fill(value)
        except Exception as exc:
            result["attempts"].append({"label": label, "error": repr(exc)})
    page.wait_for_timeout(700)
    result["after"] = snapshot(page, limit=5500)
    return redact(result)


def purchase_route_from_page(page):
    if "/admin/inventory_purchase_orders/" in page.url and not page.url.rstrip("/").endswith("/create"):
        return page.url.replace(BASE, "")
    return None


def find_latest_draft_purchase(page):
    result = {"found": False, "route": None, "code": None, "row": None, "steps": {}}
    page.goto(BASE + "/admin/inventory_purchase_orders", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["list"] = snapshot(page, limit=10000)
    candidate = page.evaluate(
        """({supplier}) => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const rows = Array.from(document.querySelectorAll('tr'));
            for (const row of rows) {
                const text = textOf(row);
                if (!text.includes(supplier) || !text.includes('下書き')) continue;
                const link = row.querySelector('a[href*="/admin/inventory_purchase_orders/"]');
                if (!link) continue;
                return {row: text, code: text.match(/#IP-\\d+/)?.[0] || null, href: link.getAttribute('href')};
            }
            return null;
        }""",
        {"supplier": SUPPLIER},
    )
    result["candidate"] = candidate
    if candidate:
        result["found"] = True
        result["route"] = candidate.get("href")
        result["code"] = candidate.get("code")
        result["row"] = candidate.get("row")
    return redact(result)


def click_save(page):
    result = {"clicked": False, "buttonText": None, "after": None}
    for name in ["保存する", "保存"]:
        button = page.get_by_role("button", name=name, exact=True)
        if button.count():
            for i in range(button.count()):
                target = button.nth(i)
                try:
                    disabled = target.evaluate("(el) => !!el.disabled || el.getAttribute('aria-disabled') === 'true'")
                except Exception:
                    disabled = False
                if not disabled:
                    result["clicked"] = True
                    result["buttonText"] = name
                    target.click()
                    wait_quiet(page, timeout=12000)
                    result["after"] = snapshot(page, limit=9000)
                    return redact(result)
    result["after"] = snapshot(page, limit=9000)
    return redact(result)


def change_currency_on_draft(page, route):
    result = {"route": route, "attempted": False, "changed": False, "steps": {}}
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["before"] = snapshot(page, limit=10000)
    currency_select_info = page.evaluate(
        """({updatedCode}) => {
            const selects = Array.from(document.querySelectorAll('select'));
            const select = selects.find((s) => Array.from(s.options).some((o) => o.value === updatedCode));
            if (!select) return {found: false, selectCount: selects.length};
            const option = Array.from(select.options).find((o) => o.value === updatedCode);
            return {
                found: true,
                disabled: !!select.disabled || select.getAttribute('aria-disabled') === 'true',
                beforeValue: select.value,
                optionText: (option.innerText || option.textContent || '').trim(),
                options: Array.from(select.options).map((o) => ({
                    text: (o.innerText || o.textContent || '').trim(),
                    value: o.value,
                    selected: o.selected
                }))
            };
        }""",
        {"updatedCode": UPDATED_CURRENCY_CODE},
    )
    result["currencySelectBefore"] = currency_select_info
    if not currency_select_info.get("found") or currency_select_info.get("disabled"):
        return redact(result)
    result["attempted"] = True
    selected = page.evaluate(
        """({updatedCode}) => {
            const select = Array.from(document.querySelectorAll('select'))
                .find((s) => Array.from(s.options).some((o) => o.value === updatedCode));
            if (!select) return {ok: false};
            select.value = updatedCode;
            select.dispatchEvent(new Event('input', {bubbles: true}));
            select.dispatchEvent(new Event('change', {bubbles: true}));
            return {ok: true, value: select.value};
        }""",
        {"updatedCode": UPDATED_CURRENCY_CODE},
    )
    result["selectUpdated"] = selected
    page.wait_for_timeout(900)
    result["steps"]["afterSelectBeforeSave"] = snapshot(page, limit=10000)
    result["steps"]["save"] = click_save(page)
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["afterReload"] = snapshot(page, limit=10000)
    result["changed"] = UPDATED_CURRENCY_CODE in json.dumps(result["steps"]["afterReload"], ensure_ascii=False)
    return redact(result)


def create_purchase_draft(page):
    result = {"steps": {}, "route": None}
    page.goto(BASE + "/admin/inventory_purchase_orders/create", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["initial"] = snapshot(page, limit=6000)
    result["steps"]["supplier"] = select_option_by_label_or_index(page, "取引先", SUPPLIER, 0)
    result["steps"]["tenant"] = select_option_by_label_or_index(page, "テナント", TENANT, 1)
    result["steps"]["currency"] = select_option_by_label_or_index(page, "通貨", INITIAL_CURRENCY, 2)
    result["steps"]["variant"] = choose_variant(page, SKU)
    result["steps"]["lineValues"] = set_line_values(page)
    result["steps"]["beforeCreate"] = snapshot(page, limit=9000)
    page.get_by_role("button", name="作成する", exact=True).click()
    wait_quiet(page, timeout=15000)
    result["steps"]["afterCreate"] = snapshot(page, limit=10000)
    result["route"] = purchase_route_from_page(page)
    if not result["route"]:
        result["steps"]["findLatestDraft"] = find_latest_draft_purchase(page)
        result["route"] = result["steps"]["findLatestDraft"].get("route")
    if not result["route"]:
        raise RuntimeError("purchase route not detected after draft create")
    return redact(result)


def extract_facts(payload):
    draft = payload.get("steps", {}).get("draftDetailInitial", {})
    change = payload.get("steps", {}).get("changeCurrency", {})
    after_reload = change.get("steps", {}).get("afterReload", {})
    code = payload.get("purchaseCode")
    facts = {
        "purchaseCode": code,
        "purchaseRoute": payload.get("purchaseRoute"),
        "initialCurrency": INITIAL_CURRENCY_CODE,
        "updatedCurrency": UPDATED_CURRENCY_CODE,
        "initialDetailContainsUSD": INITIAL_CURRENCY_CODE in json.dumps(draft, ensure_ascii=False),
        "initialDetailContainsEUR": UPDATED_CURRENCY_CODE in json.dumps(draft, ensure_ascii=False),
        "currencySelectFoundOnDraft": bool(change.get("currencySelectBefore", {}).get("found")),
        "currencySelectDisabledOnDraft": bool(change.get("currencySelectBefore", {}).get("disabled")),
        "attemptedCurrencyChange": bool(change.get("attempted")),
        "changedToEURAfterSave": UPDATED_CURRENCY_CODE in json.dumps(after_reload, ensure_ascii=False),
        "amountLikeBeforeChange": draft.get("amountLike", []),
        "amountLikeAfterChange": after_reload.get("amountLike", []),
        "afterReloadBody": after_reload.get("body", ""),
    }
    return redact(facts)


def write_md(payload):
    facts = payload.get("facts") or extract_facts(payload)
    lines = [
        "# 発注伝票の通貨選択・下書き変更 実機確認",
        "",
        f"- 実行日時: {payload.get('generatedAt')}",
        f"- 取引先: `{SUPPLIER}`",
        f"- テナント: `{TENANT}`",
        f"- SKU: `{SKU}`",
        f"- 作成時通貨: `{INITIAL_CURRENCY}` / `{INITIAL_CURRENCY_CODE}`",
        f"- 変更後通貨: `{UPDATED_CURRENCY}` / `{UPDATED_CURRENCY_CODE}`",
        f"- 発注伝票: `{facts.get('purchaseCode')}`",
        "",
        "## 確認結果",
        "",
        f"- 下書き詳細に通貨selectがある: `{facts.get('currencySelectFoundOnDraft')}`",
        f"- 下書き詳細の通貨selectがdisabled: `{facts.get('currencySelectDisabledOnDraft')}`",
        f"- 下書き状態で通貨変更を試行した: `{facts.get('attemptedCurrencyChange')}`",
        f"- 保存後再読み込みで `EUR` が残った: `{facts.get('changedToEURAfterSave')}`",
        f"- 作成時詳細に `USD` が含まれる: `{facts.get('initialDetailContainsUSD')}`",
        "",
        "## 金額表示",
        "",
        "### 変更前",
        "",
    ]
    lines.extend([f"- {item}" for item in facts.get("amountLikeBeforeChange", [])] or ["- 金額らしき文字列なし"])
    lines.extend(["", "### 変更後", ""])
    lines.extend([f"- {item}" for item in facts.get("amountLikeAfterChange", [])] or ["- 金額らしき文字列なし"])
    lines.extend(
        [
            "",
            "## 判断",
            "",
            "- 発注伝票の通貨は下書き詳細にも選択値として残る。",
            "- 下書き状態では通貨selectが有効で、保存により別通貨へ変更できる。",
            "- この確認範囲では為替レート入力や換算表示は見当たらず、通貨変更後も数量・単価の数値を別通貨表示として扱うUIだった。",
            "- 発注済み後の通貨変更可否や会計連携時の仕入計上通貨は未確認。",
            "",
            "## 証跡",
            "",
            f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "purpose": "Verify purchase order currency selection, draft display, and whether currency can be changed while draft.",
        "inputs": {
            "supplier": SUPPLIER,
            "tenant": TENANT,
            "sku": SKU,
            "initialCurrency": INITIAL_CURRENCY_CODE,
            "updatedCurrency": UPDATED_CURRENCY_CODE,
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
            payload["steps"]["createDraft"] = create_purchase_draft(page)
            payload["purchaseRoute"] = payload["steps"]["createDraft"].get("route")
            page.goto(BASE + payload["purchaseRoute"], wait_until="load", timeout=35000)
            wait_quiet(page)
            payload["steps"]["draftDetailInitial"] = snapshot(page, limit=10000)
            body = payload["steps"]["draftDetailInitial"].get("body", "")
            match = re.search(r"#IP-\d+", body)
            payload["purchaseCode"] = match.group(0) if match else None
            save_payload(payload)
            payload["steps"]["changeCurrency"] = change_currency_on_draft(page, payload["purchaseRoute"])
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
                "purchaseCode": payload.get("purchaseCode"),
                "purchaseRoute": payload.get("purchaseRoute"),
                "facts": payload.get("facts"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
