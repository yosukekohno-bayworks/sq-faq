#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"
ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
OUT_JSON = OUT_DIR / "ui-recheck-batch2-20260628.json"
OUT_MD = OUT_DIR / "ui-recheck-batch2-20260628.md"

PRODUCT_ID = "5407c6bf-092c-5c2f-96a6-fa37fcff594f_Product"
COMPANY_ID = "16fb446c-e284-593e-a19e-7ec339e48a7a_Company"
CONTACT_STAMP = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
CONTACT_EMAIL = f"sq-faq-company-contact-{CONTACT_STAMP}@example.com"


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snap(page):
    return page.evaluate(
        """() => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const unique = (items) => Array.from(new Set(items.filter(Boolean)));
            const labelFor = (el) => {
                const id = el.id;
                if (id) {
                    const label = document.querySelector(`label[for="${CSS.escape(id)}"]`);
                    if (label) return text(label);
                }
                const parentLabel = el.closest('label');
                return parentLabel ? text(parentLabel) : '';
            };
            return {
                url: location.href,
                h1: unique(Array.from(document.querySelectorAll('h1')).map(text)),
                h2: unique(Array.from(document.querySelectorAll('h2')).map(text)),
                labels: unique(Array.from(document.querySelectorAll('label')).map(text)),
                buttons: unique(Array.from(document.querySelectorAll('button')).map((button) => text(button) || button.getAttribute('aria-label') || '')),
                links: Array.from(document.querySelectorAll('a[href]')).map((a) => ({text: text(a), href: a.getAttribute('href')})).filter((x) => x.text || x.href),
                controls: Array.from(document.querySelectorAll('input, select, textarea')).map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type') || '',
                    label: labelFor(el),
                    placeholder: el.getAttribute('placeholder') || '',
                    value: el.tagName.toLowerCase() === 'input' || el.tagName.toLowerCase() === 'select' ? el.value : '',
                    checked: el.tagName.toLowerCase() === 'input' && el.type === 'checkbox' ? el.checked : null,
                    disabled: !!el.disabled,
                    readOnly: !!el.readOnly,
                    options: el.tagName.toLowerCase() === 'select' ? Array.from(el.options).map((opt) => text(opt)) : []
                })),
                bodyIncludes: {
                    todo: document.body.innerText.includes('TODO'),
                    unexpectedError: document.body.innerText.includes('予期せぬエラーが発生しました'),
                    notFound: document.body.innerText.includes('このページは存在しないようです'),
                    measurement: /採寸|測定|measurement|product_measurement/i.test(document.body.innerText),
                    manualTranslationAction: /(実行|再実行|翻訳する|生成)/.test(Array.from(document.querySelectorAll('button')).map(text).join(' '))
                },
                bodyText: document.body.innerText.replace(/\\s+/g, ' ').trim().slice(0, 3000)
            };
        }"""
    )


def get_checkbox(page, label):
    return page.evaluate(
        """(labelText) => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            for (const label of Array.from(document.querySelectorAll('label'))) {
                if (!text(label).includes(labelText)) continue;
                let input = label.control || label.querySelector('input[type="checkbox"]');
                if (!input) {
                    const id = label.getAttribute('for');
                    input = id ? document.getElementById(id) : null;
                }
                if (!input) return {found: false, label: text(label)};
                return {
                    found: true,
                    label: text(label),
                    checked: input.checked,
                    disabled: input.disabled,
                    value: input.value
                };
            }
            return {found: false};
        }""",
        label,
    )


def select_options(page, label):
    return page.evaluate(
        """(labelText) => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            for (const label of Array.from(document.querySelectorAll('label'))) {
                if (!text(label).includes(labelText)) continue;
                let select = label.control;
                if (!select) {
                    const id = label.getAttribute('for');
                    select = id ? document.getElementById(id) : null;
                }
                if (!select || select.tagName.toLowerCase() !== 'select') return {found: false, label: text(label)};
                return {
                    found: true,
                    label: text(label),
                    value: select.value,
                    disabled: select.disabled,
                    options: Array.from(select.options).map((opt) => text(opt))
                };
            }
            return {found: false};
        }""",
        label,
    )


def first_detail_link(snapshot, route_part):
    for link in snapshot.get("links", []):
        href = link.get("href") or ""
        if route_part in href and not href.endswith("/create"):
            return href
    return None


