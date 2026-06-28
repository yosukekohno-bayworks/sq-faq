#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "16-draft-order-after-seeded-customer-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
CUSTOMER_JSON = OUT_DIR / "17-purchasing-customer-graphql-create-verify-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

CUSTOMER_BY_EXTERNAL_ID = """
query PurchasingCustomerByExternalID($externalID: String!) {
  purchasingCustomerByExternalID(externalID: $externalID) {
    id
    externalID
    fullName
    email
    orderCount
    tenant { id name }
  }
}
"""


def compact(text, limit=2600):
    return " ".join((text or "").split())[:limit]


def wait_soft(page, timeout=12000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(800)


def gql(page, query, variables=None):
    return page.evaluate(
        """async ({query, variables}) => {
            const res = await fetch('/api/graphql', {
                method: 'POST',
                credentials: 'include',
                headers: { 'content-type': 'application/json' },
                body: JSON.stringify({ query, variables }),
            });
            const text = await res.text();
            let json = null;
            try { json = JSON.parse(text); } catch {}
            return { status: res.status, ok: res.ok, json, textSample: text.slice(0, 1200) };
        }""",
        {"query": query, "variables": variables or {}},
    )


def snapshot(page, label):
    return {
        "label": label,
        "url": page.url,
        "title": page.title(),
        "bodySample": compact(page.inner_text("body"), 3600),
        "headers": [compact(x, 300) for x in page.locator("h1,h2,h3,th").all_inner_texts() if compact(x, 300)],
        "rows": [compact(x, 700) for x in page.locator("tr").all_inner_texts()[:30] if compact(x, 700)],
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
            })).slice(0, 180)"""
        ),
    }


def main():
    previous = json.loads(CUSTOMER_JSON.read_text(encoding="utf-8"))
    external_id = previous["testCustomer"]["externalID"]
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "seededCustomerExternalID": external_id,
        "steps": [],
        "facts": {},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            page.goto(f"{BASE}/admin/draft_orders", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            lookup = gql(page, CUSTOMER_BY_EXTERNAL_ID, {"externalID": external_id})
            customer = (((lookup.get("json") or {}).get("data") or {}).get("purchasingCustomerByExternalID"))
            payload["customerLookup"] = lookup
            payload["facts"]["seededPurchasingCustomerExists"] = bool(customer)
            if customer:
                payload["facts"]["seededPurchasingCustomerID"] = customer.get("id")
                payload["facts"]["seededPurchasingCustomerName"] = customer.get("fullName")
                payload["facts"]["seededPurchasingCustomerEmail"] = customer.get("email")
                payload["facts"]["seededPurchasingCustomerOrderCount"] = customer.get("orderCount")
                payload["facts"]["seededPurchasingCustomerTenant"] = (customer.get("tenant") or {}).get("name")
            list_snapshot = snapshot(page, "draft-order-list")
            payload["steps"].append(list_snapshot)
            create_controls = [
                c for c in list_snapshot["controls"]
                if any(k in " ".join([str(c.get("text") or ""), str(c.get("ariaLabel") or ""), str(c.get("href") or "")]) for k in ["作成", "下書き", "draft"])
            ]
            payload["facts"]["draftOrderCreateControls"] = create_controls
            payload["facts"]["draftOrderCreateButtonVisible"] = any("下書き注文を作成" in (c.get("text") or "") for c in create_controls)
            payload["facts"]["draftOrderCreateControlHasHref"] = any(c.get("href") for c in create_controls if "下書き注文を作成" in (c.get("text") or ""))
            payload["facts"]["draftOrderCreateControlDisabled"] = any(
                c.get("disabled") or c.get("ariaDisabled") == "true" or "disabled" in (c.get("className") or "").lower()
                for c in create_controls
                if "下書き注文を作成" in (c.get("text") or "")
            )
            before_url = page.url
            try:
                page.get_by_text("下書き注文を作成", exact=True).first.click(timeout=5000)
                wait_soft(page, 6000)
                payload["facts"]["draftOrderCreateClickSucceeded"] = True
            except Exception as exc:
                payload["facts"]["draftOrderCreateClickSucceeded"] = False
                payload["facts"]["draftOrderCreateClickError"] = repr(exc)[:600]
            payload["facts"]["draftOrderCreateClickChangedUrl"] = page.url != before_url
            payload["steps"].append(snapshot(page, "after-create-click-attempt"))
            page.goto(f"{BASE}/admin/draft_orders/create", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            direct_snapshot = snapshot(page, "direct-create-url")
            payload["steps"].append(direct_snapshot)
            direct_text = direct_snapshot["bodySample"]
            payload["facts"]["directCreateUrl"] = page.url.replace(BASE, "")
            payload["facts"]["directCreateShowsUnexpectedError"] = "予期せぬエラー" in direct_text
            payload["facts"]["directCreateMentionsDraftOrder"] = "下書き注文" in direct_text
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# 下書き注文 顧客シード後の再確認 2026-06-28",
                "",
                f"- 検証用購入顧客あり: `{payload['facts'].get('seededPurchasingCustomerExists')}`",
                f"- 顧客名: `{payload['facts'].get('seededPurchasingCustomerName')}`",
                f"- 顧客メール: `{payload['facts'].get('seededPurchasingCustomerEmail')}`",
                f"- 顧客の注文数: `{payload['facts'].get('seededPurchasingCustomerOrderCount')}`",
                f"- 一覧の作成ボタン表示: `{payload['facts'].get('draftOrderCreateButtonVisible')}`",
                f"- 作成コントロールhrefあり: `{payload['facts'].get('draftOrderCreateControlHasHref')}`",
                f"- 作成コントロールdisabled扱い: `{payload['facts'].get('draftOrderCreateControlDisabled')}`",
                f"- 作成クリックでURL変更: `{payload['facts'].get('draftOrderCreateClickChangedUrl')}`",
                f"- `/admin/draft_orders/create` 直接アクセスで予期せぬエラー: `{payload['facts'].get('directCreateShowsUnexpectedError')}`",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                "",
                "## 一覧本文",
                "",
                list_snapshot["bodySample"],
                "",
                "## 直接アクセス本文",
                "",
                direct_snapshot["bodySample"],
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
