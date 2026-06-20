import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "order-customer-accounting-current-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const targets = [
  { name: "orders-list", url: "https://www.sqstackstaging.com/admin/orders" },
  { name: "orders-create-direct", url: "https://www.sqstackstaging.com/admin/orders/create" },
  { name: "draft-orders-list", url: "https://www.sqstackstaging.com/admin/draft_orders" },
  { name: "draft-orders-create-direct", url: "https://www.sqstackstaging.com/admin/draft_orders/create" },
  { name: "order-returns-list", url: "https://www.sqstackstaging.com/admin/order_returns" },
  { name: "order-returns-create-direct", url: "https://www.sqstackstaging.com/admin/order_returns/create" },
  { name: "purchasing-customers-list", url: "https://www.sqstackstaging.com/admin/purchasing_customers" },
  { name: "purchasing-customers-create-direct", url: "https://www.sqstackstaging.com/admin/purchasing_customers/create" },
  { name: "sale-change-line-items-list", url: "https://www.sqstackstaging.com/admin/sale_change_line_items" },
  { name: "sale-change-line-items-create-direct", url: "https://www.sqstackstaging.com/admin/sale_change_line_items/create" },
];

const records = [];
const network = [];
const consoleLogs = [];
let shotIndex = 1;

function compact(items, limit = 240) {
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

async function getControls(page) {
  return await page
    .locator("button, a, input, select, textarea")
    .evaluateAll((els) =>
      els.slice(0, 260).map((el) => {
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
          disabled: el.disabled || el.getAttribute("aria-disabled") === "true",
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
    title: await page.title().catch(() => ""),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 220))
        .catch(() => []),
      220,
    ),
    controls,
    primaryActions: controls.filter((control) =>
      /(作成|追加|返品|返金|注文|売上|顧客|エクスポート|インポート|保存|登録|キャンセル|詳細|表示)/.test(
        `${control.text} ${control.ariaLabel} ${control.title} ${control.href}`,
      ),
    ),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(注文|下書き|返品|返金|顧客|会社|売上|会計|購入|ポイント|作成|追加|登録|詳細|CSV|エクスポート|インポート|アイテムが見つかりません|注文が見つかりません|顧客が見つかりません|予期せぬエラー|このページは存在しない|このページの準備が整いました|Application error|404|エラー|disabled|無効)/.test(line),
        ),
      320,
    ),
    classification: {
      empty: text.includes("アイテムが見つかりませんでした") || text.includes("注文が見つかりませんでした") || text.includes("顧客が見つかりませんでした"),
      notFound: text.includes("このページは存在しないようです") || /404/.test(text),
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
  if (!/graphql|orders|order_returns|purchasing_customers|sale_change_line_items|draft_orders/.test(url) && response.status() < 400) return;
  let body = "";
  if (/graphql|api/.test(url) || response.status() >= 400) {
    body = await response.text().catch(() => "");
  }
  network.push({
    url,
    method: response.request().method(),
    status: response.status(),
    postData: (response.request().postData() || "").slice(0, 5000),
    body: body.slice(0, 8000),
  });
});

let failed = null;
try {
  for (const target of targets) {
    await page.goto(target.url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await settle(page);
    const record = await snapshot(page, target.name, target.url);

    const candidateRows = record.rows.filter((row) => /#|注文|顧客|売上|返品|Draft|Order/.test(row));
    const candidateLinks = record.controls.filter(
      (control) =>
        control.tag === "a" &&
        control.href &&
        /(orders|order_returns|purchasing_customers|sale_change_line_items|draft_orders)\/[^/?#]+/.test(control.href) &&
        !/\/create$/.test(control.href),
    );
    if (candidateRows.length || candidateLinks.length) {
      await snapshot(page, `${target.name}-data-candidates`, target.url, { candidateRows, candidateLinks });
    }
  }
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", page.url(), { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "order-customer-accounting-current-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), targets, failed, consoleLogs, network, records }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
