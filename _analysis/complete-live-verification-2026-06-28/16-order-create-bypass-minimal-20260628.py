#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "16-order-create-bypass-minimal-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")

TENANT_ID = "da86c1b7-191a-51c2-80e9-f9c3a2a09d9f_Tenant"
TENANT_NAME = "ユニクロ"
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"
FULFILLMENT_LOCATION_ID = "8b7c4983-7e88-549c-b23a-6fafc2c4d52c_Location"
FULFILLMENT_LOCATION_NAME = "ユニクロ物流倉庫"
CUSTOMER_JSON = OUT_DIR / "17-purchasing-customer-graphql-create-uniqlo-20260628.json"
STAMP = datetime.now().strftime("%Y%m%d%H%M%S")

ORDER_FIELDS = """
fragment OrderFields on Order {
  id
  externalID
  source
  managementCode
  managementNumber
  receiptNumber
  currencyCode
  inventoryBehavior
  bypassesPointCalculation
  excludesFromCustomerRankCalculation
  excludesFromSalesRecording
  isCancelled
  isDeleted
  isEditable
  isLocked
  merchantCancellable
  merchantRefundable
  merchantReturnable
  merchantFulfillable
  paymentStatus
  fulfillmentStatus
  requiresFulfillment
  totalQuantity
  currentTotalQuantity
  purchasedAt
  fulfilledAt
  cancelledAt
  tags
  email
  purchasingCustomer {
    id
    fullName
    email
    orderCount
    pointsApproved
    pointsPending
  }
}
"""

ORDER_BY_EXTERNAL_ID = ORDER_FIELDS + """
query OrderByExternalID($externalID: String!) {
  orderByExternalID(externalID: $externalID) {
    ...OrderFields
  }
}
"""

ORDER_CREATE = ORDER_FIELDS + """
mutation CreateOrder($input: OrderCreateInput!, $option: OrderCreateOptionInput!) {
  orderCreate(input: $input, option: $option) {
    order {
      ...OrderFields
    }
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
            return { status: res.status, ok: res.ok, json, textSample: text.slice(0, 1800) };
        }""",
        {"query": query, "variables": variables or {}},
    )


def snapshot(page, label):
    body = page.inner_text("body")
    return {
        "label": label,
        "url": page.url,
        "title": page.title(),
        "bodySample": compact(body, 3600),
        "headers": [compact(x, 300) for x in page.locator("h1,h2,h3,th").all_inner_texts() if compact(x, 300)],
        "rows": [compact(x, 900) for x in page.locator("tr").all_inner_texts()[:40] if compact(x, 900)],
        "buttons": [compact(x, 300) for x in page.locator("button").all_inner_texts()[:80] if compact(x, 300)],
        "links": page.evaluate(
            """() => Array.from(document.querySelectorAll('a[href]')).slice(0, 120).map((a) => ({
                text: (a.innerText || a.textContent || '').trim().replace(/\\s+/g, ' '),
                href: a.getAttribute('href'),
            }))"""
        ),
    }


def load_customer():
    data = json.loads(CUSTOMER_JSON.read_text(encoding="utf-8"))
    facts = data.get("facts") or {}
    email = facts.get("customerEmail") or (data.get("testCustomer") or {}).get("email")
    return {
        "id": facts["customerID"],
        "email": email,
        "fullName": facts.get("customerFullName"),
        "tenantID": facts.get("customerTenantID") or TENANT_ID,
        "tenantName": facts.get("customerTenantName") or TENANT_NAME,
    }


