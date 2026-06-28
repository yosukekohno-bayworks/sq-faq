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
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "18-crm-rank-multiplier-add-delete-20260628.json"
MD = OUT.with_suffix(".md")
SHOT_AFTER_ADD = OUT.with_name("18-crm-rank-multiplier-after-add-20260628.png")
SHOT_AFTER_DELETE = OUT.with_name("18-crm-rank-multiplier-after-delete-20260628.png")

RULE_NAME = "TEST_FAQ_注文ポイント付与ルール"
RULE_ROUTE = "/admin/point_calculation_rules/4d73fe29-07c9-5370-80a2-61c3ad3aadfa_PointCalculationRule"
RANK_MULTIPLIERS_ROUTE = RULE_ROUTE + "/rank_multipliers"
TARGET_RANK = "Bronze"
TARGET_MULTIPLIER = "2"


def compact(text, limit=2400):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def page_snapshot(page, limit=3500):
    return page.evaluate(
        """(limit) => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            return {
                url: location.href,
                h1: Array.from(document.querySelectorAll('h1')).map(text).filter(Boolean),
                h2: Array.from(document.querySelectorAll('h2')).map(text).filter(Boolean),
                rows: Array.from(document.querySelectorAll('tr')).map(text).filter(Boolean),
                buttons: Array.from(document.querySelectorAll('button')).map((button) => ({
                    text: text(button),
                    disabled: !!button.disabled,
                    ariaDisabled: button.getAttribute('aria-disabled')
                })).filter((x) => x.text),
                body: document.body ? text(document.body).slice(0, limit) : ''
            };
        }""",
        limit,
    )


def dialog_snapshot(dialog):
    return {
        "text": compact(dialog.inner_text(timeout=5000), 3000),
        "selects": dialog.locator("select").evaluate_all(
            """selects => selects.map((select, index) => ({
                index,
                value: select.value,
                options: Array.from(select.options).map((option) => ({
                    value: option.value,
                    text: (option.innerText || option.textContent || '').trim(),
                    disabled: option.disabled
                }))
            }))"""
        ),
        "inputs": dialog.locator("input").evaluate_all(
            """inputs => inputs.map((input, index) => ({
                index,
                type: input.getAttribute('type'),
                placeholder: input.getAttribute('placeholder'),
                value: input.value
            }))"""
        ),
        "buttons": dialog.locator("button").evaluate_all(
            """buttons => buttons.map((button) => ({
                text: (button.innerText || button.textContent || '').replace(/\\s+/g, ' ').trim(),
                disabled: !!button.disabled
            }))"""
        ),
    }


def rows(page):
    return page.locator("tr").evaluate_all(
        """trs => trs.map((tr) => (tr.innerText || tr.textContent || '').replace(/\\s+/g, ' ').trim()).filter(Boolean)"""
    )


def find_row(page, text):
    for row in rows(page):
        if text in row:
            return row
    return None


def add_rank_multiplier(page):
    result = {}
    page.get_by_role("button", name="追加する", exact=True).click()
    page.wait_for_selector('[role="dialog"]', timeout=15000)
    dialog = page.locator('[role="dialog"]').last
    result["dialogBefore"] = dialog_snapshot(dialog)
    select = dialog.locator("select").first
    options = result["dialogBefore"]["selects"][0]["options"] if result["dialogBefore"]["selects"] else []
    target = next((option for option in options if option["text"] == TARGET_RANK and not option["disabled"]), None)
    if not target:
        result["error"] = f"target rank {TARGET_RANK} not selectable"
        return result
    select.select_option(value=target["value"])
    dialog.locator('input[type="number"]').first.fill(TARGET_MULTIPLIER)
    page.wait_for_timeout(500)
    result["dialogFilled"] = dialog_snapshot(dialog)
    dialog.get_by_role("button", name="追加する", exact=True).click()
    wait_quiet(page, timeout=9000)
    for _ in range(3):
        if find_row(page, TARGET_RANK):
            break
        page.reload(wait_until="load")
        wait_quiet(page, timeout=7000)
    result["afterAdd"] = page_snapshot(page)
    result["rowAfterAdd"] = find_row(page, TARGET_RANK)
    page.screenshot(path=str(SHOT_AFTER_ADD), full_page=True)
    return result


def delete_rank_multiplier(page):
    result = {}
    row = page.locator("tr").filter(has_text=TARGET_RANK).first
    if not row.count():
        result["error"] = "target row not found"
        result["beforeDeleteRows"] = rows(page)
        return result
    checkbox = row.locator('input[type="checkbox"]').first
    if checkbox.count():
        checkbox.check()
    else:
        row.click()
    page.wait_for_timeout(600)
    result["afterSelect"] = page_snapshot(page)
    page.get_by_role("button", name="削除する", exact=True).click()
    page.wait_for_selector('[role="dialog"]', timeout=15000)
    dialog = page.locator('[role="dialog"]').last
    result["deleteDialog"] = compact(dialog.inner_text(timeout=5000), 2500)
    dialog.get_by_role("button", name="削除する", exact=True).click()
    wait_quiet(page, timeout=9000)
    page.reload(wait_until="load")
    wait_quiet(page, timeout=7000)
    result["afterDelete"] = page_snapshot(page)
    result["rowAfterDelete"] = find_row(page, TARGET_RANK)
    page.screenshot(path=str(SHOT_AFTER_DELETE), full_page=True)
    return result


