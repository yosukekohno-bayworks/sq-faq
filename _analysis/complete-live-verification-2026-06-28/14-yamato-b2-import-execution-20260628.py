#!/usr/bin/env python3
import csv
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "14-yamato-b2-import-execution-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
HELPER_PATH = OUT_DIR / "14-yamato-b2-status-change-on-20260628.py"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


spec = importlib.util.spec_from_file_location("yb2_helper", HELPER_PATH)
yb2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(yb2)


def compact(text, limit=1800):
    return " ".join((text or "").split())[:limit]


def text_of(page):
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def wait_soft(page, ms=1000):
    try:
        page.wait_for_load_state("networkidle", timeout=9000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(ms)


def save(payload):
    OUT_JSON.write_text(json.dumps(yb2.redact(payload), ensure_ascii=False, indent=2), encoding="utf-8")


def record(payload, page, step):
    body = text_of(page)
    payload.setdefault("steps", []).append({
        "step": step,
        "url": page.url,
        "bodySample": compact(body, 2600),
        "codes": sorted(set(yb2.re.findall(r"#(?:IM|IO|II)-\\d+", body))),
    })
    save(payload)


def collect_form_diagnostics(page):
    return page.evaluate(
        """() => {
            const visibleText = (el) => (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
            const attrs = (el) => ({
                tag: el.tagName.toLowerCase(),
                text: visibleText(el).slice(0, 500),
                name: el.getAttribute('name'),
                type: el.getAttribute('type'),
                role: el.getAttribute('role'),
                ariaLabel: el.getAttribute('aria-label'),
                ariaDisabled: el.getAttribute('aria-disabled'),
                disabled: Boolean(el.disabled),
                value: el.tagName.toLowerCase() === 'input' && el.type === 'file'
                    ? Array.from(el.files || []).map((f) => f.name).join(',')
                    : (el.value || '').slice(0, 200),
                accept: el.getAttribute('accept'),
                href: el.getAttribute('href'),
            });
            return {
                url: location.href,
                title: document.title,
                h1: Array.from(document.querySelectorAll('h1')).map(visibleText),
                forms: Array.from(document.forms).map((form) => ({
                    action: form.getAttribute('action'),
                    method: form.getAttribute('method'),
                    enctype: form.getAttribute('enctype'),
                    text: visibleText(form).slice(0, 1200),
                    controls: Array.from(form.querySelectorAll('input, textarea, select, button')).map(attrs),
                })),
                buttons: Array.from(document.querySelectorAll('button')).map(attrs),
                links: Array.from(document.querySelectorAll('a[href]')).slice(0, 80).map(attrs),
                alerts: Array.from(document.querySelectorAll('[role="alert"], .Polaris-Banner, .Polaris-InlineError, .Polaris-FormLayout__Error, [class*="error"], [class*="Error"]')).map(visibleText).filter(Boolean).slice(0, 30),
                bodySample: visibleText(document.body).slice(0, 1800),
            };
        }"""
    )


def make_csv(path, outbound_code, variant):
    management_number = outbound_code if variant == "with_hash" else outbound_code.lstrip("#")
    waybill = f"FAQYB2{STAMP.replace('_', '')[-12:]}"
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["伝票番号", "お届け先コード", "お届け先名", "荷物状況", "日付", "時刻", "出荷日", "サイズ品目", "運賃", "お客様管理番号"])
        writer.writerow([waybill, "", "", "", "", "", "2026-06-28", "", "", management_number])
    return {"path": str(path.relative_to(ROOT)), "waybill": waybill, "managementNumber": management_number}


def poll_detail(page, label, attempts=24):
    body = text_of(page)
    for _ in range(attempts):
        norm = " ".join(body.split())
        if f"{label} 成功" in norm or f"{label} 失敗" in norm:
            return body
        page.wait_for_timeout(5000)
        page.reload(wait_until="domcontentloaded", timeout=60000)
        wait_soft(page, 500)
        body = text_of(page)
    return body


def extract_count(text, label):
    match = yb2.re.search(rf"{label}\\s*(\\d+)件", text or "")
    return int(match.group(1)) if match else None


def validation_is_ready(text):
    norm = " ".join((text or "").split())
    return "CSVのバリデーションを実行しています" not in norm


def click_button(page, name, scope=None):
    (scope or page).get_by_role("button", name=name, exact=True).first.click(timeout=15000)


