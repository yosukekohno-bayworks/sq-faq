import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "sales-settings-current-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const base = "https://www.sqstackstaging.com";
const records = [];
const network = [];
const consoleLogs = [];
let shotIndex = 1;

function compact(items, limit = 260) {
  return [...new Set(items.map((item) => (item || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(value) {
  return value.replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 150) || "screen";
}

function safeUrl(url) {
  try {
    const parsed = new URL(url);
    if (parsed.hostname.includes("clerk")) parsed.search = "";
    if (parsed.searchParams.has("__session")) parsed.searchParams.set("__session", "[redacted]");
    return parsed.toString();
  } catch {
    return url;
  }
}

async function settle(page, extraMs = 800) {
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(extraMs);
}

async function goto(page, url) {
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
}

async function getControls(page) {
  return await page
    .locator("button, a, input, select, textarea")
    .evaluateAll((els) =>
      els.slice(0, 560).map((el) => {
        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);
        return {
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute("type") || "",
          role: el.getAttribute("role") || "",
          text: el.textContent?.trim().replace(/\s+/g, " ") || "",
          ariaLabel: el.getAttribute("aria-label") || "",
          title: el.getAttribute("title") || "",
          href: el.href || "",
          placeholder: el.getAttribute("placeholder") || "",
          value: String(el.value || "").slice(0, 400),
          checked: el.checked || false,
          disabled: el.disabled || el.getAttribute("aria-disabled") === "true" || false,
          visible:
            style.visibility !== "hidden" &&
            style.display !== "none" &&
            rect.width > 0 &&
            rect.height > 0,
        };
      }),
    )
    .catch(() => []);
}

async function getSelectOptions(page) {
  return await page
    .locator("select")
    .evaluateAll((selects) =>
      selects.slice(0, 60).map((select, index) => ({
        index,
        value: select.value || "",
        disabled: select.disabled,
        options: Array.from(select.options).map((option) => ({
          text: option.textContent?.trim().replace(/\s+/g, " ") || "",
          value: option.value || "",
          disabled: option.disabled,
        })),
      })),
    )
    .catch(() => []);
}

async function snapshot(page, name, requestedUrl, extra = {}) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(shotIndex).padStart(2, "0")}-${slugify(name)}.png`);
  const text = await page.locator("body").innerText({ timeout: 12000 }).catch(() => "");
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const controls = await getControls(page);
  const record = {
    name,
    requestedUrl,
    url: page.url(),
    title: await page.title().catch(() => ""),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => []), 40),
    h2: compact(await page.locator("h2").allInnerTexts().catch(() => []), 120),
    dialogs: compact(await page.locator('[role="dialog"], [role="menu"]').allInnerTexts().catch(() => []), 100),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 300))
        .catch(() => []),
      300,
    ),
    controls,
    links: controls.filter((control) => control.tag === "a" && control.href).map((control) => ({ text: control.text, href: control.href })),
    buttons: controls.filter((control) => control.tag === "button").map((control) => ({ text: control.text, ariaLabel: control.ariaLabel, disabled: control.disabled, visible: control.visible })),
    checkedInputs: controls.filter((control) => control.checked).map((control) => ({ type: control.type, value: control.value, text: control.text, ariaLabel: control.ariaLabel })),
    selectOptions: await getSelectOptions(page),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(販売価格|通常価格|セール価格|予約販売|販売上限|販売閾値|ルール|通貨|日本円|JPY|価格|税込|商品バリエーション|SKU|販売数|販売上限数|集計|開始日時|チャネル|デフォルト|閾値|自動追加|ブランドコード|一致する|インポート|CSV|アイテムが見つかりません|選択してください|保存する|作成する|登録する|追加する|このページの準備が整いました|このページは存在しない|エラー)/.test(
            line,
          ),
        ),
      520,
    ),
    classification: {
      empty: text.includes("アイテムが見つかりませんでした"),
      notFound: text.includes("このページは存在しないようです"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} url=${record.url} empty=${record.classification.empty} notFound=${record.classification.notFound}`);
  shotIndex += 1;
  return record;
}

