import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-csv-import-error-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const previous = JSON.parse(await fs.readFile(path.join(OUT_DIR, "unconfirmed-valid-csv-import-record.json"), "utf8"));
const detailUrl = previous.detailUrl;
if (!detailUrl) throw new Error("No detailUrl in previous record.");

function compact(lines, limit = 160) {
  return [...new Set(lines.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

async function text(page) {
  return page.locator("body").innerText().catch((error) => String(error));
}

async function shot(page, name) {
  const file = path.join(SCREEN_DIR, `${name}.png`);
  await page.screenshot({ path: file, fullPage: true, animations: "disabled" }).catch(() => {});
  return path.relative(ROOT, file);
}

function important(body) {
  return compact(
    body
      .split(/\n+/)
      .map((line) => line.trim())
      .filter((line) =>
        /(CSV|インポート|商品|検証|実行|成功|失敗|エラー|0個|1個|作成日|ステータス|command|product_code|title|option|必須|無効|不正|TEST_FAQ|ファイル|行|列|詳細)/.test(line),
      ),
    220,
  );
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});
const page = await context.newPage();
page.setDefaultTimeout(16000);

const record = { generatedAt: new Date().toISOString(), detailUrl, steps: [], error: null };

try {
  await page.goto(detailUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(1000);
  const links = await page.locator("a").evaluateAll((els) =>
    els.map((a) => ({ text: a.textContent?.trim() || "", href: a.href || "" })).filter((a) => a.text || a.href),
  );
  record.steps.push({
    step: "detail",
    url: page.url(),
    text: important(await text(page)),
    links,
    screenshot: await shot(page, "01-detail"),
  });

  const failureLink = links.find((a) => /0個の商品|検証失敗|失敗/.test(a.text) && /csv_import/.test(a.href));
  if (failureLink) {
    await page.goto(failureLink.href, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(1000);
    record.steps.push({
      step: "failure-link",
      url: page.url(),
      text: important(await text(page)),
      links: await page.locator("a").evaluateAll((els) =>
        els.map((a) => ({ text: a.textContent?.trim() || "", href: a.href || "" })).filter((a) => a.text || a.href),
      ).catch(() => []),
      screenshot: await shot(page, "02-failure-link"),
    });
  }
} catch (error) {
  record.error = error.message;
  record.steps.push({ step: "error", url: page.url(), text: important(await text(page)), screenshot: await shot(page, "99-error") });
}

await fs.writeFile(path.join(OUT_DIR, "unconfirmed-csv-import-error-detail-record.json"), JSON.stringify(record, null, 2));
await context.close();
