#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "08-metafield-owner-ui-impact-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")
RUN_STAMP = datetime.now().strftime("%H%M%S")
RUN_NAMESPACE = f"faqmf{RUN_STAMP}"

TARGETS = [
    {
        "label": "組織",
        "slug": "organization",
        "ownerType": "ORGANIZATION",
        "listRoute": "/admin/settings",
        "detailRoute": "/admin/settings",
        "routeNote": "組織の専用詳細画面は見つからないため、設定トップを代表画面にした。",
    },
    {
        "label": "ロケーション",
        "slug": "location",
        "ownerType": "LOCATION",
        "listRoute": "/admin/settings/locations",
        "detailPattern": r"^/admin/settings/locations/[0-9a-f-]+[-0-9a-f]*_Location$",
        "fallbackDetailRoute": "/admin/settings/locations/1f0fd500-ee41-50b5-afb9-217ab8af9db3_Location",
    },
    {
        "label": "会社",
        "slug": "company",
        "ownerType": "COMPANY",
        "listRoute": "/admin/companies",
        "detailPattern": r"^/admin/companies/[0-9a-f-]+[-0-9a-f]*_Company$",
        "fallbackDetailRoute": "/admin/companies/16fb446c-e284-593e-a19e-7ec339e48a7a_Company",
    },
    {
        "label": "仕入れ先ベンダー",
        "slug": "inventory_supplier",
        "ownerType": "INVENTORY_SUPPLIER",
        "listRoute": "/admin/settings/suppliers",
        "detailPattern": r"^/admin/settings/suppliers/[0-9a-f-]+[-0-9a-f]*_InventorySupplier$",
        "fallbackDetailRoute": "/admin/settings/suppliers/62acd1f7-d25a-5b93-a4e8-fbfcb23b59ff_InventorySupplier",
    },
    {
        "label": "商品",
        "slug": "product",
        "ownerType": "PRODUCT",
        "listRoute": "/admin/products",
        "detailPattern": r"^/admin/products/[0-9a-f-]+[-0-9a-f]*_Product$",
        "fallbackDetailRoute": "/admin/products/91f45bd1-03b7-5aad-a888-42530a13011d_Product",
    },
    {
        "label": "バリエーション",
        "slug": "product_variant",
        "ownerType": "PRODUCT_VARIANT",
        "listRoute": "/admin/products",
        "detailPattern": r"^/admin/products/[0-9a-f-]+[-0-9a-f]*_Product/variants/[0-9a-f-]+[-0-9a-f]*_ProductVariant$",
        "fallbackDetailRoute": "/admin/products/91f45bd1-03b7-5aad-a888-42530a13011d_Product/variants/9d94e684-4882-5ebc-bbbb-513915a8bfc7_ProductVariant",
        "discoverViaProduct": True,
    },
    {
        "label": "顧客",
        "slug": "purchasing_customer",
        "ownerType": "PURCHASING_CUSTOMER",
        "listRoute": "/admin/purchasing_customers",
        "detailPattern": r"^/admin/purchasing_customers/[0-9a-f-]+[-0-9a-f]*_PurchasingCustomer$",
        "fallbackDetailRoute": "/admin/purchasing_customers/e284db39-9ba1-587e-a3b1-aa0700076c2e_PurchasingCustomer",
        "routeNote": "一覧は空の場合があるため、過去検証で作成済みの検証顧客詳細をfallbackにした。",
    },
    {
        "label": "注文",
        "slug": "order",
        "ownerType": "ORDER",
        "listRoute": "/admin/orders",
        "detailPattern": r"^/admin/orders/[0-9a-f-]+[-0-9a-f]*_Order$",
        "fallbackDetailRoute": "/admin/orders/4c7e4e96-6d5b-5c73-bf86-9693cf7c4734_Order",
    },
    {
        "label": "下書き注文",
        "slug": "draft_order",
        "ownerType": "DRAFT_ORDER",
        "listRoute": "/admin/draft_orders",
        "detailRoute": "/admin/draft_orders",
        "routeNote": "現行UIでは下書き注文の作成ボタンがdisabled相当で、詳細レコードを開けないため一覧を代表画面にした。",
    },
    {
        "label": "ディスカウント",
        "slug": "order_price_adjustment_rule",
        "ownerType": "ORDER_PRICE_ADJUSTMENT_RULE",
        "listRoute": "/admin/order_price_adjustment_rules",
        "detailPattern": r"^/admin/order_price_adjustment_rules/[0-9a-f-]+[-0-9a-f]*_OrderPriceAdjustmentRule$",
        "fallbackDetailRoute": "/admin/order_price_adjustment_rules/2c0e23bd-77df-5440-a291-2c8dfd057f45_OrderPriceAdjustmentRule",
    },
    {
        "label": "在庫移動伝票",
        "slug": "inventory_movement_order",
        "ownerType": "INVENTORY_MOVEMENT_ORDER",
        "listRoute": "/admin/inventory_movement_orders",
        "detailPattern": r"^/admin/inventory_movement_orders/[0-9a-f-]+[-0-9a-f]*_InventoryMovementOrder$",
        "fallbackDetailRoute": "/admin/inventory_movement_orders/d7573bf2-aba0-574f-ac27-774061ea17d9_InventoryMovementOrder",
    },
    {
        "label": "在庫調整伝票",
        "slug": "inventory_adjustment_order",
        "ownerType": "INVENTORY_ADJUSTMENT_ORDER",
        "listRoute": "/admin/inventory_adjustment_orders",
        "detailPattern": r"^/admin/inventory_adjustment_orders/[0-9a-f-]+[-0-9a-f]*_InventoryAdjustmentOrder$",
        "fallbackDetailRoute": "/admin/inventory_adjustment_orders/656af2b4-e907-52d7-a665-6a7dcef5b31a_InventoryAdjustmentOrder",
    },
    {
        "label": "在庫取置伝票",
        "slug": "inventory_reservation_order",
        "ownerType": "INVENTORY_RESERVATION_ORDER",
        "listRoute": "/admin/inventory_reservation_orders",
        "detailPattern": r"^/admin/inventory_reservation_orders/[0-9a-f-]+[-0-9a-f]*_InventoryReservationOrder$",
        "fallbackDetailRoute": "/admin/inventory_reservation_orders/4e4aa346-7103-552f-99f3-8d089495279e_InventoryReservationOrder",
    },
    {
        "label": "発注伝票",
        "slug": "inventory_purchase_order",
        "ownerType": "INVENTORY_PURCHASE_ORDER",
        "listRoute": "/admin/inventory_purchase_orders",
        "detailPattern": r"^/admin/inventory_purchase_orders/[0-9a-f-]+[-0-9a-f]*_InventoryPurchaseOrder$",
        "fallbackDetailRoute": "/admin/inventory_purchase_orders/536f9387-9a2b-59da-aab8-131ca9b82a3b_InventoryPurchaseOrder",
    },
    {
        "label": "入荷指示",
        "slug": "inventory_inbound_order",
        "ownerType": "INVENTORY_INBOUND_ORDER",
        "listRoute": "/admin/inventory_inbound_orders",
        "detailPattern": r"^/admin/inventory_inbound_orders/[0-9a-f-]+[-0-9a-f]*_InventoryInboundOrder$",
        "fallbackDetailRoute": "/admin/inventory_inbound_orders/3506bdef-629c-5ebd-98fd-ca256a1959c5_InventoryInboundOrder",
    },
    {
        "label": "出荷指示",
        "slug": "inventory_outbound_order",
        "ownerType": "INVENTORY_OUTBOUND_ORDER",
        "listRoute": "/admin/inventory_outbound_orders",
        "detailPattern": r"^/admin/inventory_outbound_orders/[0-9a-f-]+[-0-9a-f]*_InventoryOutboundOrder$",
        "fallbackDetailRoute": "/admin/inventory_outbound_orders/380d6c15-ba98-5391-8397-f8c7ec577c45_InventoryOutboundOrder",
    },
]

