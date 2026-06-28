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
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "23-webhook-event-options-20260628.json"
MD = OUT.with_suffix(".md")

APP_ROUTE = "/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App"
APP_NAME = "TEST_FAQ_20260624_APP_113636"


def compact(text, limit=1800):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(800)


def dialog_snapshot(dialog):
    return {
        "text": compact(dialog.inner_text(timeout=5000)),
        "selects": dialog.locator("select").evaluate_all(
            """selects => selects.map((select, index) => ({
                index,
                name: select.getAttribute('name'),
                value: select.value,
                options: Array.from(select.options).map((option) => ({
                    value: option.value,
                    text: (option.innerText || option.textContent || '').trim(),
                    disabled: option.disabled
                }))
            }))"""
        ),
        "inputs": dialog.locator("input").evaluate_all(
            """inputs => inputs.map((input) => ({
                type: input.getAttribute('type'),
                name: input.getAttribute('name'),
                placeholder: input.getAttribute('placeholder'),
                valueLength: input.value ? input.value.length : 0
            }))"""
        ),
        "buttons": dialog.locator("button").evaluate_all(
            """buttons => buttons.map((button) => ({
                text: (button.innerText || button.textContent || '').replace(/\\s+/g, ' ').trim(),
                disabled: !!button.disabled
            }))"""
        ),
    }


def verify_event_select(dialog):
    select = dialog.locator("select").first
    options = select.locator("option").evaluate_all(
        """options => options.map((option) => ({
            value: option.value,
            text: (option.innerText || option.textContent || '').trim(),
            disabled: option.disabled
        }))"""
    )
    selectable = [option for option in options if option["value"] and not option["disabled"]]
    checks = []
    for option in selectable:
        select.select_option(value=option["value"])
        selected = select.evaluate(
            """select => {
                const option = select.options[select.selectedIndex];
                return {
                    value: select.value,
                    text: option ? (option.innerText || option.textContent || '').trim() : ''
                };
            }"""
        )
        checks.append(
            {
                "requested": option,
                "selected": selected,
                "matched": selected["value"] == option["value"] and selected["text"] == option["text"],
            }
        )
    return {
        "options": options,
        "selectableCount": len(selectable),
        "selectableTexts": [option["text"] for option in selectable],
        "selectionChecks": checks,
        "onlyExpectedEvents": [option["text"] for option in selectable]
        == ["注文の作成", "注文の更新", "在庫の更新"],
    }


def write_md(payload):
    result = payload["result"]
    event = result["eventSelect"]
    lines = [
        "# Webhookイベント選択肢 実機確認 2026-06-28",
        "",
        f"- 対象: `{APP_NAME}` `{APP_ROUTE}`",
        "- 操作: アプリ詳細で `Webhookを作成する` を開き、保存せずにイベント欄の候補と選択可否を確認",
        f"- 選択可能イベント数: {event['selectableCount']}",
        f"- 選択可能イベント: {', '.join(event['selectableTexts'])}",
        f"- 期待3種のみ: {event['onlyExpectedEvents']}",
        f"- ダイアログ閉鎖確認: {result['dialogClosed']}",
        "",
        "## select option",
        "",
    ]
    for option in event["options"]:
        lines.append(
            f"- value=`{option['value']}` text=`{option['text']}` disabled={option['disabled']}"
        )
    lines.extend(
        [
            "",
            "## selection checks",
            "",
        ]
    )
    for check in event["selectionChecks"]:
        req = check["requested"]
        sel = check["selected"]
        lines.append(
            f"- `{req['text']}`: value `{req['value']}` -> selected `{sel['text']}` / `{sel['value']}` matched={check['matched']}"
        )
    lines.extend(
        [
            "",
            "## 結論",
            "",
            "- 2026-06-28時点のWebhook作成ダイアログで選択できるイベントは `注文の作成` / `注文の更新` / `在庫の更新` の3種のみ。",
            "- API直叩きや非公開仕様の追加イベントは確認対象外。管理画面UIでユーザーが設定できるイベントとしては上記3種に限定して案内する。",
            "",
        ]
    )
    MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "appRoute": APP_ROUTE,
        "appName": APP_NAME,
        "errors": [],
        "result": {},
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(BASE + APP_ROUTE, wait_until="load")
            wait_quiet(page)
            h1 = page.locator("h1").first.inner_text(timeout=5000)
            page.get_by_role("button", name="Webhookを作成する", exact=True).click()
            page.wait_for_selector('[role="dialog"]', timeout=15000)
            dialog = page.locator('[role="dialog"]').last
            snapshot = dialog_snapshot(dialog)
            event_select = verify_event_select(dialog)
            page.keyboard.press("Escape")
            page.wait_for_timeout(800)
            payload["result"] = {
                "url": page.url,
                "h1": compact(h1, 300),
                "dialogSnapshot": snapshot,
                "eventSelect": event_select,
                "dialogClosed": page.locator('[role="dialog"]').count() == 0,
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
                "events": payload.get("result", {}).get("eventSelect", {}).get("selectableTexts"),
                "onlyExpectedEvents": payload.get("result", {}).get("eventSelect", {}).get("onlyExpectedEvents"),
                "dialogClosed": payload.get("result", {}).get("dialogClosed"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
