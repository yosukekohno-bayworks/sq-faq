#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "17-purchasing-customer-graphql-create-verify-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
TENANT_ID = "f6262fd1-2406-5716-9cb5-cad1137b403c_Tenant"
STAMP = datetime.now().strftime("%Y%m%d%H%M%S")


CREATE_MUTATION = """
mutation CreatePurchasingCustomer($input: PurchasingCustomerCreateInput!) {
  purchasingCustomerCreate(input: $input) {
    purchasingCustomer {
      id
      externalID
      firstName
      lastName
      fullName
      email
      phone
      barcode
      tags
      orderCount
      pointsApproved
      pointsPending
      tenant { id name }
    }
  }
}
"""

CUSTOMER_BY_EXTERNAL_ID = """
query PurchasingCustomerByExternalID($externalID: String!) {
  purchasingCustomerByExternalID(externalID: $externalID) {
    id
    externalID
    firstName
    lastName
    fullName
    email
    phone
    barcode
    tags
    orderCount
    pointsApproved
    pointsPending
    tenant { id name }
  }
}
"""


def compact(text, limit=2200):
    return " ".join((text or "").split())[:limit]


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


def wait_soft(page, timeout=12000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(800)


def snapshot(page, label):
    body = page.inner_text("body")
    return {
        "label": label,
        "url": page.url,
        "h1": [x.strip() for x in page.locator("h1").all_inner_texts()],
        "h2": [x.strip() for x in page.locator("h2").all_inner_texts()],
        "bodySample": compact(body),
        "tableHeaders": [
            compact(x, 300)
            for x in page.locator("th").all_inner_texts()
            if compact(x, 300)
        ],
        "rows": [
            compact(x, 500)
            for x in page.locator("tr").all_inner_texts()[:20]
            if compact(x, 500)
        ],
        "buttons": [
            compact(x, 300)
            for x in page.locator("button").all_inner_texts()[:80]
            if compact(x, 300)
        ],
        "inputs": page.evaluate(
            """() => Array.from(document.querySelectorAll('input, textarea, select')).map((el) => ({
                tag: el.tagName.toLowerCase(),
                type: el.getAttribute('type'),
                placeholder: el.getAttribute('placeholder'),
                value: el.tagName.toLowerCase() === 'select' ? Array.from(el.options).map(o => o.textContent.trim()).join(' / ') : (el.value || ''),
                disabled: Boolean(el.disabled),
                ariaLabel: el.getAttribute('aria-label'),
            }))"""
        ),
        "links": page.evaluate(
            """() => Array.from(document.querySelectorAll('a[href]')).slice(0, 100).map((a) => ({
                text: (a.innerText || a.textContent || '').trim().replace(/\\s+/g, ' '),
                href: a.getAttribute('href'),
            }))"""
        ),
    }


def click_if_visible(page, text):
    loc = page.get_by_text(text, exact=True)
    if loc.count() == 0:
        return False
    loc.first.click(timeout=10000)
    wait_soft(page, 6000)
    return True


def main():
    previous = None
    if OUT_JSON.exists():
        try:
            previous = json.loads(OUT_JSON.read_text()).get("testCustomer")
        except Exception:
            previous = None
    email = (previous or {}).get("email") or f"sq-faq-customer-{STAMP}@example.invalid"
    external_id = (previous or {}).get("externalID") or f"FAQ_E2E_CUSTOMER_{STAMP}"
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "testCustomer": {
            "externalID": external_id,
            "email": email,
            "tenantID": TENANT_ID,
            "tag": "FAQ_E2E_20260628",
        },
        "steps": [],
        "facts": {},
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            page.goto(f"{BASE}/admin/purchasing_customers", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "before-create-list"))
            existing_result = gql(page, CUSTOMER_BY_EXTERNAL_ID, {"externalID": external_id})
            payload["existingLookup"] = existing_result
            customer = (((existing_result.get("json") or {}).get("data") or {}).get("purchasingCustomerByExternalID"))
            mutation_input = {
                "tenantID": TENANT_ID,
                "externalID": external_id,
                "source": "API",
                "barcode": f"FAQBAR{STAMP[-10:]}",
                "firstName": "FAQ",
                "lastName": f"検証顧客{STAMP[-6:]}",
                "email": email,
                "phone": "0000000000",
                "tags": ["FAQ_E2E_20260628"],
            }
            if not customer:
                result = gql(page, CREATE_MUTATION, {"input": mutation_input})
                payload["createResult"] = result
                customer = (((result.get("json") or {}).get("data") or {}).get("purchasingCustomerCreate") or {}).get("purchasingCustomer")
            else:
                payload["createResult"] = {"skipped": True, "reason": "existing purchasing customer found by externalID"}
            if not customer:
                raise RuntimeError(f"customer create failed: {payload.get('createResult')}")
            payload["facts"]["customerID"] = customer.get("id")
            payload["facts"]["customerEmail"] = customer.get("email")
            payload["facts"]["customerFullName"] = customer.get("fullName")
            payload["facts"]["createdByInternalGraphql"] = True
            page.goto(f"{BASE}/admin/purchasing_customers", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "after-create-list"))
            payload["facts"]["listShowsCustomerEmail"] = email in page.inner_text("body")
            payload["facts"]["listShowsCustomerName"] = "検証顧客" in page.inner_text("body")
            search_opened = click_if_visible(page, "検索と絞り込みの結果")
            payload["facts"]["searchPanelOpened"] = search_opened
            if search_opened:
                payload["steps"].append(snapshot(page, "search-panel-opened"))
                input_box = page.get_by_placeholder("メールアドレスで検索する")
                if input_box.count() > 0:
                    input_box.first.fill(email)
                    page.keyboard.press("Enter")
                    wait_soft(page)
                    payload["steps"].append(snapshot(page, "email-search-result"))
                    payload["facts"]["emailSearchShowsOnlyTestCustomer"] = email in page.inner_text("body")
                filter_clicked = click_if_visible(page, "絞り込みを追加")
                payload["facts"]["filterMenuOpened"] = filter_clicked
                if filter_clicked:
                    payload["steps"].append(snapshot(page, "filter-menu-opened"))
            detail_url = f"{BASE}/admin/purchasing_customers/{customer['id']}"
            page.goto(detail_url, wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "customer-detail-direct"))
            detail_body = page.inner_text("body")
            payload["facts"]["detailUrl"] = page.url.replace(BASE, "")
            payload["facts"]["detailShowsEmail"] = email in detail_body
            payload["facts"]["detailShowsPointLabels"] = "ポイント" in detail_body
            payload["facts"]["detailShowsOrderLabels"] = "注文" in detail_body
            payload["facts"]["detailShowsRankLabels"] = "ランク" in detail_body
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# 購入顧客を内部GraphQLで作成して一覧・詳細を確認 2026-06-28",
                "",
                f"- 作成方法: 管理画面セッションの内部GraphQL `purchasingCustomerCreate`",
                f"- 顧客ID: `{payload['facts'].get('customerID')}`",
                f"- メール: `{email}`",
                f"- タグ: `FAQ_E2E_20260628`",
                f"- 一覧にメール表示: `{payload['facts'].get('listShowsCustomerEmail')}`",
                f"- 検索パネル表示: `{payload['facts'].get('searchPanelOpened')}`",
                f"- メール検索結果に表示: `{payload['facts'].get('emailSearchShowsOnlyTestCustomer')}`",
                f"- フィルタメニュー表示: `{payload['facts'].get('filterMenuOpened')}`",
                f"- 詳細URL: `{payload['facts'].get('detailUrl')}`",
                f"- 詳細にメール表示: `{payload['facts'].get('detailShowsEmail')}`",
                f"- 詳細にポイント/注文/ランク系表示: `point={payload['facts'].get('detailShowsPointLabels')}`, `order={payload['facts'].get('detailShowsOrderLabels')}`, `rank={payload['facts'].get('detailShowsRankLabels')}`",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                "",
                "## 備考",
                "",
                "- 管理画面UIには購入顧客の新規作成ボタンはありません。今回の作成は内部GraphQLでの検証用シードです。",
                "- `purchasingCustomerCreate` の削除mutationは今回の読み取り専用スキーマ確認では見つかっていません。検証顧客はタグとメールで識別します。",
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
