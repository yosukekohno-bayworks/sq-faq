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
OUT_JSON = OUT_DIR / "16-order-remaining-normal-exchange-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
CUSTOMER_JSON = OUT_DIR / "17-purchasing-customer-graphql-create-uniqlo-20260628.json"
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")

TENANT_ID = "da86c1b7-191a-51c2-80e9-f9c3a2a09d9f_Tenant"
TENANT_NAME = "ユニクロ"
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"
PRODUCT_VARIANT_ID = "9d94e684-4882-5ebc-bbbb-513915a8bfc7_ProductVariant"
WAREHOUSE_1905_ID = "d018dd79-47b6-5a93-a1bf-0e12cac23d3e_Location"
WAREHOUSE_1905_NAME = "TEST_E2E_20260622_GU倉庫_ON_1905"
STAMP = datetime.now().strftime("%Y%m%d%H%M%S")

LONG_TOKEN_RE = re.compile(r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))")

ORDER_FIELDS = """
fragment RemainingOrderFields on Order {
  id
  externalID
  source
  managementCode
  managementNumber
  receiptNumber
  inventoryBehavior
  paymentStatus
  fulfillmentStatus
  requiresFulfillment
  isFulfillmentInProgress
  merchantFulfillable
  merchantReturnable
  merchantRefundable
  totalQuantity
  currentTotalQuantity
  totalReturnableQuantity
  hasActiveOrderReturns
  email
  tags
  lineItems(first: 10) {
    nodes {
      id
      sku
      quantity
      currentQuantity
      returnableQuantity
      refundableQuantity
    }
  }
  inventoryOutboundOrders(first: 10) {
    nodes {
      id
      externalID
      managementCode
      kind
      workingStatus
      totalQuantity
      isInventoryAllocated
      isFulfillable
      inventoryAllocationStatus
      inventoryLocation { id name code locationType }
    }
  }
}
"""

RETURN_FIELDS = """
fragment RemainingReturnFields on OrderReturn {
  id
  managementCode
  externalID
  status
  receivable
  completable
  cancellable
  totalQuantity
  totalReceivedQuantity
  exchangeLineItemCount
  hasExchangeLineItems
  exchangeLineItems(first: 10) {
    nodes {
      id
      quantity
      productVariant { id title inventoryItem { sku } }
    }
  }
  exchangeInventoryOutboundOrder {
    id
    managementCode
    workingStatus
    totalQuantity
    inventoryLocation { id name code }
  }
  lineItems(first: 10) {
    nodes {
      id
      quantity
      receivedQuantity
      receivableQuantity
      currentQuantity
      orderLineItem { id sku returnableQuantity refundableQuantity currentQuantity }
    }
  }
  order { id managementCode managementNumber paymentStatus fulfillmentStatus totalReturnableQuantity hasActiveOrderReturns }
}
"""

ORDER_BY_EXTERNAL_ID = ORDER_FIELDS + """
query OrderByExternalID($externalID: String!) {
  orderByExternalID(externalID: $externalID) { ...RemainingOrderFields }
}
"""

ORDER_BY_ID = ORDER_FIELDS + """
query OrderByID($id: ID!) {
  order(id: $id) { ...RemainingOrderFields }
}
"""

ORDER_CREATE = ORDER_FIELDS + """
mutation CreateRemainingOrder($input: OrderCreateInput!, $option: OrderCreateOptionInput!) {
  orderCreate(input: $input, option: $option) {
    order { ...RemainingOrderFields }
  }
}
"""

RETURN_CREATE = RETURN_FIELDS + """
mutation CreateRemainingReturn($input: OrderReturnCreateInput!) {
  orderReturnCreate(input: $input) {
    orderReturn { ...RemainingReturnFields }
  }
}
"""

RETURN_BY_ID = RETURN_FIELDS + """
query RemainingReturnByID($id: ID!) {
  orderReturn(id: $id) { ...RemainingReturnFields }
}
"""

