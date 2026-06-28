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

SOURCE_LOCATION = "TEST_E2E_20260622_GU倉庫_ON_1905"
DEST_LOCATION = "TEST_E2E_20260622_GU店舗_OFF_1905"
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"
CARRIER = f"FAQCarrier-{datetime.now().strftime('%Y%m%d%H%M%S')}"
TRACKING_CODE = f"FAQTRACK-{datetime.now().strftime('%Y%m%d%H%M%S')}"

LONG_TOKEN_RE = re.compile(r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))")


def redact(value):
    if isinstance(value, str):
        return LONG_TOKEN_RE.sub("[REDACTED_LONG_VALUE]", value)
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    return value


def compact(text, limit=4500):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def snapshot(page, limit=6000):
    data = page.evaluate(
        """() => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const attr = (el, name) => el.getAttribute(name);
            const nodes = (selector, limit = 120) => Array.from(document.querySelectorAll(selector)).slice(0, limit);
            const controls = nodes('button, a, input, textarea, select, [role="button"], [role="menuitem"]', 260)
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
                .filter((x) => x.text || x.href || x.ariaLabel || x.placeholder || x.value);
            const rows = nodes('tr', 100).map(textOf).filter(Boolean);
            const links = nodes('a', 220).map((el) => ({text: textOf(el), href: attr(el, 'href')}))
                .filter((x) => x.href || x.text);
            const body = document.body ? document.body.innerText : '';
            return {
                url: location.href,
                h1: nodes('h1', 10).map(textOf).filter(Boolean),
                h2: nodes('h2', 30).map(textOf).filter(Boolean),
                controls,
                rows,
                links,
                body
            };
        }"""
    )
    body = data.get("body", "")
    data["body"] = compact(body, limit)
    data["codes"] = sorted(set(re.findall(r"#(?:IM|IO|II)-\\d+", body)))
    return redact(data)


def save_payload(payload):
    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2))


def route_from_url(page, prefix):
    if prefix in page.url and not page.url.rstrip("/").endswith("/create"):
        return page.url.replace(BASE, "")
    return None


def route_from_links(page, route_prefix):
    links = page.evaluate(
        """(routePrefix) => Array.from(document.querySelectorAll('a'))
            .map((a) => ({text: (a.innerText || a.textContent || '').replace(/\\s+/g, ' ').trim(), href: a.getAttribute('href')}))
            .filter((x) => x.href && x.href.includes(routePrefix))""",
        route_prefix,
    )
    return redact(links)


