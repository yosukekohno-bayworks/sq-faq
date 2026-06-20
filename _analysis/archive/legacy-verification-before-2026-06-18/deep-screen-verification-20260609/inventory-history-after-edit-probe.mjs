import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "inventory-history-after-edit-screenshots");
await fs.rm(SCREEN_DIR, { recursive: true, force: true });
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const base = "https://www.sqstackstaging.com";
const itemID = "a1da5885-98b4-5b9b-bcee-891a9c3fd29e_InventoryItem";
const urls = [
  { name: "history-target-location-8b7", url: `${base}/admin/inventory_items/${itemID}/history?location_id=8b7c4983-7e88-549c-b23a-6fafc2c4d52c_Location` },
  { name: "history-clicked-location-b9f", url: `${base}/admin/inventory_items/${itemID}/history?location_id=b9f67abc-3da0-5165-953b-ea304a92460b_Location` },
  { name: "detail-after-edit", url: `${base}/admin/inventory_items/${itemID}?location_id=8b7c4983-7e88-549c-b23a-6fafc2c4d52c_Location` },
];

const records = [];
const network = [];
const consoleLogs = [];
let shotIndex = 1;

function compact(items, limit = 260) {
  return [...new Set(items.map((item) => (item || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(value) {
  return value.replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 140) || "screen";
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

async function settle(page, extraMs = 3500) {
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 18000 }).catch(() => {});
  await page.waitForTimeout(extraMs);
}

async function snapshot(page, name) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(shotIndex).padStart(2, "0")}-${slugify(name)}.png`);
  const text = await page.locator("body").innerText({ timeout: 12000 }).catch(() => "");
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const record = {
    name,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => []), 30),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 360))
        .catch(() => []),
      360,
    ),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) => /(在庫|変更履歴|調整履歴|物流倉庫|販売可能|手持ち|理由|数量|TEST_FAQ_Codex|486125-09-XL|このページは存在しない|予期せぬエラー|アイテムが見つかりません|履歴はありません)/.test(line)),
      520,
    ),
    classification: {
      skeletonOnly: !text.trim() || text.trim().length < 40,
      emptyHistory: text.includes("在庫の変更履歴はありません"),
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      hasReason: text.includes("TEST_FAQ_Codex"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
  };
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} skeleton=${record.classification.skeletonOnly} emptyHistory=${record.classification.emptyHistory} reason=${record.classification.hasReason}`);
  shotIndex += 1;
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  locale: "ja-JP",
  timezoneId: "Asia/Tokyo",
});

const page = context.pages()[0] || (await context.newPage());
page.setDefaultTimeout(25000);

page.on("console", (message) => {
  if (["error", "warning"].includes(message.type())) consoleLogs.push({ type: message.type(), text: message.text().slice(0, 1200) });
});

page.on("response", async (response) => {
  const url = response.url();
  let hostname = "";
  try {
    hostname = new URL(url).hostname;
  } catch {}
  const isClerk = hostname.includes("clerk");
  const isNextStatic = url.includes("/_next/static/");
  const isVercelInsight = url.includes("/_vercel/insights/");
  const shouldTrack = /\/api\/graphql|\/admin\/inventory/.test(url) || (response.status() >= 400 && !isClerk && !isNextStatic && !isVercelInsight);
  if (!shouldTrack) return;
  const rawPostData = response.request().postData() || "";
  network.push({
    status: response.status(),
    url: safeUrl(url),
    method: response.request().method(),
    postData: isClerk || rawPostData.includes("__session") ? "" : rawPostData.slice(0, 1600),
  });
});

let failed = null;
try {
  for (const target of urls) {
    await page.goto(target.url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await settle(page);
    await snapshot(page, target.name);
  }
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state");
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "inventory-history-after-edit-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), failed, targets: urls, records, network, console: consoleLogs }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
