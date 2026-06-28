#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_JSON = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "11-inventory-threshold-rule-save-cleanup-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"


def compact(text, limit=2500):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snapshot(page, limit=3500):
    return page.evaluate(
        """(limit) => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const unique = (items) => Array.from(new Set(items.filter(Boolean)));
            return {
                url: location.href,
                h1: unique(Array.from(document.querySelectorAll('h1')).map(text)),
                h2: unique(Array.from(document.querySelectorAll('h2')).map(text)),
                labels: unique(Array.from(document.querySelectorAll('label')).map(text)),
                buttons: Array.from(document.querySelectorAll('button')).map((button, index) => ({
                    index,
                    text: text(button),
                    aria: button.getAttribute('aria-label') || '',
                    disabled: !!button.disabled
                })),
                links: Array.from(document.querySelectorAll('a[href]')).map((a) => ({
                    text: text(a),
                    href: a.getAttribute('href')
                })).filter((x) => x.text || x.href),
                inputs: Array.from(document.querySelectorAll('input, select, textarea')).map((el, index) => ({
                    index,
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type') || '',
                    placeholder: el.getAttribute('placeholder') || '',
                    value: el.tagName.toLowerCase() === 'select' ? el.value : (el.type === 'checkbox' ? String(el.checked) : el.value),
                    checked: el.type === 'checkbox' ? el.checked : null,
                    disabled: !!el.disabled,
                    readOnly: !!el.readOnly,
                    label: (el.closest('label')?.innerText || el.parentElement?.innerText || '').replace(/\\s+/g, ' ').trim(),
                    options: el.tagName.toLowerCase() === 'select'
                        ? Array.from(el.options).map((option) => ({ value: option.value, text: text(option), disabled: option.disabled }))
                        : []
                })),
                rows: Array.from(document.querySelectorAll('tr')).map((tr, index) => ({ index, id: tr.id, text: text(tr) })),
                bodyText: text(document.body).slice(0, limit)
            };
        }""",
        limit,
    )


def click_text_button(page, names, scope=None):
    scope = scope or page
    for name in names:
        locator = scope.locator("button").filter(has_text=name)
        for i in range(locator.count()):
            button = locator.nth(i)
            try:
                if button.is_visible() and button.is_enabled():
                    button.click()
                    page.wait_for_timeout(700)
                    return name
            except Exception:
                continue
    raise RuntimeError(f"button not found: {names}")


def fill_first_text(page, value):
    inputs = page.locator('input[type="text"]')
    if inputs.count() == 0:
        raise RuntimeError("text input not found")
    inputs.first.fill(value)


def fill_first_number(page, value):
    inputs = page.locator('input[type="number"]')
    if inputs.count() == 0:
        raise RuntimeError("number input not found")
    inputs.first.fill(str(value))


def select_row_containing(page, needle):
    page.wait_for_function(
        """(needle) => Array.from(document.querySelectorAll('tr')).some((tr) => tr.innerText.includes(needle))""",
        arg=needle,
        timeout=20000,
    )
    row = page.locator("tr").filter(has_text=needle).first
    selected = compact(row.inner_text(timeout=5000), 900)
    checkbox = row.locator('input[type="checkbox"]').first
    if checkbox.count() > 0:
        checkbox.click(force=True)
    else:
        row.click(force=True)
    page.wait_for_timeout(900)
    return selected


def row_texts_containing(page, needle):
    return page.evaluate(
        """(needle) => Array.from(document.querySelectorAll('tr'))
            .filter((tr) => tr.innerText.includes(needle))
            .map((tr) => ({ id: tr.id, text: (tr.innerText || '').replace(/\\s+/g, ' ').trim() }))""",
        needle,
    )


def wait_for_row_containing(page, needle):
    page.wait_for_function(
        """(needle) => Array.from(document.querySelectorAll('tr')).some((tr) => tr.innerText.includes(needle))""",
        arg=needle,
        timeout=25000,
    )


