import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "inventory-quantities-current-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const targets = {
  inventoryList: "https://www.sqstackstaging.com/admin/inventory_items",
  adjustmentList: "https://www.sqstackstaging.com/admin/inventory_adjustment_orders",
  adjustmentCreate: "https://www.sqstackstaging.com/admin/inventory_adjustment_orders/create",
  movementList: "https://www.sqstackstaging.com/admin/inventory_movement_orders",
  movementCreate: "https://www.sqstackstaging.com/admin/inventory_movement_orders/create",
  reservationList: "https://www.sqstackstaging.com/admin/inventory_reservation_orders",
  reservationCreate: "https://www.sqstackstaging.com/admin/inventory_reservation_orders/create",
};

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

async function settle(page, extraMs = 900) {
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(extraMs);
}

async function goto(page, url) {
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
}

async function getControls(page) {
  return await page
    .locator("button, a, input, select, textarea")
    .evaluateAll((els) =>
      els.slice(0, 320).map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute("type") || "",
          role: el.getAttribute("role") || "",
          text: el.textContent?.trim().replace(/\s+/g, " ") || "",
          ariaLabel: el.getAttribute("aria-label") || "",
          title: el.getAttribute("title") || "",
          href: el.href || "",
          placeholder: el.getAttribute("placeholder") || "",
          value: el.value || "",
          disabled: el.disabled || el.getAttribute("aria-disabled") === "true" || false,
          ariaDisabled: el.getAttribute("aria-disabled") || "",
          bbox: {
            x: Math.round(rect.x),
            y: Math.round(rect.y),
            width: Math.round(rect.width),
            height: Math.round(rect.height),
          },
        };
      }),
    )
    .catch(() => []);
}

