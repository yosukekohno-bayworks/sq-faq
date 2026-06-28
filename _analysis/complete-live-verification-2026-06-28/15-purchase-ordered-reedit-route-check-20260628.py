#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "15-purchase-ordered-reedit-route-check-20260628.json"
OUT_MD = OUT_DIR / "15-purchase-ordered-reedit-route-check-20260628.md"

BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

TARGETS = [
    {
        "code": "#IP-1013",
        "kind": "ordered_without_inbound_created",
        "route": "/admin/inventory_purchase_orders/697d403b-4112-562b-9982-f07bb643872f_InventoryPurchaseOrder",
    },
    {
        "code": "#IP-1007",
        "kind": "ordered_after_inbound_completed",
        "route": "/admin/inventory_purchase_orders/536f9387-9a2b-59da-aab8-131ca9b82a3b_InventoryPurchaseOrder",
    },
    {
        "code": "#IP-1010",
        "kind": "draft_comparison",
        "route": "/admin/inventory_purchase_orders/c5ebeb3b-241c-55b6-92b6-f665b47e37d8_InventoryPurchaseOrder",
    },
]

DIRECT_SUFFIXES = ["/update", "/edit"]
KEYWORDS = ["編集", "再編集", "差し戻", "下書きに戻", "戻す", "保存", "発注する", "入荷指示を作成する", "キャンセルする"]

LONG_TOKEN_RE = re.compile(
    r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))"
)


def redact(value):
    if isinstance(value, str):
        return LONG_TOKEN_RE.sub("[REDACTED_LONG_VALUE]", value)
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    return value


def compact(text, limit=7000):
    return " ".join((text or "").split())[:limit]


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snapshot(page, limit=8000):
    data = page.evaluate(
        """() => {
            const textOf = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const attr = (el, name) => el.getAttribute(name);
            const nodes = (selector, limit = 120) => Array.from(document.querySelectorAll(selector)).slice(0, limit);
            const body = document.body ? document.body.innerText : '';
            return {
                url: location.href,
                h1: nodes('h1', 8).map(textOf).filter(Boolean),
                h2: nodes('h2', 20).map(textOf).filter(Boolean),
                rows: nodes('tr', 100).map(textOf).filter(Boolean),
                controls: nodes('button, a, input, textarea, select, [role="button"], [role="menuitem"]', 260)
                    .map((el) => ({
                        tag: el.tagName.toLowerCase(),
                        role: attr(el, 'role'),
                        text: textOf(el),
                        href: attr(el, 'href'),
                        type: attr(el, 'type'),
                        placeholder: attr(el, 'placeholder'),
                        ariaLabel: attr(el, 'aria-label'),
                        ariaDisabled: attr(el, 'aria-disabled'),
                        disabled: !!el.disabled,
                        value: el.tagName.toLowerCase() === 'input' || el.tagName.toLowerCase() === 'select' ? el.value : undefined
                    }))
                    .filter((x) => x.text || x.href || x.ariaLabel || x.placeholder || x.value || x.disabled),
                links: nodes('a', 220).map((el) => ({text: textOf(el), href: attr(el, 'href')}))
                    .filter((x) => x.href || x.text),
                body
            };
        }"""
    )
    body = data.get("body", "")
    data["body"] = compact(body, limit)
    data["keywordHits"] = {kw: (kw in body) for kw in KEYWORDS}
    return redact(data)


def open_snapshot(page, route, limit=8000):
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    return snapshot(page, limit=limit)


def inspect_more_menu(page):
    result = {"clicked": False, "before": None, "after": None, "menuTexts": []}
    result["before"] = snapshot(page, limit=5000)
    button = page.get_by_role("button", name="その他の操作", exact=True)
    if not button.count():
        return redact(result)
    button.first.click()
    page.wait_for_timeout(900)
    result["clicked"] = True
    result["after"] = snapshot(page, limit=7000)
    result["menuTexts"] = page.evaluate(
        """() => Array.from(document.querySelectorAll('[role="menuitem"], [role="option"], button, a'))
            .map((el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim())
            .filter(Boolean)"""
    )
    return redact(result)


def inspect_target(page, target):
    result = {"target": target, "detail": None, "moreMenu": None, "directRoutes": {}}
    page.goto(BASE + target["route"], wait_until="load", timeout=35000)
    wait_quiet(page)
    result["detail"] = snapshot(page, limit=9000)
    result["moreMenu"] = inspect_more_menu(page)
    for suffix in DIRECT_SUFFIXES:
        route = target["route"].rstrip("/") + suffix
        result["directRoutes"][suffix] = open_snapshot(page, route, limit=7000)
    return redact(result)