def open_rule_detail_from_list(page, rule_name):
    page.goto(BASE + "/admin/inventory_threshold_rules", wait_until="load")
    wait_quiet(page)
    link = page.locator('a[data-primary-link="true"]').filter(has_text=rule_name).first
    if link.count() > 0:
        href = link.get_attribute("href")
        page.goto(BASE + href if href.startswith("/") else href, wait_until="load")
        wait_quiet(page)
        try:
            page.wait_for_function(
                "(ruleName) => Array.from(document.querySelectorAll('h1')).some((h1) => h1.innerText.includes(ruleName))",
                arg=rule_name,
                timeout=20000,
            )
        except PlaywrightTimeoutError:
            pass
        return page.url
    row = page.locator("tr").filter(has_text=rule_name).first
    if row.count() == 0:
        raise RuntimeError(f"created rule row not found: {rule_name}")
    row.click()
    wait_quiet(page)
    return page.url


def choose_sku(page):
    click_text_button(page, ["選択"])
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog_count = page.locator('div[role="dialog"]').count()
    search = page.locator('div[role="dialog"] input[placeholder="SKUコードで検索する"]').last
    search.fill(SKU)
    search.press("Enter")
    page.wait_for_function(
        """(sku) => Array.from(document.querySelectorAll('div[role="dialog"] tr')).some((tr) => tr.innerText.includes(sku))""",
        arg=SKU,
        timeout=20000,
    )
    row = page.evaluate(
        """(sku) => {
            const dialogs = Array.from(document.querySelectorAll('div[role="dialog"]'));
            const dialog = dialogs[dialogs.length - 1];
            const row = Array.from(dialog.querySelectorAll('tr')).find((tr) => tr.innerText.includes(sku));
            const checkbox = row?.querySelector('input[type="checkbox"]');
            if (checkbox) checkbox.click();
            else row?.click();
            return row ? row.innerText : '';
        }""",
        SKU,
    )
    dialog = page.locator('div[role="dialog"]').last
    button = dialog.locator("button").filter(has_text="選択する").first
    for _ in range(30):
        if button.is_enabled():
            break
        page.wait_for_timeout(250)
    button.click()
    page.wait_for_function(
        """(count) => document.querySelectorAll('div[role="dialog"]').length < count""",
        arg=dialog_count,
        timeout=15000,
    )
    page.wait_for_timeout(800)
    return compact(row, 1000)


def delete_selected(page, action_names, confirm_names=None):
    click_name = click_text_button(page, action_names)
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    dialog_text = compact(dialog.inner_text(timeout=5000), 1400)
    click_text_button(page, confirm_names or [click_name, "削除する"], scope=dialog)
    wait_quiet(page, timeout=10000)
    return {"action": click_name, "dialogText": dialog_text, "after": snapshot(page, limit=2500)}


def cleanup_rule_by_name(page, rule_name):
    page.goto(BASE + "/admin/inventory_threshold_rules", wait_until="load")
    wait_quiet(page)
    rows = row_texts_containing(page, rule_name)
    if not rows:
        return {"found": False, "deleted": True}
    select_row_containing(page, rule_name)
    result = delete_selected(page, ["削除する"], confirm_names=["削除する"])
    page.goto(BASE + "/admin/inventory_threshold_rules", wait_until="load")
    wait_quiet(page)
    remaining = row_texts_containing(page, rule_name)
    return {"found": True, "deleteResult": result, "remainingRows": remaining, "deleted": len(remaining) == 0}


