import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "settings-data-masters-current-screenshots");
await fs.rm(SCREEN_DIR, { recursive: true, force: true });
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const base = "https://www.sqstackstaging.com";
const targets = [
  { name: "tenants-list", url: `${base}/admin/settings/tenants` },
  { name: "locations-list", url: `${base}/admin/settings/locations` },
  { name: "locations-create", url: `${base}/admin/settings/locations/create`, action: "toggle-location-address" },
  { name: "location-groups-list", url: `${base}/admin/settings/location_groups` },
  { name: "location-groups-create", url: `${base}/admin/settings/location_groups/create`, action: "open-location-picker" },
  { name: "brands-list", url: `${base}/admin/settings/brands` },
  { name: "brands-create", url: `${base}/admin/settings/brands/create` },
  { name: "suppliers-list", url: `${base}/admin/settings/suppliers` },
  { name: "suppliers-create", url: `${base}/admin/settings/suppliers/create` },
  { name: "payment-methods-list", url: `${base}/admin/settings/payment_methods` },
  { name: "payment-methods-create", url: `${base}/admin/settings/payment_methods/create` },
  { name: "translation-list", url: `${base}/admin/settings/translation` },
  { name: "translation-rule-create", url: `${base}/admin/settings/translation/translation_rules/create` },
  { name: "measurement-rules-list", url: `${base}/admin/settings/product_measurement_rules` },
  { name: "measurement-rule-create", url: `${base}/admin/settings/product_measurement_rules/create`, action: "measurement-add-item" },
  { name: "metafield-definitions-root", url: `${base}/admin/settings/metafield_definitions` },
  { name: "metafield-definitions-product", url: `${base}/admin/settings/metafield_definitions/product` },
  { name: "metafield-definitions-product-create", url: `${base}/admin/settings/metafield_definitions/product/create` },
  { name: "company-locations-settings-direct", url: `${base}/admin/settings/company_locations` },
];

const records = [];
const network = [];
const consoleLogs = [];
let shotIndex = 1;

function compact(items, limit = 300) {
  return [...new Set(items.map((item) => (item || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(value) {
  return value.replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 140) || "screen";
}

function safeUrl(url) {
  try {
    const parsed = new URL(url);
    if (parsed.hostname.includes("clerk")) parsed.search = "";
    if (parsed.searchParams.has("__session")) parsed.searchParams.set("__session", "[redacted]");
    return parsed.toString();
  } catch {
    return url;
  }
}

async function settle(page, extraMs = 900) {
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

async function getSelectOptions(page) {
  return await page
    .locator("select")
    .evaluateAll((selects) =>
      selects.slice(0, 80).map((select, index) => ({
        index,
        value: select.value || "",
        disabled: select.disabled,
        options: Array.from(select.options).map((option) => ({
          text: option.textContent?.trim().replace(/\s+/g, " ") || "",
          value: option.value || "",
          disabled: option.disabled,
        })),
      })),
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
    h2: compact(await page.locator("h2").allInnerTexts().catch(() => []), 120),
    h3: compact(await page.locator("h3").allInnerTexts().catch(() => []), 120),
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
    selectOptions: await getSelectOptions(page),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(テナント|ロケーション|場所種別|場所コード|公開|アーカイブ|ロケーショングループ|ブランド|取引先|決済方法|支払い待ち|代引き|翻訳|言語|自動で作成|採寸|単位|肩幅|メタフィールド|定義|商品|バリエーション|顧客|注文|下書き注文|会社|ディスカウント|在庫|調整|取置|発注|入荷|出荷|仕入れ先|タイプ|JSON|リッチテキスト|保存|作成|追加|選択|検索|アイテムが見つかりません|このページの準備が整いました|予期せぬエラー|このページは存在しない|TODO|未設定)/.test(
            line,
          ),
        ),
      600,
    ),
    classification: {
      empty: text.includes("アイテムが見つかりませんでした"),
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} url=${record.url} empty=${record.classification.empty} notFound=${record.classification.notFound} unexpected=${record.classification.unexpectedError}`);
  shotIndex += 1;
  return record;
}

async function clickButton(page, nameRe, label) {
  const locator = page.getByRole("button", { name: nameRe }).first();
  if (!(await locator.isVisible().catch(() => false))) return false;
  await locator.click({ timeout: 8000 }).catch(() => {});
  await settle(page, 700);
  console.log(`clicked: ${label}`);
  return true;
}

async function runAction(page, target) {
  if (target.action === "toggle-location-address") {
    const checkbox = page.getByLabel(/ロケーションの住所を登録する/).first();
    if (await checkbox.isVisible().catch(() => false)) {
      await checkbox.click({ timeout: 8000 }).catch(() => {});
      await settle(page, 600);
      await snapshot(page, `${target.name}-address-expanded`, target.url, { action: target.action });
    }
    return;
  }
  if (target.action === "open-location-picker") {
    await clickButton(page, /選択|検索/, "location-group-location-picker");
    await snapshot(page, `${target.name}-location-picker-opened`, target.url, { action: target.action });
    return;
  }
  if (target.action === "measurement-add-item") {
    await clickButton(page, /採寸項目を追加|追加/, "measurement-add-item");
    await snapshot(page, `${target.name}-item-added`, target.url, { action: target.action });
  }
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
  const sanitizedUrl = safeUrl(url);
  let hostname = "";
  try {
    hostname = new URL(url).hostname;
  } catch {}
  const isClerk = hostname.includes("clerk");
  const isNextStatic = url.includes("/_next/static/");
  const isVercelInsight = url.includes("/_vercel/insights/");
  const shouldTrack = /\/api\/graphql|\/admin\/settings/.test(url) || (response.status() >= 400 && !isClerk && !isNextStatic && !isVercelInsight);
  if (!shouldTrack) return;
  let body = "";
  if (!isClerk && !isNextStatic && !isVercelInsight && (/\/api\/graphql/.test(url) || response.status() >= 400)) {
    body = await response.text().catch(() => "");
  }
  const rawPostData = response.request().postData() || "";
  const postData = isClerk || rawPostData.includes("__session") ? "" : rawPostData.slice(0, 2000);
  network.push({
    status: response.status(),
    url: sanitizedUrl,
    method: response.request().method(),
    postData,
    body: body.slice(0, 4000),
  });
});

let failed = null;
try {
  for (const target of targets) {
    await goto(page, target.url);
    await snapshot(page, target.name, target.url);
    await runAction(page, target);
  }
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", page.url(), { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "settings-data-masters-current-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), failed, targets, records, network, console: consoleLogs }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
