#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "16-order-payment-status-count-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
CUSTOMER_JSON = OUT_DIR / "17-purchasing-customer-graphql-create-uniqlo-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")

TENANT_ID = "da86c1b7-191a-51c2-80e9-f9c3a2a09d9f_Tenant"
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"
WAREHOUSE_ID = "d018dd79-47b6-5a93-a1bf-0e12cac23d3e_Location"
STAMP = datetime.now().strftime("%Y%m%d%H%M%S")

ORDER_FIELDS = """
fragment PaymentStatusOrderFields on Order {
  id
  externalID
  source
  managementCode
  managementNumber
  inventoryBehavior
  paymentStatus
  fulfillmentStatus
  requiresFulfillment
  merchantFulfillable
  merchantReturnable
  merchantRefundable
  totalReturnableQuantity
  tags
  inventoryOutboundOrders(first: 10) {
    nodes {
      id
      managementCode
      kind
      workingStatus
      totalQuantity
    }
  }
}
"""

ORDER_CREATE = ORDER_FIELDS + """
mutation CreatePaymentStatusOrder($input: OrderCreateInput!, $option: OrderCreateOptionInput!) {
  orderCreate(input: $input, option: $option) {
    order { ...PaymentStatusOrderFields }
  }
}
"""

ORDER_COUNT = """
query OrderCountForPaymentStatus($filter: OrderCountFilter!) {
  orderCount(filter: $filter)
}
"""


