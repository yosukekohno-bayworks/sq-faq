#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "16-order-create-support-data-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")
SKU = "TEST_E2E_20260622_GU_1905_NAVY_M"

LOCATIONS_QUERY = """
query LocationsForOrderCreate {
  locations(first: 100) {
    nodes {
      id
      name
      displayName
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

PRODUCT_VARIANTS_QUERY = """
query ProductVariantsForOrderCreate($first: Int!) {
  productVariants(first: $first) {
    nodes {
      id
      title
      externalID
      status
      barcode
      price { amount currencyCode }
      product { id title code }
      inventoryItem { sku }
    }
  }
}
"""


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
            return { status: res.status, ok: res.ok, json, textSample: text.slice(0, 1600) };
        }""",
        {"query": query, "variables": variables or {}},
    )


def wait_soft(page):
    try:
        page.wait_for_load_state("networkidle", timeout=12000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(500)


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "targetSku": SKU,
        "locationsResult": None,
        "productVariantsResult": None,
        "facts": {},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            page.goto(f"{BASE}/admin/orders", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            locations = gql(page, LOCATIONS_QUERY)
            variants = gql(page, PRODUCT_VARIANTS_QUERY, {"first": 100})
            payload["locationsResult"] = locations
            payload["productVariantsResult"] = variants
            location_nodes = (((locations.get("json") or {}).get("data") or {}).get("locations") or {}).get("nodes") or []
            variant_nodes = (((variants.get("json") or {}).get("data") or {}).get("productVariants") or {}).get("nodes") or []
            target_variants = [v for v in variant_nodes if ((v.get("inventoryItem") or {}).get("sku") == SKU)]
            payload["facts"] = {
                "locationCount": len(location_nodes),
                "activeLocations": [
                    {
                        "id": x.get("id"),
                        "name": x.get("name"),
                        "code": x.get("code"),
                        "locationType": x.get("locationType"),
                        "isRetailLocation": x.get("isRetailLocation"),
                        "isLocalPickupEnabled": x.get("isLocalPickupEnabled"),
                    }
                    for x in location_nodes
                    if not x.get("isArchived") and not x.get("isClosed")
                ],
                "targetVariantCountInFirst100": len(target_variants),
                "targetVariants": target_variants,
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# orderCreate用サポートデータ確認 2026-06-28",
                "",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                f"- ロケーション件数: `{payload['facts']['locationCount']}`",
                f"- 対象SKU `{SKU}` のfirst100内一致: `{payload['facts']['targetVariantCountInFirst100']}`",
                "",
                "## active locations",
                "",
            ]
            for loc in payload["facts"]["activeLocations"]:
                lines.append(f"- `{loc['code']}` / `{loc['name']}` / `{loc['locationType']}` / `{loc['id']}` / retail={loc['isRetailLocation']} pickup={loc['isLocalPickupEnabled']}")
            lines.append("")
            lines.append("## target variants")
            lines.append("")
            for variant in target_variants:
                lines.append(f"- `{((variant.get('inventoryItem') or {}).get('sku'))}` / `{variant.get('id')}` / `{(variant.get('product') or {}).get('title')}` / `{variant.get('title')}`")
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