async function firstHref(page, pattern, exclude = []) {
  const hrefs = await page
    .locator("a")
    .evaluateAll((els) => els.map((el) => el.href).filter(Boolean))
    .catch(() => []);
  return [...new Set(hrefs)].find((href) => pattern.test(href) && exclude.every((item) => !href.includes(item))) || null;
}

async function clickText(page, textRe, name) {
  const locator = page.getByText(textRe).first();
  if (!(await locator.isVisible().catch(() => false))) return false;
  await locator.click({ timeout: 5000 }).catch(() => {});
  await settle(page, 500);
  console.log(`clicked: ${name}`);
  return true;
}

async function clickButton(page, nameRe, name) {
  const locator = page.getByRole("button", { name: nameRe }).first();
  if (!(await locator.isVisible().catch(() => false))) return false;
  await locator.click({ timeout: 5000 }).catch(() => {});
  await settle(page, 500);
  console.log(`clicked: ${name}`);
  return true;
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  locale: "ja-JP",
  timezoneId: "Asia/Tokyo",
  acceptDownloads: false,
});

context.on("page", (page) => {
  page.on("console", (message) => {
    if (message.type() === "error") consoleLogs.push({ type: message.type(), text: message.text().slice(0, 600) });
  });
  page.on("response", (response) => {
    if (response.status() >= 400) network.push({ status: response.status(), url: safeUrl(response.url()), method: response.request().method() });
  });
});

const page = context.pages()[0] || (await context.newPage());
page.on("console", (message) => {
  if (message.type() === "error") consoleLogs.push({ type: message.type(), text: message.text().slice(0, 600) });
});
page.on("response", (response) => {
  if (response.status() >= 400) network.push({ status: response.status(), url: safeUrl(response.url()), method: response.request().method() });
});

