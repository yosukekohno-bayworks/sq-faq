import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "linked-inbound-outbound-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const targets = [
  {
    name: "outbound-IO-1001-direct",
    url: "https://www.sqstackstaging.com/admin/inventory_outbound_orders/b6e0aaf1-8c54-58f8-9ee8-6cebc84e80bb_InventoryOutboundOrder",
  },
  {
    name: "inbound-II-1001-direct",
    url: "https://www.sqstackstaging.com/admin/inventory_inbound_orders/6e9b70ed-dde6-53a1-a46b-cbd45cfafafa_InventoryInboundOrder",
  },
];

function compact(items, limit = 220) {
  return [...new Set(items.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

async function snapshot(page, target, index) {
  await page.goto(target.url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(1000);
  const text = await page.locator("body").innerText().catch(() => "");
  const screenshotFile = path.join(SCREEN_DIR, `${String(index).padStart(2, "0")}-${target.name}.png`);
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  return {
    name: target.name,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => []), 180),
    rows: compact(await page.locator("tr, [role=row]").evaluateAll((els) =>
      els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 180),
    ).catch(() => []), 180),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) => /(入荷|出荷|#II|#IO|#IM|ステータス|作業|完了|待ち|登録|巻き戻|商品|SKU|数量|ロケーション|配送|到着|引当|実績|外部|予期せぬ|存在しない)/.test(line)),
      280,
    ),
    hasInboundRegisterButton: text.includes("入荷実績を登録する"),
    hasOutboundRegisterButton: text.includes("出荷実績を登録する"),
    hasRollbackWarning: text.includes("巻き戻すことができません") || text.includes("巻き戻せません"),
    classification: {
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      notFound: text.includes("このページは存在しないようです"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
  };
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
for (const target of targets) {
  const record = await snapshot(page, target, index++);
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} inboundBtn=${record.hasInboundRegisterButton} outboundBtn=${record.hasOutboundRegisterButton} class=${JSON.stringify(record.classification)}`);
}

await fs.writeFile(
  path.join(OUT_DIR, "linked-inbound-outbound-detail-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2),
);

await context.close();
