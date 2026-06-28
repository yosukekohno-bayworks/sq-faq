import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.async_api import async_playwright


BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
OUT = Path(__file__).with_suffix(".json")
MD = Path(__file__).with_suffix(".md")

TARGETS = [
    {
        "name": "管理メンバー",
        "path": "/admin/settings/users",
        "row_href_prefix": "/admin/settings/users/user_",
        "queries": ["河野", "陽介", "kohno", "特権管理者", "河野 kohno", "__NO_MATCH_FAQ_20260628__"],
    },
    {
        "name": "商品",
        "path": "/admin/products",
        "row_href_prefix": "/admin/products/",
        "queries": ["486125", "UNIQLO", "TEST_E2E", "486125 UNIQLO", "__NO_MATCH_FAQ_20260628__"],
    },
    {
        "name": "在庫",
        "path": "/admin/inventory_items",
        "row_href_prefix": "/admin/inventory_items/",
        "queries": ["486125", "486125-31-XL", "ユニクロ", "486125 ユニクロ", "__NO_MATCH_FAQ_20260628__"],
    },
    {
        "name": "ロケーション",
        "path": "/admin/settings/locations",
        "row_href_prefix": "/admin/settings/locations/",
        "queries": ["R0001", "W0001", "銀座", "R0001 銀座", "__NO_MATCH_FAQ_20260628__"],
    },
    {
        "name": "カタログ",
        "path": "/admin/catalogs",
        "row_href_prefix": "/admin/catalogs/",
        "queries": ["TEST_FAQ", "UNIQLO", "__NO_MATCH_FAQ_20260628__"],
    },
    {
        "name": "移動伝票",
        "path": "/admin/inventory_movement_orders",
        "row_href_prefix": "/admin/inventory_movement_orders/",
        "queries": ["IM-1027", "#IM-1027", "入荷完了", "__NO_MATCH_FAQ_20260628__"],
    },
    {
        "name": "出荷管理",
        "path": "/admin/inventory_outbound_orders",
        "row_href_prefix": "/admin/inventory_outbound_orders/",
        "queries": ["IO-1027", "#IO-1027", "出荷完了", "__NO_MATCH_FAQ_20260628__"],
    },
    {
        "name": "入荷管理",
        "path": "/admin/inventory_inbound_orders",
        "row_href_prefix": "/admin/inventory_inbound_orders/",
        "queries": ["II-1029", "#II-1029", "入荷完了", "__NO_MATCH_FAQ_20260628__"],
    },
]


async def visible_controls(page):
    return await page.locator("input, textarea, button, a, [role=button], [role=menuitem], [role=option]").evaluate_all(
        """els => els
          .filter(el => {
            const s = window.getComputedStyle(el);
            const r = el.getBoundingClientRect();
            return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0;
          })
          .map(el => ({
            tag: el.tagName.toLowerCase(),
            role: el.getAttribute('role'),
            type: el.getAttribute('type'),
            text: (el.innerText || el.value || '').trim().slice(0, 120),
            placeholder: el.getAttribute('placeholder'),
            ariaLabel: el.getAttribute('aria-label'),
            href: el.getAttribute('href')
          }))"""
    )


async def wait_ready(page):
    try:
        await page.wait_for_load_state("networkidle", timeout=20000)
    except Exception:
        pass
    try:
        await page.wait_for_function(
            """() => document.body && (
              document.body.innerText.includes('このページの準備が整いました') ||
              document.body.innerText.length > 1000
            )""",
            timeout=15000,
        )
    except Exception:
        pass
    await page.wait_for_timeout(1000)


async def table_rows(page, href_prefix=None):
    if href_prefix:
        anchors = await page.locator(f'a[href^="{href_prefix}"]').evaluate_all(
            """els => els
              .filter(el => {
                const s = window.getComputedStyle(el);
                const r = el.getBoundingClientRect();
                return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0;
              })
              .map(el => (el.innerText || el.textContent || '').trim())"""
        )
        rows = []
        for text in anchors:
            compact = " ".join(text.split())
            if compact and compact not in rows:
                rows.append(compact[:260])
        if rows:
            return rows
    rows = []
    for row in await page.locator("table tbody tr, [role=row]").all():
        text = " ".join((await row.inner_text()).split())
        if text:
            rows.append(text[:260])
    return rows[:30]


async def h1_text(page):
    vals = []
    for h in await page.locator("h1").all():
        t = " ".join((await h.inner_text()).split())
        if t:
            vals.append(t)
    return vals


async def first_search_input(page):
    inputs = await page.locator("input:visible").all()
    for inp in inputs:
        meta = await inp.evaluate(
            """el => ({
              placeholder: el.getAttribute('placeholder') || '',
              ariaLabel: el.getAttribute('aria-label') || '',
              type: el.getAttribute('type') || '',
              value: el.value || ''
            })"""
        )
        joined = " ".join([meta["placeholder"], meta["ariaLabel"]])
        if "検索" in joined or "キーワード" in joined or "コード" in joined or "番号" in joined:
            return inp, meta
    return None, None


