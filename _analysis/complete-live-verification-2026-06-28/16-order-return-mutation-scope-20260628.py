#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "16-order-return-mutation-scope-20260628.json"
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
      ofType { kind name }
    }
  }
}
"""

MUTATION_QUERY = TYPE_REF + """
query {
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
query TypeInfo($name: String!) {
  __type(name: $name) {
    kind
    name
    inputFields {
      name
      type { ...TypeRef }
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


def main():
    payload = {"generatedAt": datetime.now(timezone.utc).isoformat(), "mutations": [], "inputTypes": {}, "errors": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        try:
            page.goto(f"{BASE}/admin/orders", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            result = gql(page, MUTATION_QUERY)
            fields = ((((result.get("json") or {}).get("data") or {}).get("__schema") or {}).get("mutationType") or {}).get("fields") or []
            for field in fields:
                name = field.get("name") or ""
                if "orderReturn" in name or "orderRefund" in name:
                    args = []
                    for arg in field.get("args") or []:
                        args.append({"name": arg.get("name"), "type": type_label(arg.get("type")), "baseType": type_name(arg.get("type"))})
                    payload["mutations"].append({"name": name, "args": args})
            to_visit = []
            for mutation in payload["mutations"]:
                for arg in mutation["args"]:
                    base = arg.get("baseType")
                    if base and base.endswith("Input") and base not in to_visit:
                        to_visit.append(base)
            while to_visit:
                base = to_visit.pop(0)
                if not base or not base.endswith("Input") or base in payload["inputTypes"]:
                    continue
                t_result = gql(page, TYPE_QUERY, {"name": base})
                t = ((t_result.get("json") or {}).get("data") or {}).get("__type") or {}
                fields = []
                for f in (t.get("inputFields") or []):
                    field = {"name": f.get("name"), "type": type_label(f.get("type")), "baseType": type_name(f.get("type"))}
                    fields.append(field)
                    nested = field.get("baseType")
                    if nested and nested.endswith("Input") and nested not in payload["inputTypes"] and nested not in to_visit:
                        to_visit.append(nested)
                payload["inputTypes"][base] = fields
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = ["# 注文返品/返金mutation一覧 2026-06-28", "", f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`", ""]
            for mutation in payload["mutations"]:
                lines.append(f"## {mutation['name']}")
                for arg in mutation["args"]:
                    lines.append(f"- `{arg['name']}`: `{arg['type']}`")
            lines.append("")
            lines.append("## input types")
            for name, fields in payload["inputTypes"].items():
                lines.append(f"### {name}")
                for field in fields:
                    lines.append(f"- `{field['name']}`: `{field['type']}`")
            OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
        except Exception as exc:
            payload["errors"].append(repr(exc))
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            raise
        finally:
            page.close()
    print(json.dumps(payload["mutations"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