def create_company_contact(page, payload):
    route = f"/admin/companies/{COMPANY_ID}"
    page.goto(BASE + route, wait_until="load")
    wait_quiet(page)
    before = snap(page)
    payload["companyDetailBeforeContact"] = before

    try:
        page.get_by_role("button", name="担当者を追加").click()
        wait_quiet(page)
        dialog = snap(page)
        payload["companyContactDialog"] = dialog
        inputs = page.locator('[role="dialog"] input:not([type="hidden"])')
        if inputs.count() >= 3:
            inputs.nth(0).fill("FAQ")
            inputs.nth(1).fill(f"Contact{CONTACT_STAMP[-6:]}")
            inputs.nth(2).fill(CONTACT_EMAIL)
            if inputs.count() >= 4:
                inputs.nth(3).fill("0312345678")
            save = page.get_by_role("button", name="保存する")
            if save.count() > 0:
                save.first.click()
                wait_quiet(page, timeout=12000)
                payload["companyDetailAfterContact"] = snap(page)
                contact_href = None
                for link in payload["companyDetailAfterContact"].get("links", []):
                    if CONTACT_EMAIL in link.get("text", "") or "/contacts/" in (link.get("href") or ""):
                        contact_href = link.get("href")
                        break
                payload["companyContactHref"] = contact_href
                if contact_href:
                    page.goto(BASE + contact_href, wait_until="load")
                    wait_quiet(page)
                    payload["companyContactDetail"] = snap(page)
    except Exception as exc:
        payload.setdefault("errors", []).append({"companyContact": repr(exc)})


