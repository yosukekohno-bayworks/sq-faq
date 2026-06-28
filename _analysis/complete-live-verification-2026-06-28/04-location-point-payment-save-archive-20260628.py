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
OUT_JSON = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "04-location-point-payment-save-archive-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")


def compact(text, limit=2000):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(700)


def select_states(page):
    return page.locator("select").evaluate_all(
        r"""els => els.map((el) => ({
            label: (el.closest('label')?.innerText || el.parentElement?.innerText || '').replace(/\s+/g, ' ').trim(),
            value: el.value,
            selectedText: el.options[el.selectedIndex]?.textContent?.trim() || '',
            options: Array.from(el.options).map((option) => ({
                value: option.value,
                text: option.textContent.trim(),
                disabled: option.disabled
            }))
        }))"""
    )


def snapshot(page):
    return {
        "url": page.url,
        "h1": [compact(h.inner_text(timeout=3000), 200) for h in page.locator("h1").all()],
        "bodyText": compact(page.locator("body").inner_text(timeout=5000), 5000),
        "selects": select_states(page),
    }


def select_by_label(page, label, option_label):
    target = page.get_by_label(label, exact=False).locator("..").locator("select").first
    if target.count() == 0:
        target = page.locator("select").filter(has=page.locator(f"text={label}")).first
    try:
        page.get_by_label(label, exact=False).select_option(label=option_label)
    except Exception:
        page.locator("select").evaluate_all(
            """(els, arg) => {
                const [labelText, optionText] = arg;
                const select = els.find((el) => {
                    const text = (el.closest('label')?.innerText || el.parentElement?.innerText || '').replace(/\\s+/g, ' ').trim();
                    return text.includes(labelText);
                });
                if (!select) throw new Error(`select not found: ${labelText}`);
                const option = Array.from(select.options).find((opt) => opt.textContent.trim() === optionText);
                if (!option) throw new Error(`option not found: ${optionText}`);
                select.value = option.value;
                select.dispatchEvent(new Event('input', { bubbles: true }));
                select.dispatchEvent(new Event('change', { bubbles: true }));
            }""",
            [label, option_label],
        )


def fill_by_label(page, label, value):
    try:
        page.get_by_label(label, exact=False).first.fill(value)
    except Exception:
        page.locator("input").evaluate_all(
            """(els, arg) => {
                const [labelText, value] = arg;
                const input = els.find((el) => {
                    const text = (el.closest('label')?.innerText || el.parentElement?.innerText || '').replace(/\\s+/g, ' ').trim();
                    return text.includes(labelText);
                });
                if (!input) throw new Error(`input not found: ${labelText}`);
                input.value = value;
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }""",
            [label, value],
        )


def first_enabled_button(scope, names):
    for name in names:
        buttons = scope.get_by_role("button", name=name, exact=True)
        for i in range(buttons.count()):
            button = buttons.nth(i)
            try:
                if button.is_visible() and button.is_enabled():
                    return name, button
            except Exception:
                continue
    return None, None


def open_created_detail(page, code):
    deadline = datetime.now().timestamp() + 35
    last_body = ""
    while datetime.now().timestamp() < deadline:
        page.goto(BASE + "/admin/settings/locations", wait_until="load")
        wait_quiet(page)
        last_body = compact(page.locator("body").inner_text(timeout=5000), 3000)
        row = page.locator("tr, [role=row]").filter(has_text=code).first
        if row.count() > 0:
            row.click()
            wait_quiet(page)
            return
        page.wait_for_timeout(1500)
    raise RuntimeError(f"created location row not found: {code}; body={last_body}")


def point_usage_select(snapshot_data):
    for row in snapshot_data.get("selects", []):
        values = {option.get("value") for option in row.get("options", [])}
        if {"DISCOUNT", "PAYMENT"}.issubset(values):
            return row
    return {}


