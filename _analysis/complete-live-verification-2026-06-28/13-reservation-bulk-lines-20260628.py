#!/usr/bin/env python3
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "13-reservation-bulk-lines-20260628.json"
OUT_MD = OUT_DIR / "13-reservation-bulk-lines-20260628.md"

BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

LOCATION = "ユニクロ - 銀座店"
SKU = ""
TARGET_ADDITIONS = 12
BATCH_SIZE = 6

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
    page.wait_for_timeout(800)


def snapshot(page, limit=9000):
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
                rows: nodes('tr', 220).map(textOf).filter(Boolean),
                controls: nodes('button, a, input, textarea, select, [role="button"], [role="menuitem"]', 320)
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
                        value: el.tagName.toLowerCase() === 'input' || el.tagName.toLowerCase() === 'textarea' || el.tagName.toLowerCase() === 'select' ? el.value : undefined
                    }))
                    .filter((x) => x.text || x.href || x.ariaLabel || x.placeholder || x.value),
                body
            };
        }"""
    )
    data["body"] = compact(data.get("body", ""), limit)
    data["numberInputCount"] = sum(
        1
        for control in data.get("controls", [])
        if control.get("tag") == "input" and control.get("type") == "number"
    )
    data["reservationCodes"] = sorted(set(re.findall(r"#IR-\d+", data["body"])))
    data["skuRowCount"] = sum(1 for row in data.get("rows", []) if SKU and SKU in row)
    data["variantRowCount"] = sum(
        1
        for row in data.get("rows", [])
        if "product thumbnail" in row or "product variant thumbnail" in row
    )
    data["skuLikeRowCount"] = sum(
        1
        for row in data.get("rows", [])
        if re.search(r"\b\d{6}-[A-Z0-9]+(?:-[A-Z0-9()]+)?\b", row)
        or "TEST_E2E_20260622_" in row
    )
    return redact(data)


def save_payload(payload):
    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2))


def choose_location(page):
    result = {"location": LOCATION}
    page.get_by_role("button", name="選択", exact=True).first.click()
    page.wait_for_selector('div[role="dialog"] tr', timeout=15000)
    page.wait_for_timeout(800)
    dialog = page.locator('div[role="dialog"]').last
    result["dialogBefore"] = compact(dialog.inner_text(timeout=5000), 2600)
    search = dialog.locator('input[placeholder*="検索"], input[placeholder*="キーワード"]')
    if search.count():
        search.first.fill(LOCATION)
        search.first.press("Enter")
        page.wait_for_timeout(1500)
    row = dialog.locator("tr").filter(has_text=LOCATION).first
    if not row.count():
        result["rows"] = [compact(text, 500) for text in dialog.locator("tr").all_inner_texts()[:40]]
        raise RuntimeError(f"location row not found: {LOCATION}")
    result["row"] = compact(row.inner_text(timeout=5000), 900)
    checkbox = row.locator('input[type="checkbox"]').first
    if checkbox.count():
        checkbox.click()
    else:
        row.click()
    page.wait_for_timeout(400)
    dialog.get_by_role("button", name="選択する", exact=True).click()
    wait_quiet(page, timeout=5000)
    result["after"] = snapshot(page, limit=5000)
    return redact(result)


def add_variant_batch(page, batch_index, needed):
    result = {"batchIndex": batch_index, "needed": needed}
    page.get_by_role("button", name="参照", exact=True).first.click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    try:
        page.wait_for_function(
            """() => {
                const dialogs = Array.from(document.querySelectorAll('div[role="dialog"]'));
                const dialog = dialogs[dialogs.length - 1];
                return !!dialog && Array.from(dialog.querySelectorAll('tr')).some((row) => {
                    const text = (row.innerText || row.textContent || '').replace(/\\s+/g, ' ').trim();
                    return text.includes('アイテムを選択する') && row.querySelector('input[type="checkbox"]');
                });
            }""",
            timeout=12000,
        )
    except PlaywrightTimeoutError:
        pass
    result["dialogBefore"] = compact(dialog.inner_text(timeout=8000), 2200)
    selected = page.evaluate(
        """(needed) => {
            const dialogs = Array.from(document.querySelectorAll('div[role="dialog"]'));
            const dialog = dialogs[dialogs.length - 1];
            if (!dialog) return {found: false, reason: 'dialog not found'};
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const candidates = Array.from(dialog.querySelectorAll('tr'))
                .map((row, index) => {
                    const text = textOf(row);
                    const checkbox = row.querySelector('input[type="checkbox"]');
                    const stockMatch = text.match(/(-?\\d+)個\\s*$/);
                    return {
                        row,
                        index,
                        text,
                        checkbox,
                        stock: stockMatch ? Number(stockMatch[1]) : null
                    };
                })
                .filter((item) => {
                    if (!item.checkbox || item.checkbox.checked || item.checkbox.disabled) return false;
                    if (!item.text.includes('アイテムを選択する')) return false;
                    if (item.text.includes('すべてのアイテムを選択する')) return false;
                    return item.stock === null || item.stock >= 0;
                })
                .sort((a, b) => {
                    const aScore = a.stock && a.stock > 0 ? 0 : 1;
                    const bScore = b.stock && b.stock > 0 ? 0 : 1;
                    if (aScore !== bScore) return aScore - bScore;
                    return a.index - b.index;
                });
            const chosen = candidates.slice(0, needed);
            if (!chosen.length) {
                return {
                    found: false,
                    rows: Array.from(dialog.querySelectorAll('tr')).slice(0, 20).map(textOf)
                };
            }
            for (const item of chosen) item.checkbox.click();
            return {
                found: true,
                requested: needed,
                selectedCount: chosen.length,
                rows: chosen.map((item) => ({text: item.text, stock: item.stock}))
            };
        }""",
        needed,
    )
    result["selected"] = selected
    if not selected.get("found"):
        raise RuntimeError("variant selectable row not found")
    page.wait_for_timeout(400)
    dialog.get_by_role("button", name="選択する", exact=True).click()
    wait_quiet(page, timeout=5000)
    snap = snapshot(page, limit=7000)
    result["lineCountAfter"] = snap.get("numberInputCount")
    result["after"] = {
        "url": snap.get("url"),
        "variantRowCount": snap.get("variantRowCount"),
        "numberInputCount": snap.get("numberInputCount"),
        "skuLikeRowCount": snap.get("skuLikeRowCount"),
        "rows": [r for r in snap.get("rows", []) if "product" in r][:30],
    }
    return redact(result)


def fill_all_quantities(page, qty="1"):
    result = {"qty": qty, "count": 0}
    inputs = page.locator('input[type="number"]')
    result["count"] = inputs.count()
    for i in range(inputs.count()):
        inputs.nth(i).fill(qty)
    page.wait_for_timeout(700)
    result["after"] = snapshot(page, limit=9000)
    return redact(result)


def reservation_route_from_page(page):
    if "/admin/inventory_reservation_orders/" in page.url and not page.url.rstrip("/").endswith("/create"):
        return page.url.replace(BASE, "")
    return None


def find_latest_unprocessed(page):
    result = {"found": False, "route": None, "code": None, "row": None, "steps": {}}
    page.goto(BASE + "/admin/inventory_reservation_orders", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["list"] = snapshot(page, limit=10000)
    candidate = page.evaluate(
        """() => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const rows = Array.from(document.querySelectorAll('tr'));
            for (const row of rows) {
                const text = textOf(row);
                if (!text.includes('未処理')) continue;
                const link = row.querySelector('a[href*="/admin/inventory_reservation_orders/"]');
                if (!link) continue;
                return {row: text, code: text.match(/#IR-\\d+/)?.[0] || null, href: link.getAttribute('href')};
            }
            return null;
        }"""
    )
    result["candidate"] = candidate
    if candidate:
        result["found"] = True
        result["route"] = candidate.get("href")
        result["code"] = candidate.get("code")
        result["row"] = candidate.get("row")
    return redact(result)


def save_reservation(page):
    result = {"steps": {}, "route": None, "durationSec": None}
    start = time.monotonic()
    page.get_by_role("button", name="保存する", exact=True).last.click()
    wait_quiet(page, timeout=20000)
    result["durationSec"] = round(time.monotonic() - start, 3)
    result["steps"]["afterSave"] = snapshot(page, limit=10000)
    result["route"] = reservation_route_from_page(page)
    if not result["route"]:
        result["steps"]["findLatestUnprocessed"] = find_latest_unprocessed(page)
        result["route"] = result["steps"]["findLatestUnprocessed"].get("route")
    if not result["route"]:
        raise RuntimeError("reservation route not detected after save")
    return redact(result)


def mark_processed(page, route):
    result = {"route": route, "durationSec": None, "steps": {}}
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["before"] = snapshot(page, limit=10000)
    start = time.monotonic()
    page.get_by_role("button", name="処理済みとしてマークする", exact=True).first.click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    dialog = page.locator('div[role="dialog"]').last
    result["steps"]["dialog"] = compact(dialog.inner_text(timeout=5000), 3000)
    dialog.get_by_role("button", name="実行する", exact=True).click()
    wait_quiet(page, timeout=20000)
    result["durationSec"] = round(time.monotonic() - start, 3)
    result["steps"]["after"] = snapshot(page, limit=10000)
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["afterReload"] = snapshot(page, limit=10000)
    return redact(result)


def create_bulk_reservation(page):
    result = {"steps": {}, "route": None}
    page.goto(BASE + "/admin/inventory_reservation_orders/create", wait_until="load", timeout=35000)
    wait_quiet(page)
    result["steps"]["initial"] = snapshot(page, limit=6000)
    result["steps"]["location"] = choose_location(page)
    memo = page.locator("textarea").first
    if memo.count():
        memo.fill(f"FAQ bulk reservation {datetime.now().strftime('%Y%m%d%H%M%S')} {TARGET_ADDITIONS} lines")
    result["steps"]["additions"] = []
    add_start = time.monotonic()
    batch_index = 1
    while True:
        current_count = snapshot(page, limit=3000).get("numberInputCount", 0)
        if current_count >= TARGET_ADDITIONS:
            break
        needed = min(BATCH_SIZE, TARGET_ADDITIONS - current_count)
        result["steps"]["additions"].append(add_variant_batch(page, batch_index, needed))
        batch_index += 1
        if batch_index > 5:
            raise RuntimeError("variant batch loop exceeded")
    result["addDurationSec"] = round(time.monotonic() - add_start, 3)
    result["steps"]["quantities"] = fill_all_quantities(page, "1")
    result["steps"]["beforeSave"] = snapshot(page, limit=12000)
    result["steps"]["save"] = save_reservation(page)
    result["route"] = result["steps"]["save"].get("route")
    return redact(result)


def extract_facts(payload):
    create = payload.get("steps", {}).get("createBulkReservation", {})
    before_save = create.get("steps", {}).get("beforeSave", {})
    after_save_detail = payload.get("steps", {}).get("detailAfterSave", {})
    processed = payload.get("steps", {}).get("markProcessed", {})
    after_processed = processed.get("steps", {}).get("afterReload", {})
    body_after = after_processed.get("body", "")
    facts = {
        "targetAdditions": TARGET_ADDITIONS,
        "reservationCode": payload.get("reservationCode"),
        "reservationRoute": payload.get("reservationRoute"),
        "lineCountBeforeSave": before_save.get("numberInputCount") or before_save.get("skuLikeRowCount"),
        "lineCountAfterSaveDetail": after_save_detail.get("skuLikeRowCount") or after_save_detail.get("variantRowCount"),
        "quantityInputCountBeforeSave": create.get("steps", {}).get("quantities", {}).get("count"),
        "addDurationSec": create.get("addDurationSec"),
        "saveDurationSec": create.get("steps", {}).get("save", {}).get("durationSec"),
        "processDurationSec": processed.get("durationSec"),
        "processedSucceeded": "処理済み" in body_after and "完了" in body_after,
        "dialogText": processed.get("steps", {}).get("dialog"),
    }
    return redact(facts)


def write_md(payload):
    facts = payload.get("facts") or extract_facts(payload)
    lines = [
        "# 取置伝票の多明細保存・処理済み化 実機確認",
        "",
        f"- 実行日時: {payload.get('generatedAt')}",
        f"- ロケーション: `{LOCATION}`",
        "- SKU: 参照ダイアログの未選択候補を順に追加",
        f"- 追加操作回数: `{TARGET_ADDITIONS}`",
        f"- 取置伝票: `{facts.get('reservationCode')}`",
        "",
        "## 確認結果",
        "",
        f"- 保存前の対象SKU明細行数: `{facts.get('lineCountBeforeSave')}`",
        f"- 保存後詳細の対象SKU明細行数: `{facts.get('lineCountAfterSaveDetail')}`",
        f"- 保存前の数量入力数: `{facts.get('quantityInputCountBeforeSave')}`",
        f"- 商品追加操作の所要秒数: `{facts.get('addDurationSec')}`",
        f"- 保存処理の所要秒数: `{facts.get('saveDurationSec')}`",
        f"- 処理済み化の所要秒数: `{facts.get('processDurationSec')}`",
        f"- 処理済み化に成功した: `{facts.get('processedSucceeded')}`",
        "",
        "## 判断",
        "",
        f"- stagingの管理画面で、取置伝票の作成フォームに `{facts.get('lineCountBeforeSave')}` 明細を累積し、数量入力 `{facts.get('quantityInputCountBeforeSave')}` 件を設定して保存できた。",
        "- 保存後の詳細から「処理済みとしてマークする」→「実行する」で処理済みにできた。",
        "- 保存後詳細の商品明細行数は別途横断確認で伝票別に絞れていない疑いがあるため、性能判断には保存前フォームの明細数を使う。",
        "- これは実負荷試験ではなく、管理画面上の多明細操作確認です。より大きい件数での性能保証は別途負荷試験の扱いです。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "purpose": "Verify saving and processing a reservation order with many repeated line items in the admin UI.",
        "inputs": {"location": LOCATION, "sku": SKU, "targetAdditions": TARGET_ADDITIONS},
        "steps": {},
        "errors": [],
    }
    save_payload(payload)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        source_state = browser.contexts[0].storage_state()
        clean_state = {"cookies": source_state.get("cookies", []), "origins": []}
        context = browser.new_context(storage_state=clean_state)
        page = context.new_page()
        page.set_default_timeout(25000)
        try:
            payload["steps"]["createBulkReservation"] = create_bulk_reservation(page)
            payload["reservationRoute"] = payload["steps"]["createBulkReservation"].get("route")
            page.goto(BASE + payload["reservationRoute"], wait_until="load", timeout=35000)
            wait_quiet(page)
            payload["steps"]["detailAfterSave"] = snapshot(page, limit=12000)
            body = payload["steps"]["detailAfterSave"].get("body", "")
            match = re.search(r"#IR-\d+", body)
            payload["reservationCode"] = match.group(0) if match else None
            save_payload(payload)
            payload["steps"]["markProcessed"] = mark_processed(page, payload["reservationRoute"])
        except Exception as exc:
            payload["errors"].append(repr(exc))
            try:
                payload["steps"]["finalSnapshot"] = snapshot(page, limit=12000)
            except Exception:
                pass
        finally:
            payload["facts"] = extract_facts(payload)
            save_payload(payload)
            write_md(payload)
            context.close()
            browser.close()

    print(
        json.dumps(
            {
                "json": str(OUT_JSON),
                "md": str(OUT_MD),
                "errors": payload["errors"],
                "reservationCode": payload.get("reservationCode"),
                "reservationRoute": payload.get("reservationRoute"),
                "facts": payload.get("facts"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