async def ensure_search_panel(page):
    inp, meta = await first_search_input(page)
    if inp:
        return "initial"
    await page.keyboard.press("f")
    await page.wait_for_timeout(1000)
    inp, meta = await first_search_input(page)
    if inp:
        return "keyboard_f"
    candidates = page.get_by_text("検索と絞り込みの結果", exact=False)
    if await candidates.count() > 0:
        try:
            await candidates.first.click()
            await page.wait_for_timeout(1000)
            inp, meta = await first_search_input(page)
            if inp:
                return "button"
        except Exception:
            pass
    return "not_found"


async def collect_filter_options(page):
    controls_before = await visible_controls(page)
    candidates = page.get_by_text("絞り込みを追加", exact=False)
    if await candidates.count() == 0:
        return []
    button = candidates.first
    try:
        await button.click()
        await page.wait_for_timeout(500)
        controls_after = await visible_controls(page)
        before_keys = {
            (c.get("tag"), c.get("role"), c.get("text"), c.get("placeholder"), c.get("ariaLabel"))
            for c in controls_before
        }
        options = []
        for c in controls_after:
            key = (c.get("tag"), c.get("role"), c.get("text"), c.get("placeholder"), c.get("ariaLabel"))
            text = c.get("text") or c.get("placeholder") or c.get("ariaLabel") or ""
            if key not in before_keys and text and text not in {"絞り込みを追加"}:
                options.append(c)
        await page.keyboard.press("Escape")
        return options
    except Exception as exc:
        return [{"error": repr(exc)}]


async def run_query(page, query, href_prefix=None):
    await ensure_search_panel(page)
    inp, meta = await first_search_input(page)
    if not inp:
        return {"query": query, "skipped": "search input not found"}
    await inp.click()
    await page.keyboard.press("Meta+A")
    await page.keyboard.press("Backspace")
    if query:
        await inp.fill(query)
    await page.wait_for_timeout(1000)
    await page.keyboard.press("Enter")
    try:
        await page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        pass
    await page.wait_for_timeout(2500)
    rows = await table_rows(page, href_prefix)
    body = " ".join((await page.locator("body").inner_text()).split())
    empty_state = "アイテムが見つかりませんでした" in body
    if empty_state:
        rows = []
    return {
        "query": query,
        "input": meta,
        "url_after": page.url,
        "row_count": len(rows),
        "rows_sample": rows[:5],
        "empty_state": empty_state,
        "body_sample": body[:500],
    }


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = await context.new_page()
        results = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "base": BASE,
            "targets": [],
        }
        for target in TARGETS:
            url = BASE + target["path"]
            await page.goto(url, wait_until="domcontentloaded")
            await wait_ready(page)
            base_rows = await table_rows(page, target["row_href_prefix"])
            search_reveal_mode = await ensure_search_panel(page)
            controls = await visible_controls(page)
            filters = await collect_filter_options(page)
            searches = []
            for query in target["queries"]:
                await page.goto(url, wait_until="domcontentloaded")
                await wait_ready(page)
                searches.append(await run_query(page, query, target["row_href_prefix"]))
            results["targets"].append(
                {
                    "name": target["name"],
                    "path": target["path"],
                    "h1": await h1_text(page),
                    "base_row_count": len(base_rows),
                    "base_rows_sample": base_rows[:5],
                    "search_inputs": [
                        c for c in controls if c.get("tag") == "input" and ((c.get("placeholder") or "") or (c.get("ariaLabel") or ""))
                    ],
                    "search_reveal_mode": search_reveal_mode,
                    "filter_options_after_click": filters,
                    "searches": searches,
                }
            )
        await page.close()
        OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        write_md(results)


def write_md(results):
    lines = [
        "# 検索・絞り込み 横断確認",
        "",
        f"- 実行日時: {results['generated_at']}",
        "- 方法: 主要一覧を開き、検索入力・`絞り込みを追加` の候補・代表クエリの結果件数を実機確認。",
        "",
    ]
    for target in results["targets"]:
        lines.extend(
            [
                f"## {target['name']} `{target['path']}`",
                "",
                f"- h1: {target['h1']}",
                f"- 初期行数: {target['base_row_count']}",
                f"- 検索パネル表示: {target.get('search_reveal_mode')}",
                f"- 検索入力: {', '.join(filter(None, [(i.get('placeholder') or i.get('ariaLabel') or '') for i in target['search_inputs']])) or 'なし'}",
                "- 絞り込み候補: "
                + (
                    ", ".join(
                        filter(
                            None,
                            [
                                (o.get("text") or o.get("placeholder") or o.get("ariaLabel") or o.get("error") or "")
                                for o in target["filter_options_after_click"]
                            ],
                        )
                    )
                    or "なし"
                ),
                "",
                "| クエリ | 件数 | 空状態 | URL変化 |",
                "|:--|--:|:--|:--|",
            ]
        )
        for s in target["searches"]:
            if s.get("skipped"):
                lines.append(f"| `{s['query']}` | - | skipped | {s['skipped']} |")
            else:
                url_changed = s["url_after"].replace(BASE, "")
                lines.append(f"| `{s['query']}` | {s['row_count']} | {s['empty_state']} | `{url_changed}` |")
        lines.append("")
    lines.extend(["## 証跡", "", f"- JSON: `{OUT}`", ""])
    MD.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(main())
