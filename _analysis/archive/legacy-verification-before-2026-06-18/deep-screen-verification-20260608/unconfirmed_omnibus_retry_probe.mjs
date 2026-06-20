import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-omnibus-retry-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const BASE = "https://www.sqstackstaging.com";
const targets = [
  "/admin",
  "/admin/omnibus_core_integrations",
  "/admin/omnibus_core_integrations/703c48d1-ffad-55d2-8683-613762453668_OmnibusCoreIntegration",
  "/admin/omnibus_core_integrations/create",
];

function compact(items, limit = 180) {
  return [...new Set(items.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(url) {
  return url.replace(/^\/admin\/?/, "").replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 150) || "admin-root";
}

function pickLines(text) {
  return compact(
    text
      .split(/\n+/)
      .map((line) => line.trim())
      .filter((line) =>
        /(OmnibusCore|TEST_MAKER_001|テナント|カタログ|ロケーション|予約|販売上限|下書き注文|有効期限|連携|接続|保存|追加|編集|削除|作成|選択してください|予期せぬ|アイテムが見つかりません|このページの準備が整いました)/.test(line),
      ),
    260,
  );
}

async function snapshot(page, url, index) {
  const networkIssues = [];
  page.removeAllListeners("response");
  page.on("response", async (response) => {
    const responseUrl = response.url();
    if (response.status() < 400 && !responseUrl.includes("/graphql")) return;
    networkIssues.push({
      status: response.status(),
      method: response.request().method(),
      url: responseUrl.replace(BASE, ""),
      bodySample: (await response.text().catch(() => "")).replace(/\s+/g, " ").slice(0, 700),
    });
  });

  const response = await page.goto(`${BASE}${url}`, { waitUntil: "domcontentloaded", timeout: 60000 }).catch(() => null);
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(1000);

  let text = await page.locator("body").innerText().catch(() => "");
  if (text.includes("予期せぬエラーが発生しました")) {
    await page.reload({ waitUntil: "domcontentloaded", timeout: 60000 }).catch(() => {});
    await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
    await page.waitForTimeout(1200);
    text = await page.locator("body").innerText().catch(() => "");
  }

  const screenshotFile = path.join(SCREEN_DIR, `${String(index).padStart(2, "0")}-${slugify(url)}.png`);
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});

  const controls = await page.locator("input, textarea, select").evaluateAll((els) =>
    els.map((el) => {
      const id = el.getAttribute("id") || "";
      const label = id
        ? document.querySelector(`label[for="${CSS.escape(id)}"]`)?.textContent?.trim() || ""
        : "";
      const closestLabel = el.closest("label")?.textContent?.trim() || "";
      return {
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute("type") || "",
        label: label || closestLabel || el.getAttribute("aria-label") || "",
        checked: "checked" in el ? Boolean(el.checked) : null,
        value:
          el.tagName.toLowerCase() === "select"
            ? Array.from(el.options || []).map((o) => ({ text: o.textContent?.trim() || "", selected: Boolean(o.selected) }))
            : el.getAttribute("value") || "",
      };
    }),
  ).catch(() => []);

  return {
    requestedUrl: url,
    finalUrl: page.url(),
    status: response?.status() ?? null,
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    h2: compact(await page.locator("h2").allInnerTexts().catch(() => [])),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => []), 120),
    labels: compact(await page.locator("label").allInnerTexts().catch(() => []), 180),
    links: await page.locator("a").evaluateAll((els) =>
      els.map((a) => ({ text: a.textContent?.trim() || "", href: a.href || "" })).filter((a) => a.text || a.href).slice(0, 180),
    ).catch(() => []),
    controlSummary: {
      total: controls.length,
      selects: controls
        .filter((c) => c.tag === "select")
        .map((c) => ({ label: c.label, options: Array.isArray(c.value) ? c.value.map((o) => o.text).filter(Boolean) : [] })),
      checkboxes: controls.filter((c) => c.type === "checkbox").map((c) => ({ label: c.label, checked: c.checked })),
    },
    classification: {
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      empty: text.includes("アイテムが見つかりませんでした"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    importantLines: pickLines(text),
    networkIssues,
    screenshot: path.relative(ROOT, screenshotFile),
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
let index = 1;
for (const target of targets) {
  const record = await snapshot(page, target, index++);
  records.push(record);
  console.log(`${target} h1=${record.h1.join(" / ")} class=${JSON.stringify(record.classification)} network=${record.networkIssues.length}`);
}

await fs.writeFile(
  path.join(OUT_DIR, "unconfirmed-omnibus-retry-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2),
);
await context.close();
