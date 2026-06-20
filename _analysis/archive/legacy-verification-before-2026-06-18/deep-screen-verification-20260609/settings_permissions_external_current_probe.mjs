import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "settings-permissions-external-current-screenshots");
await fs.rm(SCREEN_DIR, { recursive: true, force: true });
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const targets = [
  { name: "retail-staff-list", url: "https://www.sqstackstaging.com/admin/settings/retail_staff_members" },
  { name: "retail-staff-create", url: "https://www.sqstackstaging.com/admin/settings/retail_staff_members/create", action: "open-location-picker" },
  { name: "users-list", url: "https://www.sqstackstaging.com/admin/settings/users" },
  { name: "users-create", url: "https://www.sqstackstaging.com/admin/settings/users/create" },
  { name: "permission-groups-list", url: "https://www.sqstackstaging.com/admin/settings/permission_groups" },
  {
    name: "permission-group-admin-detail",
    url: "https://www.sqstackstaging.com/admin/settings/permission_groups/434b6285-7690-535c-9adb-9899e62b9c01_PermissionGroup",
  },
  {
    name: "permission-group-store-staff-detail",
    url: "https://www.sqstackstaging.com/admin/settings/permission_groups/f974f72a-838e-5bed-9202-1160c6fbe462_PermissionGroup",
  },
  { name: "shopify-list", url: "https://www.sqstackstaging.com/admin/shopify_integrations" },
  { name: "shopify-create", url: "https://www.sqstackstaging.com/admin/shopify_integrations/create" },
  { name: "omnibuscore-list", url: "https://www.sqstackstaging.com/admin/omnibus_core_integrations" },
  {
    name: "omnibuscore-detail",
    url: "https://www.sqstackstaging.com/admin/omnibus_core_integrations/703c48d1-ffad-55d2-8683-613762453668_OmnibusCoreIntegration",
  },
  { name: "smaregi-list", url: "https://www.sqstackstaging.com/admin/smaregi_integrations" },
  { name: "smaregi-create", url: "https://www.sqstackstaging.com/admin/smaregi_integrations/create" },
  { name: "retail-portal-list", url: "https://www.sqstackstaging.com/admin/retail_portal_integrations" },
  { name: "retail-portal-create", url: "https://www.sqstackstaging.com/admin/retail_portal_integrations/create" },
  { name: "logizard-list", url: "https://www.sqstackstaging.com/admin/logizard_integrations" },
  { name: "logizard-create", url: "https://www.sqstackstaging.com/admin/logizard_integrations/create" },
  { name: "recustomer-list", url: "https://www.sqstackstaging.com/admin/recustomer_integrations" },
  { name: "recustomer-create", url: "https://www.sqstackstaging.com/admin/recustomer_integrations/create" },
];

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

async function getControls(page) {
  return await page
    .locator("button, a, input, select, textarea")
    .evaluateAll((els) =>
      els.slice(0, 320).map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute("type") || "",
          role: el.getAttribute("role") || "",
          text: el.textContent?.trim().replace(/\s+/g, " ") || "",
          ariaLabel: el.getAttribute("aria-label") || "",
          title: el.getAttribute("title") || "",
          href: el.href || "",
          placeholder: el.getAttribute("placeholder") || "",
          value: el.value || "",
          checked: el.checked || false,
          disabled: el.disabled || el.getAttribute("aria-disabled") === "true" || el.className?.toString().includes("disabled") || false,
          ariaDisabled: el.getAttribute("aria-disabled") || "",
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
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    h2: compact(await page.locator("h2").allInnerTexts().catch(() => []), 80),
    dialogs: compact(await page.locator('[role="dialog"]').allInnerTexts().catch(() => []), 80),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 260))
        .catch(() => []),
      260,
    ),
    controls,
    selectOptions: await page
      .locator("select")
      .evaluateAll((selects) =>
        selects.slice(0, 40).map((select) => ({
          label: select.closest("label")?.textContent?.trim().replace(/\s+/g, " ") || "",
          value: select.value || "",
          options: Array.from(select.options)
            .map((option) => option.textContent?.trim().replace(/\s+/g, " ") || "")
            .filter(Boolean),
        })),
      )
      .catch(() => []),
    checkedPermissions: controls
      .filter((control) => control.type === "checkbox" && control.checked)
      .map((control) => control.text || control.ariaLabel || control.title || control.value)
      .filter(Boolean),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(販売員|販売スタッフ|ロケーション|管理メンバー|権限|権限グループ|特権管理者|店舗スタッフ|Shopify|OmnibusCore|スマレジ|リテールポータル|ロジザード|Recustomer|連携|同期|在庫|注文|商品|カタログ|トークン|接続|保存|作成|追加|インポート|エクスポート|SKU|JAN|EAN|UPC|メール|招待|アイテムが見つかりません|このページの準備が整いました|予期せぬ|存在しない|エラー)/.test(line),
        ),
      380,
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
  console.log(
    `${record.name}: h1=${record.h1.join(" / ")} url=${record.url} empty=${record.classification.empty} notFound=${record.classification.notFound} unexpected=${record.classification.unexpectedError}`,
  );
  shotIndex += 1;
  return record;
}

async function maybeOpenRetailStaffLocationPicker(page, target) {
  if (target.action !== "open-location-picker") return;
  const action = page.getByRole("button", { name: /検索|選択/ }).first();
  if (!(await action.isVisible().catch(() => false))) return;
  await action.click({ timeout: 12000 }).catch(() => {});
  await settle(page, 1000);
  await snapshot(page, `${target.name}-location-picker`, target.url, { action: "open-location-picker" });
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});

const page = await context.newPage();
page.setDefaultTimeout(25000);

page.on("console", (msg) => {
  if (["error", "warning"].includes(msg.type())) {
    consoleLogs.push({ type: msg.type(), text: msg.text().slice(0, 2000) });
  }
});

page.on("response", async (response) => {
  const url = response.url();
  if (!/graphql|integrations|settings\/users|permission_groups|retail_staff_members/.test(url) && response.status() < 400) return;
  let body = "";
  if (/graphql|api/.test(url) || response.status() >= 400) {
    body = await response.text().catch(() => "");
  }
  network.push({
    url: safeUrl(url),
    method: response.request().method(),
    status: response.status(),
    postData: (response.request().postData() || "").slice(0, 5000),
    body: body.slice(0, 8000),
  });
});

let failed = null;
try {
  for (const target of targets) {
    await page.goto(target.url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await settle(page);
    await snapshot(page, target.name, target.url);
    await maybeOpenRetailStaffLocationPicker(page, target);
  }
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", page.url(), { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "settings-permissions-external-current-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), targets, failed, consoleLogs, network, records }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
