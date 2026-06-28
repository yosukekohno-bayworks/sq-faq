#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_JSON = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "03-org-tenant-id-ui-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")

ID_RE = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}_(Organization|Tenant)\b",
    re.IGNORECASE,
)
MASKED_ID_RE = re.compile(r"\b[0-9a-f]{8}\.\.\._(Organization|Tenant)\b", re.IGNORECASE)


def compact(text, limit=2500):
    return " ".join((text or "").split())[:limit]


def mask_ids(text):
    def repl(match):
        raw = match.group(0)
        suffix = match.group(1)
        return raw[:8] + "..._" + suffix

    return ID_RE.sub(repl, text or "")


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(800)


def snapshot(page, limit=3500):
    data = page.evaluate(
        """(limit) => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const unique = (items) => Array.from(new Set(items.filter(Boolean)));
            return {
                url: location.href,
                h1: unique(Array.from(document.querySelectorAll('h1')).map(text)),
                h2: unique(Array.from(document.querySelectorAll('h2')).map(text)),
                labels: unique(Array.from(document.querySelectorAll('label')).map(text)),
                buttons: unique(Array.from(document.querySelectorAll('button')).map((button) => text(button) || button.getAttribute('aria-label') || button.title || '')),
                inputs: Array.from(document.querySelectorAll('input, textarea, select')).map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type') || '',
                    name: el.getAttribute('name') || '',
                    placeholder: el.getAttribute('placeholder') || '',
                    value: el.tagName.toLowerCase() === 'select' ? el.value : (el.value || ''),
                    disabled: !!el.disabled,
                    readOnly: !!el.readOnly,
                    label: (el.closest('label')?.innerText || el.parentElement?.innerText || '').replace(/\\s+/g, ' ').trim(),
                    options: el.tagName.toLowerCase() === 'select'
                        ? Array.from(el.options).map((opt) => ({ value: opt.value, text: text(opt), disabled: opt.disabled }))
                        : []
                })),
                bodyText: document.body.innerText.replace(/\\s+/g, ' ').trim().slice(0, limit)
            };
        }""",
        limit,
    )
    data["bodyText"] = mask_ids(data.get("bodyText", ""))
    for row in data.get("inputs", []):
        row["value"] = mask_ids(row.get("value", ""))
        row["label"] = mask_ids(row.get("label", ""))
    return data


def ids_in_snapshot(snap):
    source = json.dumps(snap, ensure_ascii=False)
    raw_ids = [mask_ids(m.group(0)) for m in ID_RE.finditer(source)]
    masked_ids = [m.group(0) for m in MASKED_ID_RE.finditer(source)]
    return sorted(set(raw_ids + masked_ids))


def get_clipboard():
    try:
        return subprocess.run(["pbpaste"], check=False, capture_output=True).stdout
    except Exception:
        return None


def set_clipboard(data):
    if data is None:
        return False
    try:
        subprocess.run(["pbcopy"], input=data, check=False, capture_output=True)
        return True
    except Exception:
        return False


def find_copy_button_for_id_suffix(page, suffix):
    return page.evaluate(
        """(suffix) => {
            const visibleText = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const input = Array.from(document.querySelectorAll('input')).find((el) => (el.value || '').endsWith(suffix));
            if (!input) return { found: false, reason: `input ending ${suffix} not found` };
            let root = input;
            let copyButton = null;
            for (let depth = 0; depth < 8 && root; depth += 1) {
                const buttons = Array.from(root.querySelectorAll ? root.querySelectorAll('button') : [])
                    .filter((button) => !button.closest('.Polaris-TopBar') && !button.closest('#AppFrameNav'));
                if (buttons.length > 0) {
                    copyButton = buttons.find((button) => {
                        const text = visibleText(button);
                        const aria = button.getAttribute('aria-label') || '';
                        const title = button.getAttribute('title') || '';
                        return /コピー|copy|クリップボード/i.test(text + ' ' + aria + ' ' + title);
                    }) || buttons[0];
                    break;
                }
                root = root.parentElement;
            }
            if (!copyButton) return { found: false };
            const buttons = Array.from(document.querySelectorAll('button'));
            return {
                found: true,
                buttonIndex: buttons.indexOf(copyButton),
                buttonText: visibleText(copyButton) || copyButton.getAttribute('aria-label') || copyButton.getAttribute('title') || '',
                inputValue: input.value
            };
        }""",
        suffix,
    )


