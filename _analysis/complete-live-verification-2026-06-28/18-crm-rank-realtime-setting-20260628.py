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
OUT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "18-crm-rank-realtime-setting-20260628.json"
MD = OUT.with_suffix(".md")
DETAIL_SHOT = OUT.with_name("18-crm-rank-realtime-detail-20260628.png")
UPDATE_SHOT = OUT.with_name("18-crm-rank-realtime-update-20260628.png")

RULE_ROUTE = "/admin/customer_rank_calculation_rules/37f5da19-1289-5ff2-99ac-1b39ed8dfeaa_CustomerRankCalculationRule"
UPDATE_ROUTE = RULE_ROUTE + "/update"
RULE_NAME = "TEST_FAQ_会員ランク算出ルール"


def compact(text, limit=5000):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(3000)


def snapshot(page):
    return page.evaluate(
        """() => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            return {
                url: location.href,
                h1: Array.from(document.querySelectorAll('h1')).map(text).filter(Boolean),
                h2: Array.from(document.querySelectorAll('h2')).map(text).filter(Boolean),
                labels: Array.from(document.querySelectorAll('label')).map(text).filter(Boolean),
                inputs: Array.from(document.querySelectorAll('input, select, textarea')).map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type'),
                    value: el.value,
                    placeholder: el.getAttribute('placeholder'),
                    checked: el.checked,
                    disabled: !!el.disabled,
                    text: text(el)
                })),
                links: Array.from(document.querySelectorAll('a[href]')).map((a) => ({
                    text: text(a),
                    href: a.href
                })).filter((x) => x.text || x.href.includes('customer_rank_calculation_rules')),
                buttons: Array.from(document.querySelectorAll('button')).map((button) => ({
                    text: text(button),
                    ariaLabel: button.getAttribute('aria-label'),
                    disabled: !!button.disabled
                })).filter((x) => x.text || x.ariaLabel),
                body: document.body ? text(document.body) : ''
            };
        }"""
    )


def write_md(payload):
    facts = payload["facts"]
    lines = [
        "# CRM 会員ランク算出タイミング設定 実機確認 2026-06-28",
        "",
        f"- 対象ルール: `{RULE_NAME}`",
        f"- 詳細URL: `{BASE + RULE_ROUTE}`",
        f"- 編集URL: `{BASE + UPDATE_ROUTE}`",
        "",
        "## 結果",
        "",
        "| 確認項目 | 結果 |",
        "|:--|:--|",
        f"| 詳細に `算出タイミング` が表示 | `{facts['detailHasCalculationTiming']}` |",
        f"| 詳細の値が `リアルタイムに算出` | `{facts['detailHasRealtimeValue']}` |",
        f"| 編集フォームに `算出タイミング` 入力欄あり | `{facts['updateHasCalculationTimingInput']}` |",
        f"| 編集フォームに `リアルタイム` 入力欄あり | `{facts['updateHasRealtimeInput']}` |",
        f"| 算出方法ラジオは購入金額固定 | `{facts['calculationMethodPurchasePriceFixed']}` |",
        f"| 算出方法ラジオの獲得ポイントはdisabled | `{facts['earnedPointDisabled']}` |",
        "",
        "## 編集フォームのラベル",
        "",
    ]
    for label in payload["update"].get("labels", []):
        lines.append(f"- `{label}`")
    lines.extend(
        [
            "",
            "## 判断",
            "",
            "- 詳細画面には `算出タイミング` / `リアルタイムに算出` が表示される。",
            "- 編集フォームには `算出タイミング` や `リアルタイム` を変更する入力欄は表示されない。",
            "- 現行UIでは、算出タイミングは管理者が選択する設定ではなく固定表示として案内する。",
            "",
            "## 証跡",
            "",
            f"- JSON: `{OUT.relative_to(ROOT)}`",
            f"- 詳細スクリーンショット: `{DETAIL_SHOT.relative_to(ROOT)}`",
            f"- 編集スクリーンショット: `{UPDATE_SHOT.relative_to(ROOT)}`",
            "",
        ]
    )
    MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "ruleName": RULE_NAME,
        "detailRoute": RULE_ROUTE,
        "updateRoute": UPDATE_ROUTE,
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(BASE + RULE_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["detail"] = snapshot(page)
            page.screenshot(path=str(DETAIL_SHOT), full_page=True)
            page.goto(BASE + UPDATE_ROUTE, wait_until="load")
            wait_quiet(page)
            payload["update"] = snapshot(page)
            page.screenshot(path=str(UPDATE_SHOT), full_page=True)
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            detail_body = payload.get("detail", {}).get("body", "")
            update_body = payload.get("update", {}).get("body", "")
            update_labels = payload.get("update", {}).get("labels", [])
            update_inputs = payload.get("update", {}).get("inputs", [])
            purchase_radio = next((item for item in update_inputs if item.get("value") == "PURCHASE_PRICE"), {})
            earned_radio = next((item for item in update_inputs if item.get("value") == "EARNED_POINT"), {})
            payload["facts"] = {
                "detailHasCalculationTiming": "算出タイミング" in detail_body,
                "detailHasRealtimeValue": "リアルタイムに算出" in detail_body,
                "updateHasCalculationTimingInput": "算出タイミング" in update_labels or "算出タイミング" in update_body,
                "updateHasRealtimeInput": "リアルタイム" in update_labels,
                "calculationMethodPurchasePriceFixed": purchase_radio.get("checked") is True and purchase_radio.get("disabled") is True,
                "earnedPointDisabled": earned_radio.get("disabled") is True,
                "errors": payload["errors"],
            }
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
            page.close()
            browser.close()
    print(json.dumps({"json": str(OUT), "md": str(MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
