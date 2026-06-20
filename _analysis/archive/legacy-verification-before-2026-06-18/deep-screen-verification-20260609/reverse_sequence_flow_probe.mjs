import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");
const resumeAllocationUrl = process.argv[3] || "";
const runName = resumeAllocationUrl ? "reverse-sequence-resume" : "reverse-sequence";
const SCREEN_DIR = path.join(OUT_DIR, `${runName}-screenshots`);
const RECORDS_FILE = path.join(OUT_DIR, `${runName}-flow-records.json`);
await fs.mkdir(SCREEN_DIR, { recursive: true });

const BASE = "https://www.sqstackstaging.com";
const SKU = "486125-31-L";
const PRODUCT = "オーバーサイズスウェットシャツ";
const SOURCE = "物流倉庫";
const DESTINATION = "ユニクロ - 銀座店";
const QTY = "2";
const INVENTORY_URL =
  "/admin/inventory_items/7505ea2c-71b4-5e57-bb7f-9ddb6ddb7668_InventoryItem?location_id=8b7c4983-7e88-549c-b23a-6fafc2c4d52c_Location";

const records = [];
const consoleLogs = [];
let shotIndex = 1;

function compact(items, limit = 220) {
  return [...new Set(items.map((item) => (item || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(value) {
  return value.replace(/^\/admin\/?/, "").replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 150) || "screen";
}

async function settle(page) {
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(900);
}

async function goto(page, url) {
  await page.goto(`${BASE}${url}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
}

async function bodyText(page) {
  return await page.locator("body").innerText({ timeout: 12000 }).catch(() => "");
}

async function visibleButtonInfo(page, name) {
  const buttons = await page
    .getByRole("button", { name })
    .evaluateAll((els) =>
      els.map((el) => ({
        text: el.textContent?.trim().replace(/\s+/g, " ") || "",
        disabled: el.disabled || el.getAttribute("aria-disabled") === "true",
        ariaDisabled: el.getAttribute("aria-disabled") || "",
      })),
    )
    .catch(() => []);
  return buttons;
}

async function snapshot(page, name, extra = {}) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(shotIndex).padStart(2, "0")}-${slugify(name)}.png`);
  const text = await bodyText(page);
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const record = {
    name,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    dialogs: compact(await page.locator('[role="dialog"]').allInnerTexts().catch(() => []), 40),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => []), 180),
    inputs: await page
      .locator("input, textarea, select")
      .evaluateAll((els) =>
        els.slice(0, 80).map((el) => ({
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute("type") || "",
          placeholder: el.getAttribute("placeholder") || "",
          value: el.value || "",
          ariaLabel: el.getAttribute("aria-label") || "",
          disabled: el.disabled || el.getAttribute("aria-disabled") === "true",
        })),
      )
      .catch(() => []),
    links: await page
      .locator("a")
      .evaluateAll((els) =>
        els
          .map((a) => ({ text: a.textContent?.trim().replace(/\s+/g, " ") || "", href: a.href || "" }))
          .filter((a) => a.text || a.href)
          .slice(0, 220),
      )
      .catch(() => []),
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
          /(在庫|入荷|出荷|移動|#II|#IO|#IM|ステータス|作業|完了|待ち|登録|巻き戻|商品|SKU|数量|ロケーション|物流倉庫|ユニクロ|引当|確保|保存|作成|エラー|予期せぬ|存在しない)/.test(line),
        ),
      300,
    ),
    registerButtons: {
      inbound: await visibleButtonInfo(page, "入荷実績を登録する"),
      outbound: await visibleButtonInfo(page, "出荷実績を登録する"),
      finalRegister: await visibleButtonInfo(page, "登録する"),
    },
    classification: {
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      notFound: text.includes("このページは存在しないようです"),
      empty: text.includes("アイテムが見つかりませんでした"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(
    `${record.name}: h1=${record.h1.join(" / ")} url=${record.url} inboundBtn=${record.registerButtons.inbound.length} outboundBtn=${record.registerButtons.outbound.length}`,
  );
  shotIndex += 1;
  return record;
}

async function clickVisible(locator, label) {
  const count = await locator.count().catch(() => 0);
  for (let index = 0; index < count; index += 1) {
    const item = locator.nth(index);
    if (await item.isVisible().catch(() => false)) {
      await item.click({ timeout: 15000 });
      await settle(item.page());
      return;
    }
  }
  throw new Error(`Could not click visible locator: ${label}`);
}

async function clickButton(page, name, options = {}) {
  const { exact = true, nth = 0, scope = page } = options;
  const locator = scope.getByRole("button", { name, exact }).nth(nth);
  await locator.waitFor({ state: "visible", timeout: 20000 });
  await locator.click({ timeout: 20000 });
  await settle(page);
}

async function clickTextRow(page, text, scope = page) {
  const row = scope.locator("tr, [role=row]").filter({ hasText: text }).first();
  if (await row.isVisible().catch(() => false)) {
    const checkbox = row.locator('input[type="checkbox"], [role="checkbox"]').first();
    if (await checkbox.isVisible().catch(() => false)) {
      await checkbox.click({ force: true });
      await settle(page);
      return;
    }
    await row.click({ force: true });
    await settle(page);
    return;
  }
  await scope.getByText(text, { exact: false }).first().click({ timeout: 20000 });
  await settle(page);
}

async function chooseCurrentDialogRow(page, rowText) {
  const dialog = page.getByRole("dialog").last();
  await dialog.waitFor({ state: "visible", timeout: 20000 });
  await clickTextRow(page, rowText, dialog);
  await clickButton(page, "選択する", { scope: dialog });
}

async function chooseLocationFromField(page, label, rowText) {
  const labelLocator = page.getByText(label, { exact: true }).last();
  await labelLocator.waitFor({ state: "visible", timeout: 20000 });
  const fieldRoot = labelLocator.locator("xpath=ancestor::*[self::div][1]");
  const input = fieldRoot.locator('input[placeholder="選択してください"], input[type="text"]').first();
  if (await input.isVisible().catch(() => false)) {
    await input.click({ timeout: 15000 });
  } else {
    await clickVisible(page.getByRole("button", { name: "選択", exact: true }), `${label} selection button`);
  }
  await settle(page);
  await chooseCurrentDialogRow(page, rowText);
}

async function ensureWarehouseAvailable(page) {
  await goto(page, INVENTORY_URL);
  await snapshot(page, "01-inventory-before-available-adjustment");
  await page.getByRole("button", { name: "販売可能数を編集", exact: true }).nth(1).click({ timeout: 20000 });
  await settle(page);
  await snapshot(page, "02-warehouse-available-dialog-open");
  const dialog = page.getByRole("dialog").last();
  await dialog.waitFor({ state: "visible", timeout: 20000 });
  const textInputs = dialog.locator('input[type="text"], textarea');
  if ((await textInputs.count()) > 0) {
    await textInputs.first().fill(`Codex reverse order check ${new Date().toISOString().slice(0, 10)}`);
  }
  await dialog.locator('input[type="number"]').first().fill(QTY);
  await snapshot(page, "03-warehouse-available-before-save");
  await clickButton(page, "保存する", { scope: dialog });
  await snapshot(page, "04-inventory-after-available-adjustment");
}

async function selectProductVariant(page) {
  await clickButton(page, "選択", { nth: 0 });
  await snapshot(page, "06-product-variant-dialog-open");
  const dialog = page.getByRole("dialog").last();
  const search = dialog.getByLabel("SKUコードで検索する", { exact: true }).first();
  if (await search.isVisible().catch(() => false)) {
    await search.fill(SKU);
    await page.keyboard.press("Enter").catch(() => {});
    await page.waitForTimeout(1200);
  }
  if (!(await dialog.getByText(SKU, { exact: false }).first().isVisible().catch(() => false))) {
    await dialog.getByText(PRODUCT, { exact: false }).first().scrollIntoViewIfNeeded().catch(() => {});
  }
  await clickTextRow(page, SKU, dialog);
  await snapshot(page, "07-product-variant-selected-in-dialog");
  await clickButton(page, "選択する", { scope: dialog });
  await snapshot(page, "08-product-variant-reflected");
}

async function createAllocationRequest(page) {
  await goto(page, "/admin/inventory_allocation_requests/create");
  await snapshot(page, "05-allocation-request-create-open");
  await selectProductVariant(page);
  await page.locator('input[type="number"]').first().fill(QTY);
  await clickButton(page, "選択", { nth: 0 });
  await snapshot(page, "09-destination-location-dialog-open");
  await chooseCurrentDialogRow(page, DESTINATION);
  await snapshot(page, "10-destination-location-reflected");
  await clickButton(page, "選択", { nth: 1 });
  await snapshot(page, "11-request-location-dialog-open");
  await chooseCurrentDialogRow(page, SOURCE);
  await snapshot(page, "12-request-location-reflected");
  await clickButton(page, "保存する", { exact: true, nth: Math.max(0, (await page.getByRole("button", { name: "保存する", exact: true }).count()) - 1) });
  await page.waitForURL(/\/admin\/inventory_allocation_requests\/.+/, { timeout: 60000 }).catch(() => {});
  await settle(page);
  await snapshot(page, "13-allocation-request-created");
}

async function confirmAllocation(page) {
  await clickButton(page, "在庫を引当てる");
  await snapshot(page, "14-allocation-confirm-dialog-open");
  const dialog = page.getByRole("dialog").last();
  await dialog.waitFor({ state: "visible", timeout: 20000 });
  const select = dialog.locator("select").first();
  if (await select.isVisible().catch(() => false)) {
    await select.selectOption({ label: SOURCE }).catch(async () => {
      await select.selectOption({ index: 1 });
    });
    await settle(page);
  }
  const numberInput = dialog.locator('input[type="number"]').first();
  if (await numberInput.isVisible().catch(() => false)) {
    await numberInput.fill(QTY);
  }
  await snapshot(page, "15-allocation-confirm-before-submit");
  await clickButton(page, "引当てる", { scope: dialog });
  await snapshot(page, "16-allocation-confirmed");
}

async function createMovementFromConfirmation(page) {
  await goto(page, "/admin/inventory_allocation_request_confirmations");
  await snapshot(page, "17-confirmations-list-before-movement");
  await clickButton(page, "移動伝票を作成する");
  await snapshot(page, "18-movement-create-dialog-open");
  const dialog = page.getByRole("dialog").last();
  const input = dialog.locator('input[placeholder="選択してください"], input[type="text"]').first();
  if (await input.isVisible().catch(() => false)) {
    await input.click({ timeout: 15000 });
  } else {
    await chooseLocationFromField(page, "移動元", SOURCE);
    return;
  }
  await settle(page);
  await snapshot(page, "19-movement-source-location-dialog-open");
  await chooseCurrentDialogRow(page, SOURCE);
  await snapshot(page, "20-movement-source-reflected");
  await clickButton(page, "実行する", { scope: dialog });
  await snapshot(page, "21-movement-created-toast");
}

function latestLink(links, pattern) {
  return links.find((link) => pattern.test(link.text) && link.href)?.href || "";
}

async function inspectGeneratedMovement(page) {
  await goto(page, "/admin/inventory_movement_orders");
  const list = await snapshot(page, "22-movement-list-after-create");
  const movementHref = latestLink(list.links, /^#IM-\d+$/);
  if (!movementHref) throw new Error("Could not find generated movement link.");
  await page.goto(movementHref, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
  const movement = await snapshot(page, "23-generated-movement-detail-before-any-shipping");
  const outboundHref = latestLink(movement.links, /^#IO-\d+$/);
  const inboundHref = latestLink(movement.links, /^#II-\d+$/);
  if (!outboundHref || !inboundHref) throw new Error(`Missing related links: outbound=${outboundHref} inbound=${inboundHref}`);

  await page.goto(outboundHref, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
  await snapshot(page, "24-generated-outbound-detail-before-inbound");

  await page.goto(inboundHref, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
  await snapshot(page, "25-generated-inbound-detail-before-outbound");
  const inboundRegister = page.getByRole("button", { name: "入荷実績を登録する", exact: true }).first();
  const inboundRegisterVisible = await inboundRegister.isVisible().catch(() => false);
  if (inboundRegisterVisible) {
    await inboundRegister.click({ timeout: 20000 });
    await settle(page);
    await snapshot(page, "26-generated-inbound-register-dialog-before-outbound", {
      note: "Dialog opened only. The final 登録する button was not clicked.",
    });
    const cancel = page.getByRole("button", { name: "キャンセル", exact: true }).last();
    if (await cancel.isVisible().catch(() => false)) {
      await cancel.click().catch(() => {});
      await settle(page);
    }
  }
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
  if (resumeAllocationUrl) {
    await page.goto(resumeAllocationUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
    await settle(page);
    await snapshot(page, "01-resume-allocation-request-detail");
  } else {
    await ensureWarehouseAvailable(page);
    await createAllocationRequest(page);
  }
  await confirmAllocation(page);
  await createMovementFromConfirmation(page);
  await inspectGeneratedMovement(page);
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    RECORDS_FILE,
    JSON.stringify(
      {
        generatedAt: new Date().toISOString(),
        scenario: {
          purpose: "Check whether inbound registration UI is available before outbound completion.",
          sku: SKU,
          quantity: QTY,
          source: SOURCE,
          destination: DESTINATION,
          finalInboundRegisterClicked: false,
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