def write_md(payload):
    add = payload["result"].get("add", {})
    delete = payload["result"].get("delete", {})
    lines = [
        "# CRM 会員ランク倍率 追加/削除 実機確認 2026-06-28",
        "",
        f"- 対象ルール: `{RULE_NAME}`",
        f"- 対象URL: `{BASE + RANK_MULTIPLIERS_ROUTE}`",
        f"- 追加対象: `{TARGET_RANK}` / `{TARGET_MULTIPLIER}倍`",
        "",
        "## 結果",
        "",
        "| 確認項目 | 結果 |",
        "|:--|:--|",
        f"| 追加ダイアログに会員ランクと倍率が表示 | `{bool(add.get('dialogBefore'))}` |",
        f"| `{TARGET_RANK}` が選択可能 | `{payload['facts']['rankSelectable']}` |",
        f"| 追加後一覧に `{TARGET_RANK}` が表示 | `{payload['facts']['addedListContainsRank']}` |",
        f"| 追加後一覧に `{TARGET_MULTIPLIER}倍` が表示 | `{payload['facts']['addedListContainsMultiplier']}` |",
        f"| 削除確認ダイアログを確認 | `{bool(delete.get('deleteDialog'))}` |",
        f"| 削除後一覧から `{TARGET_RANK}` が消える | `{payload['facts']['deletedListOmitsRank']}` |",
        "",
        "## 削除確認ダイアログ",
        "",
        delete.get("deleteDialog", ""),
        "",
        "## 判断",
        "",
        "- 注文ポイント付与ルール詳細の `会員ランク倍率` タブでは、会員ランクを選択し倍率を保存できる。",
        "- 保存後は会員ランク名と倍率が一覧に反映される。",
        "- 行選択後の `削除する` で削除確認ダイアログを経て削除でき、リロード後も一覧から消える。",
        "- 実注文に対する倍率計算結果は、注文/顧客/ポイント実績が必要なため未確認。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT.relative_to(ROOT)}`",
        f"- 追加後スクリーンショット: `{SHOT_AFTER_ADD.relative_to(ROOT)}`",
        f"- 削除後スクリーンショット: `{SHOT_AFTER_DELETE.relative_to(ROOT)}`",
        "",
    ]
    MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "rule": {"name": RULE_NAME, "route": RULE_ROUTE, "rankMultipliersRoute": RANK_MULTIPLIERS_ROUTE},
        "target": {"rank": TARGET_RANK, "multiplier": TARGET_MULTIPLIER},
        "errors": [],
        "result": {},
        "facts": {},
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(BASE + RANK_MULTIPLIERS_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["result"]["initial"] = page_snapshot(page)
            initial_row = find_row(page, TARGET_RANK)
            if initial_row:
                if (TARGET_MULTIPLIER + "倍") in initial_row:
                    payload["result"]["cleanupBeforeTest"] = delete_rank_multiplier(page)
                    page.goto(BASE + RANK_MULTIPLIERS_ROUTE, wait_until="load")
                    wait_quiet(page)
                else:
                    payload["errors"].append(f"{TARGET_RANK} already exists before test with unexpected row: {initial_row}")
            if not payload["errors"]:
                payload["result"]["add"] = add_rank_multiplier(page)
                payload["result"]["delete"] = delete_rank_multiplier(page)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            try:
                payload["result"]["finalSnapshot"] = page_snapshot(page)
            except Exception:
                pass
        finally:
            add = payload["result"].get("add", {})
            delete = payload["result"].get("delete", {})
            row_after_add = add.get("rowAfterAdd") or ""
            row_after_delete = delete.get("rowAfterDelete")
            options = []
            if add.get("dialogBefore", {}).get("selects"):
                options = add["dialogBefore"]["selects"][0]["options"]
            payload["facts"] = {
                "rankSelectable": any(option["text"] == TARGET_RANK and not option["disabled"] for option in options),
                "addedListContainsRank": TARGET_RANK in row_after_add,
                "addedListContainsMultiplier": (TARGET_MULTIPLIER + "倍") in row_after_add,
                "deleteDialog": delete.get("deleteDialog"),
                "deletedListOmitsRank": not delete.get("error") and row_after_delete is None,
                "errors": payload["errors"],
            }
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
            page.close()
            browser.close()
    print(json.dumps({"json": str(OUT), "md": str(MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
