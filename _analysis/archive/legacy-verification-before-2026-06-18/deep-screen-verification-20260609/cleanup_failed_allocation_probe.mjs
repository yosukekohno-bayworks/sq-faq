import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "cleanup-failed-allocation-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const target =
  "https://www.sqstackstaging.com/admin/inventory_allocation_requests/0ed61436-77db-5f97-a45d-80fe5ddfea7d_InventoryAllocationRequest";
const records = [];
let shotIndex = 1;

function compact(items, limit = 180) {
  return [...new Set(items.map((item) => (item || "").trim()).filter(Boolean))].slice(0, limit);
}

async function settle(page) {
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(900);
}

async function snapshot(page, name, extra = {}) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(shotIndex).padStart(2, "0")}-${name}.png`);
  const text = await page.locator("body").innerText({ timeout: 12000 }).catch(() => "");
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const record = {
    name,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    dialogs: compact(await page.locator('[role="dialog"]').allInnerTexts().catch(() => []), 40),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => []), 120),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) => /(在庫依頼|確認待ち|終了|クローズ|実行|未完了|SKU|物流倉庫|ユニクロ|ロケーション|作成|完了|エラー)/.test(line)),
      220,
    ),
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} url=${record.url}`);
  shotIndex += 1;
}

async function clickFirstVisible(page, locator, label) {
  const count = await locator.count().catch(() => 0);
  for (let index = 0; index < count; index += 1) {
    const item = locator.nth(index);
    if (await item.isVisible().catch(() => false)) {
      await item.click({ timeout: 15000 });
      await settle(page);
      return;
    }
  }
  throw new Error(`Could not click ${label}`);
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(25000);

let failed = null;
try {
  await page.goto(target, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
  await snapshot(page, "01-before-close");
  const text = await page.locator("body").innerText().catch(() => "");
  if (!text.includes("終了")) {
    await page.getByRole("button", { name: "その他の操作", exact: true }).click();
    await settle(page);
    await snapshot(page, "02-actions-open");
    await clickFirstVisible(page, page.getByText(/クローズ|終了/), "close action");
    await snapshot(page, "03-close-dialog");
    await page.getByRole("button", { name: "実行する", exact: true }).last().click();
    await settle(page);
    await snapshot(page, "04-after-close");
  }
  await page.goto("https://www.sqstackstaging.com/admin/inventory_allocation_requests", {
    waitUntil: "domcontentloaded",
    timeout: 60000,
  });
  await settle(page);
  await snapshot(page, "05-allocation-list-after-cleanup");
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "cleanup-failed-allocation-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), failed, records }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