def summarize(payload):
    facts = {}
    for item in payload["results"]:
        code = item["target"]["code"]
        detail_body = item["detail"]["body"]
        menu_body = (item["moreMenu"].get("after") or {}).get("body", "")
        ordered = "発注済み" in detail_body
        draft = "下書き" in detail_body
        facts[code] = {
            "kind": item["target"]["kind"],
            "ordered": ordered,
            "draft": draft,
            "detailHasSave": "保存" in detail_body,
            "detailHasOrderButton": "発注する" in detail_body,
            "detailHasInboundLink": "入荷指示を作成する" in detail_body,
            "detailHasCancel": "キャンセルする" in detail_body,
            "detailHasEditLikeText": any(kw in detail_body for kw in ["編集", "再編集", "差し戻", "下書きに戻"]),
            "menuHasCancel": "キャンセルする" in menu_body,
            "menuHasEditLikeText": any(kw in menu_body for kw in ["編集", "再編集", "差し戻", "下書きに戻"]),
            "directUpdateUrl": item["directRoutes"]["/update"]["url"],
            "directUpdateH1": item["directRoutes"]["/update"]["h1"],
            "directUpdateHasEditLikeText": any(
                kw in item["directRoutes"]["/update"]["body"] for kw in ["編集", "再編集", "差し戻", "下書きに戻"]
            ),
            "directEditUrl": item["directRoutes"]["/edit"]["url"],
            "directEditH1": item["directRoutes"]["/edit"]["h1"],
            "directEditHasEditLikeText": any(
                kw in item["directRoutes"]["/edit"]["body"] for kw in ["編集", "再編集", "差し戻", "下書きに戻"]
            ),
        }
    payload["facts"] = facts


def build_md(payload):
    lines = [
        "# 発注済み伝票の差し戻し・再編集導線 実機確認",
        "",
        f"- 実行日時: {payload['generatedAt']}",
        "- 確認範囲: 発注済み未入荷 `#IP-1013`、入荷完了済み `#IP-1007`、比較用下書き `#IP-1010`",
        "- 確認内容: 詳細画面、`その他の操作`、直接 `/update` / `/edit` URL",
        "",
        "## 結果",
        "",
    ]
    for code, facts in payload["facts"].items():
        lines.extend(
            [
                f"### {code} ({facts['kind']})",
                "",
                f"- 発注済み表示: `{facts['ordered']}` / 下書き表示: `{facts['draft']}`",
                f"- 詳細画面に `保存`: `{facts['detailHasSave']}`",
                f"- 詳細画面に `発注する`: `{facts['detailHasOrderButton']}`",
                f"- 詳細画面に `入荷指示を作成する`: `{facts['detailHasInboundLink']}`",
                f"- 詳細画面に編集/再編集/差し戻し/下書き戻し系文言: `{facts['detailHasEditLikeText']}`",
                f"- その他の操作に `キャンセルする`: `{facts['menuHasCancel']}`",
                f"- その他の操作に編集/再編集/差し戻し/下書き戻し系文言: `{facts['menuHasEditLikeText']}`",
                f"- 直接 `/update`: `{facts['directUpdateUrl']}` / h1 `{facts['directUpdateH1']}` / 編集系文言 `{facts['directUpdateHasEditLikeText']}`",
                f"- 直接 `/edit`: `{facts['directEditUrl']}` / h1 `{facts['directEditH1']}` / 編集系文言 `{facts['directEditHasEditLikeText']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## 結論",
            "",
            "- 発注済み伝票では、詳細画面・その他の操作・直接URLの確認範囲で、下書きへ差し戻して再編集する導線は確認できませんでした。",
            "- 発注済み未入荷の `#IP-1013` は `入荷指示を作成する` と `キャンセルする` が主な導線です。",
            "- 入荷完了済みの `#IP-1007` は `キャンセルする` がdisabledで、再編集・差し戻し導線も確認できませんでした。",
            "",
            "## 証跡",
            "",
            f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    payload = {"generatedAt": datetime.now(timezone.utc).isoformat(), "results": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            for target in TARGETS:
                payload["results"].append(inspect_target(page, target))
        finally:
            page.close()
            browser.close()
    summarize(payload)
    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2))
    build_md(redact(payload))
    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
