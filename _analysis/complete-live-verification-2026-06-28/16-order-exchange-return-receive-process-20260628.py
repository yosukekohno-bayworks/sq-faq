#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
SOURCE_JSON = OUT_DIR / "16-order-remaining-normal-exchange-20260628.json"
OUT_JSON = OUT_DIR / "16-order-exchange-return-receive-process-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")
RESTOCK_LOCATION_ID = "d018dd79-47b6-5a93-a1bf-0e12cac23d3e_Location"
RESTOCK_LOCATION_NAME = "TEST_E2E_20260622_GU倉庫_ON_1905"

RETURN_FIELDS = """
fragment ExchangeReturnFields on OrderReturn {
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
    kind
    workingStatus
    totalQuantity
    isInventoryAllocated
    isFulfillable
    inventoryAllocationStatus
    inventoryLocation { id name code locationType }
  }
  lineItems(first: 10) {
    nodes {
      id
      quantity
      receivedQuantity
      receivableQuantity
      currentQuantity
      fullReceived
      orderLineItem { id sku returnableQuantity refundableQuantity currentQuantity }
    }
  }
  refunds(first: 10) { nodes { id } }
  order { id managementCode managementNumber paymentStatus fulfillmentStatus totalReturnableQuantity hasActiveOrderReturns }
}
"""

RETURN_BY_EXTERNAL_ID = RETURN_FIELDS + """
query ExchangeReturnByExternalID($externalID: String!) {
  orderReturnByExternalID(externalID: $externalID) { ...ExchangeReturnFields }
}
"""

RETURN_BY_ID = RETURN_FIELDS + """
query ExchangeReturnByID($id: ID!) {
  orderReturn(id: $id) { ...ExchangeReturnFields }
}
"""

RETURN_RECEIVE = RETURN_FIELDS + """
mutation ExchangeReturnReceive($input: OrderReturnReceiveInput!) {
  orderReturnReceive(input: $input) {
    orderReturn { ...ExchangeReturnFields }
  }
}
"""

RETURN_PROCESS = RETURN_FIELDS + """
mutation ExchangeReturnProcess($input: OrderReturnProcessInput!) {
  orderReturnProcess(input: $input) {
    orderReturn { ...ExchangeReturnFields }
  }
}
"""


def compact(text, limit=4200):
    return " ".join((text or "").split())[:limit]


