import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "admin-screenshots");
const checklist = JSON.parse(
  await fs.readFile(path.join(OUT_DIR, "admin-url-checklist.json"), "utf8"),
);

await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.env.SQ_PROFILE_DIR;
if (!profileDir) {
  throw new Error("SQ_PROFILE_DIR is required");
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});

const page = await context.newPage();
page.setDefaultTimeout(15000);

function slugify(url) {
  return url
    .replace(/^\/admin\/?/, "")
    .replace(/[^A-Za-z0-9_-]+/g, "__")
    .replace(/^_+|_+$/g, "")
    .slice(0, 140) || "admin-root";
}

function compact(items, limit = 80) {
  return [...new Set(items.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

async function getAllText(selector) {
  return page.locator(selector).allInnerTexts().catch(() => []);
}

async function safeScreenshot(file) {
  try {
    await page.screenshot({ path: file, fullPage: true, animations: "disabled" });
    return path.relative(ROOT, file);
  } catch (error) {
    return `screenshot-error: ${error.message}`;
  }
}

const records = [];
for (const [index, url] of checklist.uniqueStaticUrls.entries()) {
  const fullUrl = `https://www.sqstackstaging.com${url}`;
  const started = Date.now();
  const errors = [];
  page.removeAllListeners("console");
  page.on("console", (msg) => {
    if (["error", "warning"].includes(msg.type())) {
      errors.push(`${msg.type()}: ${msg.text()}`.slice(0, 500));
    }
  });

  let responseStatus = null;
  let gotoError = null;
  try {
    const response = await page.goto(fullUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
    responseStatus = response?.status() ?? null;
    await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(900);
  } catch (error) {
    gotoError = error.message;
  }

  const bodyText = await page.locator("body").innerText().catch((error) => String(error));
  const h1 = compact(await getAllText("h1"));
  const h2 = compact(await getAllText("h2"));
  const buttons = compact(await getAllText("button"), 120);
  const links = compact(await getAllText("a"), 120);
  const labels = compact(await getAllText("label"), 120);
  const tableHeaders = compact(await getAllText("th"), 120);
  const inputs = await page
    .locator("input, textarea, select")
    .evaluateAll((els) =>
      els.slice(0, 160).map((el) => ({
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute("type") || "",
        name: el.getAttribute("name") || "",
        placeholder: el.getAttribute("placeholder") || "",
        value: el.tagName.toLowerCase() === "select"
          ? Array.from(el.options || []).map((o) => o.textContent?.trim()).filter(Boolean).slice(0, 40)
          : "",
        ariaLabel: el.getAttribute("aria-label") || "",
        disabled: Boolean(el.disabled),
      })),
    )
    .catch(() => []);

  const fileName = `${String(index + 1).padStart(3, "0")}-${slugify(url)}.png`;
  const screenshot = await safeScreenshot(path.join(SCREEN_DIR, fileName));
  const lower = bodyText.toLowerCase();
  const record = {
    index: index + 1,
    url,
    fullUrl,
    finalUrl: page.url(),
    responseStatus,
    gotoError,
    title: await page.title().catch(() => ""),
    h1,
    h2,
    classification: {
      login: /ログイン|メールアドレス|パスワード/.test(bodyText),
      notFound: bodyText.includes("このページは存在しないようです"),
      unexpectedError: bodyText.includes("予期せぬエラーが発生しました"),
      todo: /^TODO$/m.test(bodyText) || bodyText.includes("\nTODO\n"),
      empty: bodyText.includes("アイテムが見つかりませんでした"),
      graphql: lower.includes("graphql") || bodyText.includes("GraphQL"),
    },
    buttons,
    links,
    labels,
    tableHeaders,
    inputs,
    textStart: bodyText.slice(0, 2200),
    consoleErrors: compact(errors, 30),
    screenshot,
    durationMs: Date.now() - started,
  };
  records.push(record);
  console.log(`${index + 1}/${checklist.uniqueStaticUrls.length} ${url} ${record.h1.join(" / ")} ${JSON.stringify(record.classification)}`);
}

await fs.writeFile(
  path.join(OUT_DIR, "admin-screen-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2),
);
await context.close();
