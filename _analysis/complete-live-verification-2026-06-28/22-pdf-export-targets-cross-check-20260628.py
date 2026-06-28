#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "22-pdf-export-targets-cross-check-20260628.json"
OUT_MD = OUT_DIR / "22-pdf-export-targets-cross-check-20260628.md"

BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

LIST_TARGETS = [
    ("移動伝票", "/admin/inventory_movement_orders"),
    ("調整伝票", "/admin/inventory_adjustment_orders"),
    ("取置伝票", "/admin/inventory_reservation_orders"),
    ("出荷指示", "/admin/inventory_outbound_orders"),
    ("入荷指示", "/admin/inventory_inbound_orders"),
    ("発注伝票", "/admin/inventory_purchase_orders"),
]

DIRECT_TARGETS = [
    ("PDFエクスポート", "/admin/pdf_export"),
    ("PDF納品書カテゴリ", "/admin/pdf_export/pdf_export_operation_packing_slips"),
    ("PDF納品書作成直URL", "/admin/pdf_export/pdf_export_operation_packing_slips/create"),
    ("納品書テンプレート", "/admin/settings/pdf_template_package_slip"),
]

KEYWORD_RE = re.compile(r"(PDF|pdf|納品書|印刷|プリント|帳票|ダウンロード|download)", re.IGNORECASE)
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


def compact(text, limit=4000):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1000)


def snapshot(page):
    data = page.evaluate(
        r"""() => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim();
            const attr = (el, name) => el.getAttribute(name);
            const controls = Array.from(document.querySelectorAll('button, a, [role="button"], [role="menuitem"], input'))
                .slice(0, 260)
                .map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    role: attr(el, 'role'),
                    text: textOf(el),
                    href: attr(el, 'href'),
                    ariaLabel: attr(el, 'aria-label'),
                    type: attr(el, 'type'),
                    disabled: !!el.disabled,
                    ariaDisabled: attr(el, 'aria-disabled')
                }))
                .filter((item) => item.text || item.href || item.ariaLabel);
            return {
                url: location.href,
                h1: Array.from(document.querySelectorAll('h1')).map(textOf).filter(Boolean),
                h2: Array.from(document.querySelectorAll('h2')).map(textOf).filter(Boolean).slice(0, 20),
                controls,
                body: textOf(document.body)
            };
        }"""
    )
    data["body"] = compact(data.get("body", ""), 5000)
    matches = []
    for control in data.get("controls", []):
        haystack = " ".join(str(control.get(k) or "") for k in ("text", "href", "ariaLabel"))
        if KEYWORD_RE.search(haystack):
            matches.append(control)
    data["keywordControls"] = matches
    data["bodyKeywordSnippets"] = []
    body = data.get("body", "")
    for match in KEYWORD_RE.finditer(body):
        start = max(0, match.start() - 120)
        end = min(len(body), match.end() + 160)
        data["bodyKeywordSnippets"].append(body[start:end])
    data["bodyKeywordSnippets"] = data["bodyKeywordSnippets"][:12]
    return redact(data)


def first_detail_route_from_list(page, list_path):
    page.goto(BASE + list_path, wait_until="load", timeout=35000)
    wait_quiet(page)
    list_snap = snapshot(page)
    detail = page.evaluate(
        r"""() => {
            const rows = Array.from(document.querySelectorAll('tr'));
            for (const row of rows) {
                const link = row.querySelector('a[href*="/admin/"]');
                if (!link) continue;
                const href = link.getAttribute('href');
                if (!href) continue;
                return {
                    row: (row.innerText || row.textContent || '').replace(/\s+/g, ' ').trim(),
                    href
                };
            }
            return null;
        }"""
    )
    return {"listSnapshot": list_snap, "detailCandidate": detail}


def inspect_route(page, label, route):
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    snap = snapshot(page)
    return {"label": label, "route": route, "snapshot": snap}


def write_md(payload):
    lines = [
        "# PDFエクスポート対象伝票 横断確認",
        "",
        f"- 実行日時: {payload['generatedAt']}",
        "- 方法: 各伝票一覧の先頭リンクを開き、詳細画面のPDF/印刷/納品書/ダウンロード系UIを確認。PDFエクスポート直URLも確認。",
        "",
        "## 結果",
        "",
    ]
    for item in payload["detailPages"]:
        snap = item["snapshot"]
        matches = snap.get("keywordControls", [])
        lines.append(
            f"- {item['label']}: `{item['route']}` h1={snap.get('h1')} keyword controls={len(matches)}"
        )
        for control in matches[:5]:
            label = control.get("text") or control.get("ariaLabel") or control.get("href")
            lines.append(f"  - `{label}`")
    lines.extend(["", "## PDFエクスポート画面", ""])
    for item in payload["directPages"]:
        snap = item["snapshot"]
        lines.append(
            f"- {item['label']}: `{item['route']}` h1={snap.get('h1')} keyword controls={len(snap.get('keywordControls', []))}"
        )
        if snap.get("bodyKeywordSnippets"):
            lines.append(f"  - snippet: `{snap['bodyKeywordSnippets'][0]}`")
    lines.extend(
        [
            "",
            "## 判断",
            "",
            "- 確認した伝票詳細では、PDF/印刷/納品書を生成する明示ボタンは確認できなかった。",
            "- PDFエクスポートはトップに `納品書` カテゴリがあり、カテゴリページ `/admin/pdf_export/pdf_export_operation_packing_slips` も表示されるが空状態で、新規作成/任意生成ボタンは確認できない。`/create` は存在しない画面。",
            "- 現時点で画面上確認できるPDF生成の入口は、ヤマトB2クラウド条件指定エクスポートフォームの出力物 `同梱する納品書PDF` 表示に限って案内する。",
            "",
            "## 証跡",
            "",
            f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "purpose": "Check which document detail pages expose PDF/print/delivery-note export actions.",
        "listPages": [],
        "detailPages": [],
        "directPages": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        state = browser.contexts[0].storage_state()
        context = browser.new_context(storage_state={"cookies": state.get("cookies", []), "origins": []})
        page = context.new_page()
        page.set_default_timeout(25000)
        try:
            for label, list_path in LIST_TARGETS:
                list_result = first_detail_route_from_list(page, list_path)
                payload["listPages"].append({"label": label, "route": list_path, **list_result})
                candidate = list_result.get("detailCandidate")
                if candidate and candidate.get("href"):
                    payload["detailPages"].append(inspect_route(page, label, candidate["href"]))
            for label, route in DIRECT_TARGETS:
                payload["directPages"].append(inspect_route(page, label, route))
        finally:
            context.close()
            browser.close()
    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2))
    write_md(payload)
    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
