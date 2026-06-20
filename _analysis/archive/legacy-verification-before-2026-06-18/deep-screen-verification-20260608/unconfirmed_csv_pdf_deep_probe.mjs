import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-csv-pdf-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const pages = [
  "/admin/csv_import",
  "/admin/csv_import/csv_import_operation_products",
  "/admin/csv_import/csv_import_operation_products/create",
  "/admin/csv_import/csv_import_operation_product_variants",
  "/admin/csv_import/csv_import_operation_product_variants/create",
  "/admin/csv_import/csv_import_operation_inventory_logical_available_quantities",
  "/admin/csv_import/csv_import_operation_inventory_logical_available_quantities/create",
  "/admin/csv_import/csv_import_operation_catalog_products",
  "/admin/csv_import/csv_import_operation_catalog_products/create",
  "/admin/pdf_export",
  "/admin/pdf_export/pdf_export_operation_packing_slips",
];

function compact(items, limit = 120) {
  return [...new Set(items.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(url) {
  return url.replace(/^\/admin\/?/, "").replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 120) || "admin-root";
}

async function snapshot(page, url, index) {
  await page.goto(`https://www.sqstackstaging.com${url}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(900);
  const text = await page.locator("body").innerText().catch((error) => String(error));
  const html = await page.locator("body").evaluate((el) => el.innerHTML).catch(() => "");
  const screenshotFile = path.join(SCREEN_DIR, `${String(index + 1).padStart(2, "0")}-${slugify(url)}.png`);
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});

  const anchors = await page.locator("a").evaluateAll((els) =>
    els.map((a) => ({
      text: a.textContent?.trim() || "",
      href: a.href || "",
      target: a.target || "",
      download: a.getAttribute("download") || "",
    })),
  ).catch(() => []);
  const inputs = await page.locator("input, textarea, select").evaluateAll((els) =>
    els.map((el) => ({
      tag: el.tagName.toLowerCase(),
      type: el.getAttribute("type") || "",
      name: el.getAttribute("name") || "",
      accept: el.getAttribute("accept") || "",
      placeholder: el.getAttribute("placeholder") || "",
      disabled: Boolean(el.disabled),
      value: el.tagName.toLowerCase() === "select"
        ? Array.from(el.options || []).map((o) => o.textContent?.trim()).filter(Boolean).slice(0, 80)
        : "",
    })),
  ).catch(() => []);

  return {
    url,
    finalUrl: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => [])),
    labels: compact(await page.locator("label").allInnerTexts().catch(() => [])),
    anchors: anchors.filter((a) => a.text || a.href).slice(0, 160),
    inputs,
    tableHeaders: compact(await page.locator("th").allInnerTexts().catch(() => [])),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(CSV|PDF|テンプレート|新規インポート|エクスポート|インポート|成功|失敗|完了|作成日|実行ステータス|ダウンロード|アイテムが見つかりません|ファイル|選択してください|保存する)/.test(line),
        ),
      140,
    ),
    flags: {
      empty: text.includes("アイテムが見つかりませんでした"),
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました"),
      hasFileInput: html.includes('type="file"'),
    },
    screenshot: path.relative(ROOT, screenshotFile),
  };
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
  acceptDownloads: true,
});
const page = await context.newPage();
page.setDefaultTimeout(18000);

const records = [];
for (const [index, url] of pages.entries()) {
  const record = await snapshot(page, url, index);
  records.push(record);
  console.log(`${index + 1}/${pages.length} ${url} ${record.h1.join(" / ")} links=${record.anchors.length} file=${record.flags.hasFileInput}`);
}

await fs.writeFile(
  path.join(OUT_DIR, "unconfirmed-csv-pdf-deep-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2),
);

await context.close();
