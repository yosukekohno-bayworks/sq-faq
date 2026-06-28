#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "17-purchasing-customer-search-filter-recheck-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
EMAIL = "sq-faq-customer-20260628094055@example.invalid"


def compact(text, limit=1800):
    return " ".join((text or "").split())[:limit]


def wait_soft(page):
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(700)


def snapshot(page, label):
    return {
        "label": label,
        "url": page.url,
        "bodySample": compact(page.inner_text("body"), 2600),
        "controls": page.evaluate(
            """() => Array.from(document.querySelectorAll('button, a[href], input, textarea, select')).map((el) => ({
                tag: el.tagName.toLowerCase(),
                text: (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' '),
                href: el.getAttribute('href'),
                type: el.getAttribute('type'),
                placeholder: el.getAttribute('placeholder'),
                ariaLabel: el.getAttribute('aria-label'),
                ariaExpanded: el.getAttribute('aria-expanded'),
                disabled: Boolean(el.disabled),
                className: el.className ? String(el.className).slice(0, 160) : '',
                value: el.value || '',
            })).slice(0, 160)"""
        ),
        "rows": [compact(x, 600) for x in page.locator("tr").all_inner_texts()[:20] if compact(x, 600)],
        "headers": [compact(x, 300) for x in page.locator("th").all_inner_texts() if compact(x, 300)],
    }


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "email": EMAIL,
        "steps": [],
        "facts": {},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            page.goto(f"{BASE}/admin/purchasing_customers", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "initial"))
            page.keyboard.press("f")
            wait_soft(page)
            payload["steps"].append(snapshot(page, "after-f-key"))
            page.keyboard.press("Escape")
            wait_soft(page)
            # Try visible icon/button candidates that might open filters/search.
            for idx, control in enumerate(payload["steps"][0]["controls"]):
                label = " ".join([control.get("text") or "", control.get("ariaLabel") or "", control.get("className") or ""])
                if not any(k in label for k in ["検索", "絞り", "filter", "Filter", "Search", "search"]):
                    continue
                try:
                    locator = page.locator("button, a[href]").nth(idx)
                    locator.click(timeout=3000)
                    wait_soft(page)
                    payload["steps"].append(snapshot(page, f"clicked-candidate-{idx}"))
                    page.keyboard.press("Escape")
                    wait_soft(page)
                except Exception as exc:
                    payload.setdefault("clickErrors", []).append({"index": idx, "label": label[:200], "error": repr(exc)})
            all_text = "\n".join(step["bodySample"] for step in payload["steps"])
            all_controls = json.dumps([c for step in payload["steps"] for c in step.get("controls", [])], ensure_ascii=False)
            payload["facts"] = {
                "customerDataPresent": "検証顧客094055FAQ" in all_text,
                "emailVisibleInList": EMAIL in payload["steps"][0]["bodySample"],
                "fKeyOpenedSearchPanel": "メールアドレスで検索する" in payload["steps"][1]["bodySample"] or "絞り込みを追加" in payload["steps"][1]["bodySample"],
                "searchPlaceholderVisibleAnywhere": "メールアドレスで検索する" in all_text or "キーワード" in all_text,
                "filterButtonVisibleAnywhere": "絞り込みを追加" in all_text,
                "searchRelatedControlLabels": [
                    {
                        "tag": c.get("tag"),
                        "text": c.get("text"),
                        "ariaLabel": c.get("ariaLabel"),
                        "placeholder": c.get("placeholder"),
                    }
                    for c in json.loads(all_controls)
                    if any(k in " ".join([str(c.get("text") or ""), str(c.get("ariaLabel") or ""), str(c.get("placeholder") or "")]) for k in ["検索", "絞り", "メール", "キーワード"])
                ],
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# 顧客管理 検索・絞り込み再確認 2026-06-28",
                "",
                f"- 顧客データあり: `{payload['facts']['customerDataPresent']}`",
                f"- 一覧にメール表示: `{payload['facts']['emailVisibleInList']}`",
                f"- Fキーで検索/絞り込み表示: `{payload['facts']['fKeyOpenedSearchPanel']}`",
                f"- 検索プレースホルダー表示: `{payload['facts']['searchPlaceholderVisibleAnywhere']}`",
                f"- `絞り込みを追加` 表示: `{payload['facts']['filterButtonVisibleAnywhere']}`",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                "",
                "## 初期一覧",
                "",
                payload["steps"][0]["bodySample"],
                "",
                "## 関連コントロール",
                "",
            ]
            for control in payload["facts"]["searchRelatedControlLabels"]:
                lines.append(f"- `{control}`")
            OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
        except Exception as exc:
            payload["errors"].append(repr(exc))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            raise
        finally:
            page.close()
    print(json.dumps(payload["facts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
