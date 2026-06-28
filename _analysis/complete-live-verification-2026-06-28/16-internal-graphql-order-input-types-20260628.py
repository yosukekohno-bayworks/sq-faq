#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "16-internal-graphql-order-input-types-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

TARGET_MUTATIONS = [
    "orderCreate",
    "orderReturnCreate",
    "orderRefundCreate",
    "saleChangeCreate",
    "purchasingCustomerCreate",
    "inventoryOutboundOrderComplete",
]

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
        ofType {
          kind
          name
          ofType { kind name }
        }
      }
    }
  }
}
"""

MUTATION_QUERY = TYPE_REF + """
query TargetMutationArgs {
  __schema {
    mutationType {
      fields {
        name
        args {
          name
          type { ...TypeRef }
        }
      }
    }
  }
}
"""

TYPE_QUERY = TYPE_REF + """
query InputType($name: String!) {
  __type(name: $name) {
    kind
    name
    inputFields {
      name
      defaultValue
      type { ...TypeRef }
    }
    enumValues {
      name
    }
  }
}
"""


def type_name(ref):
    cur = ref
    while cur:
        if cur.get("name"):
            return cur["name"]
        cur = cur.get("ofType")
    return None


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
            return { status: res.status, ok: res.ok, json, textSample: text.slice(0, 1000) };
        }""",
        {"query": query, "variables": variables or {}},
    )


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "targetMutations": TARGET_MUTATIONS,
        "mutationArgs": {},
        "inputTypes": {},
        "facts": {},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            page.goto(f"{BASE}/admin/orders", wait_until="domcontentloaded", timeout=60000)
            try:
                page.wait_for_load_state("networkidle", timeout=12000)
            except PlaywrightTimeoutError:
                pass
            result = gql(page, MUTATION_QUERY)
            fields = (((result.get("json") or {}).get("data") or {}).get("__schema") or {}).get("mutationType", {}).get("fields") or []
            to_visit = []
            for field in fields:
                if field.get("name") not in TARGET_MUTATIONS:
                    continue
                args = []
                for arg in field.get("args") or []:
                    ref = arg.get("type") or {}
                    name = type_name(ref)
                    args.append({"name": arg.get("name"), "type": type_label(ref), "baseType": name})
                    if name and name not in to_visit:
                        to_visit.append(name)
                payload["mutationArgs"][field["name"]] = args
            visited = set()
            while to_visit:
                name = to_visit.pop(0)
                if name in visited or name.startswith("__"):
                    continue
                visited.add(name)
                type_result = gql(page, TYPE_QUERY, {"name": name})
                t = ((type_result.get("json") or {}).get("data") or {}).get("__type")
                if not t:
                    continue
                input_fields = []
                for field in t.get("inputFields") or []:
                    ref = field.get("type") or {}
                    base = type_name(ref)
                    input_fields.append({
                        "name": field.get("name"),
                        "type": type_label(ref),
                        "baseType": base,
                        "defaultValue": field.get("defaultValue"),
                    })
                    if base and base not in visited and base not in to_visit and base.endswith("Input"):
                        to_visit.append(base)
                payload["inputTypes"][name] = {
                    "kind": t.get("kind"),
                    "fields": input_fields,
                    "enumValues": [v.get("name") for v in t.get("enumValues") or []],
                }
            payload["facts"] = {
                "targetMutationCount": len(payload["mutationArgs"]),
                "inputTypeCount": len(payload["inputTypes"]),
                "hasOrderCreateInput": bool(payload["mutationArgs"].get("orderCreate")),
                "hasPurchasingCustomerCreateInput": bool(payload["mutationArgs"].get("purchasingCustomerCreate")),
                "orderCreateArgs": payload["mutationArgs"].get("orderCreate"),
                "purchasingCustomerCreateArgs": payload["mutationArgs"].get("purchasingCustomerCreate"),
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# 内部GraphQL 入力型確認 2026-06-28",
                "",
                f"- 対象mutation: `{', '.join(TARGET_MUTATIONS)}`",
                f"- mutation確認数: `{payload['facts']['targetMutationCount']}`",
                f"- input型確認数: `{payload['facts']['inputTypeCount']}`",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                "",
                "## mutation args",
                "",
            ]
            for name, args in payload["mutationArgs"].items():
                lines.append(f"### {name}")
                for arg in args:
                    lines.append(f"- `{arg['name']}`: `{arg['type']}`")
            lines.append("")
            lines.append("## input fields")
            for name, info in payload["inputTypes"].items():
                if not (name.endswith("Input") or name.endswith("Option")):
                    continue
                lines.append("")
                lines.append(f"### {name}")
                for field in info.get("fields") or []:
                    lines.append(f"- `{field['name']}`: `{field['type']}`")
                if info.get("enumValues"):
                    lines.append(f"- enum: `{', '.join(info['enumValues'])}`")
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