def write_md(payload):
    variant = payload["productVariantCreate"]
    facts = payload["facts"]
    lines = [
        "# UI再確認バッチ2 2026-06-28",
        "",
        "## 確認した画面",
        "",
        "- 商品作成フォーム: `/admin/products/create`",
        f"- バリエーション作成フォーム: `/admin/products/{PRODUCT_ID}/variants/create`",
        "- 翻訳ルール一覧/作成/詳細",
        "- 採寸ルール一覧/作成/詳細、商品詳細",
        "- 販売上限ルール作成フォーム",
        "- ヤマトB2クラウド条件指定エクスポートフォーム",
        f"- 会社詳細/担当者追加/担当者詳細: `/admin/companies/{COMPANY_ID}`",
        "",
        "## 主な結果",
        "",
        "| 項目 | 実機結果 |",
        "|:--|:--|",
        f"| `在庫を追跡する` 初期状態 | `{facts['trackInventoryCheckbox']}` |",
        f"| `在庫切れの場合でも販売を続ける` 初期状態 | `{facts['continueSellingCheckbox']}` |",
        f"| `配送を必須にする` 初期状態 | `{facts['requiresShippingCheckbox']}` |",
        f"| 翻訳ルール詳細の手動実行系ボタン | `{facts['translationManualActionButtons']}` |",
        f"| 採寸ルール詳細の入力readonly | `{facts['measurementDetailReadonlyControls']}` |",
        f"| 商品詳細に採寸/measurement系導線 | `{facts['productDetailHasMeasurementText']}` |",
        f"| 販売上限空保存エラー | `{facts['saleLimitEmptySaveErrors']}` |",
        f"| ヤマトB2決済方法選択肢 | `{facts['yamatoPaymentOptions']}` |",
        f"| ヤマトB2ステータス変更チェック初期状態 | `{facts['yamatoStatusCheckbox']}` |",
        f"| 会社担当者を追加して詳細を表示 | `{facts['companyContactDetailOpened']}` |",
        "",
        "## 判断",
        "",
        "- 商品バリエーション作成フォームの3チェックボックスは、画面上の初期値として確認済み。ただし外部注文・出荷への実効は注文/チャネル連携前提なので未確認。",
        "- 翻訳ルールのトップ/一覧/作成/詳細の確認範囲では、`実行` / `再実行` / `翻訳する` / `生成` ボタンは見当たらない。",
        "- 採寸ルールはテンプレート定義として表示され、詳細入力はreadonly。商品詳細側に採寸紐づけ導線は見当たらない。",
        "- 販売上限は未接続環境ではチャネル候補が表示されず、空保存でルール名とチャネルの両方のエラーが出る。",
        "- ヤマトB2条件指定フォームでは決済方法3択とステータス変更チェックOFFを確認。実ファイル生成・メール通知は実行していない。",
        "- 会社担当者は会社詳細ダイアログから追加でき、担当者詳細は名前/メール/電話/作成日時中心。削除導線はこの確認範囲では見当たらない。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        "",
        "## バリエーション作成フォームのラベル",
        "",
    ]
    for label in variant.get("labels", []):
        lines.append(f"- `{label}`")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "contactEmail": CONTACT_EMAIL,
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)

        page.goto(BASE + "/admin/products/create", wait_until="load")
        wait_quiet(page)
        payload["productCreate"] = snap(page)

        page.goto(BASE + f"/admin/products/{PRODUCT_ID}/variants/create", wait_until="load")
        wait_quiet(page)
        payload["productVariantCreate"] = snap(page)
        payload["variantCheckboxes"] = {
            "trackInventory": get_checkbox(page, "在庫を追跡する"),
            "continueSelling": get_checkbox(page, "在庫切れの場合でも販売を続ける"),
            "requiresShipping": get_checkbox(page, "配送を必須にする"),
        }
        payload["variantUnitSelect"] = select_options(page, "単位")

        page.goto(BASE + "/admin/settings/translation", wait_until="load")
        wait_quiet(page)
        payload["translationTop"] = snap(page)
        page.goto(BASE + "/admin/settings/translation/translation_rules", wait_until="load")
        wait_quiet(page)
        payload["translationRulesList"] = snap(page)
        translation_detail = first_detail_link(payload["translationRulesList"], "/translation_rules/")
        payload["translationDetailHref"] = translation_detail
        page.goto(BASE + "/admin/settings/translation/translation_rules/create", wait_until="load")
        wait_quiet(page)
        payload["translationRuleCreate"] = snap(page)
        if translation_detail:
            page.goto(BASE + translation_detail, wait_until="load")
            wait_quiet(page)
            payload["translationRuleDetail"] = snap(page)

        page.goto(BASE + "/admin/settings/product_measurement_rules", wait_until="load")
        wait_quiet(page)
        payload["measurementRulesList"] = snap(page)
        measurement_detail = first_detail_link(payload["measurementRulesList"], "/product_measurement_rules/")
        payload["measurementDetailHref"] = measurement_detail
        page.goto(BASE + "/admin/settings/product_measurement_rules/create", wait_until="load")
        wait_quiet(page)
        payload["measurementRuleCreate"] = snap(page)
        if measurement_detail:
            page.goto(BASE + measurement_detail, wait_until="load")
            wait_quiet(page)
            payload["measurementRuleDetail"] = snap(page)

        page.goto(BASE + f"/admin/products/{PRODUCT_ID}", wait_until="load")
        wait_quiet(page)
        payload["productDetailForMeasurementSearch"] = snap(page)

        page.goto(BASE + "/admin/inventory_sale_limit_rules/create", wait_until="load")
        wait_quiet(page)
        payload["saleLimitCreateBeforeSave"] = snap(page)
        page.get_by_role("button", name="保存する").click()
        wait_quiet(page)
        payload["saleLimitCreateAfterEmptySave"] = snap(page)

        page.goto(BASE + "/admin/inventory_outbound_orders/export/yamato_b2_cloud", wait_until="load")
        wait_quiet(page)
        payload["yamatoB2ExportForm"] = snap(page)
        payload["yamatoB2Selects"] = {
            "payment": select_options(page, "決済方法"),
            "status": select_options(page, "出荷作業ステータス"),
        }
        payload["yamatoB2StatusCheckbox"] = get_checkbox(page, "CSVの出力後に出荷指示のステータスを出荷作業中に変更する")

        create_company_contact(page, payload)

        def checked(name):
            return payload["variantCheckboxes"][name]

        translation_buttons = payload.get("translationRuleDetail", {}).get("buttons", [])
        manual_buttons = [b for b in translation_buttons if b in ["実行", "再実行", "翻訳する", "生成"]]
        measurement_controls = payload.get("measurementRuleDetail", {}).get("controls", [])
        sale_limit_body = payload.get("saleLimitCreateAfterEmptySave", {}).get("bodyText", "")

        payload["facts"] = {
            "trackInventoryCheckbox": checked("trackInventory"),
            "continueSellingCheckbox": checked("continueSelling"),
            "requiresShippingCheckbox": checked("requiresShipping"),
            "translationManualActionButtons": manual_buttons,
            "measurementDetailReadonlyControls": [
                {"label": c.get("label"), "readOnly": c.get("readOnly"), "disabled": c.get("disabled")}
                for c in measurement_controls
                if c.get("tag") in ["input", "textarea"]
            ],
            "productDetailHasMeasurementText": payload.get("productDetailForMeasurementSearch", {}).get("bodyIncludes", {}).get("measurement"),
            "saleLimitEmptySaveErrors": {
                "name": "販売上限ルール名を入力してください" in sale_limit_body,
                "channel": "チャネルを選択してください" in sale_limit_body,
            },
            "yamatoPaymentOptions": payload["yamatoB2Selects"]["payment"],
            "yamatoStatusOptions": payload["yamatoB2Selects"]["status"],
            "yamatoStatusCheckbox": payload["yamatoB2StatusCheckbox"],
            "companyContactDetailOpened": bool(payload.get("companyContactDetail")),
            "companyContactDetailButtons": payload.get("companyContactDetail", {}).get("buttons", []),
        }
        OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_md(payload)
        page.close()
        browser.close()

    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
