#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
ORDER_JSON = OUT_DIR / "16-order-create-bypass-minimal-20260628.json"
OUT_JSON = OUT_DIR / "16-order-return-create-unreceived-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")
STAMP = datetime.now().strftime("%Y%m%d%H%M%S")

ORDER_WITH_LINE_ITEMS = """
query OrderWithLineItems($id: ID!) {
  order(id: $id) {
    id
    managementCode
    managementNumber
    fulfillmentStatus
    paymentStatus
    merchantReturnable
    merchantRefundable
    totalReturnableQuantity
    hasActiveOrderReturns
    lineItems(first: 10) {
      nodes {
        id
        sku
        quantity
        currentQuantity
        refundableQuantity
        returnableQuantity
      }
    }
  }
}
"""

RETURN_FIELDS = """
fragment ReturnFields on OrderReturn {
  id
  managementCode
  externalID
  status
  receivable
  completable
  cancellable
  totalQuantity
  totalReceivedQuantity
  order {
    id
    managementCode
    managementNumber
    fulfillmentStatus
    paymentStatus
    totalReturnableQuantity
    hasActiveOrderReturns
  }
  lineItems(first: 10) {
    nodes {
      id
      externalID
      reason
      quantity
      receivedQuantity
      receivableQuantity
      currentQuantity
      fullReceived
      orderLineItem {
        id
        sku
      }
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

RETURN_CREATE = RETURN_FIELDS + """
mutation CreateOrderReturn($input: OrderReturnCreateInput!) {
  orderReturnCreate(input: $input) {
    orderReturn {
      ...ReturnFields
    }
  }
}
"""


def compact(text, limit=3200):
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
    return {
        "label": label,
        "url": page.url,
        "title": page.title(),
        "bodySample": compact(page.inner_text("body"), 4200),
        "headers": [compact(x, 300) for x in page.locator("h1,h2,h3,th").all_inner_texts() if compact(x, 300)],
        "rows": [compact(x, 1000) for x in page.locator("tr").all_inner_texts()[:50] if compact(x, 1000)],
        "buttons": [compact(x, 300) for x in page.locator("button").all_inner_texts()[:100] if compact(x, 300)],
        "links": page.evaluate(
            """() => Array.from(document.querySelectorAll('a[href]')).slice(0, 140).map((a) => ({
                text: (a.innerText || a.textContent || '').trim().replace(/\\s+/g, ' '),
                href: a.getAttribute('href'),
            }))"""
        ),
    }


def main():
    order_facts = json.loads(ORDER_JSON.read_text(encoding="utf-8"))["facts"]["order"]
    order_id = order_facts["id"]
    external_id = f"FAQ_RETURN_UNRECEIVED_{STAMP}"
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "testReturn": {
            "externalID": external_id,
            "orderID": order_id,
            "orderManagementCode": order_facts["managementCode"],
            "received": False,
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
            page.goto(f"{BASE}/admin/orders/{order_id}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "order-detail-before-return"))
            before_order = gql(page, ORDER_WITH_LINE_ITEMS, {"id": order_id})
            payload["beforeOrderQuery"] = before_order
            order = (((before_order.get("json") or {}).get("data") or {}).get("order") or {})
            line_items = (((order.get("lineItems") or {}).get("nodes")) or [])
            target_line = next((x for x in line_items if (x.get("returnableQuantity") or 0) > 0), None)
            if not target_line:
                raise RuntimeError(f"no returnable line item: {line_items}")
            input_payload = {
                "orderID": order_id,
                "externalID": external_id,
                "received": False,
                "orderReturnLineItems": [
                    {
                        "externalID": f"FAQ-RETURN-LINE-{STAMP}",
                        "orderLineItemID": target_line["id"],
                        "quantity": 1,
                        "reason": "FAQ実機検証: 未受領返品",
                    }
                ],
            }
            result = gql(page, RETURN_CREATE, {"input": input_payload})
            payload["createResult"] = result
            order_return = ((((result.get("json") or {}).get("data") or {}).get("orderReturnCreate") or {}).get("orderReturn"))
            if not order_return:
                raise RuntimeError(f"orderReturnCreate failed: {result}")
            payload["facts"]["createdReturn"] = order_return
            page.goto(f"{BASE}/admin/order_returns", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "order-returns-list-after-create"))
            list_body = page.inner_text("body")
            payload["facts"]["returnListShowsManagementCode"] = order_return.get("managementCode") in list_body
            page.goto(f"{BASE}/admin/order_returns/{order_return['id']}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "order-return-detail"))
            detail_body = page.inner_text("body")
            payload["facts"]["returnDetailURL"] = page.url
            payload["facts"]["returnDetailShowsManagementCode"] = order_return.get("managementCode") in detail_body
            page.goto(f"{BASE}/admin/orders/{order_id}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "order-detail-after-return"))
            after_order = gql(page, ORDER_WITH_LINE_ITEMS, {"id": order_id})
            payload["afterOrderQuery"] = after_order
            after_order_data = (((after_order.get("json") or {}).get("data") or {}).get("order") or {})
            payload["facts"]["afterOrder"] = {
                "hasActiveOrderReturns": after_order_data.get("hasActiveOrderReturns"),
                "totalReturnableQuantity": after_order_data.get("totalReturnableQuantity"),
                "lineItems": (((after_order_data.get("lineItems") or {}).get("nodes")) or []),
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# 注文返品を内部GraphQLで作成（未受領） 2026-06-28",
                "",
                f"- 元注文: `{order_facts['managementCode']}` / `{order_id}`",
                f"- 返品ID: `{order_return.get('id')}`",
                f"- 返品管理コード: `{order_return.get('managementCode')}`",
                f"- 作成時status: `{order_return.get('status')}`",
                f"- receivable/completable/cancellable: `{order_return.get('receivable')}` / `{order_return.get('completable')}` / `{order_return.get('cancellable')}`",
                f"- 数量: total `{order_return.get('totalQuantity')}` / received `{order_return.get('totalReceivedQuantity')}`",
                f"- 返品一覧に表示: `{payload['facts'].get('returnListShowsManagementCode')}`",
                f"- 返品詳細に表示: `{payload['facts'].get('returnDetailShowsManagementCode')}`",
                f"- 注文側 hasActiveOrderReturns: `{payload['facts']['afterOrder'].get('hasActiveOrderReturns')}`",
                f"- 注文側 totalReturnableQuantity: `{payload['facts']['afterOrder'].get('totalReturnableQuantity')}`",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                "",
                "## 注意",
                "",
                "- `received=false` で作成したため、受領・返金・在庫戻しの完了挙動はこのスクリプトでは実行していません。",
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
