import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "permission-state-current-screenshots");
await fs.rm(SCREEN_DIR, { recursive: true, force: true });
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const targets = [
  {
    name: "permission-group-admin-detail",
    url: "https://www.sqstackstaging.com/admin/settings/permission_groups/434b6285-7690-535c-9adb-9899e62b9c01_PermissionGroup",
  },
  {
    name: "permission-group-store-staff-detail",
    url: "https://www.sqstackstaging.com/admin/settings/permission_groups/f974f72a-838e-5bed-9202-1160c6fbe462_PermissionGroup",
  },
];

const records = [];
const network = [];
let shotIndex = 1;

async function settle(page, extraMs = 1000) {
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(extraMs);
}

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

async function snapshot(page, name, requestedUrl) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(shotIndex).padStart(2, "0")}-${slugify(name)}.png`);
  const text = await page.locator("body").innerText({ timeout: 12000 }).catch(() => "");
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const permissionInputs = await page
    .locator('input[type="checkbox"], [role="checkbox"]')
    .evaluateAll((els) =>
      els.map((el) => {
        const input = el;
        const id = input.getAttribute("id") || "";
        let label = "";
        if (input.getAttribute("aria-label")) label = input.getAttribute("aria-label") || "";
        if (!label && id) {
          const labelEl = document.querySelector(`label[for="${CSS.escape(id)}"]`);
          label = labelEl?.textContent || "";
        }
        if (!label) label = input.closest("label")?.textContent || "";
        if (!label) {
          const wrapper = input.closest('[class*="Choice"], [class*="Checkbox"], [class*="Option"], li, tr, [role="row"]');
          label = wrapper?.textContent || "";
        }
        return {
          label: label.trim().replace(/\s+/g, " "),
          checked: input instanceof HTMLInputElement ? input.checked : input.getAttribute("aria-checked") === "true",
          disabled: input instanceof HTMLInputElement ? input.disabled : input.getAttribute("aria-disabled") === "true",
          ariaChecked: input.getAttribute("aria-checked") || "",
          ariaLabel: input.getAttribute("aria-label") || "",
          type: input.getAttribute("type") || "",
          role: input.getAttribute("role") || "",
          name: input.getAttribute("name") || "",
          value: input.getAttribute("value") || "",
        };
      }),
    )
    .catch(() => []);
  const record = {
    name,
    requestedUrl,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => []), 20),
    ready: text.includes("このページの準備が整いました"),
    permissionInputs,
    checkedCount: permissionInputs.filter((item) => item.checked).length,
    uncheckedCount: permissionInputs.filter((item) => !item.checked).length,
    totalCount: permissionInputs.length,
    checkedLabels: permissionInputs.filter((item) => item.checked).map((item) => item.label).filter(Boolean),
    uncheckedLabels: permissionInputs.filter((item) => !item.checked).map((item) => item.label).filter(Boolean),
    screenshot: path.relative(ROOT, screenshotFile),
  };
  records.push(record);
  console.log(`${name}: h1=${record.h1.join(" / ")} checked=${record.checkedCount}/${record.totalCount}`);
  shotIndex += 1;
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  locale: "ja-JP",
  timezoneId: "Asia/Tokyo",
});

const page = context.pages()[0] || (await context.newPage());
page.on("response", (response) => {
  if (response.status() >= 400) network.push({ status: response.status(), url: safeUrl(response.url()), method: response.request().method() });
});

let failed = null;
try {
  for (const target of targets) {
    await page.goto(target.url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await settle(page);
    await snapshot(page, target.name, target.url);
  }
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "permission-state-current-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), failed, records, network }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
