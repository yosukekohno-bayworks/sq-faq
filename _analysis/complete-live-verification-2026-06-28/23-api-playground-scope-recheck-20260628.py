#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "23-api-playground-scope-recheck-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
APP_ROUTE = "/admin/settings/apps/c960abe2-56d7-5b23-b8f2-ec66df6c8060_App"
APP_NAME = "TEST_FAQ_20260624_APP_113636"

SECRET_PATTERNS = [
    re.compile(r"(?i)(bearer\\s+)[A-Za-z0-9_./+=-]{12,}"),
    re.compile(r"(?i)((?:token|secret|authorization|api[_-]?key)\\s*[:=]\\s*)['\\\"]?[A-Za-z0-9_./+=-]{12,}"),
]


def redact(value):
    if value is None:
        return value
    text = str(value)
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(lambda m: (m.group(1) if m.groups() else "") + "[REDACTED]", text)
    return text


def compact(text, limit=1200):
    return redact(" ".join((text or "").split())[:limit])


def wait_soft(page, ms=1000):
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(ms)


def visible(page):
    return page.evaluate(
        """() => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const visible = (el) => {
                const box = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return box.width > 0 && box.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
            };
            return {
                url: location.href,
                title: document.title,
                h1: Array.from(document.querySelectorAll('h1')).filter(visible).map(text).filter(Boolean),
                links: Array.from(document.querySelectorAll('a[href]')).filter(visible).map((a) => ({
                    text: text(a),
                    href: a.href,
                    target: a.target || null,
                    rel: a.rel || null
                })).filter((x) => x.text || x.href),
                buttons: Array.from(document.querySelectorAll('button')).filter(visible).map((button) => ({
                    text: text(button),
                    ariaLabel: button.getAttribute('aria-label')
                })).filter((x) => x.text || x.ariaLabel),
                inputs: Array.from(document.querySelectorAll('input, textarea')).filter(visible).map((input) => ({
                    tag: input.tagName.toLowerCase(),
                    type: input.getAttribute('type'),
                    placeholder: input.getAttribute('placeholder'),
                    ariaLabel: input.getAttribute('aria-label'),
                    valueLength: input.value ? input.value.length : 0
                })),
                bodySample: text(document.body).slice(0, 3000),
                localStorageKeys: Object.keys(localStorage || {}),
                sessionStorageKeys: Object.keys(sessionStorage || {})
            };
        }"""
    )


def sanitize_snapshot(snapshot):
    if not snapshot:
        return snapshot
    clean = dict(snapshot)
    clean["url"] = redact(clean.get("url"))
    clean["title"] = redact(clean.get("title"))
    clean["bodySample"] = compact(clean.get("bodySample", ""))
    for key in ["h1", "localStorageKeys", "sessionStorageKeys"]:
        clean[key] = [redact(x) for x in clean.get(key, [])]
    for key in ["links", "buttons", "inputs"]:
        clean[key] = [
            {k: redact(v) for k, v in row.items()}
            for row in clean.get(key, [])
        ]
    return clean


def write_outputs(payload):
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    r = payload.get("result", {})
    lines = [
        "# API Playground 導線・認証注入確認 2026-06-28",
        "",
        f"- 対象アプリ: `{APP_NAME}`",
        f"- 対象画面: `{APP_ROUTE}`",
        f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
        "",
        "## 結果",
        "",
        f"- Playgroundリンクを検出: `{'確認' if r.get('playgroundLinkFound') else '未確認'}`",
        f"- Playgroundリンク先: `{r.get('playgroundHref') or ''}`",
        f"- Playgroundページを開けた: `{'確認' if r.get('playgroundPageOpened') else '未確認'}`",
        f"- stagingアプリ詳細から開いてもリンク先は本番ドメイン: `{'確認' if r.get('hrefIsProductionDomain') else '未確認'}`",
        f"- URLクエリにトークン/アプリIDらしき値なし: `{'確認' if r.get('noCredentialLikeQuery') else '未確認'}`",
        f"- localStorage/sessionStorageはキー名のみ保存、値は保存なし: `確認`",
        "",
        "## アプリ詳細の操作要素",
        "",
    ]
    for button in payload.get("appDetail", {}).get("buttons", []):
        label = button.get("text") or button.get("ariaLabel")
        if label:
            lines.append(f"- `{label}`")
    lines.append("")
    lines.append("## Playgroundページ")
    lines.append("")
    pg = payload.get("playground", {})
    lines.append(f"- URL: `{pg.get('url', '')}`")
    lines.append(f"- title: `{pg.get('title', '')}`")
    if pg.get("bodySample"):
        lines.append(f"- 本文抜粋: {pg['bodySample'][:500]}")
    if pg.get("localStorageKeys"):
        lines.append(f"- localStorage keys: `{', '.join(pg['localStorageKeys'])}`")
    if pg.get("sessionStorageKeys"):
        lines.append(f"- sessionStorage keys: `{', '.join(pg['sessionStorageKeys'])}`")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "appName": APP_NAME,
        "appRoute": APP_ROUTE,
        "result": {},
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(f"{BASE}{APP_ROUTE}", wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            raw_app_detail = visible(page)
            app_detail = sanitize_snapshot(raw_app_detail)
            payload["appDetail"] = app_detail
            playground_links = [
                link for link in raw_app_detail.get("links", [])
                if "playground" in (link.get("href") or "").lower() or "Playground" in (link.get("text") or "")
            ]
            playground_href = playground_links[0]["href"] if playground_links else None

            if playground_href:
                pg = context.new_page()
                try:
                    pg.goto(playground_href, wait_until="domcontentloaded", timeout=60000)
                    wait_soft(pg, 2500)
                    payload["playground"] = sanitize_snapshot(visible(pg))
                finally:
                    if not pg.is_closed():
                        pg.close()

            no_credential_query = True
            if playground_href and "?" in playground_href:
                query = playground_href.split("?", 1)[1].lower()
                no_credential_query = not any(k in query for k in ["token", "secret", "authorization", "app", "client"])

            payload["result"] = {
                "playgroundLinkFound": bool(playground_href),
                "playgroundHref": redact(playground_href),
                "playgroundPageOpened": bool(payload.get("playground", {}).get("url")),
                "hrefIsProductionDomain": bool(playground_href and "https://sq.stackservice.com/" in playground_href),
                "noCredentialLikeQuery": no_credential_query,
            }
        finally:
            write_outputs(payload)
            if not page.is_closed():
                page.close()
    print(json.dumps(payload["result"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
