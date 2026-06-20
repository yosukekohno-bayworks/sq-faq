import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "purchase-order-current-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const targets = {
  create: "https://www.sqstackstaging.com/admin/inventory_purchase_orders/create",
  list: "https://www.sqstackstaging.com/admin/inventory_purchase_orders",
  inbound: "https://www.sqstackstaging.com/admin/inventory_inbound_orders",
};

const records = [];
const network = [];
const consoleLogs = [];
let shotIndex = 1;

function compact(items, limit = 220) {
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
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(extraMs);
}

async function goto(page, url) {
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
}

async function snapshot(page, name, extra = {}) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(shotIndex).padStart(2, "0")}-${slugify(name)}.png`);
  const text = await page.locator("body").innerText({ timeout: 12000 }).catch(() => "");
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const record = {
    name,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(発注|入荷|取引先|テナント|通貨|商品|単価|数量|金額|作成|保存|選択|486125|オーバーサイズ|エラー|成功|GraphQL|unknown field|しばらく|アイテムが見つかりません|このページの準備が整いました)/.test(line),
        ),
      280,
    ),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 220))
        .catch(() => []),
      220,
    ),
    controls: await page
      .locator("button, a, input, select, textarea")
      .evaluateAll((els) =>
        els.slice(0, 240).map((el) => ({
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute("type") || "",
          text: el.textContent?.trim().replace(/\s+/g, " ") || "",
          ariaLabel: el.getAttribute("aria-label") || "",
          placeholder: el.getAttribute("placeholder") || "",
          value: el.value || "",
          disabled: el.disabled || el.getAttribute("aria-disabled") === "true",
        })),
      )
      .catch(() => []),
    classification: {
      visibleError: /エラー|しばらくして|GraphQL|unknown field/.test(text),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      empty: text.includes("アイテムが見つかりませんでした"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} url=${record.url} error=${record.classification.visibleError}`);
  shotIndex += 1;
  return record;
}

async function selectByPreferredLabel(page, label, preferred) {
  const select = page.getByLabel(label, { exact: true });
  const options = await select.locator("option").evaluateAll((els) =>
    els.map((el, index) => ({ index, label: el.textContent?.trim() || "", value: el.value || "" })),
  );
  const chosen =
    preferred.map((needle) => options.find((option) => option.label.includes(needle))).find(Boolean) ||
    options.find((option) => option.label && !option.label.includes("選択してください")) ||
    options[0];
  if (!chosen) throw new Error(`No option found for ${label}`);
  await select.selectOption({ index: chosen.index });
  return chosen;
}

async function fillPurchaseOrder(page) {
  await goto(page, targets.create);
  await snapshot(page, "01-purchase-order-create-open");

  const supplier = await selectByPreferredLabel(page, "取引先", ["TEST_FAQ_DEEP", "TEST_FAQ_Supplier2", "TEST_FAQ_Supplier"]);
  const tenant = await selectByPreferredLabel(page, "テナント", ["ユニクロ"]);
  const currency = await selectByPreferredLabel(page, "通貨", ["日本円"]);
  await settle(page);
  await snapshot(page, "02-purchase-order-header-selected", { selected: { supplier, tenant, currency } });

  const search = page.locator('input[placeholder="商品を検索する"]').first();
  if (!(await search.isVisible().catch(() => false))) {
    await page.getByRole("button", { name: /商品を追加する/ }).click({ timeout: 15000 }).catch(() => {});
    await settle(page);
  }
  await page.locator('input[placeholder="商品を検索する"]').first().fill("486125-31-L");
  await page.waitForTimeout(1400);
  await snapshot(page, "03-purchase-order-variant-search");

  const row = page.locator("tr").filter({ hasText: "486125-31-L" }).first();
  await row.locator('input[type="checkbox"]').first().check({ force: true });
  await snapshot(page, "04-purchase-order-variant-checked");

  await page.getByRole("button", { name: "選択する", exact: true }).last().click();
  await settle(page);
  await snapshot(page, "05-purchase-order-variant-selected");

  const editableNumbers = page.locator('input[type="number"]:not([disabled])');
  const count = await editableNumbers.count().catch(() => 0);
  const filled = [];
  for (let index = 0; index < count; index += 1) {
    const input = editableNumbers.nth(index);
    const value = index === 0 ? "100" : "1";
    await input.fill(value).catch(() => {});
    filled.push({ index, value });
  }
  await settle(page);
  await snapshot(page, "06-purchase-order-numbers-filled", { filled });

  const beforeUrl = page.url();
  await page.getByRole("button", { name: "作成する", exact: true }).click({ timeout: 20000 });
  await settle(page, 3500);
  await snapshot(page, "07-purchase-order-after-submit", { beforeUrl });
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
    consoleLogs.push({ type: msg.type(), text: msg.text().slice(0, 2000) });
  }
});
page.on("response", async (response) => {
  const request = response.request();
  const url = response.url();
  let hostname = "";
  try {
    hostname = new URL(url).hostname;
  } catch {}
  const isClerk = hostname.includes("clerk");
  const isNextStatic = url.includes("/_next/static/");
  const isVercelInsight = url.includes("/_vercel/insights/");
  const shouldTrack = /\/api\/graphql|\/admin\/inventory_purchase_orders/.test(url) || (response.status() >= 400 && !isClerk && !isNextStatic && !isVercelInsight);
  if (!shouldTrack) return;
  let body = "";
  if (!isClerk && !isNextStatic && !isVercelInsight && (/\/api\/graphql/.test(url) || response.status() >= 400)) {
    body = await response.text().catch(() => "");
  }
  const rawPostData = request.postData() || "";
  network.push({
    url: safeUrl(url),
    method: request.method(),
    status: response.status(),
    postData: isClerk || rawPostData.includes("__session") ? "" : rawPostData.slice(0, 5000),
    body: body.slice(0, 8000),
  });
});

let failed = null;
try {
  await fillPurchaseOrder(page);
  await goto(page, targets.list);
  await snapshot(page, "08-purchase-order-list-after-submit");
  await goto(page, targets.inbound);
  await snapshot(page, "09-inbound-list-after-purchase-order-submit");
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "purchase-order-current-behavior-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), targets, failed, consoleLogs, network, records }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
