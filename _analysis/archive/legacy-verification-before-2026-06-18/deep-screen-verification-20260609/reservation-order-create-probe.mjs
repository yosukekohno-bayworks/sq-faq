import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "reservation-order-create-screenshots");
await fs.rm(SCREEN_DIR, { recursive: true, force: true });
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const base = "https://www.sqstackstaging.com";
const itemID = "a1da5885-98b4-5b9b-bcee-891a9c3fd29e_InventoryItem";
const locationName = "物流倉庫";
const sku = "486125-09-XL";
const productText = "オーバーサイズスウェットシャツ";
const memo = `TEST_FAQ_Codex取置確認_${new Date().toISOString().slice(0, 10)}`;
const urls = {
  inventoryDetail: `${base}/admin/inventory_items/${itemID}?location_id=8b7c4983-7e88-549c-b23a-6fafc2c4d52c_Location`,
  reservationList: `${base}/admin/inventory_reservation_orders`,
  reservationCreate: `${base}/admin/inventory_reservation_orders/create`,
};

const records = [];
const network = [];
const consoleLogs = [];
let shotIndex = 1;

function compact(items, limit = 280) {
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

async function settle(page, extraMs = 900) {
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 18000 }).catch(() => {});
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
      els.slice(0, 620).map((el) => {
        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);
        return {
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute("type") || "",
          role: el.getAttribute("role") || "",
          text: el.textContent?.trim().replace(/\s+/g, " ") || "",
          ariaLabel: el.getAttribute("aria-label") || "",
          title: el.getAttribute("title") || "",
          href: el.href || "",
          placeholder: el.getAttribute("placeholder") || "",
          value: String(el.value || "").slice(0, 500),
          checked: el.checked || false,
          disabled: el.disabled || el.getAttribute("aria-disabled") === "true" || false,
          visible: style.visibility !== "hidden" && style.display !== "none" && rect.width > 0 && rect.height > 0,
        };
      }),
    )
    .catch(() => []);
}

async function snapshot(page, name, extra = {}) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(shotIndex).padStart(2, "0")}-${slugify(name)}.png`);
  const text = await page.locator("body").innerText({ timeout: 12000 }).catch(() => "");
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const controls = await getControls(page);
  const record = {
    name,
    url: page.url(),
    title: await page.title().catch(() => ""),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => []), 30),
    dialogs: compact(await page.locator('[role="dialog"], [role="menu"]').allInnerTexts().catch(() => []), 140),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 400))
        .catch(() => []),
      400,
    ),
    controls,
    links: controls.filter((control) => control.tag === "a" && control.href).map((control) => ({ text: control.text, href: control.href })),
    buttons: controls.filter((control) => control.tag === "button").map((control) => ({ text: control.text, ariaLabel: control.ariaLabel, disabled: control.disabled, visible: control.visible })),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) => /(取置|在庫|販売可能|確保済み|手持ち|確定済み|ロケーション|物流倉庫|商品|SKU|486125-09-XL|数量|メモ|保存|参照|選択|未処理|処理済み|ステータス|成功|失敗|予期せぬエラー|このページは存在しない|TEST_FAQ_Codex)/.test(line)),
      620,
    ),
    classification: {
      empty: text.includes("アイテムが見つかりませんでした"),
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      hasSku: text.includes(sku),
      hasMemo: text.includes(memo),
      hasLocation: text.includes(locationName),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} url=${record.url} empty=${record.classification.empty} sku=${record.classification.hasSku}`);
  shotIndex += 1;
  return record;
}

async function clickVisible(page, locator, label) {
  const target = locator.first();
  if (!(await target.isVisible().catch(() => false))) return false;
  await target.click({ timeout: 10000 });
  await settle(page, 900);
  console.log(`clicked: ${label}`);
  return true;
}

