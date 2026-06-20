import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "inventory-available-edit-save-screenshots");
await fs.rm(SCREEN_DIR, { recursive: true, force: true });
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const base = "https://www.sqstackstaging.com";
const itemID = "a1da5885-98b4-5b9b-bcee-891a9c3fd29e_InventoryItem";
const locationName = "物流倉庫";
const sku = "486125-09-XL";
const reason = `TEST_FAQ_Codex確認_${new Date().toISOString().slice(0, 10)}`;
const urls = {
  detail: `${base}/admin/inventory_items/${itemID}?location_id=8b7c4983-7e88-549c-b23a-6fafc2c4d52c_Location`,
  adjustments: `${base}/admin/inventory_adjustment_orders`,
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
  await page.waitForLoadState("networkidle", { timeout: 15000 }).catch(() => {});
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
      els.slice(0, 560).map((el) => {
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
    h2: compact(await page.locator("h2").allInnerTexts().catch(() => []), 100),
    dialogs: compact(await page.locator('[role="dialog"], [role="menu"]').allInnerTexts().catch(() => []), 120),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 360))
        .catch(() => []),
      360,
    ),
    controls,
    links: controls.filter((control) => control.tag === "a" && control.href).map((control) => ({ text: control.text, href: control.href })),
    buttons: controls.filter((control) => control.tag === "button").map((control) => ({ text: control.text, ariaLabel: control.ariaLabel, disabled: control.disabled, visible: control.visible })),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) => /(在庫|販売可能|確定済み|確保済み|破損|検品|予備|手持ち|ロケーション|調整履歴|調整伝票|管理番号|ステータス|実施|未完了|完了|理由|数量|保存|成功|失敗|予期せぬエラー|このページは存在しない|変更履歴|物流倉庫|SKU|486125-09-XL|TEST_FAQ_Codex)/.test(line)),
      560,
    ),
    classification: {
      empty: text.includes("アイテムが見つかりませんでした") || text.includes("在庫の変更履歴はありません"),
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      hasReason: text.includes(reason),
      hasSku: text.includes(sku),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} url=${record.url} empty=${record.classification.empty} reason=${record.classification.hasReason}`);
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

async function openLocationEdit(page) {
  const row = page.locator("tr, [role=row]").filter({ hasText: locationName }).first();
  if (!(await row.isVisible().catch(() => false))) return false;
  const button = row.locator("button").first();
  if (await button.isVisible().catch(() => false)) {
    await button.click({ timeout: 10000 });
    await settle(page, 800);
    return true;
  }
  await row.click({ timeout: 10000 });
  await settle(page, 800);
  return true;
}

async function fillEditDialog(page) {
  const dialog = page.locator('[role="dialog"]').last();
  if (!(await dialog.isVisible().catch(() => false))) return false;
  const inputs = dialog.locator("input");
  await inputs.nth(0).fill(reason);
  await inputs.nth(1).fill("1");
  await settle(page, 300);
  return true;
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
  await goto(page, urls.adjustments);
  await snapshot(page, "adjustment-list-before");

  await goto(page, urls.detail);
  await snapshot(page, "inventory-detail-before");

  const opened = await openLocationEdit(page);
  await snapshot(page, "inventory-edit-dialog-opened", { opened });

  const filled = await fillEditDialog(page);
  await snapshot(page, "inventory-edit-dialog-filled", { opened, filled, reason, quantity: 1 });

  const saved = await clickVisible(page, page.getByRole("button", { name: /保存する|保存$/ }), "save-available-edit");
  await snapshot(page, "inventory-after-save", { opened, filled, saved, reason, quantity: 1 });

  await goto(page, urls.detail);
  await snapshot(page, "inventory-detail-after-reload", { reason });

  const historyClicked = await clickVisible(page, page.getByRole("link", { name: /調整履歴/ }).or(page.getByRole("button", { name: /調整履歴/ })), "open-adjustment-history");
  await snapshot(page, "inventory-history-after", { historyClicked, reason });

  await goto(page, urls.adjustments);
  await snapshot(page, "adjustment-list-after", { reason });
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "inventory-available-edit-save-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), failed, target: { itemID, sku, locationName, reason, urls }, records, network, console: consoleLogs }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
