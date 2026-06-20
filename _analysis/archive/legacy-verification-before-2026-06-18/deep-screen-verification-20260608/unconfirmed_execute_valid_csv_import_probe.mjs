import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-execute-valid-csv-import-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const previous = JSON.parse(await fs.readFile(path.join(OUT_DIR, "unconfirmed-valid-csv-import-record.json"), "utf8"));
const detailUrl = previous.detailUrl;
const productCode = previous.productCode;
const productTitle = "TEST_FAQ_CSV_RECHECK_20260608_商品";
if (!detailUrl) throw new Error("No detailUrl in previous record.");

function compact(lines, limit = 180) {
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
        /(CSV|インポート|商品|検証|実行|成功|失敗|完了|未実行|処理中|エラー|0個|1個|作成日|ステータス|TEST_FAQ|商品管理|商品コード|検索|アイテムが見つかりません)/.test(line),
      ),
    220,
  );
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
  detailUrl,
  productCode,
  steps: [],
  productVisibleAfterExecution: false,
  error: null,
};

try {
  await page.goto(detailUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(1000);
  record.steps.push({ step: "before-execute", url: page.url(), text: important(await bodyText(page)), screenshot: await shot(page, "01-before-execute") });

  await page.getByRole("button", { name: "実行する", exact: true }).click();
  await page.waitForLoadState("networkidle", { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2500);
  record.steps.push({ step: "after-click-execute", url: page.url(), text: important(await bodyText(page)), screenshot: await shot(page, "02-after-click-execute") });

  const modalText = await bodyText(page);
  if (modalText.includes("CSVの取り込み処理を実行しますか？")) {
    await page.getByRole("button", { name: "実行する", exact: true }).last().click();
    await page.waitForLoadState("networkidle", { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(2500);
    record.steps.push({ step: "after-confirm-execute", url: page.url(), text: important(await bodyText(page)), screenshot: await shot(page, "025-after-confirm-execute") });
  }

  let detailText = await bodyText(page);
  for (let i = 0; i < 12 && !/実行ステータス[\s\S]*(成功|失敗|完了)/.test(detailText); i += 1) {
    await page.waitForTimeout(5000);
    await page.reload({ waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
    detailText = await bodyText(page);
  }
  record.steps.push({ step: "detail-after-poll", url: page.url(), text: important(detailText), screenshot: await shot(page, "03-detail-after-poll") });

  await page.goto("https://www.sqstackstaging.com/admin/products", { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(1200);
  const search = page.locator('input[type="search"], input[placeholder*="検索"], input[aria-label*="検索"]').first();
  if (await search.count()) {
    await search.fill(productCode).catch(() => {});
    await page.keyboard.press("Enter").catch(() => {});
    await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(1800);
  }
  const productsText = await bodyText(page);
  record.productVisibleAfterExecution = productsText.includes(productCode) || productsText.includes(productTitle);
  record.steps.push({ step: "products-search-after-execute", url: page.url(), text: important(productsText), screenshot: await shot(page, "04-products-search-after-execute") });
} catch (error) {
  record.error = error.message;
  record.steps.push({ step: "error", url: page.url(), text: important(await bodyText(page)), screenshot: await shot(page, "99-error") });
}

await fs.writeFile(path.join(OUT_DIR, "unconfirmed-execute-valid-csv-import-record.json"), JSON.stringify(record, null, 2));
await context.close();
