import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-retail-tenant-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

function compact(items, limit = 180) {
  return [...new Set(items.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

async function snapshot(page, name, index, extra = {}) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(index).padStart(2, "0")}-${name}.png`);
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const text = await page.locator("body").innerText().catch(() => "");
  const rows = await page.locator("tr, [role=row]").evaluateAll((els) =>
    els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 160),
  ).catch(() => []);
  const controls = await page.locator("input, select").evaluateAll((els) =>
    els.map((el) => {
      const id = el.getAttribute("id") || "";
      const label = id ? document.querySelector(`label[for="${CSS.escape(id)}"]`)?.textContent?.trim() || "" : "";
      return {
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute("type") || "",
        label: label || el.closest("label")?.textContent?.trim() || el.getAttribute("aria-label") || "",
        value: el.tagName.toLowerCase() === "select"
          ? Array.from(el.options).map((o) => `${o.selected ? "*" : ""}${o.textContent?.trim() || ""}`)
          : el.getAttribute("value") || "",
      };
    }),
  ).catch(() => []);
  return {
    name,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    labels: compact(await page.locator("label").allInnerTexts().catch(() => []), 220),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => []), 160),
    rows: compact(rows, 160),
    controls,
    textLines: compact(text.split(/\n+/).map((line) => line.trim()), 320),
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(20000);

const records = [];
await page.goto("https://www.sqstackstaging.com/admin/retail_portal_integrations/create", { waitUntil: "domcontentloaded", timeout: 60000 });
await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
await page.waitForTimeout(900);
records.push(await snapshot(page, "initial", 1));

await page.getByLabel("テナント").selectOption({ label: "ユニクロ" }).catch(() => {});
await page.waitForTimeout(1200);
records.push(await snapshot(page, "tenant-selected", 2));

const inventoryButton = page.getByRole("button", { name: /選択/ }).nth(1);
const inventoryClicked = await inventoryButton.isVisible().catch(() => false);
if (inventoryClicked) {
  await inventoryButton.click().catch(() => {});
  await page.waitForTimeout(1300);
}
records.push(await snapshot(page, "inventory-modal-after-tenant", 3, { interaction: { inventoryClicked } }));

await fs.writeFile(
  path.join(OUT_DIR, "unconfirmed-retail-tenant-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2),
);

for (const record of records) {
  console.log(`${record.name}: h1=${record.h1.join(" / ")} rows=${record.rows.length}`);
}

await context.close();
