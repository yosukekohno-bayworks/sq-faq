import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-recheck-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const candidateProfiles = process.argv.slice(2);
if (candidateProfiles.length === 0) {
  throw new Error("Pass at least one Chrome profile directory.");
}

const targetUrls = [
  "/admin/orders",
  "/admin/order_returns",
  "/admin/purchasing_customers",
  "/admin/draft_orders",
  "/admin/sale_change_line_items",
  "/admin/inventory_purchase_orders",
  "/admin/inventory_purchase_orders/create",
  "/admin/inventory_inbound_orders",
  "/admin/pdf_export/pdf_export_operation_packing_slips",
  "/admin/shopify_integrations/create",
  "/admin/smaregi_integrations/create",
  "/admin/omnibus_core_integrations/create",
  "/admin/recustomer_integrations/create",
  "/admin/retail_portal_integrations/create",
  "/admin/settings/permission_groups",
  "/admin/settings/users/create",
];

function compact(items, limit = 80) {
  return [...new Set(items.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(url) {
  return url
    .replace(/^\/admin\/?/, "")
    .replace(/[^A-Za-z0-9_-]+/g, "__")
    .replace(/^_+|_+$/g, "")
    .slice(0, 120) || "admin-root";
}

async function extract(page, url, index) {
  const fullUrl = `https://www.sqstackstaging.com${url}`;
  const errors = [];
  page.removeAllListeners("console");
  page.on("console", (msg) => {
    if (["error", "warning"].includes(msg.type())) {
      errors.push(`${msg.type()}: ${msg.text()}`.slice(0, 400));
    }
  });

  let responseStatus = null;
  let gotoError = null;
  try {
    const response = await page.goto(fullUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
    responseStatus = response?.status() ?? null;
    await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(800);
  } catch (error) {
    gotoError = error.message;
  }

  const text = await page.locator("body").innerText().catch((error) => String(error));
  const h1 = compact(await page.locator("h1").allInnerTexts().catch(() => []));
  const h2 = compact(await page.locator("h2").allInnerTexts().catch(() => []));
  const buttons = compact(await page.locator("button").allInnerTexts().catch(() => []), 100);
  const links = compact(await page.locator("a").allInnerTexts().catch(() => []), 100);
  const labels = compact(await page.locator("label").allInnerTexts().catch(() => []), 140);
  const file = path.join(SCREEN_DIR, `${String(index + 1).padStart(2, "0")}-${slugify(url)}.png`);
  let screenshot = null;
  try {
    await page.screenshot({ path: file, fullPage: true, animations: "disabled" });
    screenshot = path.relative(ROOT, file);
  } catch (error) {
    screenshot = `screenshot-error: ${error.message}`;
  }

  return {
    index: index + 1,
    url,
    finalUrl: page.url(),
    responseStatus,
    gotoError,
    h1,
    h2,
    classification: {
      login: /ログイン|メールアドレス|パスワード/.test(text),
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました"),
      empty: text.includes("アイテムが見つかりませんでした") || text.includes("注文が見つかりませんでした"),
      disabledCreate: /作成する/.test(text) && /Polaris-Button--disabled/.test(await page.locator("body").evaluate((el) => el.innerHTML).catch(() => "")),
    },
    buttons,
    links,
    labels,
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(注文管理|返品|顧客管理|下書き|売上実績|発注|入荷|納品書|Shopify|スマレジ|OmnibusCore|Recustomer|リテールポータル|権限|ユーザー|アイテムが見つかりません|注文が見つかりません|予期せぬ|存在しない|作成する|連携する|保存する|CSV|PDF)/.test(line),
        ),
      120,
    ),
    screenshot,
    consoleErrors: compact(errors, 20),
  };
}

let selectedProfile = null;
let selectedContext = null;
let selectedPage = null;
const profileAttempts = [];

for (const profileDir of candidateProfiles) {
  let context = null;
  try {
    context = await chromium.launchPersistentContext(profileDir, {
      executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
      headless: true,
      viewport: { width: 1440, height: 1100 },
      ignoreHTTPSErrors: true,
    });
    const page = await context.newPage();
    page.setDefaultTimeout(15000);
    await page.goto("https://www.sqstackstaging.com/admin/orders", { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(800);
    const text = await page.locator("body").innerText().catch(() => "");
    const login = /ログイン|メールアドレス|パスワード/.test(text);
    const admin = text.includes("注文管理") || text.includes("SQ - 管理画面");
    profileAttempts.push({ profileDir, login, admin, finalUrl: page.url(), textStart: text.slice(0, 300) });
    if (!login && admin) {
      selectedProfile = profileDir;
      selectedContext = context;
      selectedPage = page;
      break;
    }
    await context.close();
  } catch (error) {
    profileAttempts.push({ profileDir, error: error.message });
    if (context) await context.close().catch(() => {});
  }
}

const records = [];
if (selectedPage) {
  for (const [index, url] of targetUrls.entries()) {
    const record = await extract(selectedPage, url, index);
    records.push(record);
    console.log(`${index + 1}/${targetUrls.length} ${url} ${record.h1.join(" / ")} ${JSON.stringify(record.classification)}`);
  }
  await selectedContext.close();
}

await fs.writeFile(
  path.join(OUT_DIR, "unconfirmed-recheck-records.json"),
  JSON.stringify({
    generatedAt: new Date().toISOString(),
    selectedProfile,
    profileAttempts,
    records,
  }, null, 2),
);