async function snapshot(page, name, requestedUrl, extra = {}) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(shotIndex).padStart(2, "0")}-${slugify(name)}.png`);
  const text = await page.locator("body").innerText({ timeout: 12000 }).catch(() => "");
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const controls = await getControls(page);
  const record = {
    name,
    requestedUrl,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    h2: compact(await page.locator("h2").allInnerTexts().catch(() => []), 80),
    dialogs: compact(await page.locator('[role="dialog"]').allInnerTexts().catch(() => []), 80),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 260))
        .catch(() => []),
      260,
    ),
    controls,
    links: controls.filter((control) => control.tag === "a" && control.href).map((control) => ({ text: control.text, href: control.href })),
    selectOptions: await page
      .locator("select")
      .evaluateAll((selects) =>
        selects.slice(0, 40).map((select) => ({
          value: select.value || "",
          options: Array.from(select.options)
            .map((option) => option.textContent?.trim().replace(/\s+/g, " ") || "")
            .filter(Boolean),
        })),
      )
      .catch(() => []),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(在庫|販売不可|確定済み|販売可能|確保済み|破損|検品|予備|手持ち|SKU|486125|TEST_FAQ|物流倉庫|ユニクロ|ロケーション|調整|移動伝票|取置|理由|数量|ステータス|出荷作業|一部受領済み|受領済み|未処理|処理済み|実行|保存|編集|履歴|アイテムが見つかりません|在庫の変更履歴はありません|このページの準備が整いました|予期せぬ|存在しない|エラー)/.test(line),
        ),
      420,
    ),
    classification: {
      empty: text.includes("アイテムが見つかりませんでした"),
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(
    `${record.name}: h1=${record.h1.join(" / ")} url=${record.url} empty=${record.classification.empty} notFound=${record.classification.notFound} unexpected=${record.classification.unexpectedError}`,
  );
  shotIndex += 1;
  return record;
}

function parseInventoryRows(rows) {
  return rows
    .map((row) => {
      const numbers = Array.from(row.matchAll(/-?\d+/g)).map((match) => Number(match[0]));
      return { row, numbers };
    })
    .filter((item) => /486125|物流倉庫|ユニクロ|TEST_FAQ|オーバーサイズ|SKU|販売可能|手持ち/.test(item.row));
}

async function searchInventory(page, query) {
  const inputs = page.locator('input[type="search"], input[placeholder*="検索"], input');
  const count = await inputs.count().catch(() => 0);
  for (let index = 0; index < count; index += 1) {
    const input = inputs.nth(index);
    if (!(await input.isVisible().catch(() => false))) continue;
    const placeholder = await input.getAttribute("placeholder").catch(() => "");
    if (!/検索|SKU|商品|在庫/.test(placeholder) && index > 2) continue;
    await input.fill(query).catch(() => {});
    await page.keyboard.press("Enter").catch(() => {});
    await settle(page, 1500);
    return true;
  }
  return false;
}

async function openFirstInventoryDetail(page) {
  const detailLinks = page.locator('a[href*="/admin/inventory_items/"]').filter({ hasText: /486125|オーバーサイズ|SKU|BEIGE|L/ });
  const count = await detailLinks.count().catch(() => 0);
  for (let index = 0; index < count; index += 1) {
    const link = detailLinks.nth(index);
    const href = await link.getAttribute("href").catch(() => "");
    if (!href || /history|create/.test(href)) continue;
    if (!(await link.isVisible().catch(() => false))) continue;
    await link.click({ timeout: 12000 }).catch(() => {});
    await settle(page, 1500);
    return href;
  }

  const anyLink = page.locator('a[href*="/admin/inventory_items/"]').first();
  if (await anyLink.isVisible().catch(() => false)) {
    const href = await anyLink.getAttribute("href").catch(() => "");
    await anyLink.click({ timeout: 12000 }).catch(() => {});
    await settle(page, 1500);
    return href;
  }
  return null;
}

async function tryOpenAvailableEditDialog(page) {
  const candidates = [
    page.getByRole("button", { name: /販売可能数を編集|販売可能.*編集|編集/ }),
    page.locator('button[aria-label*="販売可能"], button[aria-label*="編集"]'),
  ];
  for (const locator of candidates) {
    const count = await locator.count().catch(() => 0);
    for (let index = 0; index < count; index += 1) {
      const button = locator.nth(index);
      if (!(await button.isVisible().catch(() => false))) continue;
      const disabled = await button.evaluate((el) => el.disabled || el.getAttribute("aria-disabled") === "true").catch(() => true);
      if (disabled) continue;
      await button.click({ timeout: 12000 }).catch(() => {});
      await settle(page, 900);
      const body = await page.locator("body").innerText().catch(() => "");
      if (/販売可能在庫数を編集|理由|数量|保存/.test(body)) return true;
    }
  }
  return false;
}

async function run() {
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
      consoleLogs.push({ type: msg.type(), text: msg.text().slice(0, 2000) });
    }
  });

  page.on("response", async (response) => {
    const url = response.url();
    if (!/graphql|inventory/.test(url) && response.status() < 400) return;
    let body = "";
    if (/graphql|api/.test(url) || response.status() >= 400) {
      body = await response.text().catch(() => "");
    }
    network.push({
      url,
      method: response.request().method(),
      status: response.status(),
      postData: (response.request().postData() || "").slice(0, 5000),
      body: body.slice(0, 12000),
    });
  });

  let failed = null;
  try {
    await goto(page, targets.inventoryList);
    const inventoryList = await snapshot(page, "01-inventory-list", targets.inventoryList);

    await searchInventory(page, "486125-31-L");
    const searched = await snapshot(page, "02-inventory-list-search-486125-31-L", targets.inventoryList, {
      parsedInventoryRows: parseInventoryRows(
        await page
          .locator("tr, [role=row]")
          .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 260))
          .catch(() => []),
      ),
    });

    const openedHref = await openFirstInventoryDetail(page);
    const detail = await snapshot(page, "03-inventory-detail", openedHref || targets.inventoryList, {
      openedHref,
      listParsedInventoryRows: parseInventoryRows(searched.rows || inventoryList.rows || []),
    });

    const editOpened = await tryOpenAvailableEditDialog(page);
    if (editOpened) {
      await snapshot(page, "04-inventory-detail-available-edit-dialog", page.url(), { editOpened });
    }

    const historyLink =
      detail.links.find((link) => /history|履歴/.test(`${link.text} ${link.href}`))?.href ||
      (page.url().endsWith("/history") ? page.url() : `${page.url().replace(/\/$/, "")}/history`);
    await goto(page, historyLink);
    await snapshot(page, "05-inventory-history", historyLink);

    for (const [name, url] of [
      ["06-adjustment-list", targets.adjustmentList],
      ["07-adjustment-create", targets.adjustmentCreate],
      ["08-movement-list", targets.movementList],
      ["09-movement-create", targets.movementCreate],
      ["10-reservation-list", targets.reservationList],
      ["11-reservation-create", targets.reservationCreate],
    ]) {
      await goto(page, url);
      await snapshot(page, name, url);
    }
  } catch (error) {
    failed = { message: error.message, stack: error.stack };
    await snapshot(page, "99-failure-state", page.url(), { failed });
    console.error(error);
  } finally {
    await fs.writeFile(
      path.join(OUT_DIR, "inventory-quantities-current-records.json"),
      JSON.stringify({ generatedAt: new Date().toISOString(), targets, failed, consoleLogs, network, records }, null, 2),
    );
    await context.close().catch(() => {});
  }

  if (failed) process.exitCode = 1;
}

await run();
