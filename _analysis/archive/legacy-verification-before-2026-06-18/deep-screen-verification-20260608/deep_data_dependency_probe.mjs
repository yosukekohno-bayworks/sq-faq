import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "data-dependency-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.env.SQ_PROFILE_DIR;
if (!profileDir) throw new Error("SQ_PROFILE_DIR is required");

const retry = JSON.parse(await fs.readFile(path.join(OUT_DIR, "retry-flow-records.json"), "utf8"));
const complex = JSON.parse(await fs.readFile(path.join(OUT_DIR, "complex-success-flow-records.json"), "utf8"));
const newCompanyUrl = new URL(retry.records.find((r) => r.id === "company_retry")?.after?.url || "https://www.sqstackstaging.com/admin/companies").pathname;
const newProductUrl = new URL(complex.records.find((r) => r.id === "product")?.after?.url || "https://www.sqstackstaging.com/admin/products").pathname;

const urls = [
  "/admin/purchasing_customers",
  "/admin/purchasing_customers/create",
  "/admin/draft_orders",
  "/admin/draft_orders/create",
  "/admin/orders",
  "/admin/order_returns",
  "/admin/order_returns/create",
  "/admin/sale_change_line_items",
  "/admin/sale_change_line_items/create",
  "/admin/companies",
  newCompanyUrl,
  "/admin/products",
  newProductUrl,
];

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(15000);

function slugify(value) {
  return value.replace(/^\/admin\/?/, "").replace(/[^A-Za-z0-9_-]+/g, "__").slice(0, 140) || "admin";
}

async function compactTexts(selector, limit = 100) {
  return [
    ...new Set((await page.locator(selector).allInnerTexts().catch(() => [])).map((x) => x.trim()).filter(Boolean)),
  ].slice(0, limit);
}

async function capture(url, index) {
  await page.goto(`https://www.sqstackstaging.com${url}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(900);
  const text = await page.locator("body").innerText().catch((error) => String(error));
  const links = await page
    .locator("a")
    .evaluateAll((els) =>
      els.slice(0, 160).map((a) => ({
        text: a.textContent?.trim() || "",
        href: a.getAttribute("href"),
        className: a.getAttribute("class") || "",
        ariaDisabled: a.getAttribute("aria-disabled") || "",
        pointerEvents: getComputedStyle(a).pointerEvents,
      })),
    )
    .catch(() => []);
  const buttons = await page
    .locator("button")
    .evaluateAll((els) =>
      els.slice(0, 160).map((button) => ({
        text: button.textContent?.trim() || "",
        disabled: button.disabled,
        className: button.getAttribute("class") || "",
      })),
    )
    .catch(() => []);
  const file = path.join(SCREEN_DIR, `${String(index).padStart(2, "0")}-${slugify(url)}.png`);
  await page.screenshot({ path: file, fullPage: true, animations: "disabled" }).catch(() => {});
  return {
    index,
    url,
    finalUrl: page.url(),
    title: await page.title().catch(() => ""),
    h1: await compactTexts("h1"),
    h2: await compactTexts("h2"),
    notFound: text.includes("このページは存在しないようです"),
    unexpectedError: text.includes("予期せぬエラーが発生しました"),
    empty: text.includes("アイテムが見つかりませんでした"),
    createLikeLinks: links.filter((l) => /作成|追加|登録/.test(l.text) || /create/.test(l.href || "")),
    primaryButtons: buttons.filter((b) => /作成|追加|保存|実行|戻る/.test(b.text) || b.className.includes("Primary")),
    textStart: text.slice(0, 2500),
    screenshot: path.relative(ROOT, file),
  };
}

const records = [];
for (const [index, url] of urls.entries()) {
  const record = await capture(url, index + 1);
  records.push(record);
  console.log(`${index + 1}/${urls.length} ${url} h1=${record.h1.join(" / ")} empty=${record.empty} nf=${record.notFound} ue=${record.unexpectedError}`);
}

await fs.writeFile(
  path.join(OUT_DIR, "data-dependency-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), newCompanyUrl, newProductUrl, records }, null, 2),
);

await context.close();
