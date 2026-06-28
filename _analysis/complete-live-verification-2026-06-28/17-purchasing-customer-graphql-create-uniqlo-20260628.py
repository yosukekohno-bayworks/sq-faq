#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "17-purchasing-customer-graphql-create-uniqlo-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")
TENANT_ID = "da86c1b7-191a-51c2-80e9-f9c3a2a09d9f_Tenant"
TENANT_NAME = "ユニクロ"
STAMP = datetime.now().strftime("%Y%m%d%H%M%S")

CREATE_MUTATION = """
mutation CreatePurchasingCustomer($input: PurchasingCustomerCreateInput!) {
  purchasingCustomerCreate(input: $input) {
    purchasingCustomer {
      id
      externalID
      firstName
      lastName
      fullName
      email
      phone
      barcode
      tags
      orderCount
      tenant { id name }
    }
  }
}
"""

CUSTOMER_BY_EXTERNAL_ID = """
query PurchasingCustomerByExternalID($externalID: String!) {
  purchasingCustomerByExternalID(externalID: $externalID) {
    id
    externalID
    firstName
    lastName
    fullName
    email
    phone
    barcode
    tags
    orderCount
    tenant { id name }
  }
}
"""


def compact(text, limit=2200):
    return " ".join((text or "").split())[:limit]


def wait_soft(page, timeout=10000):
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
        "bodySample": compact(page.inner_text("body"), 2800),
        "rows": [compact(x, 700) for x in page.locator("tr").all_inner_texts()[:30] if compact(x, 700)],
        "headers": [compact(x, 300) for x in page.locator("h1,h2,h3,th").all_inner_texts() if compact(x, 300)],
    }


def main():
    previous = None
    if OUT_JSON.exists():
        try:
            previous = json.loads(OUT_JSON.read_text(encoding="utf-8")).get("testCustomer")
        except Exception:
            previous = None
    email = (previous or {}).get("email") or f"sq-faq-uniqlo-customer-{STAMP}@example.invalid"
    external_id = (previous or {}).get("externalID") or f"FAQ_E2E_UNIQLO_CUSTOMER_{STAMP}"
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "testCustomer": {
            "externalID": external_id,
            "email": email,
            "tenantID": TENANT_ID,
            "tenantName": TENANT_NAME,
            "tag": "FAQ_E2E_20260628",
        },
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
            payload["steps"].append(snapshot(page, "before-create-list"))
            existing_result = gql(page, CUSTOMER_BY_EXTERNAL_ID, {"externalID": external_id})
            payload["existingLookup"] = existing_result
            customer = (((existing_result.get("json") or {}).get("data") or {}).get("purchasingCustomerByExternalID"))
            mutation_input = {
                "tenantID": TENANT_ID,
                "externalID": external_id,
                "source": "API",
                "barcode": f"FAQUNI{STAMP[-10:]}",
                "firstName": "FAQ",
                "lastName": f"検証顧客ユニクロ{STAMP[-6:]}",
                "email": email,
                "phone": "0000000000",
                "tags": ["FAQ_E2E_20260628"],
            }
            if not customer:
                result = gql(page, CREATE_MUTATION, {"input": mutation_input})
                payload["createResult"] = result
                customer = (((result.get("json") or {}).get("data") or {}).get("purchasingCustomerCreate") or {}).get("purchasingCustomer")
            else:
                payload["createResult"] = {"skipped": True, "reason": "existing purchasing customer found by externalID"}
            if not customer:
                raise RuntimeError(f"customer create failed: {payload.get('createResult')}")
            payload["facts"] = {
                "customerID": customer.get("id"),
                "customerEmail": customer.get("email"),
                "customerFullName": customer.get("fullName"),
                "customerTenantID": (customer.get("tenant") or {}).get("id"),
                "customerTenantName": (customer.get("tenant") or {}).get("name"),
                "customerOrderCount": customer.get("orderCount"),
                "createdByInternalGraphql": True,
            }
            page.goto(f"{BASE}/admin/purchasing_customers/{customer['id']}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "customer-detail-direct"))
            detail_text = page.inner_text("body")
            payload["facts"]["detailShowsCustomer"] = customer.get("fullName") in detail_text and customer.get("email") in detail_text
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# 購入顧客を内部GraphQLで作成（ユニクロテナント） 2026-06-28",
                "",
                f"- 作成方法: 管理画面セッションの内部GraphQL `purchasingCustomerCreate`",
                f"- テナント: `{payload['facts'].get('customerTenantName')}` / `{payload['facts'].get('customerTenantID')}`",
                f"- 顧客ID: `{payload['facts'].get('customerID')}`",
                f"- 氏名: `{payload['facts'].get('customerFullName')}`",
                f"- メール: `{email}`",
                f"- 詳細に表示: `{payload['facts'].get('detailShowsCustomer')}`",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                "",
                "## 備考",
                "",
                "- 管理画面UIには購入顧客の新規作成ボタンがないため、ディスカウント対象顧客候補の検証用に内部GraphQLで作成しました。",
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