def run_import_attempt(page, payload, outbound_code, variant):
    csv_path = OUT_DIR / f"14-yamato-b2-import-{variant}-{STAMP}.csv"
    csv_info = make_csv(csv_path, outbound_code, variant)
    result = {
        "variant": variant,
        "csv": csv_info,
        "validationSuccess": False,
        "executionSuccess": False,
        "outboundCompletedAfterExecution": False,
    }
    responses = []

    def on_response(response):
        if "sqstackstaging.com" not in response.url:
            return
        if "/admin/csv_import/" not in response.url and "/graphql" not in response.url:
            return
        responses.append({
            "method": response.request.method,
            "url": response.url,
            "status": response.status,
            "resourceType": response.request.resource_type,
        })

    page.on("response", on_response)
    payload.setdefault("attempts", []).append(result)
    try:
        page.goto(f"{BASE}/admin/csv_import/csv_import_operation_fulfillment_by_yamato_b2_clouds/create", wait_until="domcontentloaded", timeout=60000)
        wait_soft(page)
        result["formInitialDiagnostics"] = collect_form_diagnostics(page)
        record(payload, page, f"{variant}-form-initial")
        page.locator('input[type="file"]').set_input_files(str(csv_path))
        wait_soft(page)
        result["formFileSelectedDiagnostics"] = collect_form_diagnostics(page)
        record(payload, page, f"{variant}-form-file-selected")
        try:
            click_button(page, "保存する")
        except Exception as exc:
            result["saveClickError"] = repr(exc)
            result["formAfterSaveDiagnostics"] = collect_form_diagnostics(page)
            result["responsesAfterSave"] = responses
            record(payload, page, f"{variant}-save-click-error")
            save(payload)
            return result
        wait_soft(page, 2500)
        result["formAfterSaveDiagnostics"] = collect_form_diagnostics(page)
        result["responsesAfterSave"] = responses
        record(payload, page, f"{variant}-after-save")
        result["detailUrl"] = page.url
    finally:
        page.remove_listener("response", on_response)

    if page.url.endswith("/create"):
        result["validationFailureText"] = compact(text_of(page), 1200)
        save(payload)
        return result

    validation_body = poll_detail(page, "検証ステータス")
    record(payload, page, f"{variant}-after-validation")
    result["validationBodySample"] = compact(validation_body, 1200)
    result["validationResultAvailable"] = validation_is_ready(validation_body)
    result["validationSuccessCount"] = extract_count(validation_body, "検証成功")
    result["validationFailureCount"] = extract_count(validation_body, "検証失敗")
    result["validationSuccess"] = (
        result["validationResultAvailable"]
        and (result["validationSuccessCount"] or 0) > 0
        and (result["validationFailureCount"] or 0) == 0
    )
    result["validationFailureText"] = compact(validation_body, 900) if not result["validationSuccess"] else ""
    save(payload)
    if not result["validationSuccess"]:
        return result

    click_button(page, "実行する")
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    record(payload, page, f"{variant}-execute-dialog")
    dialog = page.locator('div[role="dialog"]').last
    result["dialogText"] = compact(dialog.inner_text(timeout=5000), 1200)
    click_button(page, "実行する", scope=dialog)
    wait_soft(page)
    page.goto(result["detailUrl"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    execution_body = poll_detail(page, "実行ステータス")
    record(payload, page, f"{variant}-after-execution")
    result["executionBodySample"] = compact(execution_body, 1200)
    result["executionSuccess"] = "成功" in execution_body and "完了" in execution_body
    save(payload)
    return result


def build_md(payload):
    facts = payload.get("facts", {})
    lines = [
        "# ヤマトB2クラウド出荷実績CSV 実取込確認 2026-06-28",
        "",
        f"- 移動伝票: `{facts.get('movementCode')}`",
        f"- 出荷指示: `{facts.get('outboundCode')}`",
        f"- 入荷指示: `{facts.get('inboundCode')}`",
        f"- 成功したCSVバリエーション: `{facts.get('successfulVariant') or 'なし'}`",
        f"- 検証成功: `{'確認' if facts.get('validationSuccess') else '未確認'}`",
        f"- 実行成功: `{'確認' if facts.get('executionSuccess') else '未確認'}`",
        f"- 実行後に出荷完了: `{'確認' if facts.get('outboundCompletedAfterExecution') else '未確認'}`",
        f"- 後処理で入荷完了: `{'確認' if facts.get('cleanupInboundCompleted') else '未確認'}`",
        f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
        "",
        "## CSV",
        "",
    ]
    for attempt in payload.get("attempts", []):
        csv_info = attempt.get("csv", {})
        lines.append(f"- `{attempt.get('variant')}`: `{csv_info.get('path')}` / お客様管理番号 `{csv_info.get('managementNumber')}` / 検証 `{'成功' if attempt.get('validationSuccess') else '失敗'}` / 実行 `{'成功' if attempt.get('executionSuccess') else '未実行または失敗'}`")
    lines.extend(["", "## ステップ", ""])
    for step in payload.get("steps", []):
        lines.append(f"### {step['step']}")
        lines.append(f"- URL: `{step['url']}`")
        if step.get("codes"):
            lines.append(f"- コード: `{', '.join(step['codes'])}`")
        lines.append(f"- 本文抜粋: {step.get('bodySample', '')[:700]}")
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "steps": [],
        "attempts": [],
        "facts": {},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            create = yb2.create_movement_order(page)
            payload["createMovement"] = create
            movement_route = create["route"]
            related = create.get("relatedLinks", [])
            outbound_route = next((x.get("href") for x in related if x.get("href") and "/admin/inventory_outbound_orders/" in x.get("href")), None)
            inbound_route = next((x.get("href") for x in related if x.get("href") and "/admin/inventory_inbound_orders/" in x.get("href")), None)
            if not outbound_route or not inbound_route:
                snap = yb2.open_snapshot(page, movement_route, limit=9000)
                payload["movementSnapshotForRelated"] = snap
                related = snap.get("links", [])
                outbound_route = next((x.get("href") for x in related if x.get("href") and "/admin/inventory_outbound_orders/" in x.get("href")), None)
                inbound_route = next((x.get("href") for x in related if x.get("href") and "/admin/inventory_inbound_orders/" in x.get("href")), None)
            if not outbound_route or not inbound_route:
                raise RuntimeError("related outbound/inbound routes not found")

            outbound_before = yb2.open_snapshot(page, outbound_route, limit=9000)
            inbound_before = yb2.open_snapshot(page, inbound_route, limit=9000)
            movement_snap = yb2.open_snapshot(page, movement_route, limit=9000)
            payload["routes"] = {"movement": movement_route, "outbound": outbound_route, "inbound": inbound_route}
            payload["facts"]["movementCode"] = yb2.code_from_snapshot(movement_snap, "#IM-")
            payload["facts"]["outboundCode"] = yb2.code_from_snapshot(outbound_before, "#IO-")
            payload["facts"]["inboundCode"] = yb2.code_from_snapshot(inbound_before, "#II-")
            payload["outboundBeforeImport"] = outbound_before
            save(payload)

            success = None
            for variant in ["with_hash", "without_hash"]:
                attempt = run_import_attempt(page, payload, payload["facts"]["outboundCode"], variant)
                if attempt.get("validationSuccess") and attempt.get("executionSuccess"):
                    success = attempt
                    break

            outbound_after = yb2.open_snapshot(page, outbound_route, limit=9000)
            payload["outboundAfterImport"] = outbound_after
            payload["facts"]["successfulVariant"] = success.get("variant") if success else None
            payload["facts"]["validationSuccess"] = bool(success and success.get("validationSuccess"))
            payload["facts"]["executionSuccess"] = bool(success and success.get("executionSuccess"))
            payload["facts"]["outboundCompletedAfterExecution"] = "出荷完了" in outbound_after.get("body", "")

            if not payload["facts"]["outboundCompletedAfterExecution"]:
                payload["cleanupOutbound"] = yb2.register_outbound(page, outbound_route)
                payload["facts"]["cleanupOutboundCompleted"] = bool(payload["cleanupOutbound"].get("completed"))
            else:
                payload["facts"]["cleanupOutboundCompleted"] = True

            payload["cleanupInbound"] = yb2.complete_inbound(page, inbound_route)
            payload["facts"]["cleanupInboundCompleted"] = bool(payload["cleanupInbound"].get("completed"))
            payload["movementAfterCleanup"] = yb2.open_snapshot(page, movement_route, limit=9000)
            save(payload)
            build_md(yb2.redact(payload))
        except Exception as exc:
            payload["errors"].append(repr(exc))
            save(payload)
            build_md(yb2.redact(payload))
            raise
        finally:
            if not page.is_closed():
                page.close()
    print(json.dumps({"facts": payload["facts"], "errors": payload["errors"], "json": str(OUT_JSON), "md": str(OUT_MD)}, ensure_ascii=False, indent=2))
    if not payload["facts"].get("executionSuccess"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
