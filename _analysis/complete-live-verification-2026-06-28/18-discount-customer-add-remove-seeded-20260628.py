#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
OUT_DIR = ROOT / "_analysis" / "complete-live-verification-2026-06-28"
INSPECT_JSON = OUT_DIR / "18-discount-customer-tab-inspect-20260628.json"
CUSTOMER_JSON = Path(os.environ.get("SQ_CUSTOMER_JSON", OUT_DIR / "17-purchasing-customer-graphql-create-uniqlo-20260628.json"))
OUT_JSON = OUT_DIR / "18-discount-customer-add-remove-seeded-20260628.json"
OUT_MD = OUT_JSON.with_suffix(".md")
BASE = "https://www.sqstackstaging.com"
CDP = os.environ.get("SQ_CDP_URL", "http://127.0.0.1:50527")


def compact(text, limit=3400):
    return " ".join((text or "").split())[:limit]


def wait_soft(page, timeout=12000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(900)


def snapshot(page, label):
    return {
        "label": label,
        "url": page.url,
        "title": page.title(),
        "bodySample": compact(page.inner_text("body"), 5200),
        "headers": [compact(x, 300) for x in page.locator("h1,h2,h3,th").all_inner_texts() if compact(x, 300)],
        "rows": [compact(x, 1000) for x in page.locator("tr").all_inner_texts()[:60] if compact(x, 1000)],
        "controls": page.evaluate(
            """() => Array.from(document.querySelectorAll('button, a[href], input, textarea, select')).map((el) => ({
                tag: el.tagName.toLowerCase(),
                text: (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' '),
                href: el.getAttribute('href'),
                type: el.getAttribute('type'),
                placeholder: el.getAttribute('placeholder'),
                ariaLabel: el.getAttribute('aria-label'),
                ariaDisabled: el.getAttribute('aria-disabled'),
                disabled: Boolean(el.disabled),
                checked: Boolean(el.checked),
                className: el.className ? String(el.className).slice(0, 220) : '',
            })).slice(0, 260)"""
        ),
    }


def has_customer(page, name, email):
    text = page.inner_text("body")
    return name in text or email in text


def click_button_by_text(page, text, *, timeout=8000):
    loc = page.get_by_role("button", name=text)
    if loc.count() == 0:
        loc = page.get_by_text(text, exact=True)
    loc.first.click(timeout=timeout)
    wait_soft(page, 8000)


def fill_first_search_input(page, value):
    selectors = [
        'input[placeholder*="email"]',
        'input[placeholder*="メール"]',
        'input[placeholder*="検索"]',
        'input[type="text"]',
    ]
    for selector in selectors:
        loc = page.locator(selector)
        for idx in range(loc.count() - 1, -1, -1):
            item = loc.nth(idx)
            if item.is_visible(timeout=1000) and item.is_enabled(timeout=1000):
                item.fill(value)
                page.keyboard.press("Enter")
                wait_soft(page, 10000)
                return True
    return False


def click_customer_checkbox(page, name, email):
    row = page.locator("tr").filter(has_text=name)
    if row.count() == 0:
        row = page.locator("tr").filter(has_text=email)
    if row.count() > 0:
        target = row.first
        checkbox = target.locator('input[type="checkbox"]')
        if checkbox.count() > 0:
            checkbox.first.click(force=True, timeout=5000)
            wait_soft(page, 5000)
            return True
        button = target.get_by_label("アイテムを選択する")
        if button.count() > 0:
            button.first.click(timeout=5000)
            wait_soft(page, 5000)
            return True
        target.click(timeout=5000)
        wait_soft(page, 5000)
        return True
    candidates = page.get_by_text(name, exact=False)
    if candidates.count() > 0:
        candidates.first.click(timeout=5000)
        wait_soft(page, 5000)
        return True
    return False


def click_select_confirm(page):
    candidates = [
        page.get_by_role("button", name="選択する"),
        page.get_by_text("選択する", exact=True),
        page.get_by_role("button", name="追加する"),
    ]
    for loc in candidates:
        if loc.count() == 0:
            continue
        for idx in range(loc.count() - 1, -1, -1):
            button = loc.nth(idx)
            try:
                if button.is_visible(timeout=1000) and button.is_enabled(timeout=1000):
                    button.click(timeout=5000)
                    wait_soft(page, 12000)
                    return True
            except Exception:
                continue
    return False


def try_remove_selected_customer(page, name, email):
    selected = click_customer_checkbox(page, name, email)
    if not selected:
        return {"rowSelectedForDelete": False}
    before = snapshot(page, "after-select-for-delete")
    delete_clicked = False
    confirm_clicked = False
    for label in ["削除する", "削除"]:
        loc = page.get_by_role("button", name=label)
        for idx in range(loc.count() - 1, -1, -1):
            try:
                button = loc.nth(idx)
                if button.is_visible(timeout=1000) and button.is_enabled(timeout=1000):
                    button.click(timeout=5000)
                    delete_clicked = True
                    wait_soft(page, 10000)
                    break
            except Exception:
                continue
        if delete_clicked:
            break
    if delete_clicked:
        # If a confirmation dialog appears, click the destructive action once more.
        for label in ["削除する", "削除"]:
            loc = page.get_by_role("button", name=label)
            for idx in range(loc.count() - 1, -1, -1):
                try:
                    button = loc.nth(idx)
                    if button.is_visible(timeout=1000) and button.is_enabled(timeout=1000):
                        button.click(timeout=5000)
                        confirm_clicked = True
                        wait_soft(page, 12000)
                        break
                except Exception:
                    continue
            if confirm_clicked:
                break
    return {
        "rowSelectedForDelete": selected,
        "deleteButtonClicked": delete_clicked,
        "deleteConfirmClicked": confirm_clicked,
        "selectionSnapshot": before,
    }


def main():
    inspect = json.loads(INSPECT_JSON.read_text(encoding="utf-8"))
    customer_seed = json.loads(CUSTOMER_JSON.read_text(encoding="utf-8"))
    rule = inspect["facts"]["selectedDiscountRule"]
    customers_url = f"{BASE}{rule['href']}/customers"
    customer_name = customer_seed["facts"]["customerFullName"]
    customer_email = customer_seed["facts"]["customerEmail"]
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "discountRule": rule,
        "customer": {
            "name": customer_name,
            "email": customer_email,
            "id": customer_seed["facts"]["customerID"],
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
            page.goto(customers_url, wait_until="domcontentloaded", timeout=60000)
            wait_soft(page)
            payload["steps"].append(snapshot(page, "before-add"))
            payload["facts"]["customerPresentBeforeAdd"] = has_customer(page, customer_name, customer_email)
            if not payload["facts"]["customerPresentBeforeAdd"]:
                click_button_by_text(page, "追加する")
                payload["steps"].append(snapshot(page, "add-menu"))
                click_button_by_text(page, "顧客を選択して追加")
                payload["steps"].append(snapshot(page, "select-customer-dialog-open"))
                payload["facts"]["searchInputFilled"] = fill_first_search_input(page, customer_email)
                payload["steps"].append(snapshot(page, "select-customer-dialog-after-search"))
                payload["facts"]["customerCandidateVisible"] = has_customer(page, customer_name, customer_email)
                payload["facts"]["customerCandidateSelected"] = click_customer_checkbox(page, customer_name, customer_email)
                payload["steps"].append(snapshot(page, "select-customer-dialog-after-select"))
                payload["facts"]["selectConfirmClicked"] = click_select_confirm(page)
                wait_soft(page, 12000)
                page.goto(customers_url, wait_until="domcontentloaded", timeout=60000)
                wait_soft(page)
            payload["steps"].append(snapshot(page, "after-add-refresh"))
            payload["facts"]["customerPresentAfterAdd"] = has_customer(page, customer_name, customer_email)
            payload["facts"]["rowsAfterAdd"] = payload["steps"][-1]["rows"]
            if payload["facts"]["customerPresentAfterAdd"]:
                remove_result = try_remove_selected_customer(page, customer_name, customer_email)
                selection_snapshot = remove_result.pop("selectionSnapshot", None)
                payload["facts"].update(remove_result)
                if selection_snapshot:
                    payload["steps"].append(selection_snapshot)
                wait_soft(page, 12000)
                page.goto(customers_url, wait_until="domcontentloaded", timeout=60000)
                wait_soft(page)
                payload["steps"].append(snapshot(page, "after-remove-refresh"))
                payload["facts"]["customerPresentAfterRemove"] = has_customer(page, customer_name, customer_email)
                payload["facts"]["rowsAfterRemove"] = payload["steps"][-1]["rows"]
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            lines = [
                "# ディスカウント対象顧客 追加・削除検証 2026-06-28",
                "",
                f"- 対象ディスカウント: `{rule['text']}`",
                f"- 対象顧客: `{customer_name}` / `{customer_email}`",
                f"- 追加前に表示: `{payload['facts'].get('customerPresentBeforeAdd')}`",
                f"- 検索入力成功: `{payload['facts'].get('searchInputFilled')}`",
                f"- 候補表示: `{payload['facts'].get('customerCandidateVisible')}`",
                f"- 候補選択: `{payload['facts'].get('customerCandidateSelected')}`",
                f"- 選択確定クリック: `{payload['facts'].get('selectConfirmClicked')}`",
                f"- 追加後に表示: `{payload['facts'].get('customerPresentAfterAdd')}`",
                f"- 削除行選択: `{payload['facts'].get('rowSelectedForDelete')}`",
                f"- 削除ボタンクリック: `{payload['facts'].get('deleteButtonClicked')}`",
                f"- 削除確認クリック: `{payload['facts'].get('deleteConfirmClicked')}`",
                f"- 削除後に表示: `{payload['facts'].get('customerPresentAfterRemove')}`",
                f"- JSON証跡: `{OUT_JSON.relative_to(ROOT)}`",
                "",
                "## 追加後の行",
                "",
            ]
            for row in payload["facts"].get("rowsAfterAdd", []):
                lines.append(f"- {row}")
            lines.extend(["", "## 削除後の行", ""])
            for row in payload["facts"].get("rowsAfterRemove", []):
                lines.append(f"- {row}")
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
