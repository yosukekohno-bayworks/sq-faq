import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "csv-pdf-current-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const base = "https://www.sqstackstaging.com";

const importOps = [
  ["products", "商品"],
  ["product_variants", "商品バリエーション"],
  ["product_images", "商品画像", "radio-image"],
  ["product_variant_images", "商品バリエーション画像", "radio-image"],
  ["catalog_products", "カタログ"],
  ["product_price_rule_regular_prices", "販売価格-通常"],
  ["product_price_rule_sale_prices", "販売価格-セール"],
  ["inventory_unit_costs", "原価"],
  ["inventory_threshold_rule_product_variants", "販売閾値"],
  ["inventory_logical_available_quantities", "販売可能在庫", "radio-inventory"],
  ["inventory_back_order_rule_product_variants", "予約販売"],
  ["product_metafields", "商品メタフィールド"],
  ["product_variant_metafields", "商品バリエーションメタフィールド"],
  ["fulfillment_by_yamato_b2_clouds", "ヤマトB2クラウド"],
  ["fulfillment_by_dhls", "DHL"],
  ["point_pluses", "ポイント一括付与"],
  ["point_campaign_order_rule_point_value_product_variants", "キャンペーン対象商品", "open-picker"],
  ["customer_rank_baselines", "基準ランク"],
  ["users", "管理ユーザー"],
  ["locations", "ロケーション"],
];

const exportOps = [
  ["inventory_logical_quantities", "在庫", "open-picker"],
  ["location_by_location_group", "ロケーション", "open-picker"],
  ["order_price_adjustment_usages", "ディスカウント利用履歴", "open-picker"],
  ["product_variants", "商品バリエーション", "toggle-product-info"],
  ["product_price_rule_sale_prices", "セール価格"],
  ["inventory_outbound_order_yamato_b2_clouds", "ヤマトB2クラウド", "history-only"],
  ["sale_changes", "売上実績-注文軸"],
  ["point_changes", "ポイント変動履歴"],
];

const targets = [
  { name: "csv-import-top", url: `${base}/admin/csv_import` },
  ...importOps.flatMap(([op, label, action]) => [
    { name: `csv-import-${op}-list`, label, url: `${base}/admin/csv_import/csv_import_operation_${op}` },
    { name: `csv-import-${op}-create`, label, url: `${base}/admin/csv_import/csv_import_operation_${op}/create`, action },
  ]),
  { name: "csv-export-top", url: `${base}/admin/csv_export` },
  ...exportOps.flatMap(([op, label, action]) => {
    const list = { name: `csv-export-${op}-list`, label, url: `${base}/admin/csv_export/csv_export_operation_${op}` };
    if (action === "history-only") {
      return [list, { name: `csv-export-${op}-create-direct`, label, url: `${base}/admin/csv_export/csv_export_operation_${op}/create` }];
    }
    return [list, { name: `csv-export-${op}-create`, label, url: `${base}/admin/csv_export/csv_export_operation_${op}/create`, action }];
  }),
  { name: "outbound-yamato-condition-export", url: `${base}/admin/inventory_outbound_orders/export/yamato_b2_cloud` },
  { name: "pdf-export-top", url: `${base}/admin/pdf_export` },
  { name: "pdf-packing-slips-list", url: `${base}/admin/pdf_export/pdf_export_operation_packing_slips` },
  { name: "pdf-packing-slips-create-direct", url: `${base}/admin/pdf_export/pdf_export_operation_packing_slips/create` },
  { name: "pdf-template-package-slip", url: `${base}/admin/settings/pdf_template_package_slip` },
];

const records = [];
const network = [];
const consoleLogs = [];
let shotIndex = 1;

