import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "inventory-quantities-exact-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const targets = {
  inventoryList: "https://www.sqstackstaging.com/admin/inventory_items",
  exactDetail:
    "https://www.sqstackstaging.com/admin/inventory_items/7505ea2c-71b4-5e57-bb7f-9ddb6ddb7668_InventoryItem",
};

const records = [];
const graphql = [];
let shotIndex = 1;

function simplifyInventoryItemNode(node, locationID) {
  return {
    locationID,
    id: node.id,
    sku: node.sku,
    product: node.productVariant?.product?.title || "",
    title: node.productVariant?.title || "",
    quantity: node.inventoryLevel?.quantity || null,
  };
}

function findInventoryLevels(value, acc = []) {
  if (!value || typeof value !== "object") return acc;
  if (value.inventoryLevel?.quantity) {
    acc.push({
      name: value.name || value.title || value.id || "",
      code: value.code || "",
      id: value.id || "",
      quantity: value.inventoryLevel.quantity,
    });
  }
  for (const child of Object.values(value)) {
    if (Array.isArray(child)) child.forEach((item) => findInventoryLevels(item, acc));
    else if (child && typeof child === "object") findInventoryLevels(child, acc);
  }
  return acc;
}

async function settle(page, extraMs = 900) {
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(extraMs);
}

function slugify(value) {
  return value.replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 140) || "screen";
}

async function snapshot(page, name) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(shotIndex).padStart(2, "0")}-${slugify(name)}.png`);
  const text = await page.locator("body").innerText({ timeout: 12000 }).catch(() => "");
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const record = {
    name,
    url: page.url(),
    h1: await page.locator("h1").allInnerTexts().catch(() => []),
    rows: await page
      .locator("tr, [role=row]")
      .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 80))
      .catch(() => []),
    importantLines: text
      .split(/\n+/)
      .map((line) => line.trim())
      .filter((line) => /(販売不可|確定済み|販売可能|確保済み|破損|検品|予備|手持ち|486125|物流倉庫|ユニクロ|SKU|ロケーション)/.test(line))
      .slice(0, 160),
    screenshot: path.relative(ROOT, screenshotFile),
  };
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} url=${record.url}`);
  shotIndex += 1;
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(25000);

page.on("response", async (response) => {
  if (!response.url().includes("/api/graphql")) return;
  const request = response.request();
  const postData = request.postData() || "";
  if (!/InventoryItemsPage|InventoryItemPage/.test(postData)) return;
  const requestJson = JSON.parse(postData);
  const body = await response.json().catch(() => null);
  if (!body) return;

  if (requestJson.operationName === "InventoryItemsPage") {
    const nodes = body.data?.inventoryItems?.nodes || [];
    graphql.push({
      operationName: requestJson.operationName,
      variables: requestJson.variables,
      matchingItems: nodes.filter((node) => /486125/.test(node.sku || "")).map((node) => simplifyInventoryItemNode(node, requestJson.variables.locationID)),
    });
  }

  if (requestJson.operationName === "InventoryItemPage") {
    graphql.push({
      operationName: requestJson.operationName,
      variables: requestJson.variables,
      inventoryItem: {
        id: body.data?.inventoryItem?.id || "",
        sku: body.data?.inventoryItem?.sku || "",
        product: body.data?.inventoryItem?.productVariant?.product?.title || "",
        title: body.data?.inventoryItem?.productVariant?.title || "",
      },
      locationQuantities: findInventoryLevels(body.data),
    });
  }
});

let failed = null;
try {
  await page.goto(targets.inventoryList, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
  await snapshot(page, "01-inventory-list");

  await page.goto(targets.exactDetail, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
  await snapshot(page, "02-exact-486125-31-L-detail");
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "inventory-quantities-exact-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), targets, failed, graphql, records }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
