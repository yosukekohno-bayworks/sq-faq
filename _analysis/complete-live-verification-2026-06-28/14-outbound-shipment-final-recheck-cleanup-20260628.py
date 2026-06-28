#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "14-outbound-shipment-carrier-tracking-20260628.json"
OUT_MD = OUT_DIR / "14-outbound-shipment-carrier-tracking-20260628.md"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

LONG_TOKEN_RE = re.compile(r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))")


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
            const nodes = (selector, limit = 120) => Array.from(document.querySelectorAll(selector)).slice(0, limit);
            const body = document.body ? document.body.innerText : '';
            return {
                url: location.href,
                h1: nodes('h1', 10).map(textOf).filter(Boolean),
                h2: nodes('h2', 30).map(textOf).filter(Boolean),
                rows: nodes('tr', 120).map(textOf).filter(Boolean),
                controls: nodes('button, a, input, textarea, select, [role="button"]', 260)
                    .map((el) => ({
                        tag: el.tagName.toLowerCase(),
                        text: textOf(el),
                        href: el.getAttribute('href'),
                        type: el.getAttribute('type'),
                        ariaDisabled: el.getAttribute('aria-disabled'),
                        disabled: !!el.disabled,
                        value: el.tagName.toLowerCase() === 'input' || el.tagName.toLowerCase() === 'select' ? el.value : undefined
                    }))
                    .filter((x) => x.text || x.href || x.value),
                body
            };
        }"""
    )
    data["body"] = compact(data.get("body", ""), limit)
    return redact(data)


def contains_in_snapshot(snap, needle):
    if not needle:
        return False
    if needle in snap.get("body", ""):
        return True
    for control in snap.get("controls", []):
        if needle in str(control.get("value") or "") or needle in str(control.get("text") or ""):
            return True
    for row in snap.get("rows", []):
        if needle in row:
            return True
    return False


def open_snapshot(page, route):
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    return snapshot(page)


def inspect_lists(page, outbound_code, carrier, tracking):
    result = {}
    for name, route in {
        "all": "/admin/inventory_outbound_orders",
        "complete": "/admin/inventory_outbound_orders?tab=complete",
    }.items():
        snap = open_snapshot(page, route)
        snap["matchingRows"] = [row for row in snap.get("rows", []) if outbound_code and outbound_code in row]
        snap["containsCarrier"] = contains_in_snapshot(snap, carrier)
        snap["containsTrackingCode"] = contains_in_snapshot(snap, tracking)
        result[name] = snap
    return redact(result)


def complete_inbound(page, inbound_route):
    result = {"route": inbound_route, "steps": {}, "completed": False, "error": None}
    if not inbound_route:
        result["error"] = "inbound route missing"
        return result
    result["steps"]["before"] = open_snapshot(page, inbound_route)
    if "入荷完了" in result["steps"]["before"].get("body", ""):
        result["completed"] = True
        return result

    link = page.get_by_text("入荷指示を一括受領で完了する", exact=True)
    if not link.count():
        result["error"] = "bulk complete link not found"
        return result
    link.first.click()
    wait_quiet(page, timeout=10000)
    if page.locator('div[role="dialog"]').count():
        dialog = page.locator('div[role="dialog"]').last
        result["steps"]["dialog"] = compact(dialog.inner_text(timeout=5000), 3000)
        for name in ["完了する", "登録する", "実行する", "保存する"]:
            button = dialog.get_by_role("button", name=name, exact=True)
            if button.count():
                button.first.click()
                wait_quiet(page, timeout=12000)
                break
    if page.get_by_role("button", name="登録する", exact=True).count() and "入荷完了" not in (page.locator("body").inner_text(timeout=5000)):
        page.get_by_role("button", name="登録する", exact=True).first.click()
        wait_quiet(page, timeout=12000)
    result["steps"]["afterClick"] = snapshot(page)
    page.goto(BASE + inbound_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["afterReload"] = snapshot(page)
    result["completed"] = "入荷完了" in result["steps"]["afterReload"].get("body", "")
    if not result["completed"]:
        receive_route = inbound_route.rstrip("/") + "/receive"
        page.goto(BASE + receive_route, wait_until="load", timeout=35000)
        wait_quiet(page)
        result["steps"]["receiveFormBefore"] = snapshot(page)
        number_inputs = page.locator('input[type="number"]')
        if number_inputs.count():
            number_inputs.last.fill("1")
            page.wait_for_timeout(500)
            result["steps"]["receiveFormAfterFill"] = snapshot(page)
            page.get_by_role("button", name="登録する", exact=True).first.click()
            wait_quiet(page, timeout=12000)
            result["steps"]["receiveAfterSubmit"] = snapshot(page)
            page.goto(BASE + inbound_route, wait_until="load", timeout=35000)
            wait_quiet(page)
            result["steps"]["afterReceiveReload"] = snapshot(page)
            result["completed"] = "入荷完了" in result["steps"]["afterReceiveReload"].get("body", "")
        else:
            result["error"] = "receive number input not found"
    return redact(result)


def update_md(payload):
    facts = payload.get("facts", {})
    inputs = payload.get("inputs", {})
    lines = [
        "# 出荷実績登録（配送キャリア・追跡コードあり）実機確認",
        "",
        f"- 実行日時: {payload.get('generatedAt')}",
        f"- 最終再確認: {payload.get('finalRecheckedAt')}",
        f"- 対象SKU: `{inputs.get('sku')}`",
        f"- 移動元: `{inputs.get('sourceLocation')}`",
        f"- 移動先: `{inputs.get('destinationLocation')}`",
        f"- 移動伝票: `{facts.get('movementCode')}` / 出荷指示: `{facts.get('outboundCode')}` / 入荷指示: `{facts.get('inboundCode')}`",
        f"- 入力した配送キャリア: `{inputs.get('carrier')}`",
        f"- 入力した追跡コード: `{inputs.get('trackingCode')}`",
        "",
        "## 確認結果",
        "",
        f"- 出荷実績登録後に `#IO-1026` は出荷完了になった: `{facts.get('outboundCompleted')}`",
        f"- 出荷指示詳細の最終再ロード画面に配送キャリアが表示される: `{facts.get('finalDetailContainsCarrier')}`",
        f"- 出荷指示詳細の最終再ロード画面に追跡コードが表示される: `{facts.get('finalDetailContainsTrackingCode')}`",
        f"- 出荷管理「すべて」一覧に配送キャリアが表示される: `{facts.get('allListContainsCarrier')}`",
        f"- 出荷管理「すべて」一覧に追跡コードが表示される: `{facts.get('allListContainsTrackingCode')}`",
        f"- 出荷管理「出荷完了」一覧に配送キャリアが表示される: `{facts.get('completeListContainsCarrier')}`",
        f"- 出荷管理「出荷完了」一覧に追跡コードが表示される: `{facts.get('completeListContainsTrackingCode')}`",
        f"- 関連入荷指示を一括受領で完了した: `{facts.get('inboundCleanupCompleted')}`",
        "- ヤマトB2条件指定エクスポート画面は表示確認のみ。CSV実ファイルのメール受信・中身確認は未実行。",
        "",
        "## 一覧の対象行",
        "",
        "### すべて",
        "",
    ]
    lines.extend([f"- {row}" for row in facts.get("allListMatchingRows", [])] or ["- 対象行なし"])
    lines.extend(["", "### 出荷完了", ""])
    lines.extend([f"- {row}" for row in facts.get("completeListMatchingRows", [])] or ["- 対象行なし"])
    lines.extend(["", "## 証跡", "", f"- JSON: `{OUT_JSON.relative_to(ROOT)}`"])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    payload = json.loads(OUT_JSON.read_text())
    inputs = payload.get("inputs", {})
    carrier = inputs.get("carrier", "")
    tracking = inputs.get("trackingCode", "")
    outbound_route = payload.get("outboundRoute")
    inbound_route = payload.get("inboundRoute")
    movement_route = payload.get("movementRoute")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            payload.setdefault("steps", {})["outboundFinalReload"] = open_snapshot(page, outbound_route)
            payload["steps"]["outboundListsFinalReload"] = inspect_lists(page, payload.get("outboundCode"), carrier, tracking)
            payload["steps"]["completeInboundCleanupFinal"] = complete_inbound(page, inbound_route)
            payload["steps"]["movementFinalReload"] = open_snapshot(page, movement_route)
            payload["finalRecheckedAt"] = datetime.now(timezone.utc).isoformat()
        finally:
            page.close()
            browser.close()

    outbound_final = payload["steps"]["outboundFinalReload"]
    list_final = payload["steps"]["outboundListsFinalReload"]
    facts = payload.setdefault("facts", {})
    facts["outboundCompleted"] = "出荷完了" in outbound_final.get("body", "")
    facts["finalDetailContainsCarrier"] = contains_in_snapshot(outbound_final, carrier)
    facts["finalDetailContainsTrackingCode"] = contains_in_snapshot(outbound_final, tracking)
    facts["allListContainsCarrier"] = bool(list_final["all"].get("containsCarrier"))
    facts["allListContainsTrackingCode"] = bool(list_final["all"].get("containsTrackingCode"))
    facts["completeListContainsCarrier"] = bool(list_final["complete"].get("containsCarrier"))
    facts["completeListContainsTrackingCode"] = bool(list_final["complete"].get("containsTrackingCode"))
    facts["allListMatchingRows"] = list_final["all"].get("matchingRows", [])
    facts["completeListMatchingRows"] = list_final["complete"].get("matchingRows", [])
    facts["inboundCleanupCompleted"] = bool(payload["steps"]["completeInboundCleanupFinal"].get("completed"))

    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2))
    update_md(payload)
    print(json.dumps({
        "json": str(OUT_JSON),
        "md": str(OUT_MD),
        "facts": facts,
        "inboundCleanup": payload["steps"]["completeInboundCleanupFinal"].get("completed"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