async function selectFromDialog(page, text, label) {
  const dialog = page.locator('[role="dialog"]').last();
  if (!(await dialog.isVisible().catch(() => false))) return false;
  const search = dialog.getByPlaceholder(/検索|コード|名前|商品/).first();
  if (await search.isVisible().catch(() => false)) {
    await search.fill(text);
    await settle(page, 1200);
  }
  const row = dialog.locator("tr, [role=row]").filter({ hasText: text }).first();
  if (await row.isVisible().catch(() => false)) {
    const checkbox = row.locator('input[type="checkbox"]').first();
    if (await checkbox.isVisible().catch(() => false)) {
      await checkbox.check({ timeout: 10000 }).catch(async () => checkbox.click({ timeout: 10000 }));
    } else {
      await row.click({ timeout: 10000 });
    }
    await settle(page, 600);
  } else {
    const textNode = dialog.getByText(text, { exact: false }).first();
    if (await textNode.isVisible().catch(() => false)) {
      await textNode.click({ timeout: 10000 });
      await settle(page, 600);
    }
  }
  const confirmed = await clickVisible(page, dialog.getByRole("button", { name: /選択する|追加する|選択/ }), `confirm-${label}`);
  return confirmed || !(await dialog.isVisible().catch(() => false));
}

async function fillCreateForm(page) {
  const textarea = page.locator("textarea").first();
  if (await textarea.isVisible().catch(() => false)) {
    await textarea.fill(memo);
  }
  const numericInputs = await page
    .locator('input[type="number"], input')
    .evaluateAll((inputs) =>
      inputs.map((input, index) => ({
        index,
        type: input.getAttribute("type") || "",
        value: input.value || "",
        placeholder: input.getAttribute("placeholder") || "",
        visible: input.offsetWidth > 0 && input.offsetHeight > 0,
      })),
    )
    .catch(() => []);
  for (const input of numericInputs.filter((candidate) => candidate.visible)) {
    if (input.type === "number" || /数量|個数/.test(input.placeholder)) {
      await page.locator('input[type="number"], input').nth(input.index).fill("1").catch(() => {});
    }
  }
  await settle(page, 500);
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
    postData: isClerk || rawPostData.includes("__session") ? "" : rawPostData.slice(0, 1800),
  });
});

let failed = null;
try {
  await goto(page, urls.inventoryDetail);
  await snapshot(page, "inventory-detail-before-reservation");

  await goto(page, urls.reservationList);
  await snapshot(page, "reservation-list-before");

  await goto(page, urls.reservationCreate);
  await snapshot(page, "reservation-create-initial");

  const locationOpened = await clickVisible(page, page.getByRole("button", { name: /選択/ }).first(), "open-location-picker");
  await snapshot(page, "reservation-location-picker-opened", { locationOpened });
  const locationSelected = await selectFromDialog(page, locationName, "location");
  await snapshot(page, "reservation-location-selected", { locationOpened, locationSelected });

  const productOpened = await clickVisible(page, page.getByRole("button", { name: /参照|選択/ }).last(), "open-product-picker");
  await snapshot(page, "reservation-product-picker-opened", { locationSelected, productOpened });
  const productSelected = await selectFromDialog(page, sku, "product");
  if (!productSelected) await selectFromDialog(page, productText, "product-fallback");
  await snapshot(page, "reservation-product-selected", { locationSelected, productOpened, productSelected });

  await fillCreateForm(page);
  await snapshot(page, "reservation-form-filled", { locationSelected, productSelected, memo, quantity: 1 });

  const saved = await clickVisible(page, page.getByRole("button", { name: /保存する|保存$/ }), "save-reservation");
  await snapshot(page, "reservation-after-save", { locationSelected, productSelected, saved, memo, quantity: 1 });

  await goto(page, urls.reservationList);
  await snapshot(page, "reservation-list-after", { memo });

  await goto(page, urls.inventoryDetail);
  await snapshot(page, "inventory-detail-after-reservation", { memo });
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "reservation-order-create-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), failed, target: { itemID, sku, locationName, memo, urls }, records, network, console: consoleLogs }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
