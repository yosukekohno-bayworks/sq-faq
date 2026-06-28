#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "16-remaining-order-introspection-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"

TYPE_QUERY = """
query TypeInfo($name: String!) {
  __type(name: $name) {
    kind
    name
    fields {
      name
      args {
        name
        type { kind name ofType { kind name ofType { kind name ofType { kind name } } } }
      }
      type { kind name ofType { kind name ofType { kind name ofType { kind name } } } }
    }
    inputFields {
      name
      type { kind name ofType { kind name ofType { kind name ofType { kind name } } } }
    }
    enumValues { name }
  }
}
"""

SUPPORT_QUERY = """
query RemainingOrderSupport($sku: String!) {
  productVariantBySKU(sku: $sku) {
    id
    title
    externalID
    status
    product { id title }
    inventoryItem { id sku }
  }
  locations(first: 100) {
    nodes {
      id
      name
      code
      locationType
      isRetailLocation
      isLocalPickupEnabled
      isInventoryAllocationRequestEnabled
      isArchived
      isClosed
    }
  }
}
"""


def compact(text, limit=3000):
    return " ".join((text or "").split())[:limit]


def type_name(node):
    if not node:
        return ""
    kind = node.get("kind")
    if kind == "NON_NULL":
        return type_name(node.get("ofType")) + "!"
    if kind == "LIST":
        return "[" + type_name(node.get("ofType")) + "]"
    return node.get("name") or kind or ""


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


def wait_soft(page):
    try:
        page.wait_for_load_state("networkidle", timeout=12000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(700)


def shape_type(type_info):
    if not type_info:
        return None
    return {
        "kind": type_info.get("kind"),
        "name": type_info.get("name"),
        "enumValues": [x["name"] for x in type_info.get("enumValues") or []],
        "fields": [
            {
                "name": f["name"],
                "type": type_name(f.get("type")),
                "args": [{"name": a["name"], "type": type_name(a.get("type"))} for a in f.get("args") or []],
            }
            for f in type_info.get("fields") or []
        ],
        "inputFields": [
            {"name": f["name"], "type": type_name(f.get("type"))}
            for f in type_info.get("inputFields") or []
        ],
    }


def main():
    type_names = [
        "ProductVariant",
        "InventoryItem",
        "InventoryLevel",
        "InventoryQuantity",
        "LocationAvailability",
        "InventoryLogicalAdjustmentGroup",
        "Order",
        "OrderFilter",
        "OrderCountFilter",
        "OrderPaymentStatus",
        "OrderFulfillmentStatus",
        "OrderReturn",
        "OrderReturnLineItem",
        "OrderExchangeLineItem",
        "OrderReturnLineItemCreateInput",
        "OrderReturnLineItemCreateExchangeLineItemInput",
        "InventoryOutboundOrder",
        "InventoryOutboundOrderWorkingStatus",
        "InventoryOutboundOrderFilter",
    ]
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "targetSku": SKU,
        "types": {},
        "support": {},
        "pages": {},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(30000)
        try:
            page.goto(f"{BASE}/admin/orders", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["pages"]["ordersBodySample"] = compact(page.inner_text("body"), 2600)
            for name in type_names:
                result = gql(page, TYPE_QUERY, {"name": name})
                payload["types"][name] = {
                    "rawStatus": result["status"],
                    "type": shape_type(((result.get("json") or {}).get("data") or {}).get("__type")),
                    "errors": (result.get("json") or {}).get("errors"),
                }
            support = gql(page, SUPPORT_QUERY, {"sku": SKU})
            payload["support"] = support
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            data = ((support.get("json") or {}).get("data") or {})
            variant = data.get("productVariantBySKU")
            locations = (((data.get("locations") or {}).get("nodes")) or [])
            active = [x for x in locations if not x.get("isArchived") and not x.get("isClosed")]
            lines = [
                "# 注文残件検証向けGraphQL型・サポートデータ確認 2026-06-28",
                "",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                f"- 対象SKU: `{SKU}`",
                f"- variant id: `{(variant or {}).get('id')}`",
                f"- inventory item id: `{((variant or {}).get('inventoryItem') or {}).get('id')}`",
                f"- active location count: `{len(active)}`",
                "",
                "## enum",
                "",
            ]
            for name in ["OrderPaymentStatus", "OrderFulfillmentStatus"]:
                info = ((payload["types"].get(name) or {}).get("type") or {})
                lines.append(f"- {name}: `{', '.join(info.get('enumValues') or [])}`")
            lines.extend(["", "## key input fields", ""])
            for name in ["OrderFilter", "OrderCountFilter", "OrderReturnLineItemCreateInput"]:
                info = ((payload["types"].get(name) or {}).get("type") or {})
                lines.append(f"### {name}")
                for field in info.get("inputFields") or []:
                    lines.append(f"- `{field['name']}`: `{field['type']}`")
                lines.append("")
            lines.append("## active locations")
            lines.append("")
            for loc in active:
                lines.append(
                    f"- `{loc.get('code')}` / `{loc.get('name')}` / `{loc.get('locationType')}` / `{loc.get('id')}`"
                )
            OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
        except Exception as exc:
            payload["errors"].append(repr(exc))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            raise
        finally:
            page.close()
    print(json.dumps({"json": str(OUT_JSON), "errors": payload["errors"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