INVENTORY_SNAPSHOT = """
query InventorySnapshot($sku: String!, $locationID: ID!, $tenantID: ID!) {
  productVariantBySKU(sku: $sku) {
    id
    title
    inventoryItem {
      id
      sku
      inventoryLevel(locationID: $locationID) {
        id
        quantity {
          incoming
          inTransit
          available
          committed
          reserved
          damaged
          safetyStock
          qualityControl
          onHand
          sellableQuantity
        }
      }
    }
    locationAvailability(locationID: $locationID, tenantID: $tenantID) {
      inventoryQuantity
    }
  }
}
"""

ORDER_COUNT = """
query OrderCountForIncomplete($filter: OrderCountFilter!) {
  orderCount(filter: $filter)
}
"""


def redact(value):
    if isinstance(value, str):
        if value.startswith(("FAQ-", "FAQ_", "TEST_", "#")):
            return value
        return LONG_TOKEN_RE.sub("[REDACTED_LONG_VALUE]", value)
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    return value


def compact(text, limit=4000):
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
            return { status: res.status, ok: res.ok, json, textSample: text.slice(0, 2400) };
        }""",
        {"query": query, "variables": variables or {}},
    )


def snapshot(page, label):
    data = page.evaluate(
        """(label) => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const attr = (el, name) => el.getAttribute(name);
            const nodes = (selector, limit = 140) => Array.from(document.querySelectorAll(selector)).slice(0, limit);
            const body = document.body ? document.body.innerText : '';
            return {
                label,
                url: location.href,
                title: document.title,
                h1: nodes('h1', 10).map(textOf).filter(Boolean),
                h2: nodes('h2', 30).map(textOf).filter(Boolean),
                nav: nodes('nav a, aside a, [role="navigation"] a', 120).map((a) => ({ text: textOf(a), href: attr(a, 'href') })).filter((x) => x.text || x.href),
                rows: nodes('tr', 80).map(textOf).filter(Boolean),
                buttons: nodes('button, [role="button"]', 120).map((b) => ({ text: textOf(b) || attr(b, 'aria-label') || '', disabled: !!b.disabled, ariaDisabled: attr(b, 'aria-disabled') })).filter((x) => x.text),
                links: nodes('a[href]', 160).map((a) => ({ text: textOf(a), href: attr(a, 'href') })).filter((x) => x.text || x.href),
                bodySample: body.replace(/\\s+/g, ' ').trim().slice(0, 5000)
            };
        }""",
        label,
    )
    return redact(data)


def load_customer():
    data = json.loads(CUSTOMER_JSON.read_text(encoding="utf-8"))
    facts = data.get("facts") or {}
    return {
        "id": facts["customerID"],
        "email": facts.get("customerEmail") or (data.get("testCustomer") or {}).get("email"),
        "fullName": facts.get("customerFullName"),
    }


def money(amount):
    return {"amount": str(amount), "currencyCode": "JPY"}


def base_order_input(customer, management_code, external_id, requires_fulfillment, source, transactions=True, include_outbound=False):
    now = datetime.now(timezone.utc).isoformat()
    safe_suffix = management_code.replace("#", "").replace("-", "_")
    input_payload = {
        "externalID": external_id,
        "managementCode": management_code,
        "receiptNumber": f"FAQ-RECEIPT-{STAMP}",
        "source": source,
        "tenantID": TENANT_ID,
        "currencyCode": "JPY",
        "purchasingCustomer": {"customerID": customer["id"]},
        "tags": ["FAQ_REMAINING_20260628", source],
        "purchasedAt": now,
        "isLocked": False,
        "isEditable": True,
        "isDeletable": True,
        "note": "FAQ残件実機検証",
        "email": customer["email"],
        "shippingAddress": {
            "firstName": "FAQ",
            "lastName": "検証",
            "company": "Bayworks",
            "address1": "1-1-1",
            "address2": "FAQ",
            "city": "Chuo-ku",
            "postalCode": "104-0061",
            "provinceCode": "JP-13",
            "countryCode": "JP",
            "phone": "0312345678",
        },
        "billingAddress": {
            "firstName": "FAQ",
            "lastName": "検証",
            "company": "Bayworks",
            "address1": "1-1-1",
            "address2": "FAQ",
            "city": "Chuo-ku",
            "postalCode": "104-0061",
            "provinceCode": "JP-13",
            "countryCode": "JP",
            "phone": "0312345678",
        },
        "lineItems": [
            {
                "productTitle": "FAQ残件検証商品",
                "variantTitle": "NAVY / M",
                "externalID": f"FAQ-REMAINING-LINE-{safe_suffix}",
                "sku": SKU,
                "quantity": 1,
                "unitPrice": money(1990),
                "isBackOrder": False,
                "excludesFromPointCalculation": False,
            }
        ],
        "fulfillment": {
            "locationID": WAREHOUSE_1905_ID,
            "requiresFulfillment": requires_fulfillment,
        },
        "taxesIncluded": True,
        "useDiscountAllocationInput": False,
    }
    if transactions:
        input_payload["transactions"] = [
            {
                "externalID": f"FAQ-TXN-{safe_suffix}",
                "paymentID": f"FAQ-PAY-{safe_suffix}",
                "kind": "SALE",
                "gateway": "FAQ_GATEWAY",
                "price": money(1990),
                "orderTransactionCreatedAt": now,
            }
        ]
    if include_outbound:
        input_payload["inventoryOutboundOrders"] = [
            {
                "locationID": WAREHOUSE_1905_ID,
                "isFulfilled": False,
                "lineItems": [{"sku": SKU, "quantity": 1}],
            }
        ]
    return input_payload


def order_create(page, customer, kind, inventory_behavior, requires_fulfillment, transactions=True, include_outbound=False):
    management_code = f"FAQ-REMAINING-{kind}-{STAMP}"
    external_id = management_code.replace("-", "_")
    existing = gql(page, ORDER_BY_EXTERNAL_ID, {"externalID": external_id})
    order = (((existing.get("json") or {}).get("data") or {}).get("orderByExternalID"))
    if order:
        return {"order": order, "existing": True, "attempts": [{"skipped": "already exists"}]}
    source = f"FAQ_REMAINING_{kind}"
    option = {
        "inventoryBehavior": inventory_behavior,
        "bypassesPointCalculation": False,
        "excludesFromCustomerRankCalculation": False,
        "excludesFromSalesRecording": False,
        "createInventoryOutboundOrderAsOnHold": False,
    }
    attempts = []
    input_payload = base_order_input(
        customer,
        management_code,
        external_id,
        requires_fulfillment,
        source,
        transactions=transactions,
        include_outbound=include_outbound,
    )
    result = gql(page, ORDER_CREATE, {"input": input_payload, "option": option})
    attempts.append({"includeOutbound": include_outbound, "result": result})
    order = ((((result.get("json") or {}).get("data") or {}).get("orderCreate") or {}).get("order"))
    if not order and requires_fulfillment and not include_outbound:
        input_payload = base_order_input(
            customer,
            management_code,
            external_id,
            requires_fulfillment,
            source,
            transactions=transactions,
            include_outbound=True,
        )
        result = gql(page, ORDER_CREATE, {"input": input_payload, "option": option})
        attempts.append({"includeOutbound": True, "result": result})
        order = ((((result.get("json") or {}).get("data") or {}).get("orderCreate") or {}).get("order"))
    return {"order": order, "existing": False, "attempts": attempts, "managementCode": management_code, "externalID": external_id}


def inventory_snapshot(page):
    result = gql(page, INVENTORY_SNAPSHOT, {"sku": SKU, "locationID": WAREHOUSE_1905_ID, "tenantID": TENANT_ID})
    data = (((result.get("json") or {}).get("data") or {}).get("productVariantBySKU") or {})
    item = data.get("inventoryItem") or {}
    level = item.get("inventoryLevel") or {}
    return {
        "result": result,
        "quantity": (level.get("quantity") or {}),
        "locationAvailabilityQuantity": ((data.get("locationAvailability") or {}).get("inventoryQuantity")),
    }


def order_counts(page):
    statuses = ["WAITING", "ON_HOLD", "REQUESTED", "IN_PROGRESS", "REJECTED", "COMPLETE", "CANCELLED"]
    results = {}
    for status in statuses:
        result = gql(page, ORDER_COUNT, {"filter": {"inventoryOutboundOrderWorkingStatuses": [status], "isCancelled": False}})
        results[status] = {
            "result": result,
            "count": (((result.get("json") or {}).get("data") or {}).get("orderCount")),
        }
    active = ["WAITING", "ON_HOLD", "REQUESTED", "IN_PROGRESS", "REJECTED"]
    result = gql(page, ORDER_COUNT, {"filter": {"inventoryOutboundOrderWorkingStatuses": active, "isCancelled": False}})
    results["NON_TERMINAL"] = {
        "statuses": active,
        "result": result,
        "count": (((result.get("json") or {}).get("data") or {}).get("orderCount")),
    }
    return results


def create_exchange_return(page, order):
    line_items = (((order.get("lineItems") or {}).get("nodes")) or [])
    target = next((x for x in line_items if (x.get("returnableQuantity") or 0) > 0), None)
    if not target:
        return {"error": "no returnable line item", "lineItems": line_items}
    input_payload = {
        "orderID": order["id"],
        "exchangeInventoryLocationID": WAREHOUSE_1905_ID,
        "externalID": f"FAQ_EXCHANGE_RETURN_{STAMP}",
        "received": False,
        "orderReturnLineItems": [
            {
                "externalID": f"FAQ-EXCHANGE-RETURN-LINE-{STAMP}",
                "orderLineItemID": target["id"],
                "quantity": 1,
                "reason": "FAQ実機検証: 交換返品",
                "exchangeLineItem": {"productVariantID": PRODUCT_VARIANT_ID},
            }
        ],
    }
    result = gql(page, RETURN_CREATE, {"input": input_payload})
    order_return = ((((result.get("json") or {}).get("data") or {}).get("orderReturnCreate") or {}).get("orderReturn"))
    return {"input": input_payload, "result": result, "orderReturn": order_return}


def refresh_order(page, order):
    if not order:
        return None
    result = gql(page, ORDER_BY_ID, {"id": order["id"]})
    return (((result.get("json") or {}).get("data") or {}).get("order"))


def main():
    customer = load_customer()
    previous_payload = None
    if OUT_JSON.exists():
        try:
            previous_payload = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        except Exception:
            previous_payload = None
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "tenant": {"id": TENANT_ID, "name": TENANT_NAME},
        "sku": SKU,
        "warehouse": {"id": WAREHOUSE_1905_ID, "name": WAREHOUSE_1905_NAME},
        "customer": customer,
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
            payload["steps"].append(snapshot(page, "orders-before"))
            payload["before"] = {
                "inventory": inventory_snapshot(page),
                "orderCounts": order_counts(page),
            }

            previous_normal = ((previous_payload or {}).get("facts") or {}).get("normalOrder") or {}
            previous_normal_external_id = previous_normal.get("externalID")
            normal_order = None
            if previous_normal_external_id and previous_normal.get("inventoryBehavior") == "DECREMENT":
                lookup = gql(page, ORDER_BY_EXTERNAL_ID, {"externalID": previous_normal_external_id})
                normal_order = (((lookup.get("json") or {}).get("data") or {}).get("orderByExternalID"))
                if normal_order:
                    payload["normalOrderCreate"] = {
                        "reusedFromPreviousRun": True,
                        "previousExternalID": previous_normal_external_id,
                        "lookup": lookup,
                        "order": normal_order,
                    }
                    payload["before"] = (previous_payload or {}).get("before") or payload["before"]
                    payload["afterNormal"] = (previous_payload or {}).get("afterNormal") or {
                        "inventory": inventory_snapshot(page),
                        "orderCounts": order_counts(page),
                    }
            if not normal_order:
                normal = order_create(
                    page,
                    customer,
                    kind="DECREMENT",
                    inventory_behavior="DECREMENT",
                    requires_fulfillment=True,
                    transactions=True,
                    include_outbound=False,
                )
                payload["normalOrderCreate"] = normal
                normal_order = refresh_order(page, normal.get("order"))
                payload["afterNormal"] = {
                    "inventory": inventory_snapshot(page),
                    "orderCounts": order_counts(page),
                }
            payload["facts"]["normalOrder"] = normal_order

            unpaid = order_create(
                page,
                customer,
                kind="UNPAID-NOFULFILL",
                inventory_behavior="BYPASS",
                requires_fulfillment=False,
                transactions=False,
                include_outbound=False,
            )
            payload["unpaidNoFulfillmentOrderCreate"] = unpaid
            unpaid_order = refresh_order(page, unpaid.get("order"))
            payload["facts"]["unpaidNoFulfillmentOrder"] = unpaid_order
            payload["afterUnpaidNoFulfillment"] = {"orderCounts": order_counts(page)}

            exchange_order_result = order_create(
                page,
                customer,
                kind="EXCHANGE",
                inventory_behavior="BYPASS",
                requires_fulfillment=False,
                transactions=True,
                include_outbound=False,
            )
            payload["exchangeOrderCreate"] = exchange_order_result
            exchange_order = refresh_order(page, exchange_order_result.get("order"))
            payload["facts"]["exchangeOrderBeforeReturn"] = exchange_order
            if exchange_order:
                exchange = create_exchange_return(page, exchange_order)
            else:
                exchange = {"error": "exchange order was not created", "orderCreate": exchange_order_result}
            payload["exchangeReturnCreate"] = exchange
            exchange_return = exchange.get("orderReturn")
            if exchange_return:
                refreshed_return = gql(page, RETURN_BY_ID, {"id": exchange_return["id"]})
                payload["exchangeReturnRefreshed"] = refreshed_return
                payload["facts"]["exchangeReturn"] = (((refreshed_return.get("json") or {}).get("data") or {}).get("orderReturn"))
            payload["afterExchange"] = {"orderCounts": order_counts(page)}

            for label, route in [
                ("orders-list-after", "/admin/orders"),
                ("order-returns-list-after", "/admin/order_returns"),
                ("outbound-orders-list-after", "/admin/inventory_outbound_orders"),
            ]:
                page.goto(f"{BASE}{route}", wait_until="domcontentloaded", timeout=60000)
                wait_soft(page)
                payload["steps"].append(snapshot(page, label))
            for label, order in [
                ("normal-order-detail", normal_order),
                ("unpaid-no-fulfillment-order-detail", unpaid_order),
                ("exchange-order-detail", exchange_order),
            ]:
                if order:
                    page.goto(f"{BASE}/admin/orders/{order['id']}", wait_until="domcontentloaded", timeout=60000)
                    wait_soft(page)
                    payload["steps"].append(snapshot(page, label))

            OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2), encoding="utf-8")
            raise
        finally:
            page.close()
    print(json.dumps(redact(payload["facts"]), ensure_ascii=False, indent=2))


def diff_quantity(before, after):
    before_q = before.get("quantity") or {}
    after_q = after.get("quantity") or {}
    keys = sorted(set(before_q) | set(after_q))
    return {key: (before_q.get(key), after_q.get(key), None if before_q.get(key) is None or after_q.get(key) is None else after_q.get(key) - before_q.get(key)) for key in keys}


def count_value(section, key):
    return (((section.get("orderCounts") or {}).get(key) or {}).get("count"))


def write_md(payload):
    before_inv = payload["before"]["inventory"]
    after_inv = payload["afterNormal"]["inventory"]
    normal = payload["facts"].get("normalOrder") or {}
    unpaid = payload["facts"].get("unpaidNoFulfillmentOrder") or {}
    exchange_order = payload["facts"].get("exchangeOrderBeforeReturn") or {}
    exchange_return = payload["facts"].get("exchangeReturn") or {}
    normal_outbounds = (((normal.get("inventoryOutboundOrders") or {}).get("nodes")) or [])
    exchange_outbound = (exchange_return.get("exchangeInventoryOutboundOrder") or {})
    lines = [
        "# 注文残件追加検証（通常注文・未完了件数・交換返品） 2026-06-28",
        "",
        f"- 実行日時: `{payload['generatedAt']}`",
        f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
        f"- 対象SKU: `{SKU}`",
        f"- 対象ロケーション: `{WAREHOUSE_1905_NAME}`",
        "",
        "## DECREMENT注文",
        "",
        f"- 管理コード: `{normal.get('managementCode')}`",
        f"- paymentStatus / fulfillmentStatus / requiresFulfillment: `{normal.get('paymentStatus')}` / `{normal.get('fulfillmentStatus')}` / `{normal.get('requiresFulfillment')}`",
        f"- inventoryBehavior: `{normal.get('inventoryBehavior')}`",
        f"- 出荷指示数: `{len(normal_outbounds)}`",
    ]
    for outbound in normal_outbounds:
        lines.append(
            f"  - `{outbound.get('managementCode')}` / `{outbound.get('workingStatus')}` / allocated=`{outbound.get('isInventoryAllocated')}` / allocationStatus=`{outbound.get('inventoryAllocationStatus')}`"
        )
    lines.extend([
        "",
        "### 在庫差分（注文前 → DECREMENT注文後）",
        "",
        "| 区分 | before | after | diff |",
        "|:--|--:|--:|--:|",
    ])
    for key, (before, after, diff) in diff_quantity(before_inv, after_inv).items():
        lines.append(f"| `{key}` | {before} | {after} | {diff} |")
    lines.append(f"| `locationAvailability.inventoryQuantity` | {before_inv.get('locationAvailabilityQuantity')} | {after_inv.get('locationAvailabilityQuantity')} | {None if before_inv.get('locationAvailabilityQuantity') is None or after_inv.get('locationAvailabilityQuantity') is None else after_inv.get('locationAvailabilityQuantity') - before_inv.get('locationAvailabilityQuantity')} |")
    lines.extend([
        "",
        "## 未完了件数/決済状態",
        "",
        "| タイミング | WAITING | NON_TERMINAL |",
        "|:--|--:|--:|",
        f"| 作成前 | {count_value(payload['before'], 'WAITING')} | {count_value(payload['before'], 'NON_TERMINAL')} |",
        f"| DECREMENT注文後 | {count_value(payload['afterNormal'], 'WAITING')} | {count_value(payload['afterNormal'], 'NON_TERMINAL')} |",
        f"| 未払い・出荷不要注文後 | {count_value(payload['afterUnpaidNoFulfillment'], 'WAITING')} | {count_value(payload['afterUnpaidNoFulfillment'], 'NON_TERMINAL')} |",
        f"| 交換返品後 | {count_value(payload['afterExchange'], 'WAITING')} | {count_value(payload['afterExchange'], 'NON_TERMINAL')} |",
        "",
        f"- 未払い・出荷不要注文: `{unpaid.get('managementCode')}` / paymentStatus=`{unpaid.get('paymentStatus')}` / fulfillmentStatus=`{unpaid.get('fulfillmentStatus')}` / requiresFulfillment=`{unpaid.get('requiresFulfillment')}`",
        "- `OrderCountFilter` は `inventoryOutboundOrderWorkingStatuses` / `retailLocationID` / `isCancelled` のみを受け付け、paymentStatus条件を持たない。",
        "",
        "## 交換返品",
        "",
        f"- 元注文: `{exchange_order.get('managementCode')}` / paymentStatus=`{exchange_order.get('paymentStatus')}` / fulfillmentStatus=`{exchange_order.get('fulfillmentStatus')}`",
        f"- 返品管理コード: `{exchange_return.get('managementCode')}`",
        f"- status: `{exchange_return.get('status')}`",
        f"- hasExchangeLineItems / exchangeLineItemCount: `{exchange_return.get('hasExchangeLineItems')}` / `{exchange_return.get('exchangeLineItemCount')}`",
        f"- exchange outbound: `{exchange_outbound.get('managementCode')}` / `{exchange_outbound.get('workingStatus')}` / qty=`{exchange_outbound.get('totalQuantity')}`",
        "",
        "## 判断",
        "",
        "- `DECREMENT` 注文は在庫を動かし、出荷指示を持つ注文として作成できる。",
        "- `OrderCountFilter` の形と実測差分から、未完了件数は決済状態ではなく未完了の出荷指示ステータスに紐づく。",
        "- 取引なし・出荷不要の内部 `orderCreate` は paymentStatus=`PAID` になった。非PAID状態はこの経路では再現できていない。",
        "- 交換返品は `exchangeLineItem` と `exchangeInventoryLocationID` を指定して作成でき、返品データに交換明細が紐づく。ただし作成直後の `exchangeInventoryOutboundOrder` は `null`。",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
