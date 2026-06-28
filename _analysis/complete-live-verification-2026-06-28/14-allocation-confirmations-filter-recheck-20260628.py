from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright

BASE = "https://www.sqstackstaging.com"
CDP = "http://127.0.0.1:50141"


def wait(page, timeout=1000):
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(timeout)


with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(CDP)
    page = browser.contexts[0].new_page()
    page.set_default_timeout(15000)
    page.set_viewport_size({"width": 1600, "height": 1200})
    page.goto(f"{BASE}/admin/inventory_allocation_request_confirmations", wait_until="load")
    wait(page)

    body = page.locator("body").inner_text()
    print("url:", page.url)
    print("h1:", [h.inner_text() for h in page.locator("h1").all()])
    for word in ["絞り込み", "ロケーション", "キーワード", "検索", "移動元", "移動先", "フィルタ"]:
        print(word, word in body)
    print(
        "buttons:",
        page.locator("button").evaluate_all(
            "els=>els.map(e=>(e.innerText||e.textContent||'').replace(/\\s+/g,' ').trim()).filter(Boolean)"
        ),
    )
    print(
        "inputs:",
        page.locator("input").evaluate_all(
            "els=>els.map(e=>({type:e.type,placeholder:e.placeholder,value:e.value,checked:e.checked,disabled:e.disabled,aria:e.getAttribute('aria-label')}))"
        ),
    )
    print(
        "rows:",
        page.locator("tr").evaluate_all(
            "els=>els.map(e=>(e.innerText||e.textContent||'').replace(/\\s+/g,' ').trim()).filter(Boolean)"
        ),
    )
    page.screenshot(
        path="_analysis/complete-live-verification-2026-06-28/14-allocation-confirmations-current-20260628.png",
        full_page=True,
    )
    page.close()
    browser.close()
