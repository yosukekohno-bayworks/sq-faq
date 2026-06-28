#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "18-discount-customer-tab-inspect-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")


def compact(text, limit=3000):
    return " ".join((text or "").split())[:limit]


def wait_soft(page, timeout=12000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(800)


def snapshot(page, label):
    return {
        "label": label,
        "url": page.url,
        "title": page.title(),
        "bodySample": compact(page.inner_text("body"), 4500),
        "headers": [compact(x, 300) for x in page.locator("h1,h2,h3,th").all_inner_texts() if compact(x, 300)],
        "rows": [compact(x, 900) for x in page.locator("tr").all_inner_texts()[:40] if compact(x, 900)],
        "controls": page.evaluate(
            """() => Array.from(document.querySelectorAll('button, a[href], input, textarea, select')).map((el) => ({
                tag: el.tagName.toLowerCase(),
                text: (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' '),
                href: el.getAttribute('href'),
                type: el.getAttribute('type'),
                placeholder: el.getAttribute('placeholder'),
                ariaLabel: el.getAttribute('aria-label'),
                ariaDisabled: el.getAttribute('aria-disabled'),
                disabled: Boolean(el.disabled),
                className: el.className ? String(el.className).slice(0, 220) : '',
            })).slice(0, 220)"""
        ),
    }


def pick_discount_href(links):
    candidates = []
    pattern = re.compile(r"^/admin/order_price_adjustment_rules/[^/?#]+$")
    for link in links:
        href = link.get("href") or ""
        text = link.get("text") or ""
        if pattern.match(href):
            score = 0
            if any(k in text for k in ["TEST", "FAQ", "検証", "テスト"]):
                score += 10
            if "無効" not in text:
                score += 1
            candidates.append({"href": href, "text": text, "score": score})
    candidates.sort(key=lambda x: (-x["score"], x["href"]))
    return candidates


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
            page.goto(f"{BASE}/admin/order_price_adjustment_rules", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            list_snapshot = snapshot(page, "discount-list")
            payload["steps"].append(list_snapshot)
            candidates = pick_discount_href([c for c in list_snapshot["controls"] if c.get("tag") == "a"])
            payload["facts"]["discountRuleCandidates"] = candidates[:20]
            if not candidates:
                payload["facts"]["hasDiscountRuleCandidate"] = False
            else:
                payload["facts"]["hasDiscountRuleCandidate"] = True
                selected = candidates[0]
                payload["facts"]["selectedDiscountRule"] = selected
                page.goto(f"{BASE}{selected['href']}", wait_until="domcontentloaded", timeout=60000)
                wait_soft(page)
                payload["steps"].append(snapshot(page, "discount-detail"))
                customers_url = f"{BASE}{selected['href']}/customers"
                page.goto(customers_url, wait_until="domcontentloaded", timeout=60000)
                wait_soft(page)
                customer_snapshot = snapshot(page, "discount-customers-tab")
                payload["steps"].append(customer_snapshot)
                body = customer_snapshot["bodySample"]
                controls_text = "\n".join(" ".join([c.get("text") or "", c.get("ariaLabel") or "", c.get("href") or ""]) for c in customer_snapshot["controls"])
                payload["facts"]["customersTabUrl"] = page.url.replace(BASE, "")
                payload["facts"]["customersTabShowsAddButton"] = "追加する" in body or "追加する" in controls_text
                payload["facts"]["customersTabShowsSeededCustomer"] = "検証顧客094055FAQ" in body or "sq-faq-customer-20260628094055@example.invalid" in body
                payload["facts"]["customersTabRows"] = customer_snapshot["rows"]
                try:
                    page.get_by_text("追加する", exact=True).first.click(timeout=5000)
                    wait_soft(page, 6000)
                    add_menu_snapshot = snapshot(page, "discount-customers-add-menu")
                    payload["steps"].append(add_menu_snapshot)
                    add_text = add_menu_snapshot["bodySample"]
                    payload["facts"]["addMenuOpened"] = True
                    payload["facts"]["addMenuHasSelectCustomer"] = "顧客を選択して追加" in add_text
                    payload["facts"]["addMenuHasSegment"] = "顧客セグメントを選択して追加" in add_text
                except Exception as exc:
                    payload["facts"]["addMenuOpened"] = False
                    payload["facts"]["addMenuClickError"] = repr(exc)[:500]
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# ディスカウント 顧客タブ探索 2026-06-28",
                "",
                f"- ルール候補あり: `{payload['facts'].get('hasDiscountRuleCandidate')}`",
                f"- 選択ルール: `{payload['facts'].get('selectedDiscountRule')}`",
                f"- 顧客タブURL: `{payload['facts'].get('customersTabUrl')}`",
                f"- `追加する` 表示: `{payload['facts'].get('customersTabShowsAddButton')}`",
                f"- 追加メニュー表示: `{payload['facts'].get('addMenuOpened')}`",
                f"- `顧客を選択して追加`: `{payload['facts'].get('addMenuHasSelectCustomer')}`",
                f"- `顧客セグメントを選択して追加`: `{payload['facts'].get('addMenuHasSegment')}`",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                "",
                "## 顧客タブ本文",
                "",
                (payload["steps"][2]["bodySample"] if len(payload["steps"]) > 2 else ""),
            ]
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
