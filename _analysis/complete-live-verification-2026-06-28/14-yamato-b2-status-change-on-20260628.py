#!/usr/bin/env python3
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "14-yamato-b2-status-change-on-20260628.json"
OUT_MD = OUT_DIR / "14-yamato-b2-status-change-on-20260628.md"

BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

SOURCE_LOCATION = "TEST_E2E_20260622_GU倉庫_ON_1905"
DEST_LOCATION = "TEST_E2E_20260622_GU店舗_OFF_1905"
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"
QTY = 1

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


def compact(text, limit=7000):
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
                rows: nodes('tr', 160).map(textOf).filter(Boolean),
                controls: nodes('button, a, input, textarea, select, [role="button"], [role="menuitem"]', 300)
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
                        value: el.tagName.toLowerCase() === 'input' || el.tagName.toLowerCase() === 'select' ? el.value : undefined,
                        checked: el.tagName.toLowerCase() === 'input' && el.type === 'checkbox' ? el.checked : undefined
                    }))
                    .filter((x) => x.text || x.href || x.ariaLabel || x.placeholder || x.value || x.checked !== undefined),
                links: nodes('a', 260).map((el) => ({text: textOf(el), href: attr(el, 'href')}))
                    .filter((x) => x.href || x.text),
                body
            };
        }"""
    )
    data["body"] = compact(data.get("body", ""), limit)
    data["codes"] = sorted(set(re.findall(r"#(?:IM|IO|II)-\d+", data["body"])))
    return redact(data)


def open_snapshot(page, route, limit=8000):
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    return snapshot(page, limit=limit)


def save(payload):
    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2))


def route_from_url(page, prefix):
    if prefix in page.url and not page.url.rstrip("/").endswith("/create"):
        return page.url.replace(BASE, "")
    return None


def route_from_links(page, prefix):
    return page.evaluate(
        """(prefix) => Array.from(document.querySelectorAll('a'))
            .map((a) => ({
                text: (a.innerText || a.textContent || '').replace(/\\s+/g, ' ').trim(),
                href: a.getAttribute('href')
            }))
            .filter((x) => x.href && x.href.includes(prefix))""",
        prefix,
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
    result = {"steps": {}, "route": None, "outboundRoute": None, "inboundRoute": None}
    page.goto(BASE + "/admin/inventory_movement_orders/create", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["initial"] = snapshot(page, limit=4500)
    result["steps"]["source"] = choose_location(page, 0, SOURCE_LOCATION)
    result["steps"]["destination"] = choose_location(page, 1, DEST_LOCATION)
    result["steps"]["variant"] = choose_variant(page, SKU)
    qty = page.locator('input[type="number"]').last
    if not qty.count():
        raise RuntimeError("quantity input not found")
    result["steps"]["quantityBefore"] = qty.input_value(timeout=5000)
    qty.fill(str(QTY))
    page.wait_for_timeout(700)
    result["steps"]["beforeSave"] = snapshot(page, limit=5500)
    page.get_by_role("button", name="保存する", exact=True).last.click()
    wait_quiet(page, timeout=12000)
    result["steps"]["afterSave"] = snapshot(page, limit=9000)
    result["route"] = route_from_url(page, "/admin/inventory_movement_orders/")
    if not result["route"]:
        fallback = find_latest_pending_movement(page)
        result["steps"]["fallbackFindAfterSave"] = fallback
        if fallback.get("found"):
            result["route"] = fallback.get("route")
            result["outboundRoute"] = fallback.get("outboundRoute")
            result["inboundRoute"] = fallback.get("inboundRoute")
            return redact(result)
    if not result["route"]:
        raise RuntimeError("movement route not detected")
    links = route_from_links(page, "/admin/inventory_")
    result["relatedLinks"] = links
    for link in links:
        href = link.get("href") or ""
        if "/admin/inventory_outbound_orders/" in href and not result["outboundRoute"]:
            result["outboundRoute"] = href
        if "/admin/inventory_inbound_orders/" in href and not result["inboundRoute"]:
            result["inboundRoute"] = href
    if not result["outboundRoute"] or not result["inboundRoute"]:
        raise RuntimeError("related outbound/inbound route not detected")
    return redact(result)


def find_latest_pending_movement(page):
    result = {"found": False, "route": None, "outboundRoute": None, "inboundRoute": None, "steps": {}}
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
                return {text, href: link.getAttribute('href')};
            }
            return null;
        }""",
        {"source": SOURCE_LOCATION, "dest": DEST_LOCATION},
    )
    result["candidate"] = candidate
    if not candidate:
        return redact(result)
    result["found"] = True
    result["route"] = candidate["href"]
    page.goto(BASE + result["route"], wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["detail"] = snapshot(page, limit=9000)
    links = route_from_links(page, "/admin/inventory_")
    result["relatedLinks"] = links
    for link in links:
        href = link.get("href") or ""
        if "/admin/inventory_outbound_orders/" in href and not result["outboundRoute"]:
            result["outboundRoute"] = href
        if "/admin/inventory_inbound_orders/" in href and not result["inboundRoute"]:
            result["inboundRoute"] = href
    return redact(result)


def code_from_snapshot(snap, prefix):
    for code in snap.get("codes", []):
        if code.startswith(prefix):
            return code
    h1 = snap.get("h1", [])
    for text in h1:
        if text.startswith(prefix):
            return text
    return None


def matching_rows(page, route, code):
    snap = open_snapshot(page, route, limit=9000)
    snap["matchingRows"] = [row for row in snap.get("rows", []) if code and code in row]
    return snap


def fill_yamato_export_form(page, started_at):
    result = {"startedAt": started_at.isoformat(), "steps": {}}
    page.goto(BASE + "/admin/inventory_outbound_orders/export/yamato_b2_cloud", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["initial"] = snapshot(page, limit=9000)
    # Use a broad start date. The first run used a narrow window and did not hit
    # the newly created movement-origin outbound order.
    start = "2026-06-01T00:00"
    end = (started_at + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M")
    inputs = page.locator('input[type="datetime-local"]')
    if inputs.count() < 2:
        raise RuntimeError("datetime-local inputs not found")
    inputs.nth(0).fill(start)
    inputs.nth(1).fill(end)
    status = page.get_by_label("出荷作業ステータス", exact=True)
    if status.count():
        status.select_option(label="出荷待ち")
    else:
        page.locator("select").nth(1).select_option(label="出荷待ち")
    checkbox = page.get_by_label("CSVの出力後に出荷指示のステータスを出荷作業中に変更する", exact=True)
    if checkbox.count():
        checkbox.first.check()
    else:
        page.locator('input[type="checkbox"]').last.check()
    page.wait_for_timeout(600)
    result["formValues"] = {"start": start, "end": end, "status": "出荷待ち", "statusChange": True}
    result["steps"]["beforeSubmit"] = snapshot(page, limit=9000)
    page.get_by_role("button", name="実行する", exact=True).click()
    wait_quiet(page, timeout=15000)
    result["steps"]["afterSubmit"] = snapshot(page, limit=9000)
    return redact(result)


def wait_for_status(page, outbound_route, expected_text, attempts=16):
    result = {"expectedText": expected_text, "attempts": []}
    for idx in range(attempts):
        snap = open_snapshot(page, outbound_route, limit=9000)
        found = expected_text in snap.get("body", "")
        result["attempts"].append({"index": idx + 1, "found": found, "snapshot": snap})
        if found:
            result["found"] = True
            return redact(result)
        page.wait_for_timeout(3000)
    result["found"] = False
    return redact(result)


def fill_dialog_field(dialog, label, value, fallback_index):
    try:
        loc = dialog.get_by_label(label, exact=True)
        if loc.count():
            loc.first.fill(value)
            return {"label": label, "method": "label", "value": value}
    except Exception as exc:
        return {"label": label, "method": "error", "error": repr(exc), "value": value}
    inputs = dialog.locator('input[type="text"], textarea')
    if inputs.count() > fallback_index:
        inputs.nth(fallback_index).fill(value)
        return {"label": label, "method": f"fallback-{fallback_index}", "value": value}
    raise RuntimeError(f"field not found: {label}")


def register_outbound(page, outbound_route):
    carrier = f"FAQCarrier-YB2-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    tracking = f"FAQTRACK-YB2-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    result = {"route": outbound_route, "carrier": carrier, "tracking": tracking, "steps": {}}
    page.goto(BASE + outbound_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["before"] = snapshot(page, limit=9000)
    button = page.get_by_role("button", name="出荷実績を登録する", exact=True)
    if not button.count():
        result["skipped"] = True
        result["reason"] = "register button not found"
        return redact(result)
    button.first.click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    result["steps"]["dialogBefore"] = compact(dialog.inner_text(timeout=5000), 3000)
    result["steps"]["fillCarrier"] = fill_dialog_field(dialog, "配送キャリア", carrier, 0)
    result["steps"]["fillTracking"] = fill_dialog_field(dialog, "追跡コード", tracking, 1)
    result["steps"]["dialogAfterFill"] = compact(dialog.inner_text(timeout=5000), 3000)
    dialog.get_by_role("button", name="登録する", exact=True).click()
    wait_quiet(page, timeout=15000)
    result["steps"]["afterSubmit"] = snapshot(page, limit=9000)
    page.goto(BASE + outbound_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["afterReload"] = snapshot(page, limit=9000)
    result["completed"] = "出荷完了" in result["steps"]["afterReload"].get("body", "")
    return redact(result)


def complete_inbound(page, inbound_route):
    result = {"route": inbound_route, "steps": {}, "completed": False}
    page.goto(BASE + inbound_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["before"] = snapshot(page, limit=9000)
    if "入荷完了" in result["steps"]["before"].get("body", ""):
        result["completed"] = True
        return redact(result)
    receive_route = inbound_route.rstrip("/") + "/receive"
    page.goto(BASE + receive_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["receiveFormBefore"] = snapshot(page, limit=9000)
    number_inputs = page.locator('input[type="number"]')
    if not number_inputs.count():
        result["error"] = "receive quantity input not found"
        return redact(result)
    number_inputs.last.fill(str(QTY))
    page.wait_for_timeout(500)
    result["steps"]["receiveFormAfterFill"] = snapshot(page, limit=9000)
    page.get_by_role("button", name="登録する", exact=True).first.click()
    wait_quiet(page, timeout=15000)
    result["steps"]["afterSubmit"] = snapshot(page, limit=9000)
    page.goto(BASE + inbound_route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["afterReload"] = snapshot(page, limit=9000)
    result["completed"] = "入荷完了" in result["steps"]["afterReload"].get("body", "")
    return redact(result)


def build_md(payload):
    facts = payload.get("facts", {})
    lines = [
        "# ヤマトB2条件指定エクスポート ステータス変更ON実機確認",
        "",
        f"- 実行日時: {payload.get('generatedAt')}",
        f"- 対象SKU: `{SKU}`",
        f"- 移動元: `{SOURCE_LOCATION}`",
        f"- 移動先: `{DEST_LOCATION}`",
        f"- 移動伝票: `{facts.get('movementCode')}`",
        f"- 出荷指示: `{facts.get('outboundCode')}`",
        f"- 入荷指示: `{facts.get('inboundCode')}`",
        "",
        "## 確認結果",
        "",
        f"- エクスポート条件: 開始 `{facts.get('exportStart')}` / 終了 `{facts.get('exportEnd')}` / 出荷作業ステータス `出荷待ち` / ステータス変更ON",
        f"- 実行前の出荷指示詳細に `出荷待ち` が表示された: `{facts.get('beforeWasWaiting')}`",
        f"- 実行後の出荷指示詳細に `出荷作業中` が表示された: `{facts.get('afterBecameInProgress')}`",
        f"- `作業中` タブに対象出荷指示行が表示された: `{facts.get('inProgressTabContainsTarget')}`",
        f"- `出荷待ち` タブに対象出荷指示行が残った: `{facts.get('waitingTabContainsTargetAfter')}`",
        f"- エクスポート実行後の遷移先URL: `{facts.get('afterSubmitUrl')}`",
        f"- 後処理として出荷実績登録で出荷完了にした: `{facts.get('cleanupOutboundCompleted')}`",
        f"- 後処理として関連入荷指示を入荷完了にした: `{facts.get('cleanupInboundCompleted')}`",
        "",
        "## 対象行",
        "",
        "### 作業中タブ",
        "",
    ]
    lines.extend([f"- {row}" for row in facts.get("inProgressRows", [])] or ["- 対象行なし"])
    lines.extend(["", "### 出荷待ちタブ（実行後）", ""])
    lines.extend([f"- {row}" for row in facts.get("waitingRowsAfter", [])] or ["- 対象行なし"])
    lines.extend(["", "## 証跡", "", f"- JSON: `{OUT_JSON.relative_to(ROOT)}`"])
    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    started_at = datetime.now()
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "sourceLocation": SOURCE_LOCATION,
            "destinationLocation": DEST_LOCATION,
            "sku": SKU,
            "quantity": QTY,
        },
        "steps": {},
        "facts": {},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            existing = find_latest_pending_movement(page)
            payload["steps"]["findExistingPendingMovement"] = existing
            if existing.get("found") and existing.get("outboundRoute") and existing.get("inboundRoute"):
                create = existing
                payload["reusedExistingPendingMovement"] = True
            else:
                create = create_movement_order(page)
                payload["steps"]["createMovement"] = create
                payload["reusedExistingPendingMovement"] = False
            movement_route = create["route"]
            outbound_route = create["outboundRoute"]
            inbound_route = create["inboundRoute"]
            payload["routes"] = {
                "movement": movement_route,
                "outbound": outbound_route,
                "inbound": inbound_route,
            }
            before = open_snapshot(page, outbound_route, limit=9000)
            payload["steps"]["outboundBeforeExport"] = before
            movement_snap = open_snapshot(page, movement_route, limit=9000)
            inbound_snap = open_snapshot(page, inbound_route, limit=9000)
            payload["steps"]["movementAfterCreate"] = movement_snap
            payload["steps"]["inboundAfterCreate"] = inbound_snap
            payload["facts"]["movementCode"] = code_from_snapshot(movement_snap, "#IM-")
            payload["facts"]["outboundCode"] = code_from_snapshot(before, "#IO-")
            payload["facts"]["inboundCode"] = code_from_snapshot(inbound_snap, "#II-")
            export = fill_yamato_export_form(page, started_at)
            payload["steps"]["yamatoExport"] = export
            payload["facts"]["exportStart"] = export["formValues"]["start"]
            payload["facts"]["exportEnd"] = export["formValues"]["end"]
            payload["facts"]["afterSubmitUrl"] = export["steps"]["afterSubmit"].get("url")
            payload["steps"]["outboundWaitInProgress"] = wait_for_status(page, outbound_route, "出荷作業中")
            after = payload["steps"]["outboundWaitInProgress"]["attempts"][-1]["snapshot"]
            outbound_code = payload["facts"]["outboundCode"]
            in_progress = matching_rows(page, "/admin/inventory_outbound_orders?tab=in_progress", outbound_code)
            waiting_after = matching_rows(page, "/admin/inventory_outbound_orders?tab=waiting", outbound_code)
            all_after = matching_rows(page, "/admin/inventory_outbound_orders", outbound_code)
            payload["steps"]["outboundListsAfterExport"] = {
                "all": all_after,
                "inProgress": in_progress,
                "waiting": waiting_after,
            }
            payload["facts"]["beforeWasWaiting"] = "出荷待ち" in before.get("body", "")
            payload["facts"]["afterBecameInProgress"] = "出荷作業中" in after.get("body", "")
            payload["facts"]["inProgressRows"] = in_progress.get("matchingRows", [])
            payload["facts"]["waitingRowsAfter"] = waiting_after.get("matchingRows", [])
            payload["facts"]["inProgressTabContainsTarget"] = bool(payload["facts"]["inProgressRows"])
            payload["facts"]["waitingTabContainsTargetAfter"] = bool(payload["facts"]["waitingRowsAfter"])
            cleanup_outbound = register_outbound(page, outbound_route)
            payload["steps"]["cleanupOutbound"] = cleanup_outbound
            cleanup_inbound = complete_inbound(page, inbound_route)
            payload["steps"]["cleanupInbound"] = cleanup_inbound
            payload["facts"]["cleanupOutboundCompleted"] = bool(cleanup_outbound.get("completed"))
            payload["facts"]["cleanupInboundCompleted"] = bool(cleanup_inbound.get("completed"))
            payload["steps"]["movementAfterCleanup"] = open_snapshot(page, movement_route, limit=9000)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            save(payload)
            raise
        finally:
            page.close()
            browser.close()
    save(payload)
    build_md(redact(payload))
    print(
        json.dumps(
            {
                "json": str(OUT_JSON),
                "md": str(OUT_MD),
                "facts": payload["facts"],
                "errors": payload["errors"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
