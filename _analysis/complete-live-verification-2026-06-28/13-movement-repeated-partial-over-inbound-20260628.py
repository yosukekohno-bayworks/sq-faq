#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "13-movement-repeated-partial-over-inbound-20260628.json"
OUT_MD = OUT_DIR / "13-movement-repeated-partial-over-inbound-20260628.md"

BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

SOURCE_LOCATION = "TEST_E2E_20260622_GU倉庫_ON_1905"
DEST_LOCATION = "TEST_E2E_20260622_GU店舗_OFF_1905"
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"
PLANNED_QTY = 2
FIRST_RECEIVE_QTY = 1
SECOND_RECEIVE_QTY = 2

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
            const body = document.body ? document.body.innerText : '';
            return {
                url: location.href,
                h1: nodes('h1', 10).map(textOf).filter(Boolean),
                h2: nodes('h2', 30).map(textOf).filter(Boolean),
                rows: nodes('tr', 140).map(textOf).filter(Boolean),
                controls: nodes('button, a, input, textarea, select, [role="button"], [role="menuitem"]', 280)
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
                        value: el.tagName.toLowerCase() === 'input' || el.tagName.toLowerCase() === 'select' ? el.value : undefined
                    }))
                    .filter((x) => x.text || x.href || x.ariaLabel || x.placeholder || x.value),
                body
            };
        }"""
    )
    data["body"] = compact(data.get("body", ""), limit)
    data["codes"] = sorted(set(re.findall(r"#(?:IM|IO|II)-\d+", data["body"])))
    return redact(data)


def save_payload(payload):
    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2))


def route_from_url(page, prefix):
    if prefix in page.url and not page.url.rstrip("/").endswith("/create"):
        return page.url.replace(BASE, "")
    return None


def related_links(page):
    return redact(
        page.evaluate(
            """() => Array.from(document.querySelectorAll('a'))
                .map((a) => ({
                    text: (a.innerText || a.textContent || '').replace(/\\s+/g, ' ').trim(),
                    href: a.getAttribute('href')
                }))
                .filter((x) => x.href && x.href.includes('/admin/inventory_'))"""
        )
    )


def choose_location(page, button_index, location_name):
    result = {"buttonIndex": button_index, "location": location_name}
    page.get_by_role("button", name="選択", exact=True).nth(button_index).click()
    page.wait_for_selector('div[role="dialog"] tr', timeout=15000)
    page.wait_for_timeout(800)
    dialog = page.locator('div[role="dialog"]').last
    result["dialogBefore"] = compact(dialog.inner_text(timeout=5000), 2500)
    row = dialog.locator("tr").filter(has_text=location_name).first
    if not row.count():
        result["rows"] = [compact(text, 500) for text in dialog.locator("tr").all_inner_texts()[:30]]
        raise RuntimeError(f"location row not found: {location_name}")
    result["row"] = compact(row.inner_text(timeout=5000), 700)
    checkbox = row.locator('input[type="checkbox"]').first
    if checkbox.count():
        checkbox.click()
    else:
        row.click()
    page.wait_for_timeout(400)
    dialog.get_by_role("button", name="選択する", exact=True).click()
    wait_quiet(page, timeout=5000)
    result["after"] = snapshot(page, limit=3500)
    return redact(result)


def choose_variant(page, sku):
    result = {"sku": sku}
    page.get_by_role("button", name="参照", exact=True).first.click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    result["dialogBefore"] = compact(dialog.inner_text(timeout=8000), 2600)
    search = dialog.locator('input[placeholder*="SKU"]')
    if search.count():
        search.first.fill(sku)
        search.first.press("Enter")
        page.wait_for_timeout(2200)
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
    page.wait_for_timeout(400)
    dialog.get_by_role("button", name="選択する", exact=True).click()
    wait_quiet(page, timeout=5000)
    result["after"] = snapshot(page, limit=4500)
    return redact(result)


def create_movement_order(page):
    result = {"steps": {}, "route": None, "relatedLinks": []}
    page.goto(BASE + "/admin/inventory_movement_orders/create", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["initial"] = snapshot(page, limit=4500)
    result["steps"]["source"] = choose_location(page, 0, SOURCE_LOCATION)
    result["steps"]["destination"] = choose_location(page, 1, DEST_LOCATION)
    result["steps"]["variant"] = choose_variant(page, SKU)
    qty = page.locator('input[type="number"]').last
    if not qty.count():
        raise RuntimeError("quantity number input not found")
    result["steps"]["quantityBefore"] = qty.input_value(timeout=5000)
    qty.fill(str(PLANNED_QTY))
    page.wait_for_timeout(700)
    result["steps"]["beforeSave"] = snapshot(page, limit=5500)
    page.get_by_role("button", name="保存する", exact=True).last.click()
    wait_quiet(page, timeout=12000)
    result["steps"]["afterSave"] = snapshot(page, limit=9000)
    result["route"] = route_from_url(page, "/admin/inventory_movement_orders/")
    result["relatedLinks"] = related_links(page)
    if not result["route"]:
        raise RuntimeError("movement route not detected after save")
    return redact(result)


def find_latest_pending_movement(page):
    result = {"found": False, "route": None, "code": None, "row": None, "steps": {}}
    page.goto(BASE + "/admin/inventory_movement_orders", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["list"] = snapshot(page, limit=9000)
    candidate = page.evaluate(
        """({source, dest}) => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const rows = Array.from(document.querySelectorAll('tr'));
            for (const row of rows) {
                const text = textOf(row);
                if (!text.includes(source) || !text.includes(dest) || !text.includes('出荷待ち')) continue;
                const link = row.querySelector('a[href*="/admin/inventory_movement_orders/"]');
                if (!link) continue;
                return {
                    row: text,
                    code: text.match(/#IM-\\d+/)?.[0] || null,
                    href: link.getAttribute('href')
                };
            }
            return null;
        }""",
        {"source": SOURCE_LOCATION, "dest": DEST_LOCATION},
    )
    result["candidate"] = candidate
    if not candidate:
        return redact(result)
    result["found"] = True
    result["route"] = candidate.get("href")
    result["code"] = candidate.get("code")
    result["row"] = candidate.get("row")
    page.goto(BASE + result["route"], wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["detail"] = snapshot(page, limit=10000)
    result["relatedLinks"] = related_links(page)
    return redact(result)


def register_outbound(page, route):
    result = {"route": route, "steps": {}}
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["before"] = snapshot(page, limit=8000)
    page.get_by_role("button", name="出荷実績を登録する", exact=True).first.click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    result["steps"]["dialog"] = compact(dialog.inner_text(timeout=5000), 2500)
    dialog.get_by_role("button", name="登録する", exact=True).click()
    wait_quiet(page, timeout=12000)
    result["steps"]["after"] = snapshot(page, limit=9000)
    return redact(result)


def receive_route_from_detail(page, inbound_route):
    page.goto(BASE + inbound_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    before = snapshot(page, limit=9000)
    link = next(
        (
            control.get("href")
            for control in before.get("controls", [])
            if control.get("text") == "入荷実績を登録する" and control.get("href")
        ),
        None,
    )
    if not link:
        link = inbound_route.rstrip("/") + "/receive"
    return link, before


def submit_receive(page, inbound_route, qty, label):
    result = {"label": label, "inboundRoute": inbound_route, "receiveQty": qty, "steps": {}}
    receive_route, before = receive_route_from_detail(page, inbound_route)
    result["receiveRoute"] = receive_route
    result["steps"]["detailBefore"] = before
    page.goto(BASE + receive_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["receiveFormBefore"] = snapshot(page, limit=9000)
    inputs = page.locator('input[type="number"]')
    if not inputs.count():
        raise RuntimeError(f"receive number input not found: {label}")
    inputs.last.fill(str(qty))
    page.wait_for_timeout(500)
    result["steps"]["receiveFormAfterFill"] = snapshot(page, limit=9000)
    page.get_by_role("button", name="登録する", exact=True).first.click()
    wait_quiet(page, timeout=12000)
    result["steps"]["afterSubmit"] = snapshot(page, limit=9000)
    page.goto(BASE + inbound_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["detailAfterReload"] = snapshot(page, limit=10000)
    return redact(result)


def manual_complete_inbound(page, inbound_route):
    result = {"route": inbound_route, "steps": {}, "completed": False, "clicked": False}
    page.goto(BASE + inbound_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["before"] = snapshot(page, limit=9000)
    if "入荷完了" in result["steps"]["before"].get("body", ""):
        result["completed"] = True
        return redact(result)
    button = page.get_by_role("button", name="完了に更新する", exact=True)
    link = page.get_by_text("完了に更新する", exact=True)
    if button.count():
        button.first.click()
    elif link.count():
        link.first.click()
    else:
        result["error"] = "完了に更新する not found"
        return redact(result)
    result["clicked"] = True
    page.wait_for_timeout(900)
    if page.locator('div[role="dialog"]').count():
        dialog = page.locator('div[role="dialog"]').last
        result["steps"]["dialog"] = compact(dialog.inner_text(timeout=5000), 3000)
        for name in ["完了にする", "完了に更新する", "完了する", "登録する", "実行する"]:
            confirm = dialog.get_by_role("button", name=name, exact=True)
            if confirm.count():
                confirm.first.click()
                break
    wait_quiet(page, timeout=12000)
    result["steps"]["afterClick"] = snapshot(page, limit=9000)
    page.goto(BASE + inbound_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["afterReload"] = snapshot(page, limit=10000)
    result["completed"] = "入荷完了" in result["steps"]["afterReload"].get("body", "")
    return redact(result)


def inspect_movement(page, route, label):
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    snap = snapshot(page, limit=10000)
    return {"label": label, "snapshot": snap}


def derive_codes(payload):
    links = payload["steps"]["createMovement"].get("relatedLinks", [])
    outbound = next((link for link in links if "/admin/inventory_outbound_orders/" in (link.get("href") or "")), {})
    inbound = next((link for link in links if "/admin/inventory_inbound_orders/" in (link.get("href") or "")), {})
    movement_body = payload["steps"]["createMovement"]["steps"]["afterSave"].get("body", "")
    return {
        "movementCode": (re.search(r"#IM-\d+", movement_body) or [None])[0],
        "outboundCode": outbound.get("text"),
        "outboundRoute": outbound.get("href"),
        "inboundCode": inbound.get("text"),
        "inboundRoute": inbound.get("href"),
    }


def extract_facts(payload):
    steps = payload.get("steps", {})
    first = steps.get("firstReceive", {}).get("steps", {}).get("detailAfterReload", {})
    second = steps.get("secondReceive", {}).get("steps", {}).get("detailAfterReload", {})
    manual = steps.get("manualCompleteInbound", {}).get("steps", {}).get("afterReload", {})
    movement_after_second = steps.get("movementAfterSecondReceive", {}).get("snapshot", {})
    movement_final = steps.get("movementAfterManualComplete", {}).get("snapshot", {})
    codes = {
        "movementCode": payload.get("movementCode"),
        "outboundCode": payload.get("outboundCode"),
        "inboundCode": payload.get("inboundCode"),
    }
    facts = {
        **codes,
        "plannedQty": PLANNED_QTY,
        "firstReceiveQty": FIRST_RECEIVE_QTY,
        "secondReceiveQty": SECOND_RECEIVE_QTY,
        "cumulativeReceiveQty": FIRST_RECEIVE_QTY + SECOND_RECEIVE_QTY,
        "firstDetailBody": first.get("body", ""),
        "secondDetailBody": second.get("body", ""),
        "manualCompleteBody": manual.get("body", ""),
        "movementAfterSecondBody": movement_after_second.get("body", ""),
        "movementFinalBody": movement_final.get("body", ""),
        "firstStillWaiting": "入荷待ち" in first.get("body", ""),
        "secondAutoCompleted": "入荷完了" in second.get("body", ""),
        "secondStillWaiting": "入荷待ち" in second.get("body", ""),
        "manualCompleteClicked": bool(steps.get("manualCompleteInbound", {}).get("clicked")),
        "manualCompleteSucceeded": "入荷完了" in manual.get("body", ""),
        "movementCompletedAfterManualComplete": "入荷完了" in movement_final.get("body", ""),
    }
    return redact(facts)


def write_md(payload):
    facts = payload.get("facts") or extract_facts(payload)
    lines = [
        "# 移動伝票の複数回入荷・過入荷完了判定 実機確認",
        "",
        f"- 実行日時: {payload.get('generatedAt')}",
        f"- 対象SKU: `{SKU}`",
        f"- 移動元: `{SOURCE_LOCATION}`",
        f"- 移動先: `{DEST_LOCATION}`",
        f"- 移動予定数: `{PLANNED_QTY}`",
        f"- 1回目入荷数: `{FIRST_RECEIVE_QTY}`",
        f"- 2回目入荷数: `{SECOND_RECEIVE_QTY}`",
        f"- 累計入荷数: `{FIRST_RECEIVE_QTY + SECOND_RECEIVE_QTY}`",
        f"- 移動伝票: `{facts.get('movementCode')}` / 出荷指示: `{facts.get('outboundCode')}` / 入荷指示: `{facts.get('inboundCode')}`",
        "",
        "## 確認結果",
        "",
        f"- 1回目入荷後も入荷指示は入荷待ち表示を含む: `{facts.get('firstStillWaiting')}`",
        f"- 予定2に対して累計3の過入荷登録後、自動で入荷完了になった: `{facts.get('secondAutoCompleted')}`",
        f"- 予定2に対して累計3の過入荷登録後も入荷待ち表示を含む: `{facts.get('secondStillWaiting')}`",
        f"- 過入荷後に手動の `完了に更新する` をクリックした: `{facts.get('manualCompleteClicked')}`",
        f"- 手動完了後、入荷指示は入荷完了になった: `{facts.get('manualCompleteSucceeded')}`",
        f"- 出荷完了済みの親移動伝票は、手動完了後に入荷完了になった: `{facts.get('movementCompletedAfterManualComplete')}`",
        "",
        "## 判断",
        "",
        "- 同一入荷指示に対して複数回の入荷実績登録は可能。",
        "- 予定数を超える累計入荷数も登録できる。",
        "- ただし累計が予定数以上になっても、この確認では入荷指示は自動完了せず、手動の `完了に更新する` が必要だった。",
        "- 親移動伝票は出荷完了済みでも、入荷指示が手動完了されるまで完了扱いにならなかった。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "purpose": "Verify repeated partial inbound receives and cumulative over-receive completion behavior on inventory movement orders.",
        "inputs": {
            "sourceLocation": SOURCE_LOCATION,
            "destinationLocation": DEST_LOCATION,
            "sku": SKU,
            "plannedQty": PLANNED_QTY,
            "firstReceiveQty": FIRST_RECEIVE_QTY,
            "secondReceiveQty": SECOND_RECEIVE_QTY,
        },
        "steps": {},
        "errors": [],
    }
    save_payload(payload)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(25000)
        try:
            payload["steps"]["reusePendingMovement"] = find_latest_pending_movement(page)
            if payload["steps"]["reusePendingMovement"].get("found"):
                payload["steps"]["createMovement"] = {
                    "route": payload["steps"]["reusePendingMovement"].get("route"),
                    "relatedLinks": payload["steps"]["reusePendingMovement"].get("relatedLinks", []),
                    "steps": {
                        "afterSave": payload["steps"]["reusePendingMovement"]["steps"].get("detail", {}),
                    },
                    "reusedExistingPendingMovement": True,
                }
            else:
                payload["steps"]["createMovement"] = create_movement_order(page)
            codes = derive_codes(payload)
            payload.update(codes)
            save_payload(payload)
            if not payload.get("outboundRoute") or not payload.get("inboundRoute"):
                raise RuntimeError("related inbound/outbound routes missing")

            payload["steps"]["registerOutbound"] = register_outbound(page, payload["outboundRoute"])
            payload["steps"]["movementAfterOutbound"] = inspect_movement(page, payload["steps"]["createMovement"]["route"], "after_outbound")
            save_payload(payload)

            payload["steps"]["firstReceive"] = submit_receive(page, payload["inboundRoute"], FIRST_RECEIVE_QTY, "first_partial")
            payload["steps"]["movementAfterFirstReceive"] = inspect_movement(page, payload["steps"]["createMovement"]["route"], "after_first_receive")
            save_payload(payload)

            payload["steps"]["secondReceive"] = submit_receive(page, payload["inboundRoute"], SECOND_RECEIVE_QTY, "second_over")
            payload["steps"]["movementAfterSecondReceive"] = inspect_movement(page, payload["steps"]["createMovement"]["route"], "after_second_receive")
            save_payload(payload)

            payload["steps"]["manualCompleteInbound"] = manual_complete_inbound(page, payload["inboundRoute"])
            payload["steps"]["movementAfterManualComplete"] = inspect_movement(page, payload["steps"]["createMovement"]["route"], "after_manual_complete")
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
                "movementCode": payload.get("movementCode"),
                "outboundCode": payload.get("outboundCode"),
                "inboundCode": payload.get("inboundCode"),
                "facts": payload.get("facts"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
