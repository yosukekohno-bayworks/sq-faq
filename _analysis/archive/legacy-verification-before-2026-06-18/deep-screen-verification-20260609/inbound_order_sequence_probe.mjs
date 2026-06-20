import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "inbound-order-sequence-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const BASE = "https://www.sqstackstaging.com";

function compact(items, limit = 220) {
  return [...new Set(items.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(value) {
  return value.replace(/^\/admin\/?/, "").replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 150) || "admin-root";
}

async function goto(page, url) {
  await page.goto(`${BASE}${url}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(1000);
}

async function snapshot(page, name, index, extra = {}) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(index).padStart(2, "0")}-${slugify(name)}.png`);
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const text = await page.locator("body").innerText().catch(() => "");
  const rows = await page.locator("tr, [role=row]").evaluateAll((els) =>
    els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 180),
  ).catch(() => []);
  return {
    name,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => []), 180),
    links: await page.locator("a").evaluateAll((els) =>
      els.map((a) => ({ text: a.textContent?.trim().replace(/\s+/g, " ") || "", href: a.href || "" })).filter((a) => a.text || a.href).slice(0, 220),
    ).catch(() => []),
    rows: compact(rows, 180),
    hasInboundRegisterButton: text.includes("入荷実績を登録する"),
    hasOutboundRegisterButton: text.includes("出荷実績を登録する"),
    hasRollbackWarning: text.includes("巻き戻すことができません") || text.includes("巻き戻せません"),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) => /(入荷|出荷|移動|#II|#IO|#IM|ステータス|作業|完了|待ち|登録|巻き戻|商品|SKU|数量|ロケーション|アイテムが見つかりません|予期せぬ|存在しない)/.test(line)),
      260,
    ),
    classification: {
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      notFound: text.includes("このページは存在しないようです"),
      empty: text.includes("アイテムが見つかりませんでした"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
}

async function clickText(page, text) {
  const exactLink = page.getByRole("link", { name: text, exact: true }).first();
  if (await exactLink.isVisible().catch(() => false)) {
    await exactLink.click();
    await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
    await page.waitForTimeout(900);
    return "link";
  }
  const row = page.locator(`text=${text}`).first();
  if (await row.isVisible().catch(() => false)) {
    await row.click().catch(() => {});
    await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
    await page.waitForTimeout(900);
    return "text";
  }
  return "";
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

await goto(page, "/admin/inventory_inbound_orders");
records.push(await snapshot(page, "inbound-list", index++));
const inboundClick = await clickText(page, "#II-1001");
records.push(await snapshot(page, "inbound-II-1001-after-click", index++, { interaction: { inboundClick } }));

await goto(page, "/admin/inventory_outbound_orders");
records.push(await snapshot(page, "outbound-list", index++));
const outboundClick = await clickText(page, "#IO-1001");
records.push(await snapshot(page, "outbound-IO-1001-after-click", index++, { interaction: { outboundClick } }));

await goto(page, "/admin/inventory_movement_orders");
records.push(await snapshot(page, "movement-list", index++));
const movementClick = await clickText(page, "#IM-1001");
records.push(await snapshot(page, "movement-IM-1001-after-click", index++, { interaction: { movementClick } }));

await fs.writeFile(
  path.join(OUT_DIR, "inbound-order-sequence-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2),
);

for (const record of records) {
  console.log(
    `${record.name}: h1=${record.h1.join(" / ")} inboundBtn=${record.hasInboundRegisterButton} outboundBtn=${record.hasOutboundRegisterButton} class=${JSON.stringify(record.classification)}`,
  );
}

await context.close();
