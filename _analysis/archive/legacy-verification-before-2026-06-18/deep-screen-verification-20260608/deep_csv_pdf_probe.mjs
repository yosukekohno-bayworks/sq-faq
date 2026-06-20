import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "csv-pdf-screenshots");
const FIXTURE_DIR = path.join(OUT_DIR, "fixtures");
await fs.mkdir(SCREEN_DIR, { recursive: true });
await fs.mkdir(FIXTURE_DIR, { recursive: true });

const invalidCsv = path.join(FIXTURE_DIR, "invalid-products.csv");
await fs.writeFile(invalidCsv, "this,is,not,a,valid,sq,product,csv\n1,2,3,4,5,6,7,8\n", "utf8");

const profileDir = process.env.SQ_PROFILE_DIR;
if (!profileDir) throw new Error("SQ_PROFILE_DIR is required");

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
  acceptDownloads: true,
});
const page = await context.newPage();
page.setDefaultTimeout(18000);

async function go(url) {
  await page.goto(`https://www.sqstackstaging.com${url}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(900);
}

async function h1() {
  return [...new Set((await page.locator("h1").allInnerTexts().catch(() => [])).map((x) => x.trim()).filter(Boolean))];
}

async function bodyText() {
  return page.locator("body").innerText().catch((error) => String(error));
}

async function screenshot(name) {
  const file = path.join(SCREEN_DIR, `${name}.png`);
  await page.screenshot({ path: file, fullPage: true, animations: "disabled" }).catch(() => {});
  return path.relative(ROOT, file);
}

async function fill(label, value) {
  await page.getByLabel(label, { exact: true }).first().fill(value);
}

async function select(label, visibleText) {
  await page.getByLabel(label, { exact: true }).first().selectOption({ label: visibleText });
}

function importantLines(text) {
  return [
    ...new Set(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(成功|失敗|検証|実行|エクスポート|インポート|アイテムが見つかりません|入力してください|選択してください|CSV|PDF|テンプレート|エラー|ダウンロード)/.test(line),
        ),
    ),
  ].slice(0, 100);
}

const scenarios = [
  {
    id: "sale_changes_export",
    url: "/admin/csv_export/csv_export_operation_sale_changes/create",
    listUrl: "/admin/csv_export/csv_export_operation_sale_changes",
    run: async () => {
      await select("テナント", "ユニクロ");
      await fill("開始日時", "2026-06-01T00:00");
      await fill("終了日時", "2026-06-08T23:59");
      await page.getByRole("button", { name: "エクスポートを開始する", exact: true }).click();
    },
  },
  {
    id: "point_changes_export",
    url: "/admin/csv_export/csv_export_operation_point_changes/create",
    listUrl: "/admin/csv_export/csv_export_operation_point_changes",
    run: async () => {
      await select("テナント", "ユニクロ");
      await fill("開始日時", "2026-06-01T00:00");
      await fill("終了日時", "2026-06-08T23:59");
      await page.getByRole("button", { name: "エクスポートを開始する", exact: true }).click();
    },
  },
  {
    id: "yamato_b2_conditional_export",
    url: "/admin/inventory_outbound_orders/export/yamato_b2_cloud",
    listUrl: "/admin/inventory_outbound_orders",
    run: async () => {
      await fill("開始日時", "2026-06-01T00:00");
      await fill("終了日時", "2026-06-08T23:59");
      await page.getByRole("button", { name: "実行する", exact: true }).click();
    },
  },
  {
    id: "invalid_product_import",
    url: "/admin/csv_import/csv_import_operation_products/create",
    listUrl: "/admin/csv_import/csv_import_operation_products",
    run: async () => {
      await page.locator('input[type="file"]').setInputFiles(invalidCsv);
      await page.getByRole("button", { name: "保存する", exact: true }).click();
    },
  },
];

const records = [];
for (const [index, scenario] of scenarios.entries()) {
  const record = {
    index: index + 1,
    id: scenario.id,
    url: scenario.url,
    listUrl: scenario.listUrl,
    before: null,
    after: null,
    list: null,
    error: null,
    screenshots: [],
  };
  try {
    await go(scenario.url);
    record.before = { url: page.url(), h1: await h1(), textStart: (await bodyText()).slice(0, 1400) };
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${scenario.id}-before`));
    await scenario.run();
    await page.waitForLoadState("networkidle", { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(2500);
    const afterText = await bodyText();
    record.after = {
      url: page.url(),
      h1: await h1(),
      importantLines: importantLines(afterText),
      textStart: afterText.slice(0, 2000),
      notFound: afterText.includes("このページは存在しないようです"),
      unexpectedError: afterText.includes("予期せぬエラーが発生しました"),
    };
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${scenario.id}-after`));
    await go(scenario.listUrl);
    const listText = await bodyText();
    record.list = {
      url: page.url(),
      h1: await h1(),
      importantLines: importantLines(listText),
      textStart: listText.slice(0, 2000),
    };
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${scenario.id}-list`));
  } catch (error) {
    record.error = error.message;
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${scenario.id}-error`));
  }
  records.push(record);
  console.log(`${index + 1}/${scenarios.length} ${scenario.id} error=${record.error ? "yes" : "no"} after=${record.after?.url || ""}`);
}

await fs.writeFile(
  path.join(OUT_DIR, "csv-pdf-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), invalidCsv: path.relative(ROOT, invalidCsv), records }, null, 2),
);

await context.close();
