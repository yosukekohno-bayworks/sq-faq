#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_analysis" / "live-notion-verification-2026-06-27" / "search-filter-audit"
BASE = "https://www.sqstackstaging.com"

PAGES = [
    ("products", "/admin/products"),
    ("inventory-items", "/admin/inventory_items"),
    ("orders", "/admin/orders"),
    ("draft-orders", "/admin/draft_orders"),
    ("order-returns", "/admin/order_returns"),
    ("purchasing-customers", "/admin/purchasing_customers"),
    ("companies", "/admin/companies"),
    ("purchase-orders", "/admin/inventory_purchase_orders"),
    ("inbound-orders", "/admin/inventory_inbound_orders"),
    ("outbound-orders", "/admin/inventory_outbound_orders"),
    ("allocation-requests", "/admin/inventory_allocation_requests"),
    ("allocation-confirmations", "/admin/inventory_allocation_request_confirmations"),
    ("discounts", "/admin/order_price_adjustment_rules"),
    ("point-rules", "/admin/point_calculation_rules"),
    ("rank-rules", "/admin/customer_rank_calculation_rules"),
    ("price-rules", "/admin/product_price_rules"),
    ("back-order-rules", "/admin/inventory_back_order_rules"),
    ("sale-limit-rules", "/admin/inventory_sale_limit_rules"),
    ("threshold-rules", "/admin/inventory_threshold_rules"),
    ("local-pickup-products", "/admin/local_pickup_product_variants"),
    ("catalogs", "/admin/catalogs"),
    ("shopify", "/admin/shopify_integrations"),
    ("omnibus-core", "/admin/omnibus_core_integrations"),
    ("smaregi", "/admin/smaregi_integrations"),
    ("retail-portal", "/admin/retail_portal_integrations"),
    ("settings-users", "/admin/settings/users"),
    ("permission-groups", "/admin/settings/permission_groups"),
    ("settings-locations", "/admin/settings/locations"),
    ("location-groups", "/admin/settings/location_groups"),
    ("brands", "/admin/settings/brands"),
    ("suppliers", "/admin/settings/suppliers"),
    ("payment-methods", "/admin/settings/payment_methods"),
    ("retail-staff", "/admin/settings/retail_staff_members"),
    ("notification-emails", "/admin/settings/organization_notification_emails"),
    ("apps", "/admin/settings/apps"),
    ("translation", "/admin/settings/translation"),
    ("metafields", "/admin/settings/metafield_definitions"),
    ("measurement-rules", "/admin/settings/product_measurement_rules"),
    ("csv-export", "/admin/csv_export"),
    ("csv-import", "/admin/csv_import"),
    ("sales", "/admin/sale_change_line_items"),
    ("b2b", "/admin/b2b"),
]

COLLECT_JS = r"""
(() => {
  const clean = (s) => (s || '').replace(/\s+/g, ' ').trim();
  const inputs = [...document.querySelectorAll('input, textarea')].map((i) => ({
    tag: i.tagName.toLowerCase(),
    type: i.getAttribute('type'),
    placeholder: i.getAttribute('placeholder'),
    value: i.value,
    ariaLabel: i.getAttribute('aria-label'),
    disabled: i.disabled,
  }));
  const buttons = [...document.querySelectorAll('button, a')].map((b) => ({
    text: clean(b.innerText),
    ariaLabel: b.getAttribute('aria-label'),
    role: b.getAttribute('role'),
    href: b.getAttribute('href'),
    disabled: !!b.disabled || b.getAttribute('aria-disabled') === 'true',
    expanded: b.getAttribute('aria-expanded'),
  })).filter((b) => b.text || b.ariaLabel || b.href);
  const rows = [...document.querySelectorAll('tr')].slice(0, 12).map((tr) =>
    [...tr.querySelectorAll('th,td')].map((td) => clean(td.innerText)).filter(Boolean)
  ).filter((r) => r.length);
  const menuItems = [...document.querySelectorAll('[role=menuitem], [role=option], [data-polaris-action-list-item], li')]
    .map((e) => clean(e.innerText)).filter(Boolean).slice(-40);
  return {
    url: location.href,
    title: document.title,
    h1: clean((document.querySelector('h1') || {}).innerText),
    inputs,
    buttons,
    rows,
    menuItems,
    bodyText: document.body.innerText.slice(0, 5000),
  };
})()
"""

CLICK_SEARCH_PANEL_JS = r"""
(() => {
  const candidates = [...document.querySelectorAll('button, a')];
  const el = candidates.find((e) => (e.innerText || '').includes('検索と絞り込みの結果'));
  if (!el) return {clicked: false};
  el.click();
  return {clicked: true, text: el.innerText};
})()
"""

CLICK_FILTER_JS = r"""
(() => {
  const candidates = [...document.querySelectorAll('button, a')];
  const el = candidates.find((e) =>
    ((e.innerText || e.getAttribute('aria-label') || '').includes('絞り込みを追加')) &&
    !e.disabled &&
    e.getAttribute('aria-disabled') !== 'true'
  );
  if (!el) return {clicked: false};
  el.click();
  return {clicked: true, text: el.innerText || el.getAttribute('aria-label')};
})()
"""


def run(args: list[str], timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=timeout)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary = []

    for slug, path in PAGES:
        url = BASE + path
        page_summary = {"slug": slug, "url": url, "ok": False}
        print(f"[audit] {slug} {path}", flush=True)

        opened = run(["browser-use", "open", url], timeout=90)
        write(OUT / f"{slug}-open.txt", opened.stdout + opened.stderr)
        time.sleep(2)

        state = run(["browser-use", "state"], timeout=60)
        write(OUT / f"{slug}-initial.md", state.stdout + state.stderr)

        initial = run(["browser-use", "eval", COLLECT_JS], timeout=60)
        write(OUT / f"{slug}-initial.json", initial.stdout + initial.stderr)

        click_search = run(["browser-use", "eval", CLICK_SEARCH_PANEL_JS], timeout=60)
        write(OUT / f"{slug}-click-search-panel.json", click_search.stdout + click_search.stderr)
        time.sleep(1)

        expanded = run(["browser-use", "eval", COLLECT_JS], timeout=60)
        write(OUT / f"{slug}-expanded.json", expanded.stdout + expanded.stderr)

        click_filter = run(["browser-use", "eval", CLICK_FILTER_JS], timeout=60)
        write(OUT / f"{slug}-click-filter.json", click_filter.stdout + click_filter.stderr)
        time.sleep(1)

        filter_menu = run(["browser-use", "eval", COLLECT_JS], timeout=60)
        write(OUT / f"{slug}-filter-menu.json", filter_menu.stdout + filter_menu.stderr)

        page_summary["ok"] = opened.returncode == 0 and initial.returncode == 0
        summary.append(page_summary)

    write(OUT / "_summary.json", json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