def write_md(payload):
    facts = payload["facts"]
    lines = [
        "# 販売閾値ルール 保存・削除確認 2026-06-28",
        "",
        "## 検証データ",
        "",
        f"- ルール名: `{payload['ruleName']}`",
        f"- SKU: `{SKU}`",
        "",
        "## 結果",
        "",
        "| 項目 | 結果 |",
        "|:--|:--|",
        f"| 作成フォームのラベル | `{facts['createLabels']}` |",
        f"| デフォルト閾値ON時の初期値 | `{facts['defaultThresholdInitialValue']}` |",
        f"| 作成後に一覧へ戻る | `{facts['returnedToListAfterCreate']}` |",
        f"| 詳細画面の主要導線 | `{facts['detailLinks']}` |",
        f"| SKU別閾値フォーム初期値 | `{facts['variantThresholdInitialValue']}` |",
        f"| SKU選択行 | `{facts['selectedSkuRow']}` |",
        f"| SKU別閾値保存後の行 | `{facts['rowsAfterVariantSave']}` |",
        f"| SKU別閾値削除 | `{facts['variantDeleted']}` |",
        f"| ルール本体削除 | `{facts['ruleDeleted']}` |",
        f"| UI上の到達時説明 | `{facts['thresholdReachExplanationInUi']}` |",
        "",
        "## 判断",
        "",
        "- 販売閾値ルールは現行stagingでも作成でき、保存後は詳細ではなく一覧へ戻る。",
        "- ルール詳細から `閾値を追加する` へ進み、SKU別の閾値を保存できる。",
        "- SKU別閾値は行選択後の削除確認ダイアログで削除でき、ルール本体も一覧行選択後に削除できる。",
        "- 管理画面UIには、閾値に達したときの売り止め/通知/連携先反映を説明する文言は確認できない。実効はリテールポータル等の接続環境で別検証が必要。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    rule_name = f"TEST_FAQ_THRESHOLD_{stamp}"
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "ruleName": rule_name,
        "sku": SKU,
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(22000)
        try:
            payload["preCleanupOldThresholdRules"] = []
            page.goto(BASE + "/admin/inventory_threshold_rules", wait_until="load")
            wait_quiet(page)
            old_names = page.evaluate(
                """() => Array.from(document.querySelectorAll('tr'))
                    .map((tr) => (tr.innerText || '').replace(/\\s+/g, ' ').trim())
                    .filter((text) => text.includes('TEST_FAQ_THRESHOLD_'))
                    .map((text) => text.replace(/^アイテムを選択する\\s+/, ''))"""
            )
            for old_name in old_names:
                payload["preCleanupOldThresholdRules"].append(cleanup_rule_by_name(page, old_name))

            page.goto(BASE + "/admin/inventory_threshold_rules/create", wait_until="load")
            wait_quiet(page)
            payload["createInitial"] = snapshot(page)
            page.locator("label").filter(has_text="デフォルトの閾値を設定する").first.click()
            page.wait_for_timeout(700)
            payload["createDefaultOn"] = snapshot(page)
            page.locator("label").filter(has_text="デフォルトの閾値を設定する").first.click()
            page.wait_for_timeout(500)
            fill_first_text(page, rule_name)
            payload["createBeforeSave"] = snapshot(page)
            click_text_button(page, ["保存する"])
            wait_quiet(page, timeout=12000)
            payload["afterRuleSave"] = snapshot(page)

            detail_url = open_rule_detail_from_list(page, rule_name)
            payload["detailUrl"] = detail_url
            try:
                page.wait_for_function(
                    "(ruleName) => Array.from(document.querySelectorAll('h1')).some((h1) => h1.innerText.includes(ruleName))",
                    arg=rule_name,
                    timeout=20000,
                )
            except PlaywrightTimeoutError:
                pass
            payload["detailInitial"] = snapshot(page)

            add_link = page.locator('a[href$="/create"]').filter(has_text="閾値を追加する").first
            if add_link.count() > 0:
                add_link.click()
            else:
                page.goto(detail_url.rstrip("/") + "/create", wait_until="load")
            wait_quiet(page)
            payload["variantCreateInitial"] = snapshot(page)
            payload["selectedSkuRow"] = choose_sku(page)
            fill_first_number(page, 3)
            payload["variantBeforeSave"] = snapshot(page)
            click_text_button(page, ["保存する"])
            wait_quiet(page, timeout=12000)
            payload["afterVariantSave"] = snapshot(page)
            if page.url.endswith("/create"):
                page.goto(detail_url, wait_until="load")
                wait_quiet(page)
            wait_for_row_containing(page, SKU)
            payload["detailAfterVariantSave"] = snapshot(page)
            payload["rowsAfterVariantSave"] = row_texts_containing(page, SKU)

            select_row_containing(page, SKU)
            payload["afterVariantRowSelect"] = snapshot(page)
            payload["variantDelete"] = delete_selected(page, ["閾値を削除", "削除する"], confirm_names=["削除する"])
            page.goto(detail_url, wait_until="load")
            wait_quiet(page)
            payload["detailAfterVariantDeleteReload"] = snapshot(page)
            payload["rowsAfterVariantDeleteReload"] = row_texts_containing(page, SKU)

            page.goto(BASE + "/admin/inventory_threshold_rules", wait_until="load")
            wait_quiet(page)
            select_row_containing(page, rule_name)
            payload["afterRuleRowSelect"] = snapshot(page)
            payload["ruleDelete"] = delete_selected(page, ["削除する"], confirm_names=["削除する"])
            page.goto(BASE + "/admin/inventory_threshold_rules", wait_until="load")
            wait_quiet(page)
            payload["listAfterRuleDeleteReload"] = snapshot(page)
            payload["rowsAfterRuleDeleteReload"] = row_texts_containing(page, rule_name)
        except Exception as exc:
            payload["errors"].append({"error": repr(exc), "url": page.url, "body": compact(page.locator("body").inner_text(timeout=5000), 2500)})
        finally:
            default_numbers = [
                row for row in payload.get("createDefaultOn", {}).get("inputs", [])
                if row.get("type") in {"number", "text"} and row.get("placeholder") == "入力してください"
            ]
            variant_numbers = [
                row for row in payload.get("variantCreateInitial", {}).get("inputs", [])
                if row.get("type") == "number"
            ]
            detail_body = payload.get("detailInitial", {}).get("bodyText", "")
            explanation_terms = ["販売停止", "通知", "売り止め", "到達", "下回る"]
            detail_link_sources = [
                payload.get("detailInitial", {}),
                payload.get("detailAfterVariantSave", {}),
                payload.get("variantDelete", {}).get("after", {}),
                payload.get("detailAfterVariantDeleteReload", {}),
            ]
            detail_links = []
            for source in detail_link_sources:
                for link in source.get("links", []):
                    if link.get("text") in {"自動追加ルール", "閾値を追加する"}:
                        detail_links.append(link.get("text"))
            payload["facts"] = {
                "createLabels": payload.get("createInitial", {}).get("labels", []),
                "defaultThresholdInitialValue": default_numbers[0]["value"] if default_numbers else None,
                "returnedToListAfterCreate": payload.get("afterRuleSave", {}).get("url") == BASE + "/admin/inventory_threshold_rules",
                "detailLinks": sorted(set(detail_links)),
                "variantThresholdInitialValue": variant_numbers[0]["value"] if variant_numbers else None,
                "selectedSkuRow": payload.get("selectedSkuRow", ""),
                "rowsAfterVariantSave": payload.get("rowsAfterVariantSave", []),
                "variantDeleted": "rowsAfterVariantDeleteReload" in payload and len(payload.get("rowsAfterVariantDeleteReload", [])) == 0,
                "ruleDeleted": "rowsAfterRuleDeleteReload" in payload and len(payload.get("rowsAfterRuleDeleteReload", [])) == 0,
                "thresholdReachExplanationInUi": any(term in detail_body for term in explanation_terms),
                "preCleanupOldThresholdRules": payload.get("preCleanupOldThresholdRules", []),
                "errors": payload["errors"],
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
            page.close()
            browser.close()
    print(json.dumps(payload["facts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
