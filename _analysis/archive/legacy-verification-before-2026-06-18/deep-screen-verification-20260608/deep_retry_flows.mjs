import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "retry-flow-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.env.SQ_PROFILE_DIR;
if (!profileDir) throw new Error("SQ_PROFILE_DIR is required");

const stamp = new Date().toISOString().replace(/[-:TZ.]/g, "").slice(0, 12);
const prefix = `TEST_FAQ_DEEP3_${stamp}`;
const startDate = "2026-06-08T00:00";
const endDate = "2026-12-31T23:59";

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(18000);

async function go(url) {
  await page.goto(`https://www.sqstackstaging.com${url}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(800);
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

async function save(buttonName = "保存する") {
  await page.getByRole("button", { name: buttonName, exact: true }).last().click();
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(1800);
}

async function verifyOnList(url, expected) {
  await go(url);
  return (await bodyText()).includes(expected);
}

function validationLines(text) {
  return [
    ...new Set(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) => /(入力してください|選択してください|追加してください|エラー|しばらくして|GraphQL|形式|対象|ポイント倍率)/.test(line)),
    ),
  ].slice(0, 80);
}

const scenarios = [
  {
    id: "company_retry",
    name: `${prefix}_会社`,
    createUrl: "/admin/companies/create",
    listUrl: "/admin/companies",
    run: async (name) => {
      await fill("会社名", name);
      await fill("会社ID", `${prefix}_company`.toLowerCase());
      await fill("ロケーション名", `${name}_ロケーション`);
      await fill("ロケーションID", `${prefix}_company_loc`.toLowerCase());
      await fill("コード", `${prefix}_codeloc`.toLowerCase());
      await select("国/地域", "日本");
      await fill("性", "検証");
      await fill("名", "太郎");
      await fill("会社", name);
      await fill("郵便番号", "100-0001");
      await select("都道府県", "東京都");
      await fill("市区町村", "千代田区");
      await fill("住所", "千代田1-1");
      await page.getByRole("checkbox", { name: "配送先住所と同じ", exact: true }).check().catch(() => {});
      await save();
    },
  },
  {
    id: "discount_retry",
    name: `${prefix}_ディスカウント`,
    createUrl: "/admin/order_price_adjustment_rules/create",
    listUrl: "/admin/order_price_adjustment_rules",
    run: async (name) => {
      await fill("タイトル", name);
      await fill("説明文", "FAQ deep verification discount retry");
      await fill("クーポンコード", `${prefix}_DISC`.replace(/_/g, "-"));
      await select("テナント", "ユニクロ");
      await select("割引方法", "割引率");
      const numbers = page.locator('input[type="number"]');
      await numbers.nth(0).fill("10");
      await numbers.nth(1).fill("1000");
      await page.getByRole("checkbox", { name: "すべての商品を割引対象に設定する", exact: true }).check();
      await fill("開始日時", startDate);
      await fill("終了日時", endDate);
      await save();
    },
  },
  {
    id: "point_campaign_retry",
    name: `${prefix}_ポイントCP`,
    createUrl: "/admin/point_campaign_order_rules/create",
    listUrl: "/admin/point_campaign_order_rules",
    run: async (name) => {
      await fill("タイトル", name);
      await fill("開始日時", startDate);
      await fill("終了日時", endDate);
      await select("ポイントキャンペーン種別", "なし");
      await page.locator('input[type="number"]').first().fill("3");
      await select("対象の注文ポイント付与ルール", "TEST_FAQ_注文ポイント付与ルール");
      await save();
    },
  },
];

const records = [];
for (const [index, scenario] of scenarios.entries()) {
  const record = {
    index: index + 1,
    id: scenario.id,
    name: scenario.name,
    createUrl: scenario.createUrl,
    listUrl: scenario.listUrl,
    after: null,
    listContains: false,
    validationLines: [],
    error: null,
    screenshots: [],
  };
  try {
    await go(scenario.createUrl);
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${scenario.id}-before`));
    await scenario.run(scenario.name);
    const text = await bodyText();
    record.after = {
      url: page.url(),
      h1: await h1(),
      textStart: text.slice(0, 1800),
      unexpectedError: text.includes("予期せぬエラーが発生しました"),
    };
    record.validationLines = validationLines(text);
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${scenario.id}-after`));
    record.listContains = await verifyOnList(scenario.listUrl, scenario.name);
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${scenario.id}-list`));
  } catch (error) {
    record.error = error.message;
    record.validationLines = validationLines(await bodyText());
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${scenario.id}-error`));
  }
  records.push(record);
  console.log(`${index + 1}/${scenarios.length} ${scenario.id} list=${record.listContains} error=${record.error ? "yes" : "no"} final=${record.after?.url || ""}`);
}

await fs.writeFile(
  path.join(OUT_DIR, "retry-flow-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), prefix, records }, null, 2),
);

await context.close();
