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
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "04-local-pickup-location-flag-candidates-20260628.json"
MD = OUT.with_suffix(".md")

LOCATION_DETAILS = [
    {
        "code": "FLAGOFF01",
        "route": "/admin/settings/locations/45ffa873-a7f2-5581-8117-5758f5a45c73_Location",
        "expectedType": "店舗",
    },
    {
        "code": "TEST_E2E_20260622_STORE_1740",
        "route": "/admin/settings/locations/1f0fd500-ee41-50b5-afb9-217ab8af9db3_Location",
        "expectedType": "店舗",
    },
]

SEARCHES = [
    {"code": "FLAGOFF01", "meaning": "店舗受取OFFの店舗ロケーション"},
    {"code": "TEST_E2E_20260622_STORE_1740", "meaning": "店舗受取ONの店舗ロケーション"},
    {"code": "W0001", "meaning": "倉庫ロケーション"},
    {"code": "R0001", "meaning": "店舗ロケーション"},
]


def compact(text, limit=1800):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def checkbox_states(page):
    return page.locator('input[type="checkbox"]').evaluate_all(
        r"""els => els.map((el) => ({
            checked: el.checked,
            text: (el.closest('label')?.innerText || el.parentElement?.innerText || '').replace(/\s+/g, ' ').trim()
        }))"""
    )


def detail_snapshot(page, item):
    page.goto(BASE + item["route"], wait_until="load")
    wait_quiet(page)
    body = compact(page.locator("body").inner_text(timeout=5000), 3000)
    checks = checkbox_states(page)
    check_map = {row["text"]: row["checked"] for row in checks}
    return {
        "code": item["code"],
        "route": item["route"],
        "url": page.url,
        "h1": [compact(h.inner_text(timeout=3000), 200) for h in page.locator("h1").all()],
        "bodySample": body,
        "locationTypeVisible": item["expectedType"] in body,
        "localPickupEnabled": check_map.get("店舗受取を有効にする"),
        "inventoryRequestEnabled": check_map.get("在庫依頼を受け付ける"),
    }


def search_rows(dialog, page, code):
    inp = dialog.locator("input").first
    inp.click()
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    inp.fill(code)
    page.keyboard.press("Enter")
    wait_quiet(page)
    rows = dialog.locator("tr, [role=row]").evaluate_all(
        r"""els => els
          .map((el) => (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim())
          .filter((text) => text && !text.startsWith('すべてのアイテムを選択する'))"""
    )
    return {
        "code": code,
        "rows": rows,
        "rowCount": len(rows),
        "found": any(code in row for row in rows),
    }


def write_md(payload):
    result = payload["result"]
    lines = [
        "# 店舗受取ロケーション候補とON/OFF 実機確認 2026-06-28",
        "",
        "## ロケーション詳細",
        "",
    ]
    for row in result["locationDetails"]:
        lines.append(
            f"- `{row['code']}`: 店舗受取ON={row['localPickupEnabled']} / 在庫依頼ON={row['inventoryRequestEnabled']} / typeVisible={row['locationTypeVisible']}"
        )
    lines.extend(["", "## 店舗受取ルール作成フォームの候補検索", ""])
    for row in result["candidateSearches"]:
        lines.append(
            f"- `{row['code']}`: found={row['found']} rowCount={row['rowCount']} rows={row['rows']}"
        )
    lines.extend(
        [
            "",
            "## 結論",
            "",
            "- 店舗受取ルール作成フォームのロケーション候補は、場所種別=店舗で絞られる。",
            "- `店舗受取を有効にする` がOFFの店舗ロケーションも候補に表示されるため、管理画面の候補表示はこのチェックでは絞り込まれない。",
            "- このチェックがストアフロント上の受取可否や連携後の挙動にどう効くかは、接続環境での確認事項として残す。",
            "",
        ]
    )
    MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "errors": [],
        "result": {},
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            details = [detail_snapshot(page, item) for item in LOCATION_DETAILS]
            page.goto(BASE + "/admin/local_pickup_retail_location_rules/create", wait_until="load")
            wait_quiet(page)
            page.get_by_role("button", name="選択", exact=True).click()
            page.wait_for_selector('[role="dialog"]', timeout=15000)
            dialog = page.locator('[role="dialog"]').last
            dialog_text = compact(dialog.inner_text(timeout=5000), 3000)
            searches = []
            for item in SEARCHES:
                row = dict(item)
                row.update(search_rows(dialog, page, item["code"]))
                searches.append(row)
            payload["result"] = {
                "locationDetails": details,
                "dialogTextSample": dialog_text,
                "candidateSearches": searches,
                "offStoreShown": next(row for row in searches if row["code"] == "FLAGOFF01")["found"],
                "onStoreShown": next(row for row in searches if row["code"] == "TEST_E2E_20260622_STORE_1740")["found"],
                "warehouseHidden": not next(row for row in searches if row["code"] == "W0001")["found"],
            }
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            if payload["result"]:
                write_md(payload)
            page.close()
            browser.close()

    print(
        json.dumps(
            {
                "errors": payload["errors"],
                "offStoreShown": payload.get("result", {}).get("offStoreShown"),
                "onStoreShown": payload.get("result", {}).get("onStoreShown"),
                "warehouseHidden": payload.get("result", {}).get("warehouseHidden"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
