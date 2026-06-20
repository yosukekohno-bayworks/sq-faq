import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "success-flow-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.env.SQ_PROFILE_DIR;
if (!profileDir) throw new Error("SQ_PROFILE_DIR is required");

const stamp = new Date().toISOString().replace(/[-:TZ.]/g, "").slice(0, 12);
const prefix = `TEST_FAQ_DEEP_${stamp}`;

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(15000);

function slugify(value) {
  return value.replace(/^\/admin\/?/, "").replace(/[^A-Za-z0-9_-]+/g, "__").slice(0, 140);
}

async function h1() {
  return [
    ...new Set((await page.locator("h1").allInnerTexts().catch(() => [])).map((x) => x.trim()).filter(Boolean)),
  ];
}

async function bodyText() {
  return page.locator("body").innerText().catch((error) => String(error));
}

async function screenshot(name) {
  const file = path.join(SCREEN_DIR, `${name}.png`);
  await page.screenshot({ path: file, fullPage: true, animations: "disabled" }).catch(() => {});
  return path.relative(ROOT, file);
}

async function go(url) {
  await page.goto(`https://www.sqstackstaging.com${url}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(700);
}

async function fill(label, value) {
  await page.getByLabel(label, { exact: true }).first().fill(value);
}

async function select(label, visibleText) {
  await page.getByLabel(label, { exact: true }).first().selectOption({ label: visibleText });
}

async function save(buttonName = "保存する") {
  await page.getByRole("button", { name: buttonName, exact: true }).last().click();
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(1500);
}

async function verifyOnList(listUrl, expectedText) {
  await go(listUrl);
  const text = await bodyText();
  return text.includes(expectedText);
}

const scenarios = [
  {
    id: "supplier",
    name: `${prefix}_取引先`,
    createUrl: "/admin/settings/suppliers/create",
    listUrl: "/admin/settings/suppliers",
    run: async (name) => {
      await fill("取引先名", name);
      await save();
    },
  },
  {
    id: "brand",
    name: `${prefix}_ブランド`,
    createUrl: "/admin/settings/brands/create",
    listUrl: "/admin/settings/brands",
    run: async (name) => {
      await fill("名前", name);
      await fill("コード", `${prefix}_BRAND`.toLowerCase());
      await save();
    },
  },
  {
    id: "catalog",
    name: `${prefix}_カタログ`,
    createUrl: "/admin/catalogs/create",
    listUrl: "/admin/catalogs",
    run: async (name) => {
      await fill("タイトル", name);
      await save();
    },
  },
  {
    id: "product_price_rule",
    name: `${prefix}_販売価格ルール`,
    createUrl: "/admin/product_price_rules/create",
    listUrl: "/admin/product_price_rules",
    run: async (name) => {
      await fill("ルール名", name);
      await select("通貨", "日本円");
      await save();
    },
  },
  {
    id: "back_order_rule",
    name: `${prefix}_予約販売ルール`,
    createUrl: "/admin/inventory_back_order_rules/create",
    listUrl: "/admin/inventory_back_order_rules",
    run: async (name) => {
      await fill("タイトル", name);
      await save();
    },
  },
  {
    id: "threshold_rule",
    name: `${prefix}_販売閾値ルール`,
    createUrl: "/admin/inventory_threshold_rules/create",
    listUrl: "/admin/inventory_threshold_rules",
    run: async (name) => {
      await fill("ルール名", name);
      await save();
    },
  },
  {
    id: "payment_method",
    name: `${prefix}_決済`,
    createUrl: "/admin/settings/payment_methods/create",
    listUrl: "/admin/settings/payment_methods",
    run: async (name) => {
      await fill("名前", name);
      await fill("コード", `${prefix}_payment`.toLowerCase());
      await fill("ゲートウェイ", `${prefix}_gateway`.toLowerCase());
      await save();
    },
  },
  {
    id: "measurement_rule",
    name: `${prefix}_採寸ルール`,
    createUrl: "/admin/settings/product_measurement_rules/create",
    listUrl: "/admin/settings/product_measurement_rules",
    run: async (name) => {
      await fill("ルール名", name);
      await select("採寸単位", "センチメートル");
      await fill("採寸項目1", "肩幅");
      await save();
    },
  },
  {
    id: "product_metafield",
    name: `${prefix}_商品MF`,
    createUrl: "/admin/settings/metafield_definitions/product/create",
    listUrl: "/admin/settings/metafield_definitions/product",
    run: async (name) => {
      await fill("名前", name);
      await fill("説明", "FAQ deep verification");
      await fill("ネームスペース", `${prefix}_ns`.toLowerCase());
      await fill("キー", `${prefix}_key`.toLowerCase());
      await select("メタフィールドのタイプ", "単一行のテキスト");
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
    before: null,
    after: null,
    listContains: false,
    error: null,
    screenshots: [],
  };
  try {
    await go(scenario.createUrl);
    record.before = { url: page.url(), h1: await h1(), textStart: (await bodyText()).slice(0, 1200) };
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${scenario.id}-before`));
    await scenario.run(scenario.name);
    record.after = {
      url: page.url(),
      h1: await h1(),
      textStart: (await bodyText()).slice(0, 1600),
      unexpectedError: (await bodyText()).includes("予期せぬエラーが発生しました"),
    };
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${scenario.id}-after`));
    record.listContains = await verifyOnList(scenario.listUrl, scenario.name);
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${scenario.id}-list`));
  } catch (error) {
    record.error = error.message;
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${scenario.id}-error`));
  }
  records.push(record);
  console.log(`${index + 1}/${scenarios.length} ${scenario.id} list=${record.listContains} error=${record.error ? "yes" : "no"} final=${record.after?.url || ""}`);
}

await fs.writeFile(
  path.join(OUT_DIR, "success-flow-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), prefix, records }, null, 2),
);

await context.close();
