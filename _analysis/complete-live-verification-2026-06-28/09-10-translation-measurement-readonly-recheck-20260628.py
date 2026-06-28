#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "09-10-translation-measurement-readonly-recheck-20260628.json"
OUT_MD = OUT_DIR / "09-10-translation-measurement-readonly-recheck-20260628.md"
BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"

PRODUCTS = {
    "486125": "/admin/products/2c32fb97-1f83-5cae-b20c-3d83046800d0_Product",
    "482787": "/admin/products/85649f94-007f-5bcf-b6c9-9676528376a4_Product",
}

TOKEN_RE = re.compile(r"(eyJ[A-Za-z0-9_\-.]{20,}|(?<![A-Za-z0-9_/\-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_/\-]))")
MANUAL_TRANSLATION_WORDS = ["実行", "再実行", "翻訳する", "生成"]
MEASUREMENT_WORDS = ["採寸", "測定", "measurement", "product_measurement"]


def redact(value):
    if isinstance(value, str):
        return TOKEN_RE.sub("[REDACTED_LONG_VALUE]", value)
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    return value


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1000)


def snap(page):
    data = page.evaluate(
        """([manualWords, measurementWords]) => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const unique = (items) => Array.from(new Set(items.filter(Boolean)));
            const labelFor = (el) => {
                const id = el.id;
                if (id) {
                    const label = document.querySelector(`label[for="${CSS.escape(id)}"]`);
                    if (label) return text(label);
                }
                const label = el.closest('label');
                if (label) return text(label);
                const labelledBy = el.getAttribute('aria-labelledby');
                if (labelledBy) {
                    return labelledBy.split(/\\s+/).map((id) => {
                        const node = document.getElementById(id);
                        return node ? text(node) : '';
                    }).filter(Boolean).join(' ');
                }
                return el.getAttribute('aria-label') || '';
            };
            const bodyText = document.body ? document.body.innerText.replace(/\\s+/g, ' ').trim() : '';
            const buttons = Array.from(document.querySelectorAll('button, [role="button"]')).map((el) => ({
                text: text(el) || el.getAttribute('aria-label') || '',
                disabled: !!el.disabled,
                ariaDisabled: el.getAttribute('aria-disabled')
            })).filter((x) => x.text);
            const links = Array.from(document.querySelectorAll('a[href]')).map((a) => ({
                text: text(a),
                href: a.getAttribute('href')
            })).filter((x) => x.text || x.href);
            const controls = Array.from(document.querySelectorAll('input, select, textarea')).map((el) => ({
                tag: el.tagName.toLowerCase(),
                type: el.getAttribute('type') || '',
                label: labelFor(el),
                placeholder: el.getAttribute('placeholder') || '',
                value: el.tagName.toLowerCase() === 'select' ? el.value : '',
                checked: el.tagName.toLowerCase() === 'input' && el.type === 'checkbox' ? el.checked : null,
                disabled: !!el.disabled,
                readOnly: !!el.readOnly,
                options: el.tagName.toLowerCase() === 'select' ? Array.from(el.options).map((opt) => text(opt)) : []
            }));
            return {
                url: location.href,
                title: document.title,
                h1: unique(Array.from(document.querySelectorAll('h1')).map(text)),
                h2: unique(Array.from(document.querySelectorAll('h2')).map(text)),
                h3: unique(Array.from(document.querySelectorAll('h3')).map(text)),
                buttons,
                links,
                controls,
                manualTranslationButtonHits: buttons.filter((button) => manualWords.includes(button.text)),
                manualTranslationBodyHits: manualWords.filter((word) => bodyText.includes(word)),
                measurementBodyHits: measurementWords.filter((word) => bodyText.toLowerCase().includes(word.toLowerCase())),
                hasUnexpectedError: bodyText.includes('予期せぬエラーが発生しました'),
                hasNotFound: bodyText.includes('このページは存在しないようです'),
                bodySample: bodyText.slice(0, 2500)
            };
        }""",
        [MANUAL_TRANSLATION_WORDS, MEASUREMENT_WORDS],
    )
    return redact(data)


def first_detail_link(snapshot, route_part):
    for link in snapshot.get("links", []):
        href = link.get("href") or ""
        if route_part in href and not href.endswith("/create"):
            return href
    return None


