import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-product-search-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const queries = [
  "TEST_FAQ_CSV_RECHECK_20260608_01",
  "TEST_FAQ_CSV_RECHECK_20260608_商品",
  "test_faq_csv_recheck_20260608_01",
];

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
        /(商品管理|インポート|商品を作成|商品|ステータス|商品コード|TEST_FAQ|CSV_RECHECK|アイテムが見つかりません|検索|絞り込み|下書き|公開中|アーカイブ)/.test(line),
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
page.setDefaultTimeout(16000);

const record = { generatedAt: new Date().toISOString(), queries, steps: [], found: false, error: null };

try {
  await page.goto("https://www.sqstackstaging.com/admin/products", { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(1000);
  record.steps.push({
    step: "initial",
    url: page.url(),
    text: important(await bodyText(page)),
    buttons: await page.locator("button").evaluateAll((els) => els.map((b) => ({
      text: b.textContent?.trim() || "",
      aria: b.getAttribute("aria-label") || "",
      title: b.getAttribute("title") || "",
      disabled: Boolean(b.disabled),
    }))).catch(() => []),
    inputs: await page.locator("input").evaluateAll((els) => els.map((i) => ({
      type: i.getAttribute("type") || "",
      placeholder: i.getAttribute("placeholder") || "",
      aria: i.getAttribute("aria-label") || "",
      value: i.value || "",
    }))).catch(() => []),
    screenshot: await shot(page, "01-initial"),
  });

  const searchButton = page.getByRole("button", { name: /検索|絞り込み/ }).first();
  if (await searchButton.count()) {
    await searchButton.click();
    await page.waitForTimeout(800);
    record.steps.push({
      step: "after-open-search",
      url: page.url(),
      text: important(await bodyText(page)),
      inputs: await page.locator("input").evaluateAll((els) => els.map((i) => ({
        type: i.getAttribute("type") || "",
        placeholder: i.getAttribute("placeholder") || "",
        aria: i.getAttribute("aria-label") || "",
        value: i.value || "",
      }))).catch(() => []),
      screenshot: await shot(page, "02-after-open-search"),
    });
  }

  for (const [index, query] of queries.entries()) {
    const input = page.locator('input[type="search"], input[placeholder*="検索"], input[aria-label*="検索"], input').last();
    if (await input.count()) {
      await input.fill(query).catch(() => {});
      await page.keyboard.press("Enter").catch(() => {});
      await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
      await page.waitForTimeout(1500);
    }
    const text = await bodyText(page);
    const found = text.includes("TEST_FAQ_CSV_RECHECK_20260608_01") || text.includes("TEST_FAQ_CSV_RECHECK_20260608_商品") || text.includes("test_faq_csv_recheck_20260608_01");
    record.found = record.found || found;
    record.steps.push({ step: `search-${index + 1}`, query, url: page.url(), found, text: important(text), screenshot: await shot(page, `0${index + 3}-search-${index + 1}`) });
  }
} catch (error) {
  record.error = error.message;
  record.steps.push({ step: "error", url: page.url(), text: important(await bodyText(page)), screenshot: await shot(page, "99-error") });
}

await fs.writeFile(path.join(OUT_DIR, "unconfirmed-product-search-record.json"), JSON.stringify(record, null, 2));
await context.close();
