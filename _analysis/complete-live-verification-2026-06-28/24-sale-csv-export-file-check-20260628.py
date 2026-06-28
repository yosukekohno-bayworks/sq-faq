#!/usr/bin/env python3
import csv
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "24-sale-csv-export-file-check-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")
STAMP = datetime.now().strftime("%Y%m%d%H%M%S")

OPERATIONS = [
    {
        "key": "sale_changes",
        "label": "売上実績（注文軸）",
        "list": "/admin/csv_export/csv_export_operation_sale_changes",
        "create": "/admin/csv_export/csv_export_operation_sale_changes/create",
    },
    {
        "key": "sale_change_line_items",
        "label": "売上実績（明細軸）",
        "list": "/admin/csv_export/csv_export_operation_sale_change_line_items",
        "create": "/admin/csv_export/csv_export_operation_sale_change_line_items/create",
    },
]


def compact(text, limit=4200):
    return " ".join((text or "").split())[:limit]


def wait_soft(page, timeout=12000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snapshot(page, label):
    return page.evaluate(
        """(label) => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const attr = (el, name) => el.getAttribute(name);
            const labelFor = (el) => {
                const id = el.id;
                if (id) {
                    const label = document.querySelector(`label[for="${CSS.escape(id)}"]`);
                    if (label) return textOf(label);
                }
                const label = el.closest('label');
                if (label) return textOf(label);
                return attr(el, 'aria-label') || '';
            };
            return {
                label,
                url: location.href,
                h1: Array.from(document.querySelectorAll('h1')).map(textOf).filter(Boolean),
                rows: Array.from(document.querySelectorAll('tr')).slice(0, 80).map(textOf).filter(Boolean),
                controls: Array.from(document.querySelectorAll('input, select, textarea, button, [role="button"], a[href]')).slice(0, 180).map((el, i) => ({
                    i,
                    tag: el.tagName.toLowerCase(),
                    role: attr(el, 'role'),
                    text: textOf(el),
                    label: labelFor(el),
                    type: attr(el, 'type'),
                    placeholder: attr(el, 'placeholder'),
                    value: el.value,
                    disabled: !!el.disabled,
                    ariaLabel: attr(el, 'aria-label'),
                    href: attr(el, 'href'),
                    options: el.tagName.toLowerCase() === 'select' ? Array.from(el.options).map((opt) => textOf(opt)) : []
                })).filter((x) => x.text || x.label || x.placeholder || x.value || x.ariaLabel || x.href || (x.options && x.options.length)),
                bodySample: (document.body ? document.body.innerText : '').replace(/\\s+/g, ' ').trim().slice(0, 5200)
            };
        }""",
        label,
    )


def choose_tenant(page, result):
    # Native select, if present.
    selects = page.locator("select")
    for i in range(selects.count()):
        options = selects.nth(i).locator("option").all_inner_texts()
        if any("ユニクロ" in opt for opt in options):
            selects.nth(i).select_option(label=next(opt for opt in options if "ユニクロ" in opt))
            result["tenantMethod"] = f"select[{i}]"
            wait_soft(page, timeout=4000)
            return True

    # Radix/custom select button.
    candidates = page.locator("button, [role='button']").filter(has_text=re.compile("選択してください|ユニクロ|テナント"))
    if not candidates.count():
        candidates = page.locator("button, [role='button']")
    for i in range(min(candidates.count(), 12)):
        try:
            before = compact(candidates.nth(i).inner_text(timeout=3000), 300)
            candidates.nth(i).click(timeout=5000)
            page.wait_for_timeout(800)
            option = page.get_by_text("ユニクロ", exact=True)
            if option.count():
                option.last.click(timeout=5000)
                result["tenantMethod"] = f"button[{i}] {before}"
                wait_soft(page, timeout=4000)
                return True
            page.keyboard.press("Escape")
        except Exception as exc:
            result.setdefault("tenantMethodErrors", []).append({"index": i, "error": repr(exc)})
    return False


def fill_dates(page, result):
    start = "2026-06-28T00:00"
    end = "2026-06-29T00:00"
    labels = [
        ("開始日時", start),
        ("終了日時", end),
    ]
    filled = []
    for label, value in labels:
        try:
            loc = page.get_by_label(label, exact=False)
            if loc.count():
                loc.first.fill(value)
                filled.append({"label": label, "method": "label", "value": value})
                continue
        except Exception as exc:
            result.setdefault("dateFillErrors", []).append({"label": label, "error": repr(exc)})

    if len(filled) < 2:
        inputs = page.locator("input")
        visible = []
        for i in range(inputs.count()):
            try:
                if inputs.nth(i).is_visible():
                    typ = inputs.nth(i).get_attribute("type")
                    visible.append((i, typ, inputs.nth(i)))
            except Exception:
                pass
        date_like = [x for x in visible if x[1] in ("datetime-local", "date", "text", None)]
        values = [start, end]
        for idx, (_, _, loc) in enumerate(date_like[:2]):
            loc.fill(values[idx])
            filled.append({"label": labels[idx][0], "method": f"visibleInput[{idx}]", "value": values[idx]})
    result["dateFilled"] = filled
    return len(filled) >= 2


def click_start_export(page, result):
    button = page.get_by_role("button", name="エクスポートを開始する", exact=True)
    if not button.count():
        button = page.locator("button").filter(has_text="エクスポートを開始する")
    if not button.count():
        result["startExportError"] = "button not found"
        return False
    button.last.click(timeout=10000)
    wait_soft(page, timeout=15000)
    return True


def parse_csv_file(path):
    raw = path.read_bytes()
    decoded = None
    encoding = None
    for enc in ["utf-8-sig", "utf-8", "cp932", "shift_jis"]:
        try:
            decoded = raw.decode(enc)
            encoding = enc
            break
        except UnicodeDecodeError:
            continue
    if decoded is None:
        decoded = raw.decode("utf-8", errors="replace")
        encoding = "utf-8-replace"
    rows = list(csv.reader(decoded.splitlines()))
    return {
        "path": str(path),
        "bytes": len(raw),
        "encoding": encoding,
        "rowCountIncludingHeader": len(rows),
        "headers": rows[0] if rows else [],
        "firstDataRows": rows[1:6],
        "containsFaqOrder": any(token in decoded for token in ["FAQ-REMAINING", "FAQ_REMAINING", "FAQ-ORDER-BYPASS", "FAQ_INTERNAL_GRAPHQL"]),
        "containsTargetSku": "TEST_E2E_20260622_GU_1905_NAVY_M" in decoded,
    }


def download_first_available(page, op, result):
    page.goto(BASE + op["list"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    result["listBeforeDownload"] = snapshot(page, "list-before-download")
    links = page.locator("a").filter(has_text=re.compile("ダウンロード|Download|download"))
    if not links.count():
        result["downloadError"] = "download link not found"
        return None
    download_path = OUT_DIR / f"24-sale-csv-{op['key']}-{STAMP}.csv"
    try:
        with page.expect_download(timeout=20000) as download_info:
            links.first.click(timeout=10000)
        download = download_info.value
        download.save_as(download_path)
        result["download"] = {
            "suggestedFilename": download.suggested_filename,
            "savedAs": str(download_path),
        }
        result["csv"] = parse_csv_file(download_path)
        return download_path
    except Exception as exc:
        result["downloadError"] = repr(exc)
        href = links.first.get_attribute("href")
        result["downloadHref"] = href
        return None


def run_operation(page, op):
    result = {"operation": op, "errors": []}
    page.goto(BASE + op["create"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    result["createInitial"] = snapshot(page, "create-initial")
    result["tenantSelected"] = choose_tenant(page, result)
    result["datesFilled"] = fill_dates(page, result)
    result["beforeSubmit"] = snapshot(page, "before-submit")
    result["submitted"] = click_start_export(page, result)
    result["afterSubmit"] = snapshot(page, "after-submit")
    # Give async export a short window, then use whatever latest success row is downloadable.
    for _ in range(6):
        page.wait_for_timeout(2500)
        page.goto(BASE + op["list"], wait_until="domcontentloaded", timeout=60000)
        wait_soft(page, timeout=8000)
        body = page.inner_text("body")
        if "ダウンロード" in body and "成功" in body:
            break
    download_first_available(page, op, result)
    return result


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "operations": [],
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(30000)
        try:
            for op in OPERATIONS:
                payload["operations"].append(run_operation(page, op))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            raise
        finally:
            page.close()
    print(json.dumps({"json": str(OUT_JSON), "operations": [{r["operation"]["key"]: r.get("csv")} for r in payload["operations"]], "errors": payload["errors"]}, ensure_ascii=False, indent=2))


def write_md(payload):
    lines = [
        "# 売上実績CSV 実ファイル確認 2026-06-28",
        "",
        f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
        "",
        "| 種別 | 実行送信 | ダウンロード | 文字コード | 行数 | FAQ注文 | 対象SKU | ヘッダー |",
        "|:--|:--|:--|:--|--:|:--|:--|:--|",
    ]
    for result in payload["operations"]:
        op = result["operation"]
        csv_info = result.get("csv") or {}
        headers = " / ".join(csv_info.get("headers") or [])
        lines.append(
            f"| {op['label']} | `{result.get('submitted')}` | `{bool(result.get('download'))}` | `{csv_info.get('encoding')}` | {csv_info.get('rowCountIncludingHeader')} | `{csv_info.get('containsFaqOrder')}` | `{csv_info.get('containsTargetSku')}` | `{headers}` |"
        )
    lines.extend(["", "## 詳細", ""])
    for result in payload["operations"]:
        op = result["operation"]
        csv_info = result.get("csv") or {}
        lines.append(f"### {op['label']}")
        lines.append(f"- tenantSelected: `{result.get('tenantSelected')}` via `{result.get('tenantMethod')}`")
        lines.append(f"- datesFilled: `{result.get('datesFilled')}` / `{result.get('dateFilled')}`")
        lines.append(f"- savedAs: `{(result.get('download') or {}).get('savedAs')}`")
        lines.append(f"- firstDataRows: `{csv_info.get('firstDataRows')}`")
        if result.get("downloadError"):
            lines.append(f"- downloadError: `{result.get('downloadError')}`")
        lines.append("")
    lines.extend([
        "## 判断",
        "",
        "- 注文軸/明細軸のCSVダウンロードリンクから実ファイルを保存し、ヘッダーとデータ行を確認する。",
        "- `containsFaqOrder` / `containsTargetSku` がtrueなら、2026-06-28の検証注文・対象SKUを含む実データ出力として扱える。",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
