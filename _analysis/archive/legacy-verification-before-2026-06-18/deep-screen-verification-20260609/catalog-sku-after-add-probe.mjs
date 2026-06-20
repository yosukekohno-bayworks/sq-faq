import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "catalog-sku-after-add-screenshots");
await fs.rm(SCREEN_DIR, { recursive: true, force: true });
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const base = "https://www.sqstackstaging.com";
const catalogPath = "/admin/catalogs/e2a819ab-3f81-558d-ad76-5fae9e8422d2_Catalog";
const productNeedle = "ポケモン UT";
const urls = {
  detail: `${base}${catalogPath}`,
  add: `${base}${catalogPath}/create`,
  sku: `${base}${catalogPath}/catalog_product_variants`,
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
    if (parsed.searchParams.has("__session")) parsed.searchParams.set("__session", "[redacted]");
    if (parsed.hostname.includes("clerk")) parsed.search = "";
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
      els.slice(0, 520).map((el) => {
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
    checkedInputs: controls.filter((control) => control.checked).map((control) => ({ type: control.type, value: control.value, text: control.text, ariaLabel: control.ariaLabel })),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) => /(カタログ|SKU|商品|商品コード|バリエーション|ステータス|販売先|自動追加|追加|選択|保存|検索|アイテムが見つかりません|このページは存在しない|予期せぬエラー|成功|失敗|未保存)/.test(line)),
      520,
    ),
    classification: {
      empty: text.includes("アイテムが見つかりませんでした"),
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      hasTargetProduct: text.includes(productNeedle),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} url=${record.url} empty=${record.classification.empty} target=${record.classification.hasTargetProduct}`);
  shotIndex += 1;
  return record;
}

async function clickVisible(page, locator, label) {
  const target = locator.first();
  if (!(await target.isVisible().catch(() => false))) return false;
  await target.click({ timeout: 10000 });
  await settle(page, 700);
  console.log(`clicked: ${label}`);
  return true;
}

async function selectProductInDialog(page) {
  const dialog = page.locator('[role="dialog"]').last();
  const scope = (await dialog.isVisible().catch(() => false)) ? dialog : page;
  const search = scope.getByPlaceholder(/検索|商品コード|商品名/).first();
  if (await search.isVisible().catch(() => false)) {
    await search.fill(productNeedle);
    await settle(page, 1200);
  }

  const row = scope.locator("tr, [role=row]").filter({ hasText: productNeedle }).first();
  if (await row.isVisible().catch(() => false)) {
    const checkbox = row.locator('input[type="checkbox"]').first();
    if (await checkbox.isVisible().catch(() => false)) {
      await checkbox.check({ timeout: 10000 }).catch(async () => {
        await checkbox.click({ timeout: 10000 });
      });
    } else {
      await row.click({ timeout: 10000 });
    }
    await settle(page, 700);
    return true;
  }

  const targetText = scope.getByText(productNeedle, { exact: false }).first();
  if (await targetText.isVisible().catch(() => false)) {
    await targetText.click({ timeout: 10000 });
    await settle(page, 700);
    return true;
  }

  const firstCheckbox = scope.locator('input[type="checkbox"]').nth(1);
  if (await firstCheckbox.isVisible().catch(() => false)) {
    await firstCheckbox.check({ timeout: 10000 }).catch(async () => {
      await firstCheckbox.click({ timeout: 10000 });
    });
    await settle(page, 700);
    return true;
  }

  return false;
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
  const shouldTrack = /\/api\/graphql|\/admin\/catalogs/.test(url) || (response.status() >= 400 && !isClerk && !isNextStatic && !isVercelInsight);
  if (!shouldTrack) return;
  const rawPostData = response.request().postData() || "";
  network.push({
    status: response.status(),
    url: safeUrl(url),
    method: response.request().method(),
    postData: isClerk || rawPostData.includes("__session") ? "" : rawPostData.slice(0, 1600),
  });
});

let failed = null;
try {
  await goto(page, urls.detail);
  await snapshot(page, "catalog-detail-before");

  await goto(page, urls.sku);
  await snapshot(page, "catalog-sku-before");

  await goto(page, urls.add);
  await snapshot(page, "catalog-add-page");

  const opened = await clickVisible(page, page.getByRole("button", { name: /選択|商品を選択|追加/ }), "open-product-picker");
  await snapshot(page, "catalog-add-picker-opened", { openedPicker: opened });

  const selected = await selectProductInDialog(page);
  await snapshot(page, "catalog-add-picker-selected", { selected });

  const confirmed = await clickVisible(page, page.getByRole("button", { name: /^選択する$/ }), "confirm-product-selection");
  await snapshot(page, "catalog-add-selected-product", { selected, confirmed });

  const saveClicked = await clickVisible(page, page.getByRole("button", { name: /商品を追加する|追加する|保存する|保存$/ }), "save-catalog-product");
  await snapshot(page, "catalog-add-after-save", { selected, confirmed, saveClicked });

  const modalConfirmed = await clickVisible(page, page.getByRole("button", { name: /^追加する$/ }), "confirm-catalog-product-add");
  await snapshot(page, "catalog-add-after-confirm", { selected, confirmed, saveClicked, modalConfirmed });

  await goto(page, urls.detail);
  await snapshot(page, "catalog-detail-after");

  await goto(page, urls.sku);
  await snapshot(page, "catalog-sku-after");
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "catalog-sku-after-add-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), failed, target: { catalogPath, productNeedle, urls }, records, network, console: consoleLogs }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
