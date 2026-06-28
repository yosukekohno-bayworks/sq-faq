#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "16-internal-graphql-order-scope-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"


INTROSPECTION = """
query CodexOperationNames {
  __schema {
    queryType {
      fields {
        name
        args { name }
      }
    }
    mutationType {
      fields {
        name
        args { name }
      }
    }
  }
}
"""


KEYWORDS = [
    "order",
    "draft",
    "return",
    "sale",
    "customer",
    "purchasing",
    "point",
    "shipment",
    "fulfillment",
]


def compact(text, limit=1200):
    return " ".join((text or "").split())[:limit]


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "purpose": "管理画面セッションの内部GraphQLで、注文/返品/売上/顧客系データ作成の余地を読み取り専用で確認する",
        "queries": [],
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
            payload["ordersPage"] = {
                "url": page.url,
                "bodySample": compact(page.inner_text("body"), 1800),
            }
            result = page.evaluate(
                """async (query) => {
                    const res = await fetch('/api/graphql', {
                        method: 'POST',
                        credentials: 'include',
                        headers: { 'content-type': 'application/json' },
                        body: JSON.stringify({ query }),
                    });
                    const text = await res.text();
                    let json = null;
                    try { json = JSON.parse(text); } catch {}
                    return { status: res.status, ok: res.ok, json, textSample: text.slice(0, 2000) };
                }""",
                INTROSPECTION,
            )
            payload["queries"].append({
                "name": "introspection_operation_names",
                "status": result.get("status"),
                "ok": result.get("ok"),
                "errors": (result.get("json") or {}).get("errors"),
            })
            schema = ((result.get("json") or {}).get("data") or {}).get("__schema") or {}
            query_fields = (schema.get("queryType") or {}).get("fields") or []
            mutation_fields = (schema.get("mutationType") or {}).get("fields") or []
            def interesting(fields):
                rows = []
                for field in fields:
                    name = field.get("name") or ""
                    lower = name.lower()
                    if any(k in lower for k in KEYWORDS):
                        rows.append({
                            "name": name,
                            "args": [arg.get("name") for arg in field.get("args") or []],
                        })
                return rows
            payload["facts"] = {
                "introspectionHttpOk": bool(result.get("ok")),
                "queryFieldCount": len(query_fields),
                "mutationFieldCount": len(mutation_fields),
                "interestingQueries": interesting(query_fields),
                "interestingMutations": interesting(mutation_fields),
                "hasOrderCreateLikeMutation": any(
                    "order" in (f.get("name") or "").lower()
                    and any(k in (f.get("name") or "").lower() for k in ["create", "add", "upsert", "insert"])
                    for f in mutation_fields
                ),
                "hasDraftOrderCreateLikeMutation": any(
                    "draft" in (f.get("name") or "").lower()
                    and "order" in (f.get("name") or "").lower()
                    and any(k in (f.get("name") or "").lower() for k in ["create", "add", "upsert", "insert"])
                    for f in mutation_fields
                ),
                "hasReturnCreateLikeMutation": any(
                    "return" in (f.get("name") or "").lower()
                    and any(k in (f.get("name") or "").lower() for k in ["create", "add", "upsert", "insert"])
                    for f in mutation_fields
                ),
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# 内部GraphQL 注文/返品/売上系操作名確認 2026-06-28",
                "",
                "- 目的: 管理画面セッションで、注文/返品/売上/顧客系データを作れる余地があるかを読み取り専用で確認",
                f"- introspection HTTP OK: `{payload['facts']['introspectionHttpOk']}`",
                f"- query fields: `{payload['facts']['queryFieldCount']}`",
                f"- mutation fields: `{payload['facts']['mutationFieldCount']}`",
                f"- order create-like mutation: `{payload['facts']['hasOrderCreateLikeMutation']}`",
                f"- draft order create-like mutation: `{payload['facts']['hasDraftOrderCreateLikeMutation']}`",
                f"- return create-like mutation: `{payload['facts']['hasReturnCreateLikeMutation']}`",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                "",
                "## 関連query",
                "",
            ]
            for row in payload["facts"]["interestingQueries"][:80]:
                lines.append(f"- `{row['name']}` args={row['args']}")
            lines.extend(["", "## 関連mutation", ""])
            for row in payload["facts"]["interestingMutations"][:120]:
                lines.append(f"- `{row['name']}` args={row['args']}")
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
