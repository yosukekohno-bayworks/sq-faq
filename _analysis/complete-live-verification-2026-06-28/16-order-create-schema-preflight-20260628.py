#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "16-order-create-schema-preflight-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")

TYPE_REF = """
fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType { kind name }
      }
    }
  }
}
"""

TYPE_QUERY = TYPE_REF + """
query TypeInfo($name: String!) {
  __type(name: $name) {
    kind
    name
    fields {
      name
      type { ...TypeRef }
    }
    inputFields {
      name
      type { ...TypeRef }
    }
    enumValues {
      name
    }
    possibleTypes {
      name
    }
  }
}
"""

MUTATION_FIELD_QUERY = TYPE_REF + """
query MutationField($name: String!) {
  __schema {
    mutationType {
      fields {
        name
        type { ...TypeRef }
        args {
          name
          type { ...TypeRef }
        }
      }
    }
  }
}
"""

TARGET_TYPES = [
    "InventoryBehavior",
    "CurrencyCode",
    "OrderTransactionKind",
    "PointApplicationType",
    "OrderCreatePayload",
    "OrderCreateInput",
    "OrderCreateOptionInput",
    "Order",
    "Location",
    "ProductVariant",
    "OrderLineItem",
    "OrderReturn",
    "OrderReturnLineItem",
]


def type_label(ref):
    if not ref:
        return ""
    kind = ref.get("kind")
    name = ref.get("name")
    inner = type_label(ref.get("ofType"))
    if kind == "NON_NULL":
        return f"{inner}!"
    if kind == "LIST":
        return f"[{inner}]"
    return name or kind or ""


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


def wait_soft(page):
    try:
        page.wait_for_load_state("networkidle", timeout=12000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(500)


def normalize_type(t):
    if not t:
        return None
    return {
        "kind": t.get("kind"),
        "name": t.get("name"),
        "fields": [
            {"name": f.get("name"), "type": type_label(f.get("type"))}
            for f in (t.get("fields") or [])
        ],
        "inputFields": [
            {"name": f.get("name"), "type": type_label(f.get("type"))}
            for f in (t.get("inputFields") or [])
        ],
        "enumValues": [v.get("name") for v in (t.get("enumValues") or [])],
        "possibleTypes": [v.get("name") for v in (t.get("possibleTypes") or [])],
    }


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "targetTypes": TARGET_TYPES,
        "types": {},
        "orderCreateMutation": None,
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            page.goto(f"{BASE}/admin/orders", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            for name in TARGET_TYPES:
                result = gql(page, TYPE_QUERY, {"name": name})
                payload["types"][name] = normalize_type(((result.get("json") or {}).get("data") or {}).get("__type"))
            field_result = gql(page, MUTATION_FIELD_QUERY, {"name": "orderCreate"})
            fields = ((((field_result.get("json") or {}).get("data") or {}).get("__schema") or {}).get("mutationType") or {}).get("fields") or []
            for field in fields:
                if field.get("name") == "orderCreate":
                    payload["orderCreateMutation"] = {
                        "name": field.get("name"),
                        "type": type_label(field.get("type")),
                        "args": [
                            {"name": arg.get("name"), "type": type_label(arg.get("type"))}
                            for arg in (field.get("args") or [])
                        ],
                    }
                    break
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# orderCreate スキーマ事前確認 2026-06-28",
                "",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                f"- orderCreate: `{payload['orderCreateMutation']}`",
                "",
            ]
            for name in TARGET_TYPES:
                info = payload["types"].get(name) or {}
                lines.append(f"## {name}")
                if info.get("enumValues"):
                    lines.append(f"- enum: `{', '.join(info['enumValues'])}`")
                if info.get("inputFields"):
                    lines.append("- inputFields:")
                    for field in info["inputFields"]:
                        lines.append(f"  - `{field['name']}`: `{field['type']}`")
                if info.get("fields"):
                    lines.append("- fields:")
                    for field in info["fields"][:80]:
                        lines.append(f"  - `{field['name']}`: `{field['type']}`")
                lines.append("")
            OUT_MD.write_text("\n".join(lines), encoding="utf-8")
        except Exception as exc:
            payload["errors"].append(repr(exc))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            raise
        finally:
            page.close()
    print(json.dumps({
        "orderCreate": payload["orderCreateMutation"],
        "InventoryBehavior": (payload["types"].get("InventoryBehavior") or {}).get("enumValues"),
        "CurrencyCodeHasJPY": "JPY" in ((payload["types"].get("CurrencyCode") or {}).get("enumValues") or []),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