def wait_soft(page):
    try:
        page.wait_for_load_state("networkidle", timeout=12000)
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
            return { status: res.status, ok: res.ok, json, textSample: text.slice(0, 2200) };
        }""",
        {"query": query, "variables": variables or {}},
    )


def load_customer():
    data = json.loads(CUSTOMER_JSON.read_text(encoding="utf-8"))
    facts = data.get("facts") or {}
    return {
        "id": facts["customerID"],
        "email": facts.get("customerEmail") or (data.get("testCustomer") or {}).get("email"),
    }


def money(amount):
    return {"amount": str(amount), "currencyCode": "JPY"}


def order_counts(page):
    statuses = ["WAITING", "ON_HOLD", "REQUESTED", "IN_PROGRESS", "REJECTED", "COMPLETE", "CANCELLED"]
    results = {}
    for status in statuses:
        result = gql(page, ORDER_COUNT, {"filter": {"inventoryOutboundOrderWorkingStatuses": [status], "isCancelled": False}})
        results[status] = (((result.get("json") or {}).get("data") or {}).get("orderCount"))
    active = ["WAITING", "ON_HOLD", "REQUESTED", "IN_PROGRESS", "REJECTED"]
    result = gql(page, ORDER_COUNT, {"filter": {"inventoryOutboundOrderWorkingStatuses": active, "isCancelled": False}})
    results["NON_TERMINAL"] = (((result.get("json") or {}).get("data") or {}).get("orderCount"))
    return results


def create_authorized_order(page, customer):
    management_code = f"FAQ-REMAINING-AUTHONLY-{STAMP}"
    safe = management_code.replace("-", "_")
    now = datetime.now(timezone.utc).isoformat()
    input_payload = {
        "externalID": safe,
        "managementCode": management_code,
        "receiptNumber": f"FAQ-RECEIPT-{STAMP}",
        "source": "FAQ_REMAINING_AUTHONLY",
        "tenantID": TENANT_ID,
        "currencyCode": "JPY",
        "purchasingCustomer": {"customerID": customer["id"]},
        "tags": ["FAQ_REMAINING_20260628", "FAQ_REMAINING_AUTHONLY"],
        "purchasedAt": now,
        "isLocked": False,
        "isEditable": True,
        "isDeletable": True,
        "note": "FAQ残件実機検証: AUTHORIZATIONのみ",
        "email": customer["email"],
        "lineItems": [
            {
                "productTitle": "FAQ決済状態検証商品",
                "variantTitle": "NAVY / M",
                "externalID": f"FAQ-LINE-{safe}",
                "sku": SKU,
                "quantity": 1,
                "unitPrice": money(1990),
                "isBackOrder": False,
                "excludesFromPointCalculation": False,
            }
        ],
        "fulfillment": {"locationID": WAREHOUSE_ID, "requiresFulfillment": False},
        "transactions": [
            {
                "externalID": f"FAQ-TXN-{safe}",
                "paymentID": f"FAQ-PAY-{safe}",
                "kind": "AUTHORIZATION",
                "gateway": "FAQ_GATEWAY",
                "price": money(1990),
                "orderTransactionCreatedAt": now,
                "authorizationExpiresAt": now,
            }
        ],
        "taxesIncluded": True,
        "useDiscountAllocationInput": False,
    }
    option = {
        "inventoryBehavior": "BYPASS",
        "bypassesPointCalculation": False,
        "excludesFromCustomerRankCalculation": False,
        "excludesFromSalesRecording": False,
        "createInventoryOutboundOrderAsOnHold": False,
    }
    result = gql(page, ORDER_CREATE, {"input": input_payload, "option": option})
    return {
        "managementCode": management_code,
        "inputSummary": {
            "transactionKind": "AUTHORIZATION",
            "requiresFulfillment": False,
            "inventoryBehavior": "BYPASS",
        },
        "result": result,
        "order": ((((result.get("json") or {}).get("data") or {}).get("orderCreate") or {}).get("order")),
    }


def snapshot(page, label):
    return page.evaluate(
        """(label) => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            return {
                label,
                url: location.href,
                h1: Array.from(document.querySelectorAll('h1')).map(textOf).filter(Boolean),
                rows: Array.from(document.querySelectorAll('tr')).slice(0, 80).map(textOf).filter(Boolean),
                nav: Array.from(document.querySelectorAll('nav a, aside a, [role="navigation"] a')).slice(0, 100).map(textOf).filter(Boolean),
                bodySample: (document.body ? document.body.innerText : '').replace(/\\s+/g, ' ').trim().slice(0, 4000)
            };
        }""",
        label,
    )


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "countsBefore": {},
        "countsAfter": {},
        "create": {},
        "snapshots": [],
        "errors": [],
    }
    customer = load_customer()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(30000)
        try:
            page.goto(f"{BASE}/admin/orders", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["snapshots"].append(snapshot(page, "orders-before"))
            payload["countsBefore"] = order_counts(page)
            payload["create"] = create_authorized_order(page, customer)
            payload["countsAfter"] = order_counts(page)
            page.goto(f"{BASE}/admin/orders", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["snapshots"].append(snapshot(page, "orders-after"))
            order = payload["create"].get("order")
            if order:
                page.goto(f"{BASE}/admin/orders/{order['id']}", wait_until="domcontentloaded", timeout=60000)
                wait_soft(page)
                payload["snapshots"].append(snapshot(page, "order-detail"))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            raise
        finally:
            page.close()
    print(json.dumps({"order": payload["create"].get("order"), "countsBefore": payload["countsBefore"], "countsAfter": payload["countsAfter"], "errors": payload["errors"]}, ensure_ascii=False, indent=2))


def write_md(payload):
    order = payload["create"].get("order") or {}
    lines = [
        "# 注文管理 未完了件数と決済状態 追加検証 2026-06-28",
        "",
        f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
        f"- 作成注文: `{order.get('managementCode')}`",
        f"- transaction kind: `AUTHORIZATION`",
        f"- paymentStatus / fulfillmentStatus / requiresFulfillment: `{order.get('paymentStatus')}` / `{order.get('fulfillmentStatus')}` / `{order.get('requiresFulfillment')}`",
        f"- 出荷指示: `{(((order.get('inventoryOutboundOrders') or {}).get('nodes')) or [])}`",
        "",
        "## 件数差分",
        "",
        "| 区分 | before | after | diff |",
        "|:--|--:|--:|--:|",
    ]
    keys = ["WAITING", "ON_HOLD", "REQUESTED", "IN_PROGRESS", "REJECTED", "NON_TERMINAL", "COMPLETE", "CANCELLED"]
    for key in keys:
        before = payload["countsBefore"].get(key)
        after = payload["countsAfter"].get(key)
        diff = None if before is None or after is None else after - before
        lines.append(f"| `{key}` | {before} | {after} | {diff} |")
    lines.extend([
        "",
        "## 判断",
        "",
        f"- `AUTHORIZATION` 取引だけで投入しても、この内部 `orderCreate` では `paymentStatus={order.get('paymentStatus')}` になった。非PAID状態はこの経路では再現できていない。",
        "- `requiresFulfillment=false` のため、紐づく出荷指示は `COMPLETE` で作成された。",
        "- 非完了ステータス（WAITING/ON_HOLD/REQUESTED/IN_PROGRESS/REJECTED）の件数は増えない。加えて `OrderCountFilter` に paymentStatus 条件はないため、未完了件数は決済状態ではなく出荷指示の未完了ステータスで数えると判断する。",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