def click_copy_for_id_suffix(page, suffix):
    result = find_copy_button_for_id_suffix(page, suffix)
    if not result.get("found") or result.get("buttonIndex", -1) < 0:
        return result
    page.locator("button").nth(result["buttonIndex"]).click()
    page.wait_for_timeout(800)
    browser_clipboard = ""
    browser_clipboard_error = ""
    try:
        browser_clipboard = page.evaluate("navigator.clipboard.readText()")
    except Exception as exc:
        browser_clipboard_error = repr(exc)
    os_clipboard = get_clipboard()
    os_clipboard_text = os_clipboard.decode("utf-8", errors="replace") if os_clipboard is not None else ""
    result.update(
        {
            "clipboard": browser_clipboard,
            "clipboardReadError": browser_clipboard_error,
            "osClipboard": os_clipboard_text,
        }
    )
    return result


def open_first_tenant_detail(page):
    page.goto(BASE + "/admin/settings/tenants", wait_until="load")
    wait_quiet(page)
    before = snapshot(page)
    link = page.locator('a[data-primary-link="true"][href*="/admin/settings/tenants/"]').first
    if link.count() > 0:
        row_text = compact(link.inner_text(timeout=1000), 500)
        link.click()
        wait_quiet(page)
        return before, {"clickedRowText": compact(mask_ids(row_text), 500)}
    return before, {"error": "tenant detail row/link not found"}


