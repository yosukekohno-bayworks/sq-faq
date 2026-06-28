#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "17-internal-graphql-customer-mutation-return-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

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
      ofType { kind name }
    }
  }
}
"""

MUTATION_RETURN_QUERY = TYPE_REF + """
query MutationReturn {
  __schema {
    mutationType {
      fields {
        name
        type { ...TypeRef }
      }
    }
  }
}
"""

TYPE_QUERY = TYPE_REF + """
query TypeFields($name: String!) {
  __type(name: $name) {
    kind
    name
    fields {
      name
      type { ...TypeRef }
      args { name type { ...TypeRef } }
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
        "target": "purchasingCustomerCreate",
        "returnType": None,
        "returnFields": [],
        "nestedTypes": {},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            page.goto(f"{BASE}/admin/purchasing_customers", wait_until="domcontentloaded", timeout=60000)
            try:
                page.wait_for_load_state("networkidle", timeout=12000)
            except PlaywrightTimeoutError:
                pass
            result = gql(page, MUTATION_RETURN_QUERY)
            fields = (((result.get("json") or {}).get("data") or {}).get("__schema") or {}).get("mutationType", {}).get("fields") or []
            target = next((f for f in fields if f.get("name") == "purchasingCustomerCreate"), None)
            if target:
                payload["returnType"] = type_name(target.get("type") or {})
            if payload["returnType"]:
                t = gql(page, TYPE_QUERY, {"name": payload["returnType"]})
                type_data = ((t.get("json") or {}).get("data") or {}).get("__type") or {}
                nested = []
                for field in type_data.get("fields") or []:
                    base = type_name(field.get("type") or {})
                    payload["returnFields"].append({
                        "name": field.get("name"),
                        "type": type_label(field.get("type") or {}),
                        "baseType": base,
                    })
                    if base:
                        nested.append(base)
                for name in nested:
                    nt = gql(page, TYPE_QUERY, {"name": name})
                    nt_data = ((nt.get("json") or {}).get("data") or {}).get("__type") or {}
                    payload["nestedTypes"][name] = [
                        {"name": f.get("name"), "type": type_label(f.get("type") or {})}
                        for f in nt_data.get("fields") or []
                    ]
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# purchasingCustomerCreate 戻り値確認 2026-06-28",
                "",
                f"- return type: `{payload['returnType']}`",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                "",
                "## fields",
                "",
            ]
            for field in payload["returnFields"]:
                lines.append(f"- `{field['name']}`: `{field['type']}`")
            for name, fields in payload["nestedTypes"].items():
                lines.extend(["", f"## {name}", ""])
                for field in fields[:80]:
                    lines.append(f"- `{field['name']}`: `{field['type']}`")
            OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
        except Exception as exc:
            payload["errors"].append(repr(exc))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            raise
        finally:
            page.close()
    print(json.dumps({"returnType": payload["returnType"], "returnFields": payload["returnFields"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
