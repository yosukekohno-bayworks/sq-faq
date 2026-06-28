#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
RECEIVE_JSON = OUT_DIR / "16-order-return-receive-20260628.json"
OUT_JSON = OUT_DIR / "16-order-return-process-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")
RESTOCK_LOCATION_ID = "8b7c4983-7e88-549c-b23a-6fafc2c4d52c_Location"
RESTOCK_LOCATION_NAME = "ユニクロ物流倉庫"

RETURN_FIELDS = """
fragment ReturnFields on OrderReturn {
  id
  managementCode
  status
  receivable
  completable
  cancellable
  totalQuantity
  totalReceivedQuantity
  order {
    id
    managementCode
    fulfillmentStatus
    paymentStatus
    totalReturnableQuantity
    hasActiveOrderReturns
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
  refunds(first: 10) {
    nodes {
      id
    }
  }
}
"""

RETURN_BY_ID = RETURN_FIELDS + """
query OrderReturnByID($id: ID!) {
  orderReturn(id: $id) {
    ...ReturnFields
  }
}
"""

RETURN_PROCESS = RETURN_FIELDS + """
mutation OrderReturnProcess($input: OrderReturnProcessInput!) {
  orderReturnProcess(input: $input) {
    orderReturn {
      ...ReturnFields
    }
  }
}
"""


def compact(text, limit=3600):
    return " ".join((text or "").split())[:limit]


def wait_soft(page, timeout=12000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
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
            return { status: res.status, ok: res.ok, json, textSample: text.slice(0, 2200) };
        }""",
        {"query": query, "variables": variables or {}},
    )


def snapshot(page, label):
    return {
        "label": label,
        "url": page.url,
        "bodySample": compact(page.inner_text("body"), 5200),
        "headers": [compact(x, 300) for x in page.locator("h1,h2,h3,th").all_inner_texts() if compact(x, 300)],
        "rows": [compact(x, 1000) for x in page.locator("tr").all_inner_texts()[:50] if compact(x, 1000)],
        "buttons": [compact(x, 300) for x in page.locator("button").all_inner_texts()[:120] if compact(x, 300)],
    }


def main():
    receive = json.loads(RECEIVE_JSON.read_text(encoding="utf-8"))
    order_id = receive["orderID"]
    return_id = receive["returnID"]
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "orderID": order_id,
        "returnID": return_id,
        "restockLocationID": RESTOCK_LOCATION_ID,
        "restockLocationName": RESTOCK_LOCATION_NAME,
        "steps": [],
        "facts": {},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(30000)
        try:
            page.goto(f"{BASE}/admin/orders/{order_id}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "order-detail-before-process"))
            before = gql(page, RETURN_BY_ID, {"id": return_id})
            payload["beforeQuery"] = before
            before_return = (((before.get("json") or {}).get("data") or {}).get("orderReturn") or {})
            refund_items = []
            for item in (((before_return.get("lineItems") or {}).get("nodes")) or []):
                order_line = item.get("orderLineItem") or {}
                if (order_line.get("refundableQuantity") or 0) > 0:
                    refund_items.append({
                        "orderLineItemID": order_line["id"],
                        "refundedPrice": {"amount": "1990", "currencyCode": "JPY"},
                        "refundedTaxPrice": {"amount": "0", "currencyCode": "JPY"},
                    })
            input_payload = {
                "orderReturnID": return_id,
                "refundLineItems": refund_items,
                "notifyCustomer": False,
                "refundsShipping": False,
                "restockInventoryLocationID": RESTOCK_LOCATION_ID,
            }
            process_result = gql(page, RETURN_PROCESS, {"input": input_payload})
            payload["processInput"] = input_payload
            payload["processResult"] = process_result
            after_return = ((((process_result.get("json") or {}).get("data") or {}).get("orderReturnProcess") or {}).get("orderReturn"))
            if not after_return:
                raise RuntimeError(f"orderReturnProcess failed: {process_result}")
            payload["facts"]["afterReturn"] = after_return
            page.goto(f"{BASE}/admin/orders/{order_id}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "order-detail-after-process"))
            page.goto(f"{BASE}/admin/order_returns", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "order-returns-list-after-process"))
            page.goto(f"{BASE}/admin/sale_change_line_items", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "sale-change-line-items-after-return-process"))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# 注文返品の完了処理 2026-06-28",
                "",
                f"- 返品ID: `{return_id}`",
                f"- status: `{after_return.get('status')}`",
                f"- receivable/completable/cancellable: `{after_return.get('receivable')}` / `{after_return.get('completable')}` / `{after_return.get('cancellable')}`",
                f"- 数量: total `{after_return.get('totalQuantity')}` / received `{after_return.get('totalReceivedQuantity')}`",
                f"- refunds count: `{len((((after_return.get('refunds') or {}).get('nodes')) or []))}`",
                f"- 注文側 hasActiveOrderReturns: `{(after_return.get('order') or {}).get('hasActiveOrderReturns')}`",
                f"- 注文側 totalReturnableQuantity: `{(after_return.get('order') or {}).get('totalReturnableQuantity')}`",
                f"- restock location: `{RESTOCK_LOCATION_NAME}`",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
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
