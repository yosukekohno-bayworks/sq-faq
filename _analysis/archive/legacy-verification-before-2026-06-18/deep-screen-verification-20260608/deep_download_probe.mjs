import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const DOWNLOAD_DIR = path.join(OUT_DIR, "downloads");
const SCREEN_DIR = path.join(OUT_DIR, "download-screenshots");
await fs.mkdir(DOWNLOAD_DIR, { recursive: true });
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.env.SQ_PROFILE_DIR;
if (!profileDir) throw new Error("SQ_PROFILE_DIR is required");

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
  acceptDownloads: true,
});
const page = await context.newPage();
page.setDefaultTimeout(18000);

const targets = [
  {
    id: "sale_changes_csv",
    url: "/admin/csv_export/csv_export_operation_sale_changes",
  },
  {
    id: "point_changes_csv",
    url: "/admin/csv_export/csv_export_operation_point_changes",
  },
];

async function go(url) {
  await page.goto(`https://www.sqstackstaging.com${url}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(900);
}

async function bodyText() {
  return page.locator("body").innerText().catch((error) => String(error));
}

async function screenshot(name) {
  const file = path.join(SCREEN_DIR, `${name}.png`);
  await page.screenshot({ path: file, fullPage: true, animations: "disabled" }).catch(() => {});
  return path.relative(ROOT, file);
}

const records = [];
for (const [index, target] of targets.entries()) {
  const record = {
    index: index + 1,
    id: target.id,
    url: target.url,
    pageTextStart: "",
    downloadError: null,
    download: null,
    screenshots: [],
  };
  try {
    await go(target.url);
    record.pageTextStart = (await bodyText()).slice(0, 1800);
    record.screenshots.push(await screenshot(`${String(index + 1).padStart(2, "0")}-${target.id}-before`));
    const link = page.getByRole("link", { name: "ダウンロード", exact: true }).first();
    const count = await link.count();
    if (count === 0) {
      throw new Error("download link not found");
    }
    const [download] = await Promise.all([
      page.waitForEvent("download", { timeout: 20000 }),
      link.click(),
    ]);
    const suggested = download.suggestedFilename();
    const savePath = path.join(DOWNLOAD_DIR, `${target.id}-${suggested}`);
    await download.saveAs(savePath);
    const stat = await fs.stat(savePath);
    const buffer = await fs.readFile(savePath);
    record.download = {
      suggestedFilename: suggested,
      path: path.relative(ROOT, savePath),
      size: stat.size,
      headUtf8: buffer.subarray(0, 500).toString("utf8"),
    };
  } catch (error) {
    record.downloadError = error.message;
  }
  records.push(record);
  console.log(`${index + 1}/${targets.length} ${target.id} downloaded=${record.download ? "yes" : "no"} error=${record.downloadError || ""}`);
}

await fs.writeFile(
  path.join(OUT_DIR, "download-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2),
);

await context.close();
