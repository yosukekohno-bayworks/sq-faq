#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "17-purchasing-customer-filter-options-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"


def compact(text, limit=2000):
    return " ".join((text or "").split())[:limit]


def wait_soft(page):
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(700)


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
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
            page.keyboard.press("f")
            wait_soft(page)
            page.get_by_role("button", name="絞り込みを追加").click(timeout=10000)
            wait_soft(page)
            body = page.inner_text("body")
            controls = page.evaluate(
                """() => Array.from(document.querySelectorAll('button, [role="menuitem"], input, select')).map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    role: el.getAttribute('role'),
                    text: (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' '),
                    ariaLabel: el.getAttribute('aria-label'),
                    placeholder: el.getAttribute('placeholder'),
                    ariaExpanded: el.getAttribute('aria-expanded'),
                    disabled: Boolean(el.disabled),
                })).slice(0, 120)"""
            )
            payload["steps"].append({
                "url": page.url,
                "bodySample": compact(body, 3000),
                "controls": controls,
            })
            options = []
            for c in controls:
                text = c.get("text") or c.get("ariaLabel") or ""
                if text in ["テナント", "メタフィールド", "会員証バーコード"]:
                    options.append(text)
            payload["facts"] = {
                "filterMenuOpened": "テナント" in body or "メタフィールド" in body,
                "options": options,
                "hasTenant": "テナント" in options,
                "hasMetafield": "メタフィールド" in options,
                "hasBarcode": "会員証バーコード" in options,
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            OUT_MD.write_text(
                "\n".join([
                    "# 顧客管理 絞り込み条件確認 2026-06-28",
                    "",
                    f"- 絞り込みメニュー表示: `{payload['facts']['filterMenuOpened']}`",
                    f"- 選択肢: `{', '.join(options)}`",
                    f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                ]) + "\n",
                encoding="utf-8",
            )
        except Exception as exc:
            payload["errors"].append(repr(exc))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            raise
        finally:
            page.close()
    print(json.dumps(payload["facts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
