import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-user-menu-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

function compact(items, limit = 200) {
  return [...new Set(items.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

async function snapshot(page, name, index, extra = {}) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(index).padStart(2, "0")}-${name}.png`);
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const text = await page.locator("body").innerText().catch(() => "");
  return {
    name,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => []), 160),
    links: await page.locator("a").evaluateAll((els) =>
      els.map((a) => ({ text: a.textContent?.trim().replace(/\s+/g, " ") || "", href: a.href || "" })).filter((a) => a.text || a.href).slice(0, 220),
    ).catch(() => []),
    menuItems: compact(await page.locator('[role="menuitem"], [role="menu"] *').allInnerTexts().catch(() => []), 160),
    textLines: compact(text.split(/\n+/).map((line) => line.trim()), 300),
    classification: {
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
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

await page.goto("https://www.sqstackstaging.com/admin/purchasing_customers", { waitUntil: "domcontentloaded", timeout: 60000 });
await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
await page.waitForTimeout(900);

const records = [];
records.push(await snapshot(page, "before", 1));

let clickedSelector = "";
for (const selector of ['button:has-text("stack-ps-yosuke")', 'button:has-text("陽介 河野")', 'button:has-text("陽介")']) {
  const button = page.locator(selector).first();
  if (await button.isVisible().catch(() => false)) {
    await button.click().catch(() => {});
    clickedSelector = selector;
    await page.waitForTimeout(900);
    break;
  }
}

records.push(await snapshot(page, "after", 2, { interaction: { clickedSelector } }));
await fs.writeFile(
  path.join(OUT_DIR, "unconfirmed-user-menu-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2),
);
for (const record of records) {
  console.log(`${record.name}: h1=${record.h1.join(" / ")} clicked=${record.interaction?.clickedSelector || ""} class=${JSON.stringify(record.classification)}`);
}
await context.close();
