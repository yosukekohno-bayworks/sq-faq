import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "form-validation-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const scenarios = [
  ["/admin/products/create", "保存する"],
  ["/admin/catalogs/create", "保存する"],
  ["/admin/companies/create", "保存する"],
  ["/admin/settings/suppliers/create", "保存する"],
  ["/admin/inventory_purchase_orders/create", "作成する"],
  ["/admin/inventory_allocation_requests/create", "保存する"],
  ["/admin/inventory_movement_orders/create", "保存する"],
  ["/admin/inventory_adjustment_orders/create", "保存する"],
  ["/admin/product_price_rules/create", "保存する"],
  ["/admin/inventory_back_order_rules/create", "保存する"],
  ["/admin/inventory_sale_limit_rules/create", "保存する"],
  ["/admin/inventory_threshold_rules/create", "保存する"],
  ["/admin/local_pickup_retail_location_rules/create", "保存する"],
  ["/admin/order_price_adjustment_rules/create", "保存する"],
  ["/admin/point_calculation_birthday_rules/create", "保存する"],
  ["/admin/point_campaign_order_rules/create", "保存する"],
  ["/admin/point_expiration_notification_rule/create", "保存する"],
  ["/admin/point_application_excluded_products/create", "保存する"],
  ["/admin/settings/brands/create", "保存する"],
  ["/admin/settings/location_groups/create", "保存する"],
  ["/admin/settings/locations/create", "保存する"],
  ["/admin/settings/metafield_definitions/product/create", "保存する"],
  ["/admin/settings/payment_methods/create", "保存する"],
  ["/admin/settings/permission_groups/create", "作成する"],
  ["/admin/settings/product_measurement_rules/create", "保存する"],
  ["/admin/settings/retail_staff_members/create", "保存する"],
  ["/admin/settings/users/create", "保存する"],
  ["/admin/recustomer_integrations/create", "保存する"],
  ["/admin/retail_portal_integrations/create", "保存する"],
  ["/admin/omnibus_core_integrations/create", "保存する"],
  ["/admin/shopify_integrations/create", "連携する"],
  ["/admin/smaregi_integrations/create", "保存する"],
];

const profileDir = process.env.SQ_PROFILE_DIR;
if (!profileDir) throw new Error("SQ_PROFILE_DIR is required");

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(15000);

function slugify(url) {
  return url.replace(/^\/admin\/?/, "").replace(/[^A-Za-z0-9_-]+/g, "__").slice(0, 140);
}

function relevantLines(text) {
  return [...new Set(
    text
      .split(/\n+/)
      .map((line) => line.trim())
      .filter((line) =>
        /(入力してください|選択してください|追加してください|アップロードしてください|1つ以上|必須|エラー|有効な|設定してください|required|invalid)/i.test(line),
      ),
  )].slice(0, 80);
}

async function compactTexts(selector, limit = 100) {
  return [
    ...new Set(
      (await page.locator(selector).allInnerTexts().catch(() => []))
        .map((x) => x.trim())
        .filter(Boolean),
    ),
  ].slice(0, limit);
}

const records = [];
for (const [index, [url, buttonName]] of scenarios.entries()) {
  const fullUrl = `https://www.sqstackstaging.com${url}`;
  let clickError = null;
  await page.goto(fullUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(700);

  const beforeUrl = page.url();
  const beforeH1 = await compactTexts("h1");
  try {
    await page.getByRole("button", { name: buttonName, exact: true }).last().click({ timeout: 8000 });
  } catch (error) {
    clickError = error.message;
  }
  await page.waitForLoadState("networkidle", { timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(1000);

  const body = await page.locator("body").innerText().catch((error) => String(error));
  const file = path.join(SCREEN_DIR, `${String(index + 1).padStart(2, "0")}-${slugify(url)}.png`);
  await page.screenshot({ path: file, fullPage: true, animations: "disabled" }).catch(() => {});
  const record = {
    index: index + 1,
    url,
    buttonName,
    beforeUrl,
    finalUrl: page.url(),
    h1: beforeH1,
    clickError,
    stayedOnForm: page.url() === beforeUrl,
    unexpectedError: body.includes("予期せぬエラーが発生しました"),
    notFound: body.includes("このページは存在しないようです"),
    validationLines: relevantLines(body),
    labels: await compactTexts("label", 120),
    buttons: await compactTexts("button", 80),
    textStart: body.slice(0, 1800),
    screenshot: path.relative(ROOT, file),
  };
  records.push(record);
  console.log(`${index + 1}/${scenarios.length} ${url} click=${buttonName} stayed=${record.stayedOnForm} errors=${record.validationLines.length}`);
}

await fs.writeFile(
  path.join(OUT_DIR, "form-validation-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2),
);

await context.close();