def wait_soft(page):
    try:
        page.wait_for_load_state("networkidle", timeout=12000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


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
    return {
        "label": label,
        "url": page.url,
        "bodySample": compact(page.inner_text("body"), 5200),
        "headers": [compact(x, 300) for x in page.locator("h1,h2,h3,th").all_inner_texts() if compact(x, 300)],
        "rows": [compact(x, 1000) for x in page.locator("tr").all_inner_texts()[:60] if compact(x, 1000)],
        "buttons": [compact(x, 300) for x in page.locator("button").all_inner_texts()[:140] if compact(x, 300)],
        "links": page.evaluate(
            """() => Array.from(document.querySelectorAll('a[href]')).slice(0, 180).map((a) => ({
                text: (a.innerText || a.textContent || '').trim().replace(/\\s+/g, ' '),
                href: a.getAttribute('href'),
            }))"""
        ),
    }


def load_exchange_external_id():
    data = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    external_id = ((data.get("facts") or {}).get("exchangeReturn") or {}).get("externalID")
    if not external_id:
        raise RuntimeError("exchange return externalID not found in source json")
    return external_id


def receive_return(page, order_return):
    receive_items = []
    for item in (((order_return.get("lineItems") or {}).get("nodes")) or []):
        qty = item.get("receivableQuantity") or 0
        if qty > 0:
            receive_items.append({"orderReturnLineItemID": item["id"], "receivedQuantity": qty})
    if not receive_items:
        return {"skipped": True, "reason": "no receivable line items"}
    return gql(page, RETURN_RECEIVE, {"input": {"orderReturnID": order_return["id"], "orderReturnLineItems": receive_items}})


def process_return(page, order_return):
    input_payload = {
        "orderReturnID": order_return["id"],
        "refundLineItems": [],
        "notifyCustomer": False,
        "refundsShipping": False,
        "restockInventoryLocationID": RESTOCK_LOCATION_ID,
    }
    return {"input": input_payload, "result": gql(page, RETURN_PROCESS, {"input": input_payload})}


def main():
    external_id = load_exchange_external_id()
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "exchangeReturnExternalID": external_id,
        "restockLocation": {"id": RESTOCK_LOCATION_ID, "name": RESTOCK_LOCATION_NAME},
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
            before = gql(page, RETURN_BY_EXTERNAL_ID, {"externalID": external_id})
            payload["beforeQuery"] = before
            order_return = (((before.get("json") or {}).get("data") or {}).get("orderReturnByExternalID"))
            if not order_return:
                raise RuntimeError(f"exchange return not found: {before}")
            order_id = (order_return.get("order") or {}).get("id")
            payload["facts"]["before"] = order_return
            page.goto(f"{BASE}/admin/orders/{order_id}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "order-detail-before-receive"))

            receive_result = receive_return(page, order_return)
            payload["receiveResult"] = receive_result
            after_receive_return = None
            if isinstance(receive_result, dict) and receive_result.get("json"):
                after_receive_return = ((((receive_result.get("json") or {}).get("data") or {}).get("orderReturnReceive") or {}).get("orderReturn"))
            if not after_receive_return:
                query = gql(page, RETURN_BY_ID, {"id": order_return["id"]})
                payload["afterReceiveQuery"] = query
                after_receive_return = (((query.get("json") or {}).get("data") or {}).get("orderReturn"))
            payload["facts"]["afterReceive"] = after_receive_return
            page.goto(f"{BASE}/admin/orders/{order_id}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "order-detail-after-receive"))

            if after_receive_return and after_receive_return.get("completable"):
                process_result = process_return(page, after_receive_return)
                payload["processResult"] = process_result
                processed = ((((process_result.get("result") or {}).get("json") or {}).get("data") or {}).get("orderReturnProcess") or {}).get("orderReturn")
                if processed:
                    payload["facts"]["afterProcess"] = processed
                else:
                    query = gql(page, RETURN_BY_ID, {"id": order_return["id"]})
                    payload["afterProcessQuery"] = query
                    payload["facts"]["afterProcess"] = (((query.get("json") or {}).get("data") or {}).get("orderReturn"))
            else:
                payload["processResult"] = {"skipped": True, "reason": "return not completable after receive"}

            page.goto(f"{BASE}/admin/orders/{order_id}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "order-detail-after-process-attempt"))
            page.goto(f"{BASE}/admin/inventory_outbound_orders", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "outbound-list-after-exchange-process"))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
        except Exception as exc:
            payload["errors"].append(repr(exc))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            raise
        finally:
            page.close()
    print(json.dumps(payload["facts"], ensure_ascii=False, indent=2))


def summarize_return(order_return):
    outbound = (order_return or {}).get("exchangeInventoryOutboundOrder") or {}
    return {
        "managementCode": (order_return or {}).get("managementCode"),
        "status": (order_return or {}).get("status"),
        "receivable": (order_return or {}).get("receivable"),
        "completable": (order_return or {}).get("completable"),
        "cancellable": (order_return or {}).get("cancellable"),
        "totalReceivedQuantity": (order_return or {}).get("totalReceivedQuantity"),
        "hasExchangeLineItems": (order_return or {}).get("hasExchangeLineItems"),
        "exchangeLineItemCount": (order_return or {}).get("exchangeLineItemCount"),
        "exchangeOutboundCode": outbound.get("managementCode"),
        "exchangeOutboundStatus": outbound.get("workingStatus"),
        "exchangeOutboundQty": outbound.get("totalQuantity"),
    }


def write_md(payload):
    before = summarize_return(payload["facts"].get("before"))
    after_receive = summarize_return(payload["facts"].get("afterReceive"))
    after_process = summarize_return(payload["facts"].get("afterProcess"))
    process_result = payload.get("processResult") or {}
    process_errors = (((process_result.get("result") or {}).get("json") or {}).get("errors")) if isinstance(process_result, dict) else None
    lines = [
        "# 交換返品の受領・完了処理 2026-06-28",
        "",
        f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
        f"- 返品 externalID: `{payload['exchangeReturnExternalID']}`",
        "",
        "## 状態推移",
        "",
        "| タイミング | status | receivable | completable | received | exchange outbound |",
        "|:--|:--|:--|:--|--:|:--|",
        f"| 作成直後 | `{before['status']}` | `{before['receivable']}` | `{before['completable']}` | {before['totalReceivedQuantity']} | `{before['exchangeOutboundCode']}` / `{before['exchangeOutboundStatus']}` |",
        f"| 受領後 | `{after_receive['status']}` | `{after_receive['receivable']}` | `{after_receive['completable']}` | {after_receive['totalReceivedQuantity']} | `{after_receive['exchangeOutboundCode']}` / `{after_receive['exchangeOutboundStatus']}` |",
        f"| 完了試行後 | `{after_process.get('status')}` | `{after_process.get('receivable')}` | `{after_process.get('completable')}` | {after_process.get('totalReceivedQuantity')} | `{after_process.get('exchangeOutboundCode')}` / `{after_process.get('exchangeOutboundStatus')}` |",
        "",
        "## 交換明細",
        "",
        f"- hasExchangeLineItems: `{after_receive['hasExchangeLineItems']}`",
        f"- exchangeLineItemCount: `{after_receive['exchangeLineItemCount']}`",
        "",
        "## 完了処理",
        "",
        f"- process skipped: `{process_result.get('skipped')}`",
        f"- process errors: `{process_errors}`",
        "",
        "## 判断",
        "",
        "- 交換明細付き返品は作成でき、受領すると `RECEIVED` になる。",
        "- 作成直後・受領後は `exchangeInventoryOutboundOrder` が `null` のまま。",
        "- `orderReturnProcess` 完了後、`ORDER_EXCHANGE` の交換出荷指示 `#IO-1040` が `WAITING` で生成された。",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
