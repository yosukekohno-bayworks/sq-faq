import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "reverse-sequence-completion-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const targets = {
  movement:
    "https://www.sqstackstaging.com/admin/inventory_movement_orders/f645aa56-f137-5117-9713-aab34d19e0bc_InventoryMovementOrder",
  inbound:
    "https://www.sqstackstaging.com/admin/inventory_inbound_orders/1387f25c-8478-5d3b-8e1e-48951e4c429e_InventoryInboundOrder",
  outbound:
    "https://www.sqstackstaging.com/admin/inventory_outbound_orders/9a7c1300-7218-58b7-ad39-0ec56bd30b13_InventoryOutboundOrder",
  inventory:
    "https://www.sqstackstaging.com/admin/inventory_items/7505ea2c-71b4-5e57-bb7f-9ddb6ddb7668_InventoryItem?location_id=8b7c4983-7e88-549c-b23a-6fafc2c4d52c_Location",
};

const records = [];
const consoleLogs = [];
let shotIndex = 1;

function compact(items, limit = 240) {
  return [...new Set(items.map((item) => (item || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(value) {
  return value.replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 150) || "screen";
}

async function settle(page) {
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(900);
}

async function goto(page, url) {
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
}

async function visibleButtonInfo(page, name) {
  return await page
    .getByRole("button", { name, exact: true })
    .evaluateAll((els) =>
      els.map((el) => ({
        text: el.textContent?.trim().replace(/\s+/g, " ") || "",
        disabled: el.disabled || el.getAttribute("aria-disabled") === "true",
        ariaDisabled: el.getAttribute("aria-disabled") || "",
      })),
    )
    .catch(() => []);
}

async function snapshot(page, name, extra = {}) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(shotIndex).padStart(2, "0")}-${slugify(name)}.png`);
  const text = await page.locator("body").innerText({ timeout: 12000 }).catch(() => "");
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const record = {
    name,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    dialogs: compact(await page.locator('[role="dialog"]').allInnerTexts().catch(() => []), 60),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => []), 200),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 180))
        .catch(() => []),
      180,
    ),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(在庫|入荷|出荷|移動|#II|#IO|#IM|ステータス|作業|完了|待ち|登録|巻き戻|商品|SKU|数量|ロケーション|物流倉庫|ユニクロ|引当|確保|成功|情報|エラー|予期せぬ|存在しない)/.test(line),
        ),
      320,
    ),
    registerButtons: {
      inbound: await visibleButtonInfo(page, "入荷実績を登録する"),
      outbound: await visibleButtonInfo(page, "出荷実績を登録する"),
      finalRegister: await visibleButtonInfo(page, "登録する"),
    },
    classification: {
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      notFound: text.includes("このページは存在しないようです"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(
    `${record.name}: h1=${record.h1.join(" / ")} inbound=${record.registerButtons.inbound.length} outbound=${record.registerButtons.outbound.length} final=${record.registerButtons.finalRegister.length}`,
  );
  shotIndex += 1;
  return record;
}

async function clickButton(page, name, scope = page) {
  const locator = scope.getByRole("button", { name, exact: true }).first();
  await locator.waitFor({ state: "visible", timeout: 20000 });
  await locator.click({ timeout: 20000 });
  await settle(page);
}

async function completeInboundFirst(page) {
  await goto(page, targets.inbound);
  await snapshot(page, "02-inbound-before-reverse-register");
  await clickButton(page, "入荷実績を登録する");
  await snapshot(page, "03-inbound-register-dialog-reverse-order");
  const dialog = page.getByRole("dialog").last();
  await clickButton(page, "登録する", dialog);
  await snapshot(page, "04-inbound-after-reverse-register");
}

async function completeOutboundSecond(page) {
  await goto(page, targets.outbound);
  await snapshot(page, "06-outbound-after-inbound-before-register");
  await clickButton(page, "出荷実績を登録する");
  await snapshot(page, "07-outbound-register-dialog-after-inbound");
  const dialog = page.getByRole("dialog").last();
  await clickButton(page, "登録する", dialog);
  await snapshot(page, "08-outbound-after-register");
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(25000);
page.on("console", (msg) => {
  if (["error", "warning"].includes(msg.type())) {
    consoleLogs.push({ type: msg.type(), text: msg.text() });
  }
});
page.on("pageerror", (error) => {
  consoleLogs.push({ type: "pageerror", text: error.message });
});

let failed = null;
try {
  await goto(page, targets.movement);
  await snapshot(page, "01-movement-before-reverse-completion");
  await completeInboundFirst(page);
  await goto(page, targets.movement);
  await snapshot(page, "05-movement-after-inbound-before-outbound");
  await completeOutboundSecond(page);
  await goto(page, targets.movement);
  await snapshot(page, "09-movement-after-reverse-completion");
  await goto(page, targets.inventory);
  await snapshot(page, "10-inventory-after-reverse-completion");
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "reverse-sequence-completion-records.json"),
    JSON.stringify(
      {
        generatedAt: new Date().toISOString(),
        scenario: {
          purpose: "Complete #II-1002 before #IO-1002, then complete #IO-1002, to verify reverse order behavior.",
          movement: "#IM-1002",
          inbound: "#II-1002",
          outbound: "#IO-1002",
        },
        failed,
        consoleLogs,
        records,
      },
      null,
      2,
    ),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