function compact(items, limit = 320) {
  return [...new Set(items.map((item) => (item || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(value) {
  return value.replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 150) || "screen";
}

async function settle(page, extraMs = 900) {
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(extraMs);
}

async function goto(page, url) {
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
}

async function getControls(page) {
  return await page
    .locator("button, a, input, select, textarea")
    .evaluateAll((els) =>
      els.slice(0, 520).map((el) => {
        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);
        return {
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute("type") || "",
          name: el.getAttribute("name") || "",
          role: el.getAttribute("role") || "",
          text: el.textContent?.trim().replace(/\s+/g, " ") || "",
          ariaLabel: el.getAttribute("aria-label") || "",
          title: el.getAttribute("title") || "",
          href: el.href || "",
          placeholder: el.getAttribute("placeholder") || "",
          value: String(el.value || "").slice(0, 800),
          valueLength: String(el.value || "").length,
          checked: el.checked || false,
          disabled:
            el.disabled ||
            el.getAttribute("aria-disabled") === "true" ||
            String(el.className || "").includes("disabled") ||
            false,
          visible:
            style.visibility !== "hidden" &&
            style.display !== "none" &&
            rect.width > 0 &&
            rect.height > 0,
          bbox: {
            x: Math.round(rect.x),
            y: Math.round(rect.y),
            width: Math.round(rect.width),
            height: Math.round(rect.height),
          },
        };
      }),
    )
    .catch(() => []);
}

async function getSelectOptions(page) {
  return await page
    .locator("select")
    .evaluateAll((selects) =>
      selects.slice(0, 80).map((select, index) => ({
        index,
        name: select.getAttribute("name") || "",
        value: select.value || "",
        disabled: select.disabled,
        context:
          select.closest("label")?.textContent?.trim().replace(/\s+/g, " ") ||
          select.closest("fieldset, section, form, div")?.textContent?.trim().replace(/\s+/g, " ").slice(0, 700) ||
          "",
        options: Array.from(select.options).map((option) => ({
          text: option.textContent?.trim().replace(/\s+/g, " ") || "",
          value: option.value || "",
          disabled: option.disabled,
        })),
      })),
    )
    .catch(() => []);
}

async function snapshot(page, name, requestedUrl, extra = {}) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(shotIndex).padStart(2, "0")}-${slugify(name)}.png`);
  const text = await page.locator("body").innerText({ timeout: 12000 }).catch(() => "");
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const controls = await getControls(page);
  const record = {
    name,
    requestedUrl,
    url: page.url(),
    title: await page.title().catch(() => ""),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => []), 30),
    h2: compact(await page.locator("h2").allInnerTexts().catch(() => []), 120),
    h3: compact(await page.locator("h3").allInnerTexts().catch(() => []), 160),
    dialogs: compact(await page.locator('[role="dialog"], [role="menu"]').allInnerTexts().catch(() => []), 120),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 360))
        .catch(() => []),
      360,
    ),
    controls,
    links: controls.filter((control) => control.tag === "a" && control.href).map((control) => ({ text: control.text, href: control.href })),
    templateLinks: controls
      .filter((control) => control.tag === "a" && /docs\.google\.com|テンプレート/.test(`${control.href} ${control.text}`))
      .map((control) => ({ text: control.text, href: control.href })),
    fileInputs: controls
      .filter((control) => control.type === "file")
      .map((control) => ({ name: control.name, ariaLabel: control.ariaLabel, valueLength: control.valueLength, visible: control.visible })),
    checkedInputs: controls
      .filter((control) => control.checked)
      .map((control) => ({ type: control.type, text: control.text, ariaLabel: control.ariaLabel, value: control.value, disabled: control.disabled })),
    disabledControls: controls
      .filter((control) => control.disabled && /(button|select|radio|checkbox|file|datetime-local|number)/.test(`${control.tag} ${control.type}`))
      .map((control) => ({ tag: control.tag, type: control.type, text: control.text, ariaLabel: control.ariaLabel, value: control.value })),
    selectOptions: await getSelectOptions(page),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(CSV|PDF|インポート|エクスポート|テンプレート|新規|履歴|実行|作成|保存|ファイル|選択|検索|ドラッグ|ドロップ|反映|絶対値|差分値|画像|上書き|追加|商品|バリエーション|カタログ|価格|原価|販売閾値|販売可能|予約販売|メタフィールド|ヤマト|DHL|ポイント|キャンペーン|基準ランク|管理ユーザー|ロケーション|ディスカウント|売上実績|注文軸|テナント|開始日時|終了日時|HTMLテンプレート|納品書|アイテムが見つかりません|このページの準備が整いました|このページは存在しない|予期せぬエラー|Application error|エラー)/.test(
            line,
          ),
        ),
      520,
    ),
    classification: {
      empty: text.includes("アイテムが見つかりませんでした"),
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(
    `${record.name}: h1=${record.h1.join(" / ")} url=${record.url} empty=${record.classification.empty} notFound=${record.classification.notFound} unexpected=${record.classification.unexpectedError}`,
  );
  shotIndex += 1;
  return record;
}

async function clickText(page, textRe, targetName, requestedUrl) {
  const candidate = page.getByText(textRe).first();
  if (!(await candidate.isVisible().catch(() => false))) return false;
  await candidate.click({ timeout: 12000 }).catch(() => {});
  await settle(page, 800);
  await snapshot(page, `${targetName}-after-${slugify(String(textRe))}`, requestedUrl, { action: "click-text", textRe: String(textRe) });
  return true;
}

async function openPicker(page, targetName, requestedUrl) {
  const buttons = page.locator("button");
  const count = await buttons.count().catch(() => 0);
  for (let index = 0; index < count; index += 1) {
    const button = buttons.nth(index);
    if (!(await button.isVisible().catch(() => false))) continue;
    const meta = await button
      .evaluate((el) => ({
        text: el.textContent?.trim().replace(/\s+/g, " ") || "",
        ariaLabel: el.getAttribute("aria-label") || "",
        disabled: el.disabled || el.getAttribute("aria-disabled") === "true",
      }))
      .catch(() => null);
    if (!meta || meta.disabled) continue;
    const label = `${meta.text} ${meta.ariaLabel}`;
    if (!/(選択|検索)/.test(label)) continue;
    if (/ファイル|保存|エクスポート|実行|削除|開始/.test(label)) continue;
    await button.click({ timeout: 12000 }).catch(() => {});
    await settle(page, 1000);
    await snapshot(page, `${targetName}-picker-opened`, requestedUrl, { action: "open-picker", clickedButton: meta });
    await page.keyboard.press("Escape").catch(() => {});
    await settle(page, 500);
    return true;
  }
  return false;
}

async function runAction(page, target) {
  if (target.action === "open-picker") {
    await openPicker(page, target.name, target.url);
    return;
  }
  if (target.action === "radio-image") {
    await clickText(page, /^画像を上書きする$/, target.name, target.url);
    await clickText(page, /^画像を追加する$/, target.name, target.url);
    return;
  }
  if (target.action === "radio-inventory") {
    await clickText(page, /^差分値で反映する$/, target.name, target.url);
    await clickText(page, /^絶対値で反映する$/, target.name, target.url);
    return;
  }
  if (target.action === "toggle-product-info") {
    await clickText(page, /商品情報を含める/, target.name, target.url);
  }
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
});

const page = await context.newPage();
page.setDefaultTimeout(25000);

page.on("console", (msg) => {
  if (["error", "warning"].includes(msg.type())) {
    consoleLogs.push({ type: msg.type(), text: msg.text().slice(0, 2000) });
  }
});

page.on("response", async (response) => {
  const url = response.url();
  if (!/graphql|csv_import|csv_export|pdf_export|pdf_template|yamato_b2_cloud/.test(url) && response.status() < 400) return;
  let body = "";
  if (/graphql|api/.test(url) || response.status() >= 400) {
    body = await response.text().catch(() => "");
  }
  network.push({
    url,
    method: response.request().method(),
    status: response.status(),
    postData: (response.request().postData() || "").slice(0, 5000),
    body: body.slice(0, 12000),
  });
});

let failed = null;

try {
  records.push({
    name: "mutation-boundary",
    note: "This probe opens list/create/form pages, toggles local radio/checkbox controls, and opens selection dialogs only. It does not click save/export/delete/execute buttons.",
  });

  for (const target of targets) {
    await goto(page, target.url);
    await snapshot(page, target.name, target.url, { label: target.label || null, action: target.action || null });
    await runAction(page, target);
  }
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", page.url(), { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "csv-pdf-current-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), targets, failed, consoleLogs, network, records }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
