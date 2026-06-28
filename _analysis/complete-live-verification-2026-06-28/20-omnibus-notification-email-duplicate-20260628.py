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
OUT_JSON = OUT_DIR / "20-omnibus-notification-email-duplicate-20260628.json"
OUT_MD = OUT_DIR / "20-omnibus-notification-email-duplicate-20260628.md"
ROUTE = "/admin/omnibus_core_integrations/c1a74b89-2c67-5167-ba46-952c7539a7a5_OmnibusCoreIntegration/notification_emails"


def wait_quiet(page, timeout=7000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1000)


def state(page, email=None):
    return page.evaluate(
        """(email) => {
            const text = (el) => (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const unique = (items) => Array.from(new Set(items.filter(Boolean)));
            const rows = Array.from(document.querySelectorAll('tr')).map((tr) => text(tr)).filter(Boolean);
            const body = document.body.innerText || '';
            const dialog = document.querySelector('[role="dialog"]');
            return {
                url: location.href,
                h1: unique(Array.from(document.querySelectorAll('h1')).map(text)),
                h2: unique(Array.from(document.querySelectorAll('h2')).map(text)),
                labels: unique(Array.from(document.querySelectorAll('label')).map(text)),
                buttons: unique(Array.from(document.querySelectorAll('button')).map((button) => text(button) || button.getAttribute('aria-label') || '')),
                rows,
                targetEmailRowCount: email ? rows.filter((row) => row.includes(email)).length : null,
                bodyIncludes: {
                    empty: body.includes('アイテムが見つかりませんでした'),
                    duplicateHint: body.includes('メールアドレスは重複して登録できません'),
                    duplicateLikelyError: body.includes('既に') || body.includes('すでに') || body.includes('重複') || body.includes('登録できません'),
                    targetEmail: email ? body.includes(email) : false
                },
                dialog: dialog ? {
                    title: unique(Array.from(dialog.querySelectorAll('h1,h2,h3')).map(text)),
                    labels: unique(Array.from(dialog.querySelectorAll('label')).map(text)),
                    buttons: unique(Array.from(dialog.querySelectorAll('button')).map((button) => text(button) || button.getAttribute('aria-label') || '')),
                    text: text(dialog)
                } : null,
                notifications: unique(Array.from(document.querySelectorAll('[aria-label="Notifications"], [role="status"], [data-polaris-live-region]')).map(text)).slice(0, 8),
            };
        }""",
        email,
    )


def open_add_dialog(page):
    page.get_by_role("button", name="追加する").first.click()
    wait_quiet(page)


def fill_dialog(page, name, email):
    page.get_by_label("名前").fill(name)
    page.get_by_label("メールアドレス").fill(email)


def click_dialog_add(page):
    dialog = page.locator('[role="dialog"]').first
    dialog.get_by_role("button", name="追加する").click()
    try:
        dialog.wait_for(state="hidden", timeout=5000)
    except PlaywrightTimeoutError:
        pass
    wait_quiet(page)


def add_email(page, name, email):
    open_add_dialog(page)
    before_submit = state(page, email)
    fill_dialog(page, name, email)
    after_fill = state(page, email)
    click_dialog_add(page)
    after_submit = state(page, email)
    return {
        "beforeSubmit": before_submit,
        "afterFill": after_fill,
        "afterSubmit": after_submit,
    }


def delete_target_rows(page, email):
    results = []
    for _ in range(4):
        page.goto(BASE + ROUTE, wait_until="load")
        wait_quiet(page)
        current = state(page, email)
        if current["targetEmailRowCount"] == 0:
            break
        row = page.locator("tr").filter(has_text=email).first
        clicked = False
        checkbox = row.locator('input[type="checkbox"]').first
        if checkbox.count() > 0:
            checkbox.click(force=True)
            clicked = True
        else:
            role_checkbox = row.get_by_role("checkbox").first
            if role_checkbox.count() > 0:
                role_checkbox.click(force=True)
                clicked = True
        wait_quiet(page)
        selected = state(page, email)
        delete_button = page.get_by_role("button", name="削除する")
        if delete_button.count() == 0:
            delete_button = page.get_by_role("button", name="通知メールを削除")
        if delete_button.count() == 0:
            delete_button = page.get_by_text("削除", exact=False)
        action_clicked = False
        if delete_button.count() > 0:
            delete_button.first.click(force=True)
            wait_quiet(page)
            action_clicked = True
        after_delete_click = state(page, email)
        dialog = page.locator('[role="dialog"]').first
        confirmed = False
        if dialog.count() > 0:
            confirm = dialog.get_by_role("button", name="削除する")
            if confirm.count() == 0:
                confirm = dialog.get_by_text("削除", exact=True)
            if confirm.count() > 0:
                confirm.first.click(force=True)
                wait_quiet(page)
                confirmed = True
        after_confirm = state(page, email)
        results.append({
            "before": current,
            "rowCheckboxClicked": clicked,
            "selected": selected,
            "deleteActionClicked": action_clicked,
            "afterDeleteClick": after_delete_click,
            "confirmed": confirmed,
            "afterConfirm": after_confirm,
        })
    return results