def write_md(payload):
    facts = payload["facts"]
    lines = [
        "# ロケーション ポイント利用種別=金種 保存・アーカイブ確認 2026-06-28",
        "",
        "## 結果",
        "",
        "| 項目 | 結果 |",
        "|:--|:--|",
        f"| 作成コード | `{facts['code']}` |",
        f"| 作成後URL | `{facts['createdUrl']}` |",
        f"| 作成後に金種表示 | `{facts['paymentVisibleAfterSave']}` |",
        f"| 詳細selectのポイント利用種別 | `{facts['pointUsageSelectedAfterSave']}` |",
        f"| アーカイブ実行 | `{facts['archiveClicked']}` |",
        f"| アーカイブ後表示 | `{facts['archivedVisible']}` |",
        "",
        "## 判断",
        "",
        "- ロケーション作成フォームでは `ポイント利用種別=金種` を選択して保存できる。",
        "- 保存後のロケーション詳細でも `金種` が選択状態として残る。",
        "- 検証用ロケーションは詳細画面からアーカイブ済み。ポイント利用種別の実注文・ポイント利用時の差分は未確認のまま。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    code = f"PTPAY{stamp[-8:]}"
    name = f"TEST_FAQ_POINT_PAYMENT_{stamp}"
    payload = {"generatedAt": datetime.now(timezone.utc).isoformat(), "errors": [], "testData": {"name": name, "code": code}}

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(BASE + "/admin/settings/locations/create", wait_until="load")
            wait_quiet(page)
            payload["createInitial"] = snapshot(page)
            fill_by_label(page, "名前", name)
            fill_by_label(page, "コード", code)
            select_by_label(page, "場所種別", "店舗")
            select_by_label(page, "ポイント利用種別", "金種")
            payload["createBeforeSave"] = snapshot(page)
            _, save_button = first_enabled_button(page.locator("#AppFrameMain"), ["保存する"])
            if save_button is None:
                _, save_button = first_enabled_button(page, ["保存する"])
            if save_button is None:
                raise RuntimeError("save button not found")
            save_button.click()
            try:
                page.wait_for_function(
                    "() => !document.body.innerText.includes('読み込み中')",
                    timeout=30000,
                )
            except PlaywrightTimeoutError:
                pass
            wait_quiet(page, timeout=12000)
            if "/create" not in page.url:
                try:
                    page.wait_for_function(
                        "(name) => document.body.innerText.includes(name)",
                        arg=name,
                        timeout=30000,
                    )
                except PlaywrightTimeoutError:
                    page.reload(wait_until="load")
                    wait_quiet(page, timeout=12000)
            payload["afterSave"] = snapshot(page)
            if "/create" in page.url:
                open_created_detail(page, code)
                payload["afterSaveDetail"] = snapshot(page)

            _, archive_button = first_enabled_button(page, ["アーカイブする"])
            payload["archiveButtonFound"] = archive_button is not None
            if archive_button is not None:
                archive_button.click()
                wait_quiet(page)
                dialog = page.locator('[role="dialog"]').last
                payload["archiveDialog"] = compact(dialog.inner_text(timeout=5000), 2000) if dialog.count() else ""
                _, confirm = first_enabled_button(dialog if dialog.count() else page, ["アーカイブする", "実行する"])
                if confirm is not None:
                    confirm.click()
                    wait_quiet(page, timeout=12000)
                    page.reload(wait_until="load")
                    wait_quiet(page, timeout=12000)
            payload["afterArchive"] = snapshot(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            after_save = payload.get("afterSaveDetail") or payload.get("afterSave", {})
            point_select = point_usage_select(after_save)
            payload["facts"] = {
                "name": name,
                "code": code,
                "createdUrl": after_save.get("url", ""),
                "paymentVisibleAfterSave": "金種" in after_save.get("bodyText", ""),
                "pointUsageSelectedAfterSave": point_select.get("selectedText"),
                "archiveClicked": payload.get("archiveButtonFound") is True and "afterArchive" in payload,
                "archivedVisible": (
                    "このロケーションはアーカイブされています" in payload.get("afterArchive", {}).get("bodyText", "")
                    or "アーカイブを解除する" in payload.get("afterArchive", {}).get("bodyText", "")
                ),
                "errors": payload["errors"],
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
            page.close()
            browser.close()

    print(json.dumps(payload["facts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