def find_pending_test_movement(page):
    result = {"found": False, "route": None, "code": None, "steps": {}}
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
                return {text, code: text.match(/#IM-\\d+/)?.[0] || null, href: link.getAttribute('href')};
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
    page.goto(BASE + result["route"], wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["detail"] = snapshot(page, limit=8000)
    result["relatedLinks"] = route_from_links(page, "/admin/inventory_")
    return redact(result)


def choose_location(page, button_index, location_name):
    result = {"location": location_name, "buttonIndex": button_index, "ok": False}
    page.get_by_role("button", name="選択", exact=True).nth(button_index).click()
    page.wait_for_selector('div[role="dialog"] tr', timeout=15000)
    page.wait_for_timeout(900)
    dialog = page.locator('div[role="dialog"]').last
    result["dialogBefore"] = compact(dialog.inner_text(timeout=5000), 2600)
    row = dialog.locator("tr").filter(has_text=location_name).first
    if not row.count():
        result["rows"] = [compact(row_text, 400) for row_text in dialog.locator("tr").all_inner_texts()[:30]]
        raise RuntimeError(f"location row not found: {location_name}")
    result["row"] = compact(row.inner_text(timeout=5000), 700)
    checkbox = row.locator('input[type="checkbox"]').first
    if checkbox.count():
        checkbox.click()
    else:
        row.click()
    page.wait_for_timeout(500)
    dialog.get_by_role("button", name="選択する", exact=True).click()
    wait_quiet(page, timeout=5000)
    result["after"] = snapshot(page, limit=3500)
    result["ok"] = True
    return redact(result)


def choose_variant(page, sku):
    result = {"sku": sku, "ok": False}
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
        result["rows"] = [compact(row_text, 500) for row_text in dialog.locator("tr").all_inner_texts()[:40]]
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
    result["after"] = snapshot(page, limit=4500)
    result["ok"] = True
    return redact(result)


def create_movement_order(page):
    result = {"steps": {}, "route": None, "relatedLinks": [], "error": None}
    page.goto(BASE + "/admin/inventory_movement_orders/create", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["initial"] = snapshot(page, limit=4200)
    result["steps"]["source"] = choose_location(page, 0, SOURCE_LOCATION)
    result["steps"]["destination"] = choose_location(page, 1, DEST_LOCATION)
    result["steps"]["variant"] = choose_variant(page, SKU)
    qty = page.locator('input[type="number"]').last
    result["steps"]["quantityBefore"] = qty.input_value(timeout=5000) if qty.count() else None
    if not qty.count():
        raise RuntimeError("quantity number input not found")
    qty.fill("1")
    page.wait_for_timeout(700)
    result["steps"]["beforeSave"] = snapshot(page, limit=5200)
    page.get_by_role("button", name="保存する", exact=True).last.click()
    wait_quiet(page, timeout=12000)
    result["steps"]["afterSave"] = snapshot(page, limit=8000)
    result["route"] = route_from_url(page, "/admin/inventory_movement_orders/")
    if not result["route"]:
        result["steps"]["findAfterSave"] = find_pending_test_movement(page)
        result["route"] = result["steps"]["findAfterSave"].get("route")
    result["relatedLinks"] = route_from_links(page, "/admin/inventory_")
    if not result["route"]:
        raise RuntimeError("movement route not detected after save")
    return redact(result)


def fill_dialog_field(dialog, label, value, fallback_index):
    result = {"label": label, "value": value, "method": None}
    try:
        loc = dialog.get_by_label(label, exact=True)
        if loc.count():
            loc.first.fill(value)
            result["method"] = "label"
            return result
    except Exception as exc:
        result["labelError"] = repr(exc)
    inputs = dialog.locator('input[type="text"], textarea')
    if inputs.count() > fallback_index:
        inputs.nth(fallback_index).fill(value)
        result["method"] = f"fallback-text-input-{fallback_index}"
        return result
    raise RuntimeError(f"dialog field not found: {label}")


def register_outbound(page, outbound_route):
    result = {"route": outbound_route, "carrier": CARRIER, "trackingCode": TRACKING_CODE, "steps": {}, "error": None}
    page.goto(BASE + outbound_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["beforeRegister"] = snapshot(page, limit=7600)
    page.get_by_role("button", name="出荷実績を登録する", exact=True).first.click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    result["steps"]["dialogBefore"] = {"text": compact(dialog.inner_text(timeout=5000), 2600)}
    result["steps"]["fillCarrier"] = fill_dialog_field(dialog, "配送キャリア", CARRIER, 0)
    result["steps"]["fillTracking"] = fill_dialog_field(dialog, "追跡コード", TRACKING_CODE, 1)
    result["steps"]["dialogAfterFill"] = {"text": compact(dialog.inner_text(timeout=5000), 2600)}
    dialog.get_by_role("button", name="登録する", exact=True).click()
    wait_quiet(page, timeout=12000)
    result["steps"]["afterRegister"] = snapshot(page, limit=9000)
    return redact(result)


def inspect_outbound_lists(page, outbound_code):
    result = {}
    for name, route in {
        "all": "/admin/inventory_outbound_orders",
        "complete": "/admin/inventory_outbound_orders?tab=complete",
    }.items():
        page.goto(BASE + route, wait_until="load", timeout=35000)
        wait_quiet(page)
        snap = snapshot(page, limit=9000)
        snap["matchingRows"] = [row for row in snap.get("rows", []) if outbound_code and outbound_code in row]
        snap["bodyContainsCarrier"] = CARRIER in snap.get("body", "")
        snap["bodyContainsTrackingCode"] = TRACKING_CODE in snap.get("body", "")
        result[name] = snap
    return redact(result)


def complete_inbound_for_cleanup(page, inbound_route):
    result = {"route": inbound_route, "steps": {}, "error": None}
    if not inbound_route:
        result["error"] = "inbound route not supplied"
        return result
    page.goto(BASE + inbound_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["beforeRegister"] = snapshot(page, limit=7600)
    buttons = page.get_by_role("button", name="入荷実績を登録する", exact=True)
    if not buttons.count():
        result["error"] = "入荷実績を登録する button not found"
        return result
    buttons.first.click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    result["steps"]["dialog"] = {"text": compact(dialog.inner_text(timeout=5000), 2600)}
    dialog.get_by_role("button", name="登録する", exact=True).click()
    wait_quiet(page, timeout=12000)
    result["steps"]["afterRegister"] = snapshot(page, limit=7600)
    return redact(result)


def inspect_export_form(page):
    page.goto(BASE + "/admin/inventory_outbound_orders/export/yamato_b2_cloud", wait_until="load", timeout=35000)
    wait_quiet(page)
    snap = snapshot(page, limit=7000)
    snap["executed"] = False
    return redact(snap)


def derive_facts(payload):
    outbound_code = payload.get("outboundCode")
    detail_after = payload.get("steps", {}).get("registerOutbound", {}).get("steps", {}).get("afterRegister", {})
    list_all = payload.get("steps", {}).get("outboundListsAfterRegister", {}).get("all", {})
    list_complete = payload.get("steps", {}).get("outboundListsAfterRegister", {}).get("complete", {})
    body = detail_after.get("body", "")
    facts = {
        "outboundCode": outbound_code,
        "movementCode": payload.get("movementCode"),
        "inboundCode": payload.get("inboundCode"),
        "detailContainsCarrier": CARRIER in body,
        "detailContainsTrackingCode": TRACKING_CODE in body,
        "allListContainsCarrier": bool(list_all.get("bodyContainsCarrier")),
        "allListContainsTrackingCode": bool(list_all.get("bodyContainsTrackingCode")),
        "completeListContainsCarrier": bool(list_complete.get("bodyContainsCarrier")),
        "completeListContainsTrackingCode": bool(list_complete.get("bodyContainsTrackingCode")),
        "completeListMatchingRows": list_complete.get("matchingRows", []),
        "allListMatchingRows": list_all.get("matchingRows", []),
    }
    return facts


def write_md(payload):
    facts = payload.get("facts") or derive_facts(payload)
    lines = [
        "# 出荷実績登録（配送キャリア・追跡コードあり）実機確認",
        "",
        f"- 実行日時: {payload.get('generatedAt')}",
        f"- 対象SKU: `{SKU}`",
        f"- 移動元: `{SOURCE_LOCATION}`",
        f"- 移動先: `{DEST_LOCATION}`",
        f"- 移動伝票: `{facts.get('movementCode')}` / 出荷指示: `{facts.get('outboundCode')}` / 入荷指示: `{facts.get('inboundCode')}`",
        f"- 入力した配送キャリア: `{CARRIER}`",
        f"- 入力した追跡コード: `{TRACKING_CODE}`",
        "",
        "## 確認結果",
        "",
        f"- 出荷実績登録後の出荷指示詳細に配送キャリアが表示される: `{facts.get('detailContainsCarrier')}`",
        f"- 出荷実績登録後の出荷指示詳細に追跡コードが表示される: `{facts.get('detailContainsTrackingCode')}`",
        f"- 出荷管理「すべて」一覧本文に配送キャリアが表示される: `{facts.get('allListContainsCarrier')}`",
        f"- 出荷管理「すべて」一覧本文に追跡コードが表示される: `{facts.get('allListContainsTrackingCode')}`",
        f"- 出荷管理「出荷完了」一覧本文に配送キャリアが表示される: `{facts.get('completeListContainsCarrier')}`",
        f"- 出荷管理「出荷完了」一覧本文に追跡コードが表示される: `{facts.get('completeListContainsTrackingCode')}`",
        "- ヤマトB2条件指定エクスポート画面は表示確認のみ。CSV実ファイルのメール受信・中身確認はこのスクリプトでは未実行。",
        "",
        "## 一覧の対象行",
        "",
        "### すべて",
        "",
    ]
    all_rows = facts.get("allListMatchingRows") or []
    lines.extend([f"- {row}" for row in all_rows] or ["- 対象行なし"])
    lines.extend(["", "### 出荷完了", ""])
    complete_rows = facts.get("completeListMatchingRows") or []
    lines.extend([f"- {row}" for row in complete_rows] or ["- 対象行なし"])
    lines.extend(["", "## 証跡", "", f"- JSON: `{OUT_JSON.relative_to(ROOT)}`"])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "purpose": "Verify where outbound shipment carrier and tracking code appear after registering an outbound shipment result.",
        "inputs": {
            "sourceLocation": SOURCE_LOCATION,
            "destinationLocation": DEST_LOCATION,
            "sku": SKU,
            "carrier": CARRIER,
            "trackingCode": TRACKING_CODE,
        },
        "errors": [],
        "steps": {},
    }
    save_payload(payload)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(25000)
        try:
            payload["steps"]["reusePendingMovement"] = find_pending_test_movement(page)
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
            save_payload(payload)
            movement_route = payload["steps"]["createMovement"].get("route")
            if not movement_route:
                raise RuntimeError("movement route missing")
            payload["movementRoute"] = movement_route
            movement_h1 = " ".join(payload["steps"]["createMovement"]["steps"]["afterSave"].get("h1", []))
            payload["movementCode"] = re.search(r"#IM-\d+", movement_h1).group(0) if re.search(r"#IM-\d+", movement_h1) else None

            links = payload["steps"]["createMovement"].get("relatedLinks", [])
            outbound_links = [link for link in links if "/admin/inventory_outbound_orders/" in (link.get("href") or "")]
            inbound_links = [link for link in links if "/admin/inventory_inbound_orders/" in (link.get("href") or "")]
            if not outbound_links:
                raise RuntimeError("related outbound route missing")
            if not inbound_links:
                raise RuntimeError("related inbound route missing")
            payload["outboundRoute"] = outbound_links[0]["href"]
            payload["inboundRoute"] = inbound_links[0]["href"]
            payload["outboundCode"] = outbound_links[0].get("text")
            payload["inboundCode"] = inbound_links[0].get("text")

            payload["steps"]["registerOutbound"] = register_outbound(page, payload["outboundRoute"])
            after_codes = payload["steps"]["registerOutbound"]["steps"]["afterRegister"].get("codes", [])
            if not payload.get("outboundCode"):
                payload["outboundCode"] = next((code for code in after_codes if code.startswith("#IO-")), None)
            save_payload(payload)

            payload["steps"]["outboundListsAfterRegister"] = inspect_outbound_lists(page, payload.get("outboundCode"))
            payload["steps"]["yamatoExportFormNoExecution"] = inspect_export_form(page)
            save_payload(payload)

            payload["steps"]["completeInboundCleanup"] = complete_inbound_for_cleanup(page, payload.get("inboundRoute"))
            page.goto(BASE + movement_route, wait_until="load", timeout=35000)
            wait_quiet(page)
            payload["steps"]["movementAfterCleanup"] = snapshot(page, limit=8000)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            try:
                payload["steps"]["finalSnapshot"] = snapshot(page, limit=8000)
            except Exception:
                pass
        finally:
            payload["facts"] = derive_facts(payload)
            save_payload(payload)
            write_md(payload)
            page.close()
            browser.close()

    print(json.dumps({
        "json": str(OUT_JSON),
        "md": str(OUT_MD),
        "errors": payload["errors"],
        "movementCode": payload.get("movementCode"),
        "outboundCode": payload.get("outboundCode"),
        "inboundCode": payload.get("inboundCode"),
        "facts": payload.get("facts"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