try {
  for (const [name, url] of [
    ["price-rules-list", `${base}/admin/product_price_rules`],
    ["price-rule-create", `${base}/admin/product_price_rules/create`],
    ["back-order-rules-list", `${base}/admin/inventory_back_order_rules`],
    ["back-order-rule-create", `${base}/admin/inventory_back_order_rules/create`],
    ["sale-limit-rules-list", `${base}/admin/inventory_sale_limit_rules`],
    ["sale-limit-rule-create", `${base}/admin/inventory_sale_limit_rules/create`],
    ["threshold-rules-list", `${base}/admin/inventory_threshold_rules`],
    ["threshold-rule-create", `${base}/admin/inventory_threshold_rules/create`],
  ]) {
    await goto(page, url);
    await snapshot(page, name, url);
  }

  await goto(page, `${base}/admin/product_price_rules`);
  const priceRule = await firstHref(page, /\/admin\/product_price_rules\/[^/?#]+$/, ["/create"]);
  if (priceRule) {
    await goto(page, priceRule);
    await snapshot(page, "price-rule-detail-first", priceRule, { discoveredUrl: priceRule });
    if (!(await clickButton(page, /^ルールを編集$/, "price-rule-edit"))) {
      await clickText(page, /^ルールを編集$/, "price-rule-edit");
    }
    await snapshot(page, "price-rule-edit-modal-opened", priceRule, { discoveredUrl: priceRule, action: "open-edit-modal" });
    await goto(page, `${priceRule}/product_variant_regulars`);
    await snapshot(page, "regular-prices-list-first-rule", `${priceRule}/product_variant_regulars`);
    await goto(page, `${priceRule}/product_variant_regulars/create`);
    await snapshot(page, "regular-price-create-first-rule", `${priceRule}/product_variant_regulars/create`);
    await clickButton(page, /^選択$/, "regular-price-variant-picker");
    await snapshot(page, "regular-price-create-picker-opened", `${priceRule}/product_variant_regulars/create`, { action: "open-variant-picker" });
    await goto(page, `${priceRule}/product_variant_sales`);
    await snapshot(page, "sale-prices-list-first-rule", `${priceRule}/product_variant_sales`);
    await goto(page, `${priceRule}/product_variant_sales/create`);
    await snapshot(page, "sale-price-create-first-rule", `${priceRule}/product_variant_sales/create`);
  } else {
    records.push({ name: "price-rule-detail-first", note: "No price rule detail link found." });
  }

  await goto(page, `${base}/admin/inventory_back_order_rules`);
  let backOrderRule = await firstHref(page, /\/admin\/inventory_back_order_rules\/[^/?#]+$/, ["/create"]);
  if (!backOrderRule) {
    await clickText(page, /TEST_FAQ_DEEP_202606080340_予約販売ルール|TEST_FAQ_予約販売ルール/, "back-order-row");
    if (/\/admin\/inventory_back_order_rules\/[^/?#]+$/.test(page.url())) backOrderRule = page.url();
  }
  if (!backOrderRule) {
    backOrderRule = `${base}/admin/inventory_back_order_rules/c885e9d7-ecb2-514e-a1ec-aadb6d57a5cb_InventoryBackOrderRule`;
  }
  if (backOrderRule) {
    await goto(page, backOrderRule);
    await snapshot(page, "back-order-rule-detail-first", backOrderRule, { discoveredUrl: backOrderRule });
    if (!(await clickButton(page, /^ルールを編集する$/, "back-order-edit"))) {
      await clickText(page, /^ルールを編集する$/, "back-order-edit");
    }
    await snapshot(page, "back-order-rule-edit-modal-opened", backOrderRule, { discoveredUrl: backOrderRule, action: "open-edit-modal" });
    await goto(page, `${backOrderRule}/create`);
    await snapshot(page, "back-order-variant-create-first", `${backOrderRule}/create`);
    await clickButton(page, /^選択$/, "back-order-variant-picker");
    await snapshot(page, "back-order-variant-create-picker-opened", `${backOrderRule}/create`, { action: "open-variant-picker" });
  } else {
    records.push({ name: "back-order-rule-detail-first", note: "No back order rule detail link found." });
  }

  await goto(page, `${base}/admin/inventory_threshold_rules`);
  let thresholdRule = await firstHref(page, /\/admin\/inventory_threshold_rules\/[^/?#]+$/, ["/create"]);
  if (!thresholdRule) {
    await clickText(page, /TEST_FAQ_DEEP_202606080340_販売閾値ルール|TEST_FAQ_販売閾値ルール/, "threshold-row");
    if (/\/admin\/inventory_threshold_rules\/[^/?#]+$/.test(page.url())) thresholdRule = page.url();
  }
  if (thresholdRule) {
    await goto(page, thresholdRule);
    await snapshot(page, "threshold-rule-detail-first", thresholdRule, { discoveredUrl: thresholdRule });
    await goto(page, `${thresholdRule}/create`);
    await snapshot(page, "threshold-rule-variant-create-first", `${thresholdRule}/create`);
    await clickButton(page, /^選択$/, "threshold-variant-picker");
    await snapshot(page, "threshold-rule-variant-create-picker-opened", `${thresholdRule}/create`, { action: "open-variant-picker" });
    await goto(page, `${thresholdRule}/automatic_add_rules`);
    await snapshot(page, "threshold-automatic-add-rules-first", `${thresholdRule}/automatic_add_rules`);
    await goto(page, `${thresholdRule}/automatic_add_rules/create`);
    await snapshot(page, "threshold-automatic-add-rule-create-first", `${thresholdRule}/automatic_add_rules/create`);
  } else {
    records.push({ name: "threshold-rule-detail-first", note: "No threshold rule detail link found." });
  }
} catch (error) {
  records.push({ name: "failure", message: error.message, stack: error.stack });
  await snapshot(page, "failure-state", page.url(), { error: error.message }).catch(() => {});
  throw error;
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "sales-settings-current-records.json"),
    JSON.stringify(
      {
        generatedAt: new Date().toISOString(),
        failed: records.find((record) => record.name === "failure")?.message || null,
        records,
        network,
        console: consoleLogs,
      },
      null,
      2,
    ),
  );
  await context.close();
}
