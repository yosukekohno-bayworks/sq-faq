import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-click-menus-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const BASE = "https://www.sqstackstaging.com";

function compact(items, limit = 240) {
  return [...new Set(items.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(value) {
  return value.replace(/^\/admin\/?/, "").replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 150) || "admin-root";
}

async function goto(page, url) {
  await page.goto(`${BASE}${url}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(900);
}

async function snapshot(page, name, index, extra = {}) {
  const text = await page.locator("body").innerText().catch(() => "");
  const screenshotFile = path.join(SCREEN_DIR, `${String(index).padStart(2, "0")}-${slugify(name)}.png`);
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const rows = await page.locator("tr, [role=row]").evaluateAll((els) =>
    els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 160),
  ).catch(() => []);
  const clickableAttrs = await page.locator("a, button").evaluateAll((els) =>
    els.map((el) => ({
      tag: el.tagName.toLowerCase(),
      text: el.textContent?.trim().replace(/\s+/g, " ") || "",
      href: el.tagName.toLowerCase() === "a" ? el.href || "" : "",
      disabled: "disabled" in el ? Boolean(el.disabled) : false,
      ariaDisabled: el.getAttribute("aria-disabled") || "",
      className: String(el.getAttribute("class") || "").slice(0, 220),
    })).filter((x) => x.text || x.href).slice(0, 260),
  ).catch(() => []);
  return {
    name,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    labels: compact(await page.locator("label").allInnerTexts().catch(() => []), 220),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => []), 180),
    links: await page.locator("a").evaluateAll((els) =>
      els.map((a) => ({ text: a.textContent?.trim().replace(/\s+/g, " ") || "", href: a.href || "" })).filter((a) => a.text || a.href).slice(0, 220),
    ).catch(() => []),
    rows: compact(rows, 160),
    clickableAttrs,
    classification: {
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      empty: text.includes("アイテムが見つかりませんでした"),
      todo: /\bTODO\b/.test(text),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    textLines: compact(text.split(/\n+/).map((line) => line.trim()), 360),
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
}

async function clickButton(page, name, nth = 0) {
  const button = page.getByRole("button", { name: new RegExp(name) }).nth(nth);
  if (await button.isVisible().catch(() => false)) {
    await button.click().catch(() => {});
    await page.waitForTimeout(800);
    return true;
  }
  return false;
}

async function selectNative(page, label, option) {
  const control = page.getByLabel(label).first();
  if (!(await control.isVisible().catch(() => false))) return false;
  const tag = await control.evaluate((el) => el.tagName.toLowerCase()).catch(() => "");
  if (tag !== "select") return false;
  await control.selectOption({ label: option }).catch(() => {});
  await page.waitForTimeout(800);
  return true;
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(20000);
const records = [];
let index = 1;

await goto(page, "/admin/orders");
records.push(await snapshot(page, "orders-before-user-menu", index++));
const userMenuClicked = await clickButton(page, "stack-ps-yosuke|陽介 河野");
records.push(await snapshot(page, "orders-after-user-menu", index++, { interaction: { userMenuClicked } }));
await page.keyboard.press("Escape").catch(() => {});

await goto(page, "/admin/purchasing_customers");
records.push(await snapshot(page, "customers-before-import-menu", index++));
const customerImportClicked = await clickButton(page, "インポート");
records.push(await snapshot(page, "customers-after-import-menu", index++, { interaction: { customerImportClicked } }));
await page.keyboard.press("Escape").catch(() => {});

await goto(page, "/admin/draft_orders");
records.push(await snapshot(page, "draft-orders-disabled-create-attrs", index++));

await goto(page, "/admin/sale_change_line_items");
records.push(await snapshot(page, "sale-change-disabled-create-attrs", index++));

await goto(page, "/admin/inventory_sale_limit_rules/create");
records.push(await snapshot(page, "sale-limit-before-save-validation", index++));
const saleLimitSaveClicked = await clickButton(page, "保存する");
records.push(await snapshot(page, "sale-limit-after-save-validation", index++, { interaction: { saleLimitSaveClicked } }));

await goto(page, "/admin/point_campaign_order_rules/create");
await selectNative(page, "ポイントキャンペーン種別", "なし");
records.push(await snapshot(page, "point-campaign-none-before-channel-select", index++));
const pointChannelClicked = await clickButton(page, "選択");
records.push(await snapshot(page, "point-campaign-none-after-channel-select", index++, { interaction: { pointChannelClicked } }));
await page.keyboard.press("Escape").catch(() => {});

await goto(page, "/admin/retail_portal_integrations/create");
const storeModalClicked = await clickButton(page, "選択", 0);
records.push(await snapshot(page, "retail-portal-store-modal-rows", index++, { interaction: { storeModalClicked } }));
await page.keyboard.press("Escape").catch(() => {});
await page.waitForTimeout(400);
const inventoryModalClicked = await clickButton(page, "選択", 1);
records.push(await snapshot(page, "retail-portal-inventory-modal-rows", index++, { interaction: { inventoryModalClicked } }));
await page.keyboard.press("Escape").catch(() => {});

await fs.writeFile(
  path.join(OUT_DIR, "unconfirmed-click-menus-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2),
);

for (const record of records) {
  console.log(`${record.name}: h1=${record.h1.join(" / ")} class=${JSON.stringify(record.classification)}`);
}

await context.close();
