import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "purchase-order-submit-retry-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.env.SQ_PROFILE_DIR;
if (!profileDir) throw new Error("SQ_PROFILE_DIR is required");

const success = JSON.parse(await fs.readFile(path.join(OUT_DIR, "success-flow-records.json"), "utf8"));
const supplier = success.records.find((r) => r.id === "supplier")?.name || "TEST_FAQ_Supplier2";

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(20000);

const consoleMessages = [];
page.on("console", (msg) => {
  if (["error", "warning"].includes(msg.type())) {
    consoleMessages.push(`${msg.type()}: ${msg.text()}`.slice(0, 1600));
  }
});

async function bodyText() {
  return page.locator("body").innerText().catch((error) => String(error));
}

async function screenshot(name) {
  const file = path.join(SCREEN_DIR, `${name}.png`);
  await page.screenshot({ path: file, fullPage: true, animations: "disabled" }).catch(() => {});
  return path.relative(ROOT, file);
}

function important(text) {
  return [
    ...new Set(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(エラー|GraphQL|unknown field|商品|取引先|テナント|通貨|数量|金額|単価|作成|選択|486125|オーバーサイズ|TEST_FAQ|しばらくして|InventoryPurchaseOrder)/.test(line),
        ),
    ),
  ].slice(0, 140);
}

const record = {
  supplier,
  attemptedSku: "486125-31-L",
  steps: [],
  final: null,
  error: null,
  consoleMessages,
};

try {
  await page.goto("https://www.sqstackstaging.com/admin/inventory_purchase_orders/create", { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(900);

  await page.getByLabel("取引先", { exact: true }).selectOption({ label: supplier });
  await page.getByLabel("テナント", { exact: true }).selectOption({ label: "ユニクロ" });
  await page.getByLabel("通貨", { exact: true }).selectOption({ label: "日本円" });
  record.steps.push({ step: "header-selected", screenshot: await screenshot("01-header-selected"), text: important(await bodyText()) });

  await page.locator('input[placeholder="商品を検索する"]').first().fill("486125-31-L");
  await page.waitForTimeout(1200);
  record.steps.push({ step: "searched", screenshot: await screenshot("02-searched"), text: important(await bodyText()) });

  const row = page.locator("tr").filter({ hasText: "486125-31-L" }).first();
  await row.locator('input[type="checkbox"]').first().check({ force: true });
  record.steps.push({ step: "row-checked", screenshot: await screenshot("03-row-checked"), text: important(await bodyText()) });

  await page.getByRole("button", { name: "選択する", exact: true }).last().click();
  await page.waitForTimeout(1200);
  record.steps.push({ step: "variant-selected", screenshot: await screenshot("04-variant-selected"), text: important(await bodyText()) });

  const numberInputs = page.locator('input[type="number"]');
  const count = await numberInputs.count();
  for (let i = 0; i < count; i += 1) {
    const input = numberInputs.nth(i);
    const current = await input.inputValue().catch(() => "");
    if (!current || current === "0") {
      await input.fill(i === 0 ? "1" : "3600").catch(() => {});
    }
  }
  record.steps.push({ step: "numbers-filled", screenshot: await screenshot("05-numbers-filled"), text: important(await bodyText()) });

  await page.getByRole("button", { name: "作成する", exact: true }).click();
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(3000);
  const text = await bodyText();
  record.final = {
    url: page.url(),
    screenshot: await screenshot("06-after-submit"),
    text: important(text),
    unexpectedError: text.includes("予期せぬエラーが発生しました"),
    visibleError: /エラー|しばらくして|GraphQL|unknown field/.test(text),
  };
} catch (error) {
  record.error = error.message;
  record.steps.push({ step: "error", screenshot: await screenshot("99-error"), text: important(await bodyText()) });
}

await fs.writeFile(
  path.join(OUT_DIR, "purchase-order-submit-retry-record.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), record }, null, 2),
);

await context.close();
