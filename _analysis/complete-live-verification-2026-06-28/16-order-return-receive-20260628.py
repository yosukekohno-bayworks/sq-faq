#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
RETURN_JSON = OUT_DIR / "16-order-return-create-unreceived-20260628.json"
OUT_JSON = OUT_DIR / "16-order-return-receive-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")

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
}
"""

RETURN_BY_ID = RETURN_FIELDS + """
query OrderReturnByID($id: ID!) {
  orderReturn(id: $id) {
    ...ReturnFields
  }
}
"""

RETURN_RECEIVE = RETURN_FIELDS + """
mutation OrderReturnReceive($input: OrderReturnReceiveInput!) {
  orderReturnReceive(input: $input) {
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
            return { status: res.status, ok: res.ok, json, textSample: text.slice(0, 1800) };
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
        "links": page.evaluate(
            """() => Array.from(document.querySelectorAll('a[href]')).slice(0, 160).map((a) => ({
                text: (a.innerText || a.textContent || '').trim().replace(/\\s+/g, ' '),
                href: a.getAttribute('href'),
            }))"""
        ),
        "dialogText": compact(page.locator("[role='dialog']").first.inner_text(), 2200) if page.locator("[role='dialog']").count() else "",
    }


def click_dialog_button(page, names):
    dialog = page.locator("[role='dialog']")
    scope = dialog.first if dialog.count() else page
    for name in names:
        loc = scope.get_by_role("button", name=name, exact=True)
        if loc.count():
            loc.last.click(timeout=10000)
            wait_soft(page)
            return name
    return None


def main():
    source = json.loads(RETURN_JSON.read_text(encoding="utf-8"))
    order_id = source["testReturn"]["orderID"]
    order_return = source["facts"]["createdReturn"]
    return_id = order_return["id"]
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "orderID": order_id,
        "returnID": return_id,
        "returnManagementCode": order_return["managementCode"],
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
            payload["steps"].append(snapshot(page, "before-receive"))
            before_query = gql(page, RETURN_BY_ID, {"id": return_id})
            payload["beforeQuery"] = before_query
            receive_button = page.get_by_role("button", name="商品を受け取る", exact=True)
            receive_text = page.get_by_text("商品を受け取る", exact=True)
            payload["facts"]["receiveButtonCountBefore"] = receive_button.count()
            payload["facts"]["receiveTextCountBefore"] = receive_text.count()
            if receive_button.count():
                receive_button.first.click(timeout=10000)
                payload["facts"]["receiveClickMode"] = "button"
            elif receive_text.count():
                receive_text.first.click(timeout=10000)
                payload["facts"]["receiveClickMode"] = "text"
            else:
                raise RuntimeError("商品を受け取る control not found")
            wait_soft(page)
            payload["steps"].append(snapshot(page, "after-click-receive"))
            clicked_confirm = click_dialog_button(page, ["商品を受け取る", "受け取る", "登録する", "保存する", "実行する"])
            payload["facts"]["confirmButtonClicked"] = clicked_confirm
            payload["steps"].append(snapshot(page, "after-confirm-receive"))
            after_query = gql(page, RETURN_BY_ID, {"id": return_id})
            payload["afterQuery"] = after_query
            after_return = (((after_query.get("json") or {}).get("data") or {}).get("orderReturn") or {})
            if after_return.get("totalReceivedQuantity") == 0 and after_return.get("receivable"):
                receive_items = []
                for item in (((after_return.get("lineItems") or {}).get("nodes")) or []):
                    if (item.get("receivableQuantity") or 0) > 0:
                        receive_items.append({
                            "orderReturnLineItemID": item["id"],
                            "receivedQuantity": item["receivableQuantity"],
                        })
                if receive_items:
                    receive_result = gql(page, RETURN_RECEIVE, {
                        "input": {
                            "orderReturnID": return_id,
                            "orderReturnLineItems": receive_items,
                        }
                    })
                    payload["graphqlReceiveResult"] = receive_result
                    after_return = ((((receive_result.get("json") or {}).get("data") or {}).get("orderReturnReceive") or {}).get("orderReturn")) or after_return
                    page.goto(f"{BASE}/admin/orders/{order_id}", wait_until="domcontentloaded", timeout=60000)
                    wait_soft(page)
                    payload["steps"].append(snapshot(page, "after-graphql-receive"))
            payload["facts"]["afterReturn"] = after_return
            body = page.inner_text("body")
            payload["facts"]["bodyHasReceivedOneOfOne"] = "1 個中の 1 個を受け取り済み" in body or "1個中の1個" in body
            payload["facts"]["bodyHasReceiveButtonAfter"] = page.get_by_role("button", name="商品を受け取る", exact=True).count() > 0
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# 注文返品の商品受け取り 2026-06-28",
                "",
                f"- 返品: `{order_return['managementCode']}` / `{return_id}`",
                f"- 確認ボタン: `{clicked_confirm}`",
                f"- status: `{after_return.get('status')}`",
                f"- receivable/completable/cancellable: `{after_return.get('receivable')}` / `{after_return.get('completable')}` / `{after_return.get('cancellable')}`",
                f"- 数量: total `{after_return.get('totalQuantity')}` / received `{after_return.get('totalReceivedQuantity')}`",
                f"- 画面で1/1受領表示: `{payload['facts'].get('bodyHasReceivedOneOfOne')}`",
                f"- 受領後も商品を受け取るボタン表示: `{payload['facts'].get('bodyHasReceiveButtonAfter')}`",
                f"- 注文側 hasActiveOrderReturns: `{(after_return.get('order') or {}).get('hasActiveOrderReturns')}`",
                f"- 注文側 totalReturnableQuantity: `{(after_return.get('order') or {}).get('totalReturnableQuantity')}`",
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