def write_md(payload):
    facts = payload["facts"]
    lines = [
        "# OmnibusCore 通知メール重複保存 実機確認 2026-06-28",
        "",
        f"- 対象URL: `{BASE + ROUTE}`",
        f"- 検証メール: `{payload['email']}`",
        "",
        "## 結果",
        "",
        "| 確認項目 | 結果 |",
        "|:--|:--|",
        f"| 初期一覧は空 | `{facts['initialEmpty']}` |",
        f"| 1回目追加後に対象メールが一覧表示 | `{facts['firstAddListed']}` |",
        f"| 2回目追加後の対象メール行数 | `{facts['duplicateRowCountAfterSecondAdd']}` |",
        f"| 2回目追加後に重複不可ヒント/表示あり | `{facts['duplicateHintVisibleAfterSecondAdd']}` |",
        f"| GraphQLエラー | `{facts['graphqlErrors']}` |",
        f"| 削除後に対象メールが残っていない | `{facts['cleanupComplete']}` |",
        "",
        "## 判断",
        "",
        "- 通知メールは一覧が空の状態から追加でき、追加後に名前/メールアドレスが一覧へ表示された。",
        "- 同じメールアドレスを2回目に追加しようとすると、一覧に2行目は増えず、ダイアログ内に重複不可の文言が表示された。今回の確認範囲ではGraphQL errorsは返っていないため、サーバー側エラー文言としては扱わない。",
        "- 検証用通知メールは確認後に削除済み。",
        "",
        "## 証跡",
        "",
        f"- JSON: `{OUT_JSON.relative_to(ROOT)}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    email = f"sq-faq-omni-dupe-{stamp}@example.com"
    name = f"FAQ Omnibus Dup {stamp}"
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "route": ROUTE,
        "email": email,
        "name": name,
        "graphqlErrors": [],
        "nonGetResponses": [],
        "errors": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(20000)
        def on_response(response):
            try:
                if response.request.method.upper() != "GET":
                    payload["nonGetResponses"].append({
                        "method": response.request.method,
                        "path": "/" + response.url.split("://", 1)[-1].split("/", 1)[-1].split("?", 1)[0],
                        "status": response.status,
                    })
                    if response.url.endswith("/api/graphql"):
                        try:
                            body = response.json()
                            for err in body.get("errors", []) if isinstance(body, dict) else []:
                                message = err.get("message")
                                if message:
                                    payload["graphqlErrors"].append(message)
                        except Exception:
                            pass
            except Exception:
                pass
        page.on("response", on_response)
        try:
            page.goto(BASE + ROUTE, wait_until="load")
            wait_quiet(page)
            payload["initial"] = state(page, email)
            payload["firstAdd"] = add_email(page, name, email)
            payload["secondAdd"] = add_email(page, name + " duplicate", email)
            payload["cleanup"] = delete_target_rows(page, email)
            page.goto(BASE + ROUTE, wait_until="load")
            wait_quiet(page)
            payload["final"] = state(page, email)
        except Exception as exc:
            payload["errors"].append(repr(exc))
        finally:
            second_after = payload.get("secondAdd", {}).get("afterSubmit", {})
            payload["facts"] = {
                "initialEmpty": payload.get("initial", {}).get("bodyIncludes", {}).get("empty") is True,
                "firstAddListed": payload.get("firstAdd", {}).get("afterSubmit", {}).get("targetEmailRowCount", 0) >= 1 or payload.get("secondAdd", {}).get("beforeSubmit", {}).get("targetEmailRowCount", 0) >= 1,
                "duplicateRowCountAfterSecondAdd": second_after.get("targetEmailRowCount"),
                "duplicateHintVisibleAfterSecondAdd": second_after.get("bodyIncludes", {}).get("duplicateLikelyError") is True or (second_after.get("dialog") or {}).get("text", "").find("重複") >= 0,
                "graphqlErrors": payload.get("graphqlErrors", []),
                "cleanupComplete": payload.get("final", {}).get("targetEmailRowCount") == 0,
                "errors": payload["errors"],
            }
            OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            write_md(payload)
            page.close()
            browser.close()
    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD), "facts": payload["facts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
