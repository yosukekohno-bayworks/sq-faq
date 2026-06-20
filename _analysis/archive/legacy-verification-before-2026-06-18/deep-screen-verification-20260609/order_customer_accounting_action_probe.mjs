import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "order-customer-accounting-action-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const probes = [
  {
    name: "draft-order-create-action",
    url: "https://www.sqstackstaging.com/admin/draft_orders",
    buttonName: "注文を作成する",
  },
  {
    name: "sale-change-line-item-create-action",
    url: "https://www.sqstackstaging.com/admin/sale_change_line_items",
    buttonName: "売上実績を作成する",
  },
  {
    name: "purchasing-customer-import-action",
    url: "https://www.sqstackstaging.com/admin/purchasing_customers",
    buttonName: "インポート",
  },
];

const records = [];
let shotIndex = 1;

function compact(items, limit = 220) {
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
          /(注文|下書き|売上|顧客|インポート|CSV|作成|エラー|予期せぬ|存在しない|アイテムが見つかりません|注文が見つかりません|このページの準備が整いました)/.test(line),
        ),
      260,
    ),
    controls: await page
      .locator("button, a")
      .evaluateAll((els) =>
        els.slice(0, 180).map((el) => ({
          tag: el.tagName.toLowerCase(),
          text: el.textContent?.trim().replace(/\s+/g, " ") || "",
          href: el.href || "",
          ariaDisabled: el.getAttribute("aria-disabled") || "",
          disabled: el.disabled || el.getAttribute("aria-disabled") === "true",
        })),
      )
      .catch(() => []),
    classification: {
      empty: text.includes("アイテムが見つかりませんでした") || text.includes("注文が見つかりませんでした"),
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
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

async function findAction(page, name) {
  const locators = [
    page.getByRole("link", { name, exact: true }),
    page.getByRole("button", { name, exact: true }),
    page.locator("a, button").filter({ hasText: name }),
  ];
  for (const locator of locators) {
    const count = await locator.count().catch(() => 0);
    for (let index = count - 1; index >= 0; index -= 1) {
      const item = locator.nth(index);
      if (await item.isVisible().catch(() => false)) return item;
    }
  }
  return null;
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(25000);

let failed = null;
try {
  for (const probe of probes) {
    await page.goto(probe.url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await settle(page);
    const before = await snapshot(page, `${probe.name}-before`, { buttonName: probe.buttonName });
    const locator = await findAction(page, probe.buttonName);
    const clickable = !!locator;
    if (clickable) {
      await locator.click({ timeout: 12000 }).catch((error) => {
        records.push({ name: `${probe.name}-click-error`, url: page.url(), error: error.message });
      });
      await settle(page, 1400);
    }
    await snapshot(page, `${probe.name}-after-click`, { buttonName: probe.buttonName, beforeUrl: before.url, clickable });
  }
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "order-customer-accounting-action-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), probes, failed, records }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
