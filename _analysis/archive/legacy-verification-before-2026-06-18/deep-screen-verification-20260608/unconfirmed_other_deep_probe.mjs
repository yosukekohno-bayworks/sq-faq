import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260608");
const SCREEN_DIR = path.join(OUT_DIR, "unconfirmed-other-deep-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const targets = [
  "/admin/pdf_export",
  "/admin/pdf_export/pdf_export_operation_packing_slips",
  "/admin/pdf_export/pdf_export_operation_packing_slips/create",
  "/admin/pdf_export/pdf_export_operation_packing_slips/new",
  "/admin/settings/pdf_template_package_slip",
  "/admin/shopify_integrations",
  "/admin/shopify_integrations/create",
  "/admin/omnibus_core_integrations",
  "/admin/omnibus_core_integrations/TEST_MAKER_001",
  "/admin/omnibus_core_integrations/create",
  "/admin/smaregi_integrations",
  "/admin/smaregi_integrations/create",
  "/admin/recustomer_integrations",
  "/admin/recustomer_integrations/create",
  "/admin/logizard_integrations",
  "/admin/retail_portal_integrations",
  "/admin/retail_portal_integrations/create",
  "/admin/settings/permission_groups",
  "/admin/settings/permission_groups/434b6285-7690-535c-9adb-9899e62b9c01_PermissionGroup",
  "/admin/settings/permission_groups/f974f72a-838e-5bed-9202-1160c6fbe462_PermissionGroup",
  "/admin/settings/users/create",
];

function compact(items, limit = 180) {
  return [...new Set(items.map((x) => (x || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(url) {
  return url.replace(/^\/admin\/?/, "").replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 130) || "admin-root";
}

function important(text) {
  return compact(
    text
      .split(/\n+/)
      .map((line) => line.trim())
      .filter((line) =>
        /(PDF|納品書|テンプレート|Shopify|スマレジ|OmnibusCore|Recustomer|ロジザード|リテールポータル|権限|グループ|ユーザー|連携|同期|注文|在庫|商品|顧客|バーコード|ロケーション|カタログ|テナント|実行|保存|接続|追加|作成|アイテムが見つかりません|予期せぬ|存在しない|入力してください|選択してください|有効期限|編集を許可|必須)/.test(line),
      ),
    240,
  );
}

async function snapshot(page, url, index) {
  const fullUrl = `https://www.sqstackstaging.com${url}`;
  const consoleMessages = [];
  page.removeAllListeners("console");
  page.on("console", (msg) => {
    if (["error", "warning"].includes(msg.type())) {
      consoleMessages.push(`${msg.type()}: ${msg.text()}`.slice(0, 600));
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

  const text = await page.locator("body").innerText().catch((error) => String(error));
  const screenshotFile = path.join(SCREEN_DIR, `${String(index + 1).padStart(2, "0")}-${slugify(url)}.png`);
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});

  const controls = await page.locator("input, textarea, select").evaluateAll((els) =>
    els.map((el) => {
      const id = el.getAttribute("id") || "";
      const label = id
        ? document.querySelector(`label[for="${CSS.escape(id)}"]`)?.textContent?.trim() || ""
        : "";
      const nearest = el.closest("label")?.textContent?.trim() || "";
      return {
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute("type") || "",
        name: el.getAttribute("name") || "",
        label: label || nearest || el.getAttribute("aria-label") || "",
        placeholder: el.getAttribute("placeholder") || "",
        checked: "checked" in el ? Boolean(el.checked) : null,
        disabled: Boolean(el.disabled),
        value: el.tagName.toLowerCase() === "select"
          ? Array.from(el.options || []).map((o) => ({
            text: o.textContent?.trim() || "",
            value: o.value || "",
            selected: Boolean(o.selected),
          })).slice(0, 120)
          : el.getAttribute("value") || "",
      };
    }),
  ).catch(() => []);

  const checkedPermissionCount = controls.filter((c) => c.type === "checkbox" && c.checked && /権限/.test(c.label)).length;
  const uncheckedPermissionCount = controls.filter((c) => c.type === "checkbox" && !c.checked && /権限/.test(c.label)).length;

  return {
    url,
    finalUrl: page.url(),
    responseStatus,
    gotoError,
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    h2: compact(await page.locator("h2").allInnerTexts().catch(() => [])),
    buttons: compact(await page.locator("button").allInnerTexts().catch(() => []), 120),
    links: await page.locator("a").evaluateAll((els) =>
      els.map((a) => ({ text: a.textContent?.trim() || "", href: a.href || "" })).filter((a) => a.text || a.href).slice(0, 180),
    ).catch(() => []),
    labels: compact(await page.locator("label").allInnerTexts().catch(() => []), 180),
    controls,
    controlSummary: {
      total: controls.length,
      checkboxes: controls.filter((c) => c.type === "checkbox").length,
      checkedPermissionCount,
      uncheckedPermissionCount,
      selects: controls.filter((c) => c.tag === "select").map((c) => ({
        label: c.label,
        options: Array.isArray(c.value) ? c.value.map((o) => o.text).filter(Boolean) : [],
      })),
    },
    classification: {
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      empty: text.includes("アイテムが見つかりませんでした"),
    },
    importantLines: important(text),
    consoleMessages: compact(consoleMessages, 40),
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
page.setDefaultTimeout(18000);

const records = [];
for (const [index, url] of targets.entries()) {
  const record = await snapshot(page, url, index);
  records.push(record);
  console.log(`${index + 1}/${targets.length} ${url} h1=${record.h1.join(" / ")} ${JSON.stringify(record.classification)}`);
}

await fs.writeFile(path.join(OUT_DIR, "unconfirmed-other-deep-records.json"), JSON.stringify({ generatedAt: new Date().toISOString(), records }, null, 2));
await context.close();