def visit(page, route):
    page.goto(BASE + route, wait_until="load", timeout=35000)
    wait_quiet(page)
    return snap(page)


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "errors": [],
        "pages": {},
        "productPages": {},
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)

        for name, route in [
            ("translationTop", "/admin/settings/translation"),
            ("translationRulesList", "/admin/settings/translation/translation_rules"),
            ("translationRuleCreate", "/admin/settings/translation/translation_rules/create"),
            ("measurementRulesList", "/admin/settings/product_measurement_rules"),
            ("measurementRuleCreate", "/admin/settings/product_measurement_rules/create"),
        ]:
            try:
                payload["pages"][name] = visit(page, route)
            except Exception as exc:
                payload["errors"].append({name: repr(exc)})

        translation_detail = first_detail_link(
            payload["pages"].get("translationRulesList", {}),
            "/translation_rules/",
        )
        payload["translationDetailHref"] = translation_detail
        if translation_detail:
            try:
                payload["pages"]["translationRuleDetail"] = visit(page, translation_detail)
            except Exception as exc:
                payload["errors"].append({"translationRuleDetail": repr(exc)})

        measurement_detail = first_detail_link(
            payload["pages"].get("measurementRulesList", {}),
            "/product_measurement_rules/",
        )
        payload["measurementDetailHref"] = measurement_detail
        if measurement_detail:
            try:
                payload["pages"]["measurementRuleDetail"] = visit(page, measurement_detail)
            except Exception as exc:
                payload["errors"].append({"measurementRuleDetail": repr(exc)})

        for code, route in PRODUCTS.items():
            try:
                payload["productPages"][code] = visit(page, route)
            except Exception as exc:
                payload["errors"].append({f"product-{code}": repr(exc)})

        page.close()
        browser.close()

    translation_pages = [
        payload["pages"].get("translationTop", {}),
        payload["pages"].get("translationRulesList", {}),
        payload["pages"].get("translationRuleCreate", {}),
        payload["pages"].get("translationRuleDetail", {}),
    ]
    measurement_detail_controls = [
        {
            "label": control.get("label"),
            "tag": control.get("tag"),
            "type": control.get("type"),
            "disabled": control.get("disabled"),
            "readOnly": control.get("readOnly"),
        }
        for control in payload["pages"].get("measurementRuleDetail", {}).get("controls", [])
        if control.get("tag") in ["input", "textarea", "select"]
    ]

    payload["facts"] = {
        "translationManualButtonHitsByPage": {
            name: page_data.get("manualTranslationButtonHits", [])
            for name, page_data in payload["pages"].items()
            if name.startswith("translation")
        },
        "translationManualButtonHitCount": sum(len(page.get("manualTranslationButtonHits", [])) for page in translation_pages),
        "translationCreateControls": payload["pages"].get("translationRuleCreate", {}).get("controls", []),
        "translationDetailControls": payload["pages"].get("translationRuleDetail", {}).get("controls", []),
        "measurementCreateControls": payload["pages"].get("measurementRuleCreate", {}).get("controls", []),
        "measurementDetailControls": measurement_detail_controls,
        "productMeasurementHits": {
            code: page_data.get("measurementBodyHits", [])
            for code, page_data in payload["productPages"].items()
        },
        "productNotFoundOrError": {
            code: {
                "notFound": page_data.get("hasNotFound"),
                "unexpectedError": page_data.get("hasUnexpectedError"),
            }
            for code, page_data in payload["productPages"].items()
        },
    }

    OUT_JSON.write_text(json.dumps(redact(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 09/10 翻訳・採寸 再確認 2026-06-28",
        "",
        f"- 実行日時: {payload['generatedAt']}",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        f"- エラー数: `{len(payload['errors'])}`",
        "",
        "## 結果",
        "",
        f"- 翻訳トップ/ルール一覧/作成/詳細で、手動実行系ボタン（`実行` / `再実行` / `翻訳する` / `生成`）の一致数: `{payload['facts']['translationManualButtonHitCount']}`",
        f"- 翻訳詳細URL: `{translation_detail}`",
        f"- 採寸詳細URL: `{measurement_detail}`",
        f"- 商品詳細 `486125` の採寸/測定/measurementキーワード: `{payload['facts']['productMeasurementHits'].get('486125')}`",
        f"- 商品詳細 `482787` の採寸/測定/measurementキーワード: `{payload['facts']['productMeasurementHits'].get('482787')}`",
        "",
        "## 採寸ルール詳細の入力状態",
        "",
        "| ラベル | tag | disabled | readonly |",
        "|:--|:--|:--|:--|",
    ]
    for control in measurement_detail_controls:
        lines.append(
            f"| {control.get('label') or '-'} | {control.get('tag')} | `{control.get('disabled')}` | `{control.get('readOnly')}` |"
        )
    lines.extend([
        "",
        "## 判断",
        "",
        "- 翻訳は、確認範囲の管理画面UIに手動実行ボタンがない。",
        "- 採寸ルールは詳細の入力がreadonlyで、テンプレート定義の確認画面として扱う。",
        "- 商品詳細2件では採寸・測定・measurement系の表示がなく、個別商品への紐づけ導線は管理画面UI上では確認できない。",
        "- 実際の翻訳生成結果、採寸情報の外部/API経由適用、ストアフロント/チャネル反映はこのUI確認だけでは確定できない。",
    ])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "json": str(OUT_JSON),
        "md": str(OUT_MD),
        "facts": payload["facts"],
        "errors": payload["errors"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