def main():
    customer = load_customer()
    previous = None
    if OUT_JSON.exists():
        try:
            previous = json.loads(OUT_JSON.read_text(encoding="utf-8")).get("testOrder")
        except Exception:
            previous = None
    external_id = (previous or {}).get("externalID") or f"FAQ_ORDER_BYPASS_{STAMP}"
    management_code = (previous or {}).get("managementCode") or f"FAQ-ORDER-BYPASS-{STAMP}"
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "testOrder": {
            "externalID": external_id,
            "managementCode": management_code,
            "tenantID": TENANT_ID,
            "tenantName": TENANT_NAME,
            "sku": SKU,
            "inventoryBehavior": "BYPASS",
            "fulfillmentLocationID": FULFILLMENT_LOCATION_ID,
            "fulfillmentLocationName": FULFILLMENT_LOCATION_NAME,
            "customer": customer,
        },
        "steps": [],
        "facts": {},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(30000)
        try:
            page.goto(f"{BASE}/admin/orders", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "orders-before-create"))
            existing = gql(page, ORDER_BY_EXTERNAL_ID, {"externalID": external_id})
            payload["existingLookup"] = existing
            order = (((existing.get("json") or {}).get("data") or {}).get("orderByExternalID"))
            if not order:
                input_payload = {
                    "externalID": external_id,
                    "managementCode": management_code,
                    "receiptNumber": f"FAQ-RECEIPT-{STAMP}",
                    "source": "FAQ_INTERNAL_GRAPHQL",
                    "tenantID": TENANT_ID,
                    "currencyCode": "JPY",
                    "purchasingCustomer": {"customerID": customer["id"]},
                    "tags": ["FAQ_E2E_20260628", "FAQ_ORDER_BYPASS"],
                    "purchasedAt": datetime.now(timezone.utc).isoformat(),
                    "isLocked": False,
                    "isEditable": True,
                    "isDeletable": True,
                    "note": "FAQ実機検証: orderCreate inventoryBehavior=BYPASS",
                    "email": customer["email"],
                    "lineItems": [
                        {
                            "productTitle": "FAQ検証商品",
                            "variantTitle": "NAVY / M",
                            "externalID": f"FAQ-LINE-{STAMP}",
                            "sku": SKU,
                            "quantity": 1,
                            "unitPrice": {"amount": "1990", "currencyCode": "JPY"},
                            "isBackOrder": False,
                            "excludesFromPointCalculation": False,
                        }
                    ],
                    "fulfillment": {
                        "locationID": FULFILLMENT_LOCATION_ID,
                        "requiresFulfillment": False,
                    },
                    "taxesIncluded": True,
                    "useDiscountAllocationInput": False,
                }
                option_payload = {
                    "inventoryBehavior": "BYPASS",
                    "bypassesPointCalculation": False,
                    "excludesFromCustomerRankCalculation": False,
                    "excludesFromSalesRecording": False,
                    "createInventoryOutboundOrderAsOnHold": False,
                }
                payload["createInputSummary"] = {
                    "input": input_payload,
                    "option": option_payload,
                }
                result = gql(page, ORDER_CREATE, {"input": input_payload, "option": option_payload})
                payload["createResult"] = result
                order = ((((result.get("json") or {}).get("data") or {}).get("orderCreate") or {}).get("order"))
            else:
                payload["createResult"] = {"skipped": True, "reason": "existing order found by externalID"}
            if not order:
                raise RuntimeError(f"orderCreate failed: {payload.get('createResult')}")
            payload["facts"]["order"] = order
            payload["facts"]["createdOrFoundOrderID"] = order.get("id")
            payload["facts"]["managementNumber"] = order.get("managementNumber")
            payload["facts"]["inventoryBehavior"] = order.get("inventoryBehavior")
            payload["facts"]["paymentStatus"] = order.get("paymentStatus")
            payload["facts"]["fulfillmentStatus"] = order.get("fulfillmentStatus")
            payload["facts"]["merchantCancellable"] = order.get("merchantCancellable")
            payload["facts"]["merchantRefundable"] = order.get("merchantRefundable")
            payload["facts"]["merchantReturnable"] = order.get("merchantReturnable")
            page.goto(f"{BASE}/admin/orders", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "orders-after-create"))
            list_body = page.inner_text("body")
            payload["facts"]["ordersListShowsManagementCode"] = management_code in list_body
            payload["facts"]["ordersListShowsManagementNumber"] = bool(order.get("managementNumber") and order.get("managementNumber") in list_body)
            detail_url = f"{BASE}/admin/orders/{order['id']}"
            page.goto(detail_url, wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "order-detail"))
            detail_body = page.inner_text("body")
            payload["facts"]["orderDetailURL"] = detail_url
            payload["facts"]["orderDetailShowsOrder"] = management_code in detail_body or (order.get("managementNumber") or "") in detail_body
            page.goto(f"{BASE}/admin/purchasing_customers/{customer['id']}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "customer-detail-after-order"))
            customer_body = page.inner_text("body")
            payload["facts"]["customerDetailShowsOrderManagementCode"] = management_code in customer_body
            payload["facts"]["customerDetailShowsOrderManagementNumber"] = bool(order.get("managementNumber") and order.get("managementNumber") in customer_body)
            page.goto(f"{BASE}/admin/sale_change_line_items", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "sale-change-line-items-after-order"))
            sale_body = page.inner_text("body")
            payload["facts"]["saleChangeLineItemsShowsOrder"] = management_code in sale_body or (order.get("managementNumber") or "") in sale_body
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# orderCreate最小注文（inventoryBehavior=BYPASS） 2026-06-28",
                "",
                f"- 作成方法: 内部GraphQL `orderCreate`",
                f"- inventoryBehavior: `{payload['facts'].get('inventoryBehavior')}`",
                f"- 注文ID: `{payload['facts'].get('createdOrFoundOrderID')}`",
                f"- 管理コード: `{management_code}`",
                f"- 管理番号: `{payload['facts'].get('managementNumber')}`",
                f"- 顧客: `{customer.get('fullName')}` / `{customer.get('email')}`",
                f"- SKU: `{SKU}`",
                f"- 注文一覧に表示: `{payload['facts'].get('ordersListShowsManagementCode') or payload['facts'].get('ordersListShowsManagementNumber')}`",
                f"- 注文詳細に表示: `{payload['facts'].get('orderDetailShowsOrder')}`",
                f"- 顧客詳細の注文履歴に表示: `{payload['facts'].get('customerDetailShowsOrderManagementCode') or payload['facts'].get('customerDetailShowsOrderManagementNumber')}`",
                f"- 売上実績一覧に表示: `{payload['facts'].get('saleChangeLineItemsShowsOrder')}`",
                f"- paymentStatus: `{payload['facts'].get('paymentStatus')}`",
                f"- fulfillmentStatus: `{payload['facts'].get('fulfillmentStatus')}`",
                f"- merchantCancellable/refundable/returnable/fulfillable: `{payload['facts'].get('merchantCancellable')}` / `{payload['facts'].get('merchantRefundable')}` / `{payload['facts'].get('merchantReturnable')}` / `{payload['facts'].get('merchantFulfillable')}`",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                "",
                "## 注意",
                "",
                "- この注文は在庫を動かさない `BYPASS` で作成したため、注文詳細・顧客履歴・売上表示の確認用です。",
                f"- `orderCreate` の必須条件を満たすため、fulfillmentロケーションは `{FULFILLMENT_LOCATION_NAME}`、`requiresFulfillment=false` を指定しています。",
                "- 注文レコードは後続のキャンセル/返品/ステータス確認に使うため、このスクリプトでは削除・キャンセルしていません。",
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
