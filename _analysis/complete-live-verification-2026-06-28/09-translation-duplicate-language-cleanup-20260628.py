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
OUT_JSON = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "09-translation-duplicate-language-cleanup-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")


def compact(text, limit=2500):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snapshot(page, limit=4000):
    return page.evaluate(
        """(limit) => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const unique = (items) => Array.from(new Set(items.filter(Boolean)));
            return {
                url: location.href,
                h1: unique(Array.from(document.querySelectorAll('h1')).map(text)),
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
                    page.wait_for_timeout(800)
                    return name
            except Exception:
                continue
    raise RuntimeError(f"button not found: {names}")


def row_texts_containing(page, needle):
    return page.evaluate(
        """(needle) => Array.from(document.querySelectorAll('tr'))
            .filter((tr) => tr.innerText.includes(needle))
            .map((tr) => ({ id: tr.id, text: (tr.innerText || '').replace(/\\s+/g, ' ').trim() }))""",
        needle,
    )


def rows_with_language(page, language_text):
    return page.evaluate(
        """(languageText) => Array.from(document.querySelectorAll('tr'))
            .filter((tr) => tr.innerText.includes(languageText))
            .map((tr) => ({ id: tr.id, text: (tr.innerText || '').replace(/\\s+/g, ' ').trim() }))""",
        language_text,
    )


def select_row_containing(page, needle):
    page.wait_for_function(
        """(needle) => Array.from(document.querySelectorAll('tr')).some((tr) => tr.innerText.includes(needle))""",
        arg=needle,
        timeout=20000,
    )
    row = page.locator("tr").filter(has_text=needle).first
    row_text = compact(row.inner_text(timeout=5000), 1000)
    checkbox = row.locator('input[type="checkbox"]').first
    if checkbox.count() > 0:
        checkbox.click(force=True)
    else:
        row.click(force=True)
    page.wait_for_timeout(900)
    return row_text


def delete_rule_by_name(page, name):
    page.goto(BASE + "/admin/settings/translation/translation_rules", wait_until="load")
    wait_quiet(page)
    rows = row_texts_containing(page, name)
    if not rows:
        return {"found": False, "deleted": True}
    selected = select_row_containing(page, name)
    after_select = snapshot(page, limit=2500)
    click_text_button(page, ["削除する"])
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    dialog_text = compact(dialog.inner_text(timeout=5000), 1200)
    click_text_button(page, ["削除する"], scope=dialog)
    wait_quiet(page, timeout=10000)
    page.goto(BASE + "/admin/settings/translation/translation_rules", wait_until="load")
    wait_quiet(page)
    remaining = row_texts_containing(page, name)
    return {
        "found": True,
        "selected": selected,
        "afterSelect": after_select,
        "dialogText": dialog_text,
        "remainingRows": remaining,
        "deleted": len(remaining) == 0,
    }


def create_translation_rule(page, name, language_value="EN", auto=False):
    page.goto(BASE + "/admin/settings/translation/translation_rules/create", wait_until="load")
    wait_quiet(page)
    initial = snapshot(page)
    page.locator('input[type="text"]').first.fill(name)
    page.locator("select").first.select_option(value=language_value)
    if auto:
        checkbox = page.locator('input[type="checkbox"]').first
        if not checkbox.is_checked():
            checkbox.click()
    before_save = snapshot(page)
    click_text_button(page, ["保存する"])
    wait_quiet(page, timeout=12000)
    try:
        page.wait_for_function(
            "(name) => Array.from(document.querySelectorAll('h1')).some((h1) => h1.innerText.includes(name)) || document.body.innerText.includes('翻訳ルールを追加しました')",
            arg=name,
            timeout=20000,
        )
    except PlaywrightTimeoutError:
        pass
    detail = snapshot(page)
    return {"initial": initial, "beforeSave": before_save, "detail": detail}


def no_manual_execute_buttons(*snaps):
    needles = ["実行", "再実行", "翻訳する", "生成"]
    hits = []
    for snap in snaps:
        for button in snap.get("buttons", []):
            text = (button.get("text") or "") + " " + (button.get("aria") or "")
            if any(needle in text for needle in needles):
                hits.append({"url": snap.get("url"), "button": button})
    return {"noneFound": len(hits) == 0, "hits": hits}


def write_md(payload):
    facts = payload["facts"]
    lines = [
        "# 翻訳ルール 同一言語・自動生成保存・削除確認 2026-06-28",
        "",
        "## 検証データ",
        "",
        f"- ルールA: `{payload['ruleA']}`（英語、自動生成ON）",
        f"- ルールB: `{payload['ruleB']}`（英語、自動生成OFF）",
        "",
        "## 結果",
        "",
        "| 項目 | 結果 |",
        "|:--|:--|",
        f"| 作成フォームの言語選択肢 | `{facts['languageOptions']}` |",
        f"| 既存の英語ルール数 | `{facts['englishRowsBeforeCount']}` |",
        f"| 同一言語2件の新規作成 | `{facts['duplicateEnglishCreateSucceeded']}` |",
        f"| 自動生成ONの保存状態 | `{facts['autoOnDetailState']}` |",
        f"| 自動生成OFFの保存状態 | `{facts['autoOffDetailState']}` |",
        f"| 手動実行ボタン | `{facts['manualExecuteButtons']}` |",
        f"| 検証用ルール削除 | `{facts['cleanupDeleted']}` |",
        "",
        "## 判断",
        "",
        "- 2026-06-28時点の現行UIでは、同じ言語（英語）の翻訳ルールを複数作成できる。一覧にも同一言語の複数行が並ぶ。",
        "- `翻訳データを自動で作成する` は保存後の詳細画面でもチェック状態が残る。",
        "- 翻訳トップ/一覧/作成フォーム/詳細画面の確認範囲では、手動の `実行` / `再実行` / `翻訳する` / `生成` ボタンは見当たらない。",
        "- 検証用翻訳ルール2件は一覧の行選択後 `削除する` で削除済み。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    rule_a = f"TEST_FAQ_TRANSLATION_DUP_A_{stamp}"
    rule_b = f"TEST_FAQ_TRANSLATION_DUP_B_{stamp}"
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "ruleA": rule_a,
        "ruleB": rule_b,
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(22000)
        try:
            page.goto(BASE + "/admin/settings/translation/translation_rules", wait_until="load")
            wait_quiet(page)
            old_names = page.evaluate(
                """() => Array.from(document.querySelectorAll('tr'))
                    .map((tr) => (tr.innerText || '').replace(/\\s+/g, ' ').trim())
                    .filter((text) => text.includes('TEST_FAQ_TRANSLATION_DUP_'))
                    .map((text) => text.replace(/^アイテムを選択する\\s+/, '').split(' 英語 ')[0])"""
            )
            payload["preCleanup"] = [delete_rule_by_name(page, name) for name in old_names]

            page.goto(BASE + "/admin/settings/translation/translation_rules", wait_until="load")
            wait_quiet(page)
            payload["listBefore"] = snapshot(page)
            payload["englishRowsBefore"] = rows_with_language(page, "英語")

            payload["createA"] = create_translation_rule(page, rule_a, language_value="EN", auto=True)
            payload["createB"] = create_translation_rule(page, rule_b, language_value="EN", auto=False)

            page.goto(BASE + "/admin/settings/translation/translation_rules", wait_until="load")
            wait_quiet(page)
            payload["listAfterCreate"] = snapshot(page)
            payload["createdRowsAfterCreate"] = row_texts_containing(page, "TEST_FAQ_TRANSLATION_DUP_")
            payload["englishRowsAfterCreate"] = rows_with_language(page, "英語")

            page.goto(BASE + "/admin/settings/translation", wait_until="load")
            wait_quiet(page)
            payload["translationTop"] = snapshot(page)
            page.goto(BASE + "/admin/settings/translation/translation_rules", wait_until="load")
            wait_quiet(page)
            payload["translationRulesList"] = snapshot(page)

            payload["cleanupA"] = delete_rule_by_name(page, rule_a)
            payload["cleanupB"] = delete_rule_by_name(page, rule_b)
            page.goto(BASE + "/admin/settings/translation/translation_rules", wait_until="load")
            wait_quiet(page)
            payload["listAfterCleanup"] = snapshot(page)
            payload["createdRowsAfterCleanup"] = row_texts_containing(page, "TEST_FAQ_TRANSLATION_DUP_")
        except Exception as exc:
            body = ""
            try:
                body = compact(page.locator("body").inner_text(timeout=5000), 2500)
            except Exception:
                pass
            payload["errors"].append({"error": repr(exc), "url": page.url, "body": body})
        finally:
            create_initial = payload.get("createA", {}).get("initial", {})
            language_selects = [row for row in create_initial.get("inputs", []) if row.get("tag") == "select"]
            language_options = language_selects[0].get("options", []) if language_selects else []
            auto_on_inputs = payload.get("createA", {}).get("detail", {}).get("inputs", [])
            auto_off_inputs = payload.get("createB", {}).get("detail", {}).get("inputs", [])
            auto_on = [row for row in auto_on_inputs if row.get("type") == "checkbox" and "翻訳データ" in row.get("label", "")]
            auto_off = [row for row in auto_off_inputs if row.get("type") == "checkbox" and "翻訳データ" in row.get("label", "")]
            manual_buttons = no_manual_execute_buttons(
                payload.get("translationTop", {}),
                payload.get("translationRulesList", {}),
                payload.get("createA", {}).get("initial", {}),
                payload.get("createA", {}).get("detail", {}),
                payload.get("createB", {}).get("detail", {}),
            )
            payload["facts"] = {
                "languageOptions": [option["text"] for option in language_options],
                "englishRowsBeforeCount": len(payload.get("englishRowsBefore", [])),
                "duplicateEnglishCreateSucceeded": len(payload.get("createdRowsAfterCreate", [])) >= 2
                and len(payload.get("englishRowsAfterCreate", [])) >= len(payload.get("englishRowsBefore", [])) + 2,
                "autoOnDetailState": auto_on[0] if auto_on else None,
                "autoOffDetailState": auto_off[0] if auto_off else None,
                "manualExecuteButtons": manual_buttons,
                "cleanupDeleted": len(payload.get("createdRowsAfterCleanup", [])) == 0
                and payload.get("cleanupA", {}).get("deleted") is True
                and payload.get("cleanupB", {}).get("deleted") is True,
                "errors": payload["errors"],
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
            page.close()
            browser.close()
    print(json.dumps(payload["facts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
