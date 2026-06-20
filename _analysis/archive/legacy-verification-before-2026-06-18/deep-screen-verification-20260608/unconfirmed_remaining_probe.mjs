import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-remaining-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const BASE = "https://www.sqstackstaging.com";

function compact(items, limit = 200) {
  return [...new Set(items.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(url) {
  return url
    .replace(/^\/admin\/?/, "")
    .replace(/[^A-Za-z0-9_-]+/g, "__")
    .replace(/^_+|_+$/g, "")
    .slice(0, 150) || "admin-root";
}

function pickLines(text) {
  return compact(
    text
      .split(/\n+/)
      .map((line) => line.trim())
      .filter((line) =>
        /(PDF|納品書|テンプレート|OmnibusCore|ロジザード|発注|注文|返品|会計|売上|権限|グループ|ユーザー|連携|同期|在庫|商品|顧客|テナント|カタログ|ロケーション|ロケーショングループ|予約|上限|閾値|有効期限|保存|追加|作成|編集|削除|接続|実行|選択|入力|アイテムが見つかりません|予期せぬ|存在しない|このページの準備が整いました)/.test(line),
      ),
    260,
  );
}

async function extract(page, url, index, note = "") {
  const fullUrl = url.startsWith("http") ? url : `${BASE}${url}`;
  const consoleMessages = [];
  const networkIssues = [];
  const responseHandler = async (response) => {
    const request = response.request();
    const responseUrl = response.url();
    const isInteresting =
      response.status() >= 400 ||
      responseUrl.includes("/graphql") ||
      responseUrl.includes("/api/");
    if (!isInteresting) return;
    let bodySample = "";
    if (response.status() >= 400 || responseUrl.includes("/graphql")) {
      bodySample = await response.text().catch(() => "");
      bodySample = bodySample.replace(/\s+/g, " ").slice(0, 800);
    }
    networkIssues.push({
      status: response.status(),
      method: request.method(),
      url: responseUrl.replace(BASE, ""),
      bodySample,
    });
  };
  const consoleHandler = (msg) => {
    if (["error", "warning"].includes(msg.type())) {
      consoleMessages.push(`${msg.type()}: ${msg.text()}`.slice(0, 700));
    }
  };

  page.on("response", responseHandler);
  page.on("console", consoleHandler);

  let responseStatus = null;
  let gotoError = "";
  try {
    const response = await page.goto(fullUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
    responseStatus = response?.status() ?? null;
    await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
    await page.waitForTimeout(1100);
  } catch (error) {
    gotoError = error.message;
  }

  const text = await page.locator("body").innerText().catch((error) => String(error));
  const screenshotFile = path.join(SCREEN_DIR, `${String(index).padStart(2, "0")}-${slugify(new URL(page.url()).pathname)}.png`);
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});

  const controls = await page.locator("input, textarea, select").evaluateAll((els) =>
    els.map((el) => {
      const id = el.getAttribute("id") || "";
      const label = id
        ? document.querySelector(`label[for="${CSS.escape(id)}"]`)?.textContent?.trim() || ""
        : "";
      const closestLabel = el.closest("label")?.textContent?.trim() || "";
      const formItem = el.closest("[class*=FormLayout], [class*=BlockStack], [class*=InlineStack], div")?.textContent?.trim() || "";
      return {
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute("type") || "",
        name: el.getAttribute("name") || "",
        label: label || closestLabel || el.getAttribute("aria-label") || "",
        context: formItem.replace(/\s+/g, " ").slice(0, 220),
        placeholder: el.getAttribute("placeholder") || "",
        checked: "checked" in el ? Boolean(el.checked) : null,
        disabled: Boolean(el.disabled),
        value:
          el.tagName.toLowerCase() === "select"
            ? Array.from(el.options || [])
                .map((o) => ({
                  text: o.textContent?.trim() || "",
                  value: o.value || "",
                  selected: Boolean(o.selected),
                }))
                .slice(0, 160)
            : el.tagName.toLowerCase() === "textarea"
              ? el.value.slice(0, 1000)
              : el.getAttribute("value") || "",
      };
    }),
  ).catch(() => []);

  const links = await page.locator("a").evaluateAll((els) =>
    els
      .map((a) => ({ text: a.textContent?.trim() || "", href: a.href || "" }))
      .filter((a) => a.text || a.href)
      .slice(0, 220),
  ).catch(() => []);

  page.off("response", responseHandler);
  page.off("console", consoleHandler);

  return {
    note,
    requestedUrl: url,
    finalUrl: page.url(),
    responseStatus,
    gotoError,
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    h2: compact(await page.locator("h2").allInnerTexts().catch(() => [])),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => []), 160),
    links,
    labels: compact(await page.locator("label").allInnerTexts().catch(() => []), 220),
    controls,
    controlSummary: {
      total: controls.length,
      checkboxes: controls.filter((c) => c.type === "checkbox").length,
      checked: controls.filter((c) => c.type === "checkbox" && c.checked).map((c) => c.label || c.context).slice(0, 160),
      unchecked: controls.filter((c) => c.type === "checkbox" && !c.checked).map((c) => c.label || c.context).slice(0, 160),
      selects: controls
        .filter((c) => c.tag === "select")
        .map((c) => ({
          label: c.label || c.context,
          options: Array.isArray(c.value) ? c.value.map((o) => o.text).filter(Boolean) : [],
        })),
    },
    classification: {
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      empty: text.includes("アイテムが見つかりませんでした"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    importantLines: pickLines(text),
    consoleMessages: compact(consoleMessages, 60),
    networkIssues: networkIssues.slice(0, 80),
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

const omnibusList = await extract(page, "/admin/omnibus_core_integrations", index++, "OmnibusCore list: collect real detail URL");
records.push(omnibusList);
const omnibusDetailHref = omnibusList.links.find((link) => /OmnibusCoreIntegration/.test(link.href))?.href;
if (omnibusDetailHref) {
  records.push(await extract(page, omnibusDetailHref, index++, "OmnibusCore detail reached from real list link"));
}

const targets = [
  ["/admin/logizard_integrations", "Logizard list"],
  ["/admin/logizard_integrations/create", "Logizard create form"],
  ["/admin/pdf_export", "PDF export top retry"],
  ["/admin/pdf_export/pdf_export_operation_packing_slips", "PDF packing slip export list"],
  ["/admin/settings/pdf_template_package_slip", "PDF package slip template settings"],
  ["/admin/draft_orders/create", "Draft order create route"],
  ["/admin/order_returns/create", "Order return create route"],
  ["/admin/sale_change_line_items/create", "Sale change line item create route"],
  ["/admin/settings/users/create", "User create form, no submit"],
];

for (const [url, note] of targets) {
  records.push(await extract(page, url, index++, note));
}

await fs.writeFile(
  path.join(OUT_DIR, "unconfirmed-remaining-records.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2),
);

for (const record of records) {
  console.log(
    `${record.note}: ${record.requestedUrl} -> h1=${record.h1.join(" / ")} class=${JSON.stringify(record.classification)} network=${record.networkIssues.length}`,
  );
}

await context.close();
