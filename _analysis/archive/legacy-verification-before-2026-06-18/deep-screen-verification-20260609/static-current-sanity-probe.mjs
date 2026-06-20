import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "static-current-sanity-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const base = "https://www.sqstackstaging.com";
const records = [];
const network = [];
const consoleLogs = [];
let shotIndex = 1;

function compact(items, limit = 260) {
  return [...new Set(items.map((item) => (item || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(value) {
  return value.replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 150) || "screen";
}

function safeUrl(url) {
  try {
    const parsed = new URL(url);
    if (parsed.hostname.includes("clerk")) {
      parsed.search = "";
    }
    if (parsed.searchParams.has("__session")) {
      parsed.searchParams.set("__session", "[redacted]");
    }
    return parsed.toString();
  } catch {
    return url;
  }
}

async function settle(page, extraMs = 800) {
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
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
      els.slice(0, 500).map((el) => {
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
          value: String(el.value || "").slice(0, 300),
          checked: el.checked || false,
          disabled: el.disabled || el.getAttribute("aria-disabled") === "true" || false,
          visible:
            style.visibility !== "hidden" &&
            style.display !== "none" &&
            rect.width > 0 &&
            rect.height > 0,
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
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => []), 30),
    h2: compact(await page.locator("h2").allInnerTexts().catch(() => []), 100),
    h3: compact(await page.locator("h3").allInnerTexts().catch(() => []), 140),
    menus: compact(await page.locator('[role="menu"], [role="dialog"]').allInnerTexts().catch(() => []), 80),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 260))
        .catch(() => []),
      260,
    ),
    controls,
    links: controls.filter((control) => control.tag === "a" && control.href).map((control) => ({ text: control.text, href: control.href })),
    buttons: controls.filter((control) => control.tag === "button").map((control) => ({ text: control.text, ariaLabel: control.ariaLabel, disabled: control.disabled, visible: control.visible })),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(TODO|このページは存在しない|ホームに戻る|商品|カタログ|SKU一覧|販売先|自動追加|アーカイブ|公開中|下書き|非公開|分析|卸売|ログアウト|プロフィール|組織|ユーザー|メニュー|ヘルプセンター|製品アップデート|Proudly built|アイテムが見つかりませんでした|このページの準備が整いました)/.test(
            line,
          ),
        ),
      420,
    ),
    classification: {
      empty: text.includes("アイテムが見つかりませんでした"),
      todoOnly: /\bTODO\b/.test(text) || text.includes("TODO"),
      notFound: text.includes("このページは存在しないようです"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} url=${record.url} empty=${record.classification.empty} todo=${record.classification.todoOnly} notFound=${record.classification.notFound}`);
  shotIndex += 1;
  return record;
}

async function firstHref(page, pattern, exclude = []) {
  const hrefs = await page
    .locator("a")
    .evaluateAll((els) => els.map((el) => el.href).filter(Boolean))
    .catch(() => []);
  return [...new Set(hrefs)].find((href) => pattern.test(href) && exclude.every((item) => !href.includes(item))) || null;
}

async function clickIfVisible(page, locator, name) {
  const count = await locator.count().catch(() => 0);
  if (!count) return false;
  const target = locator.first();
  if (!(await target.isVisible().catch(() => false))) return false;
  await target.click({ timeout: 5000 }).catch(() => {});
  await settle(page, 500);
  console.log(`clicked: ${name}`);
  return true;
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  locale: "ja-JP",
  timezoneId: "Asia/Tokyo",
  acceptDownloads: false,
});

context.on("page", (page) => {
  page.on("console", (message) => {
    if (message.type() === "error") consoleLogs.push({ type: message.type(), text: message.text().slice(0, 600) });
  });
  page.on("response", (response) => {
    if (response.status() >= 400) {
      network.push({ status: response.status(), url: safeUrl(response.url()), method: response.request().method() });
    }
  });
});

const page = context.pages()[0] || (await context.newPage());
page.on("console", (message) => {
  if (message.type() === "error") consoleLogs.push({ type: message.type(), text: message.text().slice(0, 600) });
});
page.on("response", (response) => {
  if (response.status() >= 400) {
    network.push({ status: response.status(), url: safeUrl(response.url()), method: response.request().method() });
  }
});

try {
  await goto(page, `${base}/admin`);
  await snapshot(page, "home-desktop", `${base}/admin`);
  await clickIfVisible(page, page.getByRole("button", { name: /stack-ps-yosuke|陽介|河野/ }), "user-menu");
  await snapshot(page, "home-user-menu-opened", `${base}/admin`, { action: "click-user-menu" });

  await page.setViewportSize({ width: 390, height: 844 });
  await goto(page, `${base}/admin`);
  await snapshot(page, "home-mobile-before-menu", `${base}/admin`, { viewport: "mobile" });
  await clickIfVisible(page, page.getByLabel("メニューを切り替える"), "mobile-menu-toggle");
  await snapshot(page, "home-mobile-menu-opened", `${base}/admin`, { viewport: "mobile", action: "click-menu-toggle" });

  await page.setViewportSize({ width: 1440, height: 1100 });
  for (const [name, url] of [
    ["analytics-current", `${base}/admin/analytics`],
    ["b2b-current", `${base}/admin/b2b`],
    ["b2b-create-direct", `${base}/admin/b2b/create`],
  ]) {
    await goto(page, url);
    await snapshot(page, name, url);
  }

  for (const [name, url] of [
    ["products-all", `${base}/admin/products`],
    ["products-published-tab", `${base}/admin/products?tab=1`],
    ["products-draft-tab", `${base}/admin/products?tab=2`],
    ["products-archived-tab", `${base}/admin/products?tab=3`],
    ["catalogs-list", `${base}/admin/catalogs`],
  ]) {
    await goto(page, url);
    await snapshot(page, name, url);
  }

  await goto(page, `${base}/admin/products`);
  const firstProduct = await firstHref(page, /\/admin\/products\/[^/?#]+$/, ["/create"]);
  if (firstProduct) {
    await goto(page, firstProduct);
    await snapshot(page, "product-detail-first-current", firstProduct, { discoveredUrl: firstProduct });
    await clickIfVisible(page, page.getByRole("button", { name: /その他|操作|More|Actions/ }), "product-other-actions");
    await snapshot(page, "product-detail-first-actions-opened", firstProduct, { discoveredUrl: firstProduct, action: "open-actions" });
  } else {
    records.push({ name: "product-detail-first-current", note: "No product detail link found." });
  }

  await goto(page, `${base}/admin/products?tab=3`);
  const firstArchivedProduct = await firstHref(page, /\/admin\/products\/[^/?#]+$/, ["/create"]);
  if (firstArchivedProduct) {
    await goto(page, firstArchivedProduct);
    await snapshot(page, "product-detail-first-archived-current", firstArchivedProduct, { discoveredUrl: firstArchivedProduct });
    await clickIfVisible(page, page.getByRole("button", { name: /その他|操作|More|Actions/ }), "archived-product-other-actions");
    await snapshot(page, "product-detail-first-archived-actions-opened", firstArchivedProduct, { discoveredUrl: firstArchivedProduct, action: "open-actions" });
  } else {
    records.push({ name: "product-detail-first-archived-current", note: "No archived product detail link found." });
  }

  await goto(page, `${base}/admin/catalogs`);
  const firstCatalog = await firstHref(page, /\/admin\/catalogs\/[^/?#]+$/, ["/create", "csv_import"]);
  if (firstCatalog) {
    await goto(page, firstCatalog);
    await snapshot(page, "catalog-detail-first-current", firstCatalog, { discoveredUrl: firstCatalog });
    await goto(page, `${firstCatalog}/catalog_product_variants`);
    await snapshot(page, "catalog-sku-list-first-current", `${firstCatalog}/catalog_product_variants`, { discoveredUrl: `${firstCatalog}/catalog_product_variants` });
    await goto(page, `${firstCatalog}/automatic_add_rules`);
    await snapshot(page, "catalog-automatic-add-rules-first-current", `${firstCatalog}/automatic_add_rules`, { discoveredUrl: `${firstCatalog}/automatic_add_rules` });
  } else {
    records.push({ name: "catalog-detail-first-current", note: "No catalog detail link found." });
  }
} catch (error) {
  records.push({ name: "failure", message: error.message, stack: error.stack });
  await snapshot(page, "failure-state", page.url(), { error: error.message }).catch(() => {});
  throw error;
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "static-current-sanity-records.json"),
    JSON.stringify(
      {
        generatedAt: new Date().toISOString(),
        failed: records.find((record) => record.name === "failure")?.message || null,
        records,
        network,
        console: consoleLogs,
      },
      null,
      2,
    ),
  );
  await context.close();
}