CREATE_MUTATION = """
mutation CreateMetafieldDefinition($input: MetafieldDefinitionCreateInput!) {
  metafieldDefinitionCreate(input: $input) {
    metafieldDefinition {
      id
      name
      namespace
      key
      ownerType
      valueType
      readOnly
    }
  }
}
"""

DELETE_MUTATION = """
mutation DeleteMetafieldDefinitions($input: MetafieldDefinitionsDeleteInput!) {
  metafieldDefinitionsDelete(input: $input) {
    __typename
  }
}
"""

MUTATION_SCHEMA_QUERY = """
query MutationSchema {
  __schema {
    mutationType {
      fields(includeDeprecated: true) {
        name
        type { kind name ofType { kind name ofType { kind name } } }
        args { name type { kind name ofType { kind name ofType { kind name } } } }
      }
    }
  }
}
"""

TOKEN_RE = re.compile(r"([A-Za-z0-9_\\-]{40,}|eyJ[A-Za-z0-9_\\-\\.]{20,})")


def redact(text):
    return TOKEN_RE.sub("[REDACTED_LONG_VALUE]", text or "")


def compact(text, limit=2000):
    return redact(" ".join((text or "").split())[:limit])


def wait_soft(page, ms=900):
    try:
        page.wait_for_load_state("networkidle", timeout=9000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(ms)


def gql(page, query, variables=None):
    return page.evaluate(
        """async ({endpoint, query, variables}) => {
            const res = await fetch(endpoint, {
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
        {"endpoint": f"{BASE}/api/graphql", "query": query, "variables": variables or {}},
    )


def visible_snapshot(page, label, field_name=None, namespace=None, key=None):
    data = page.evaluate(
        """() => {
            const txt = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const visible = (el) => {
                const box = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return box.width > 0 && box.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
            };
            return {
                url: location.href,
                title: document.title,
                h1: Array.from(document.querySelectorAll('h1')).filter(visible).map(txt).filter(Boolean),
                h2: Array.from(document.querySelectorAll('h2')).filter(visible).map(txt).filter(Boolean),
                h3: Array.from(document.querySelectorAll('h3')).filter(visible).map(txt).filter(Boolean),
                buttons: Array.from(document.querySelectorAll('button')).filter(visible).map(txt).filter(Boolean).slice(0, 80),
                inputs: Array.from(document.querySelectorAll('input, textarea, select')).filter(visible).map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type'),
                    placeholder: el.getAttribute('placeholder'),
                    ariaLabel: el.getAttribute('aria-label'),
                    name: el.getAttribute('name'),
                    disabled: Boolean(el.disabled),
                    valueText: el.tagName.toLowerCase() === 'select'
                        ? Array.from(el.options || []).map(o => (o.textContent || '').trim()).filter(Boolean).slice(0, 12).join(' / ')
                        : ''
                })).slice(0, 100),
                links: Array.from(document.querySelectorAll('a[href]')).filter(visible).map((a) => ({
                    text: txt(a),
                    href: a.getAttribute('href')
                })).filter(x => x.text || x.href).slice(0, 100),
                bodyText: txt(document.body),
            };
        }"""
    )
    body = data.get("bodyText") or ""
    watch_terms = [x for x in [field_name, namespace, key, "メタフィールド"] if x]
    lines = []
    for term in watch_terms:
        start = 0
        while term in body[start:]:
            index = body.find(term, start)
            window = compact(body[max(0, index - 220):index + len(term) + 360], 650)
            if window and window not in lines:
                lines.append(window)
            start = index + len(term)
    return {
        "label": label,
        "url": redact(data.get("url")),
        "title": redact(data.get("title")),
        "h1": [redact(x) for x in data.get("h1", [])],
        "h2": [redact(x) for x in data.get("h2", [])[:20]],
        "h3": [redact(x) for x in data.get("h3", [])[:20]],
        "buttons": [redact(x) for x in data.get("buttons", [])],
        "inputs": [{k: redact(str(v)) if v is not None else v for k, v in row.items()} for row in data.get("inputs", [])],
        "links": [{k: redact(str(v)) if v is not None else v for k, v in row.items()} for row in data.get("links", [])],
        "bodySample": compact(body, 2600),
        "hasUnexpectedError": "予期せぬエラーが発生しました" in body,
        "hasNotFound": "このページは存在しないようです" in body or "見つかりませんでした" in body,
        "hasFieldName": bool(field_name and field_name in body),
        "hasNamespaceKey": bool(namespace and key and f"{namespace}.{key}" in body),
        "hasMetafieldText": "メタフィールド" in body,
        "matchingLines": lines[:20],
    }


def path_from_href(href):
    if not href:
        return None
    parsed = urlparse(urljoin(BASE, href))
    return parsed.path


def discover_detail_route(page, target, known_routes):
    if target.get("detailRoute"):
        return target["detailRoute"], "fixed"

    pattern = target.get("detailPattern")
    if target.get("discoverViaProduct"):
        product_route = known_routes.get("product")
        if product_route:
            page.goto(BASE + product_route, wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            found = find_first_matching_link(page, pattern)
            if found:
                return found, f"discovered via {product_route}"

    page.goto(BASE + target["listRoute"], wait_until="domcontentloaded", timeout=60000)
    wait_soft(page)
    found = find_first_matching_link(page, pattern)
    if found:
        return found, f"discovered from {target['listRoute']}"
    return target.get("fallbackDetailRoute") or target["listRoute"], "fallback"


def find_first_matching_link(page, pattern):
    if not pattern:
        return None
    regex = re.compile(pattern)
    links = page.evaluate(
        """() => Array.from(document.querySelectorAll('a[href]')).map((a) => a.getAttribute('href'))"""
    )
    for href in links:
        path = path_from_href(href)
        if path and regex.match(path):
            return path
    return None


def definition_input_for(target):
    short = target["slug"][:28].replace("_", "")
    return {
        "name": f"FAQMF {target['slug']} {RUN_STAMP}"[:50],
        "description": "FAQ live UI impact verification. Remove after capture.",
        "ownerType": target["ownerType"],
        "namespace": RUN_NAMESPACE,
        "key": f"k{short}{RUN_STAMP}"[:50],
        "valueType": "BOOLEAN",
        "readOnly": False,
    }


def write_outputs(payload):
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# メタフィールド定義 16対象 UI反映確認 2026-06-28",
        "",
        f"- 実行時刻: `{payload['generatedAt']}`",
        f"- namespace: `{payload['namespace']}`",
        f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
        "",
        "## 結論",
        "",
        "- 定義作成の成否、定義一覧での表示、対象画面で入力欄/表示名が出るかを分けて確認した。",
        "- `対象画面に出た` は、定義追加後に代表画面本文へ検証用定義名が新規出現したことを意味する。",
        "- 下書き注文と組織は、現行UIで専用詳細レコードを開けないため、一覧/設定トップでの代表確認に留めた。",
        "",
        "## 結果表",
        "",
        "| 対象 | ownerType | 定義作成 | 定義一覧 | 代表画面 | 対象画面に出た | メタフィールド文言 | 備考 |",
        "|---|---|---:|---:|---|---:|---:|---|",
    ]
    for row in payload["targets"]:
        after = row.get("afterSnapshot") or {}
        created = "OK" if row.get("createdDefinition") else "NG"
        listed = "OK" if row.get("definitionListVisible") else "NG"
        appeared = "OK" if row.get("fieldAppearedOnObjectPage") else "NG"
        mf = "OK" if after.get("hasMetafieldText") else "NG"
        note = row.get("routeNote") or row.get("discoverSource") or ""
        if row.get("createError"):
            note = compact(row["createError"], 120)
        lines.append(
            f"| {row['label']} | `{row['ownerType']}` | {created} | {listed} | `{row.get('detailRoute') or ''}` | {appeared} | {mf} | {note} |"
        )

    lines.extend(["", "## 対象画面で出た行", ""])
    for row in payload["targets"]:
        after = row.get("afterSnapshot") or {}
        lines.append(f"### {row['label']}")
        lines.append("")
        lines.append(f"- 代表画面: `{row.get('detailRoute') or ''}`")
        lines.append(f"- 定義名: `{row.get('definitionInput', {}).get('name', '')}`")
        if row.get("fieldAppearedOnObjectPage"):
            for line in after.get("matchingLines", [])[:8]:
                lines.append(f"- {line}")
        else:
            lines.append("- 代表画面本文には検証用定義名は出なかった。")
        if row.get("routeNote"):
            lines.append(f"- 注記: {row['routeNote']}")
        lines.append("")

    cleanup = payload.get("cleanup", {})
    lines.extend([
        "## 後片付け",
        "",
        f"- 削除対象定義数: `{cleanup.get('requestedDeleteCount', 0)}`",
        f"- 削除mutation HTTP成功: `{'OK' if cleanup.get('deleteHttpOk') else 'NG'}`",
    ])
    if cleanup.get("deleteErrors"):
        lines.append(f"- 削除エラー: `{compact(json.dumps(cleanup['deleteErrors'], ensure_ascii=False), 500)}`")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "namespace": RUN_NAMESPACE,
        "targets": [],
        "schema": {},
        "cleanup": {},
    }
    created_ids = []

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(BASE + "/admin/settings/metafield_definitions", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            schema_result = gql(page, MUTATION_SCHEMA_QUERY)
            fields = ((((schema_result.get("json") or {}).get("data") or {}).get("__schema") or {}).get("mutationType") or {}).get("fields") or []
            payload["schema"] = {
                "httpStatus": schema_result.get("status"),
                "errors": (schema_result.get("json") or {}).get("errors"),
                "metafieldMutations": [
                    {"name": f.get("name"), "args": f.get("args"), "type": f.get("type")}
                    for f in fields
                    if "metafieldDefinition" in f.get("name", "")
                ],
            }

            known_routes = {}
            for target in TARGETS:
                detail_route, source = discover_detail_route(page, target, known_routes)
                if target["slug"] == "product":
                    known_routes["product"] = detail_route

                definition_input = definition_input_for(target)
                row = {
                    "label": target["label"],
                    "slug": target["slug"],
                    "ownerType": target["ownerType"],
                    "definitionInput": definition_input,
                    "detailRoute": detail_route,
                    "discoverSource": source,
                    "routeNote": target.get("routeNote"),
                }

                try:
                    page.goto(BASE + detail_route, wait_until="domcontentloaded", timeout=60000)
                    wait_soft(page)
                    row["beforeSnapshot"] = visible_snapshot(
                        page,
                        f"{target['label']}-before",
                        definition_input["name"],
                        definition_input["namespace"],
                        definition_input["key"],
                    )
                except Exception as exc:
                    row["beforeError"] = repr(exc)

                create_result = gql(page, CREATE_MUTATION, {"input": definition_input})
                row["createResult"] = create_result
                created = (((create_result.get("json") or {}).get("data") or {}).get("metafieldDefinitionCreate") or {}).get("metafieldDefinition")
                if created:
                    row["createdDefinition"] = created
                    created_ids.append(created["id"])
                else:
                    row["createError"] = compact(create_result.get("textSample", ""), 1000)

                definition_list_route = f"/admin/settings/metafield_definitions?ownerType={target['slug']}"
                try:
                    page.goto(BASE + definition_list_route, wait_until="domcontentloaded", timeout=60000)
                    wait_soft(page)
                    list_snapshot = visible_snapshot(
                        page,
                        f"{target['label']}-definition-list",
                        definition_input["name"],
                        definition_input["namespace"],
                        definition_input["key"],
                    )
                    row["definitionListRoute"] = definition_list_route
                    row["definitionListSnapshot"] = list_snapshot
                    row["definitionListVisible"] = list_snapshot["hasFieldName"] or list_snapshot["hasNamespaceKey"]
                except Exception as exc:
                    row["definitionListError"] = repr(exc)

                try:
                    page.goto(BASE + detail_route, wait_until="domcontentloaded", timeout=60000)
                    wait_soft(page, 1400)
                    row["afterSnapshot"] = visible_snapshot(
                        page,
                        f"{target['label']}-after",
                        definition_input["name"],
                        definition_input["namespace"],
                        definition_input["key"],
                    )
                    before_has = (row.get("beforeSnapshot") or {}).get("hasFieldName")
                    after_has = row["afterSnapshot"].get("hasFieldName")
                    row["fieldAppearedOnObjectPage"] = bool(after_has and not before_has)
                except Exception as exc:
                    row["afterError"] = repr(exc)

                payload["targets"].append(row)
                write_outputs(payload)

            if created_ids:
                delete_result = gql(page, DELETE_MUTATION, {"input": {"metafieldDefinitionIDs": created_ids}})
                payload["cleanup"] = {
                    "requestedDeleteCount": len(created_ids),
                    "requestedDeleteIDs": created_ids,
                    "deleteHttpOk": bool(delete_result.get("ok")),
                    "deleteStatus": delete_result.get("status"),
                    "deleteErrors": (delete_result.get("json") or {}).get("errors"),
                    "deleteResultSample": compact(delete_result.get("textSample", ""), 1200),
                }
        finally:
            write_outputs(payload)
            if not page.is_closed():
                page.close()

    summary = [
        {
            "label": row["label"],
            "created": bool(row.get("createdDefinition")),
            "definitionListVisible": bool(row.get("definitionListVisible")),
            "fieldAppearedOnObjectPage": bool(row.get("fieldAppearedOnObjectPage")),
            "detailRoute": row.get("detailRoute"),
        }
        for row in payload["targets"]
    ]
    print(json.dumps({"namespace": RUN_NAMESPACE, "summary": summary, "cleanup": payload.get("cleanup")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
