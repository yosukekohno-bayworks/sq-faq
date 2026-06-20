import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-valid-csv-import-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const fixture = path.join(OUT_DIR, "fixtures/valid-products-recheck.csv");
const productCode = "TEST_FAQ_CSV_RECHECK_20260608_01";
const productTitle = "TEST_FAQ_CSV_RECHECK_20260608_商品";

function compact(lines, limit = 120) {
  return [...new Set(lines.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

async function bodyText(page) {
  return page.locator("body").innerText().catch((error) => String(error));
}

async function shot(page, name) {
  const file = path.join(SCREEN_DIR, `${name}.png`);
  await page.screenshot({ path: file, fullPage: true, animations: "disabled" }).catch(() => {});
  return path.relative(ROOT, file);
}

function important(text) {
  return compact(
    text
      .split(/\n+/)
      .map((line) => line.trim())
      .filter((line) =>
        /(CSV|インポート|商品|テンプレート|新規|作成日|実行ステータス|成功|失敗|完了|処理中|エラー|ファイル|保存|TEST_FAQ_CSV|検証|バリデーション|詳細|ステータス)/.test(line),
      ),
    180,
  );
}

async function extractLinks(page) {
  return page.locator("a").evaluateAll((els) =>
    els.map((a) => ({ text: a.textContent?.trim() || "", href: a.href || "" })).filter((a) => a.text || a.href),
  ).catch(() => []);
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(20000);

const record = {
  generatedAt: new Date().toISOString(),
  fixture: path.relative(ROOT, fixture),
  productCode,
  steps: [],
  detailUrl: null,
  productVisibleAfterImport: false,
  error: null,
};

try {
  await page.goto("https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products/create", { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(900);
  record.steps.push({
    step: "create-before-upload",
    url: page.url(),
    text: important(await bodyText(page)),
    screenshot: await shot(page, "01-create-before-upload"),
  });

  await page.locator('input[type="file"]').setInputFiles(fixture);
  await page.waitForTimeout(900);
  record.steps.push({
    step: "create-file-selected",
    url: page.url(),
    text: important(await bodyText(page)),
    screenshot: await shot(page, "02-create-file-selected"),
  });

  await page.getByRole("button", { name: "保存する", exact: true }).click();
  await page.waitForLoadState("networkidle", { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2500);
  record.steps.push({
    step: "after-submit",
    url: page.url(),
    text: important(await bodyText(page)),
    screenshot: await shot(page, "03-after-submit"),
  });

  await page.goto("https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products", { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(1200);

  let listText = await bodyText(page);
  for (let i = 0; i < 8 && /処理中/.test(listText) && !/失敗|成功/.test(listText); i += 1) {
    await page.waitForTimeout(5000);
    await page.reload({ waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
    listText = await bodyText(page);
  }
  const links = await extractLinks(page);
  const importLinks = links.filter((a) => /CSVImportOperationProduct/.test(a.href));
  record.detailUrl = importLinks[0]?.href || null;
  record.steps.push({
    step: "list-after-submit",
    url: page.url(),
    text: important(listText),
    links: importLinks.slice(0, 6),
    screenshot: await shot(page, "04-list-after-submit"),
  });

  if (record.detailUrl) {
    await page.goto(record.detailUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(1200);
    record.steps.push({
      step: "detail",
      url: page.url(),
      text: important(await bodyText(page)),
      screenshot: await shot(page, "05-detail"),
    });
  }

  await page.goto("https://www.sqstackstaging.com/admin/products", { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(1200);
  const search = page.locator('input[type="search"], input[placeholder*="検索"], input[aria-label*="検索"]').first();
  if (await search.count()) {
    await search.fill(productCode).catch(() => {});
    await page.keyboard.press("Enter").catch(() => {});
    await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(1500);
  }
  const productsText = await bodyText(page);
  record.productVisibleAfterImport = productsText.includes(productCode) || productsText.includes(productTitle);
  record.steps.push({
    step: "products-search",
    url: page.url(),
    text: important(productsText),
    screenshot: await shot(page, "06-products-search"),
  });
} catch (error) {
  record.error = error.message;
  record.steps.push({
    step: "error",
    url: page.url(),
    text: important(await bodyText(page)),
    screenshot: await shot(page, "99-error"),
  });
}

await fs.writeFile(
  path.join(OUT_DIR, "unconfirmed-valid-csv-import-record.json"),
  JSON.stringify(record, null, 2),
);

await context.close();