def write_md(payload):
    facts = payload["facts"]
    lines = [
        "# 組織ID・テナントID UI確認 2026-06-28",
        "",
        "## 方針",
        "",
        "- IDの実値は記録せず、形式と表示/編集可否/コピー導線だけを確認。",
        "- クリップボード確認では元の内容を出力せず、確認後に復元を試行。",
        "",
        "## 結果",
        "",
        "| 項目 | 結果 |",
        "|:--|:--|",
        f"| 設定トップに組織ID表示 | `{facts['orgIdVisible']}` |",
        f"| 組織IDの形式 | `{facts['orgIdsMasked']}` |",
        f"| 組織IDコピー導線 | `{facts['orgCopy']}` |",
        f"| テナント一覧を開ける | `{facts['tenantListVisible']}` |",
        f"| テナント詳細にテナントID表示 | `{facts['tenantIdVisible']}` |",
        f"| テナントIDの形式 | `{facts['tenantIdsMasked']}` |",
        f"| テナント詳細の主要ラベル | `{facts['tenantDetailLabels']}` |",
        f"| テナントID入力欄の編集不可性 | `{facts['tenantIdControlState']}` |",
        f"| テナントIDコピー導線 | `{facts['tenantCopy']}` |",
        "",
        "## 判断",
        "",
        "- 設定トップでは `組織ID` が `{uuid}_Organization` 形式で表示され、コピー導線も確認できる。",
        "- テナント詳細では `テナントID` が `{uuid}_Tenant` 形式で表示される。",
        "- テナント詳細で編集対象として確認できるのは `テナント名` と `注文IDプレフィックス` で、テナントIDは編集欄として扱われていない。",
        "- 組織ID/テナントIDをAPIや外部連携でどう渡すかは、この画面だけでは確定できない。管理画面UIで確定できるのは表示・コピー・システム生成IDであることまで。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {"generatedAt": datetime.now(timezone.utc).isoformat(), "errors": []}
    original_clipboard = get_clipboard()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        context.grant_permissions(["clipboard-read", "clipboard-write"], origin=BASE)
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(BASE + "/admin/settings", wait_until="load")
            wait_quiet(page)
            payload["settings"] = snapshot(page)
            org_copy = click_copy_for_id_suffix(page, "_Organization")
            payload["orgCopyProbe"] = {
                **org_copy,
                "clipboard": mask_ids(org_copy.get("clipboard", "")),
                "osClipboard": mask_ids(org_copy.get("osClipboard", "")),
                "inputValue": mask_ids(org_copy.get("inputValue", "")),
                "clipboardMatchesOrgId": bool(re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}_Organization", org_copy.get("clipboard", ""), re.IGNORECASE))
                or bool(re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}_Organization", org_copy.get("osClipboard", ""), re.IGNORECASE)),
            }

            tenant_list, tenant_nav = open_first_tenant_detail(page)
            payload["tenantList"] = tenant_list
            payload["tenantNavigation"] = tenant_nav
            payload["tenantDetail"] = snapshot(page)
            tenant_copy = click_copy_for_id_suffix(page, "_Tenant")
            payload["tenantCopyProbe"] = {
                **tenant_copy,
                "clipboard": mask_ids(tenant_copy.get("clipboard", "")),
                "osClipboard": mask_ids(tenant_copy.get("osClipboard", "")),
                "inputValue": mask_ids(tenant_copy.get("inputValue", "")),
                "clipboardMatchesTenantId": bool(re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}_Tenant", tenant_copy.get("clipboard", ""), re.IGNORECASE))
                or bool(re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}_Tenant", tenant_copy.get("osClipboard", ""), re.IGNORECASE)),
            }
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            restored = set_clipboard(original_clipboard)
            settings = payload.get("settings", {})
            tenant_list = payload.get("tenantList", {})
            tenant_detail = payload.get("tenantDetail", {})
            tenant_inputs = tenant_detail.get("inputs", [])
            tenant_id_controls = [
                row for row in tenant_inputs
                if "テナントID" in row.get("label", "") or str(row.get("value", "")).endswith("_Tenant")
            ]
            tenant_id_control_state = [
                {
                    "tag": row.get("tag"),
                    "disabled": row.get("disabled"),
                    "readOnly": row.get("readOnly"),
                    "label": row.get("label"),
                    "value": row.get("value"),
                }
                for row in tenant_id_controls
            ]
            payload["facts"] = {
                "orgIdVisible": "組織ID" in settings.get("bodyText", "") and bool(ids_in_snapshot(settings)),
                "orgIdsMasked": ids_in_snapshot(settings),
                "orgCopy": {
                    "buttonFound": payload.get("orgCopyProbe", {}).get("found") is True,
                    "clipboardReadable": not bool(payload.get("orgCopyProbe", {}).get("clipboardReadError")),
                    "clipboardMatchesOrgId": payload.get("orgCopyProbe", {}).get("clipboardMatchesOrgId") is True,
                    "maskedClipboard": payload.get("orgCopyProbe", {}).get("clipboard", ""),
                    "maskedOsClipboard": payload.get("orgCopyProbe", {}).get("osClipboard", ""),
                },
                "tenantListVisible": "テナント" in tenant_list.get("bodyText", ""),
                "tenantIdVisible": "テナントID" in tenant_detail.get("bodyText", "") and bool(ids_in_snapshot(tenant_detail)),
                "tenantIdsMasked": ids_in_snapshot(tenant_detail),
                "tenantDetailLabels": tenant_detail.get("labels", []),
                "tenantIdControlState": tenant_id_control_state or "テナントID用の編集input/selectは検出されず、表示テキストとして確認",
                "tenantCopy": {
                    "buttonFound": payload.get("tenantCopyProbe", {}).get("found") is True,
                    "clipboardReadable": not bool(payload.get("tenantCopyProbe", {}).get("clipboardReadError")),
                    "clipboardMatchesTenantId": payload.get("tenantCopyProbe", {}).get("clipboardMatchesTenantId") is True,
                    "maskedClipboard": payload.get("tenantCopyProbe", {}).get("clipboard", ""),
                    "maskedOsClipboard": payload.get("tenantCopyProbe", {}).get("osClipboard", ""),
                },
                "clipboardRestored": restored,
                "errors": payload["errors"],
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
            page.close()
            browser.close()
    print(json.dumps(payload["facts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
