import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-interactive-readonly-screenshots");
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

function interestingLines(text) {
  return compact(
    text
      .split(/\n+/)
      .map((line) => line.trim())
      .filter((line) =>
        /(注文|下書き|返品|売上実績|顧客|会社|販売上限|販売閾値|ポイントキャンペーン|チャネル|リテールポータル|店舗ロケーション|在庫ロケーション|場所コード|販売員|配送先住所|送料明細|注文明細|完了|選択|保存|作成|追加|エクスポート|インポート|PDF|納品書|卸売|分析|TODO|アイテムが見つかりません|予期せぬ|存在しない|このページの準備が整いました|ログアウト|プロフィール|アカウント|権限)/.test(line),
      ),
    320,
  );
}

async function snapshot(page, name, index, extra = {}) {
  const text = await page.locator("body").innerText().catch(() => "");
  const screenshotFile = path.join(SCREEN_DIR, `${String(index).padStart(2, "0")}-${slugify(name)}.png`);
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});

  const controls = await page.locator("input, textarea, select").evaluateAll((els) =>
    els.map((el) => {
      const id = el.getAttribute("id") || "";
      const label = id
        ? document.querySelector(`label[for="${CSS.escape(id)}"]`)?.textContent?.trim() || ""
        : "";
      const closestLabel = el.closest("label")?.textContent?.trim() || "";
      const context = el.closest("div, label")?.textContent?.trim()?.replace(/\s+/g, " ").slice(0, 220) || "";
      return {
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute("type") || "",
        label: label || closestLabel || el.getAttribute("aria-label") || "",
        name: el.getAttribute("name") || "",
        context,
        checked: "checked" in el ? Boolean(el.checked) : null,
        disabled: Boolean(el.disabled),
        value:
          el.tagName.toLowerCase() === "select"
            ? Array.from(el.options || []).map((o) => ({ text: o.textContent?.trim() || "", selected: Boolean(o.selected) }))
            : el.getAttribute("value") || "",
      };
    }),
  ).catch(() => []);

  return {
    name,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => []), 180),
    links: await page.locator("a").evaluateAll((els) =>
      els.map((a) => ({ text: a.textContent?.trim() || "", href: a.href || "" })).filter((a) => a.text || a.href).slice(0, 220),
    ).catch(() => []),
    labels: compact(await page.locator("label").allInnerTexts().catch(() => []), 260),
    controls,
    controlSummary: {
      total: controls.length,
      disabled: controls.filter((c) => c.disabled).map((c) => c.label || c.context).slice(0, 120),
      checkboxes: controls.filter((c) => c.type === "checkbox").map((c) => ({ label: c.label || c.context, checked: c.checked, disabled: c.disabled })),
      radios: controls.filter((c) => c.type === "radio").map((c) => ({ label: c.label || c.context, checked: c.checked, disabled: c.disabled })),
      selects: controls.filter((c) => c.tag === "select").map((c) => ({
        label: c.label || c.context,
        options: Array.isArray(c.value) ? c.value.map((o) => `${o.selected ? "*" : ""}${o.text}`).filter(Boolean) : [],
      })),
    },
    classification: {
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      empty: text.includes("アイテムが見つかりませんでした"),
      todo: /\bTODO\b/.test(text),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    importantLines: interestingLines(text),
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
}

async function goto(page, url) {
  await page.goto(`${BASE}${url}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(900);
}

async function clickFirstVisible(page, locators) {
  for (const locator of locators) {
    const element = page.locator(locator).first();
    if (await element.isVisible().catch(() => false)) {
      await element.click().catch(() => {});
      await page.waitForTimeout(700);
      return locator;
    }
  }
  return "";
}

async function clickButtonByText(page, text, nth = 0) {
  const button = page.getByRole("button", { name: new RegExp(text) }).nth(nth);
  if (await button.isVisible().catch(() => false)) {
    await button.click().catch(() => {});
    await page.waitForTimeout(800);
    return true;
  }
  return false;
}

async function selectIfNative(page, label, option) {
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

await goto(page, "/admin/products");
records.push(await snapshot(page, "products-before-user-menu", index++));
const userMenuClicked = await clickFirstVisible(page, [
  'button:has-text("stack-ps-yosuke")',
  'button:has-text("陽介 河野")',
  '[aria-label*="ユーザー"]',
  '[aria-label*="アカウント"]',
]);
records.push(await snapshot(page, "products-after-user-menu", index++, { interaction: { userMenuClicked } }));
await page.keyboard.press("Escape").catch(() => {});

const staticTargets = [
  ["/admin/orders", "orders-list-actions"],
  ["/admin/draft_orders", "draft-orders-list-actions"],
  ["/admin/order_returns", "order-returns-list-actions"],
  ["/admin/sale_change_line_items", "sale-change-list-actions"],
  ["/admin/purchasing_customers", "purchasing-customers-list-actions"],
  ["/admin/purchasing_customers/create", "purchasing-customers-create-route"],
  ["/admin/b2b", "b2b-page"],
  ["/admin/b2b/create", "b2b-create-route"],
  ["/admin/analytics", "analytics-page"],
];

for (const [url, name] of staticTargets) {
  await goto(page, url);
  records.push(await snapshot(page, name, index++));
}

await goto(page, "/admin/inventory_sale_limit_rules/create");
records.push(await snapshot(page, "sale-limit-create-initial", index++));

await goto(page, "/admin/point_campaign_order_rules/create");
records.push(await snapshot(page, "point-campaign-create-initial", index++));
const selectedNone = await selectIfNative(page, "ポイントキャンペーン種別", "なし");
records.push(await snapshot(page, "point-campaign-create-after-type-none", index++, { interaction: { selectedNone } }));
const selectedProduct = await selectIfNative(page, "ポイントキャンペーン種別", "商品");
records.push(await snapshot(page, "point-campaign-create-after-type-product", index++, { interaction: { selectedProduct } }));

await goto(page, "/admin/retail_portal_integrations/create");
records.push(await snapshot(page, "retail-portal-create-initial", index++));
const storeModalOpened = await clickButtonByText(page, "選択", 0);
records.push(await snapshot(page, "retail-portal-store-location-modal", index++, { interaction: { storeModalOpened } }));
await page.keyboard.press("Escape").catch(() => {});
await page.waitForTimeout(500);
const inventoryModalOpened = await clickButtonByText(page, "選択", 1);
records.push(await snapshot(page, "retail-portal-inventory-location-modal", index++, { interaction: { inventoryModalOpened } }));
await page.keyboard.press("Escape").catch(() => {});

await fs.writeFile(
  path.join(OUT_DIR, "unconfirmed-interactive-readonly-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2),
);

for (const record of records) {
  console.log(`${record.name}: h1=${record.h1.join(" / ")} class=${JSON.stringify(record.classification)}`);
}

await context.close();
