import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "public-help-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const browser = await chromium.launch({
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
});
const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
page.setDefaultTimeout(15000);

function normalize(url) {
  try {
    const parsed = new URL(url);
    parsed.hash = "";
    parsed.search = "";
    return parsed.toString().replace(/\/$/, "");
  } catch {
    return null;
  }
}

function slugify(url) {
  const u = new URL(url);
  return u.pathname
    .replace(/^\/docs\/guide\/?/, "")
    .replace(/[^A-Za-z0-9_-]+/g, "__")
    .replace(/^_+|_+$/g, "")
    .slice(0, 140) || "introduction";
}

async function capture(url, index) {
  let status = null;
  let gotoError = null;
  try {
    const response = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
    status = response?.status() ?? null;
    await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(500);
  } catch (error) {
    gotoError = error.message;
  }
  const body = await page.locator("body").innerText().catch((error) => String(error));
  const h1 = await page.locator("h1").allInnerTexts().catch(() => []);
  const h2 = await page.locator("h2").allInnerTexts().catch(() => []);
  const links = await page
    .locator("a[href]")
    .evaluateAll((els) => els.map((a) => ({ text: a.textContent?.trim() || "", href: a.href })))
    .catch(() => []);
  const images = await page
    .locator("img")
    .evaluateAll((els) => els.map((img) => ({ alt: img.alt || "", src: img.src || "" })))
    .catch(() => []);
  const screenshotPath = path.join(
    SCREEN_DIR,
    `${String(index).padStart(3, "0")}-${slugify(url)}.png`,
  );
  try {
    await page.screenshot({ path: screenshotPath, fullPage: true, animations: "disabled" });
  } catch {
    // Keep the textual record even if a screenshot fails.
  }
  return {
    url,
    finalUrl: page.url(),
    status,
    gotoError,
    title: await page.title().catch(() => ""),
    h1: [...new Set(h1.map((x) => x.trim()).filter(Boolean))],
    h2: [...new Set(h2.map((x) => x.trim()).filter(Boolean))],
    textLength: body.length,
    hasImage: images.length > 0,
    imageCount: images.length,
    linkCount: links.length,
    guideLinks: [...new Set(links.map((l) => normalize(l.href)).filter((href) => href?.startsWith("https://docs.sqstack.com/docs/guide/")))].sort(),
    images: images.slice(0, 20),
    textStart: body.slice(0, 1800),
    screenshot: path.relative(ROOT, screenshotPath),
  };
}

const start = "https://docs.sqstack.com/docs/guide/introduction";
const queue = [start];
const seen = new Set();
const records = [];
while (queue.length) {
  const url = queue.shift();
  const norm = normalize(url);
  if (!norm || seen.has(norm)) continue;
  seen.add(norm);
  const record = await capture(norm, records.length + 1);
  records.push(record);
  console.log(`${records.length} ${record.status} ${norm} ${record.h1.join(" / ")} len=${record.textLength} img=${record.imageCount}`);
  for (const link of record.guideLinks) {
    if (!seen.has(link)) queue.push(link);
  }
}

const directChecks = [];
for (const url of [
  "https://docs.sqstack.com/docs/llms.txt",
  "https://docs.sqstack.com/llms.txt",
  "https://docs.sqstack.com/docs/llms-full.txt",
  "https://docs.sqstack.com/llms-full.txt",
  "https://docs.sqstack.com/docs/guide/shopify-integration",
  "https://docs.sqstack.com/guide/shopify-integration",
  "https://docs.sqstack.com/docs/guide/retail-portal-integration",
  "https://docs.sqstack.com/guide/retail-portal-integration",
]) {
  let status = null;
  let textStart = "";
  try {
    const response = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
    status = response?.status() ?? null;
    await page.waitForTimeout(500);
    textStart = (await page.locator("body").innerText().catch(() => "")).slice(0, 1200);
  } catch (error) {
    textStart = error.message;
  }
  directChecks.push({ url, status, finalUrl: page.url(), textStart });
}

await fs.writeFile(
  path.join(OUT_DIR, "public-help-screen-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records, directChecks }, null, 2),
);

await browser.close();
