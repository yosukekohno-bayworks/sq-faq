import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "pdf-packing-slip-screenshots");
const DOWNLOAD_DIR = path.join(OUT_DIR, "pdf-packing-slip-downloads");
await fs.mkdir(SCREEN_DIR, { recursive: true });
await fs.mkdir(DOWNLOAD_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const targets = {
  outbound:
    "https://www.sqstackstaging.com/admin/inventory_outbound_orders/9a7c1300-7218-58b7-ad39-0ec56bd30b13_InventoryOutboundOrder",
  pdfTop: "https://www.sqstackstaging.com/admin/pdf_export",
  pdfList: "https://www.sqstackstaging.com/admin/pdf_export/pdf_export_operation_packing_slips",
  yamatoExport:
    "https://www.sqstackstaging.com/admin/inventory_outbound_orders/export/yamato_b2_cloud",
};

const records = [];
const consoleLogs = [];
let shotIndex = 1;

function compact(items, limit = 260) {
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
      els.slice(0, 260).map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute("type") || "",
          role: el.getAttribute("role") || "",
          text: el.textContent?.trim().replace(/\s+/g, " ") || "",
          ariaLabel: el.getAttribute("aria-label") || "",
          title: el.getAttribute("title") || "",
          href: el.href || "",
          placeholder: el.getAttribute("placeholder") || "",
          value: el.value || "",
          disabled: el.disabled || el.getAttribute("aria-disabled") === "true",
          ariaDisabled: el.getAttribute("aria-disabled") || "",
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

async function snapshot(page, name, extra = {}) {
  const screenshotFile = path.join(SCREEN_DIR, `${String(shotIndex).padStart(2, "0")}-${slugify(name)}.png`);
  const text = await page.locator("body").innerText({ timeout: 12000 }).catch(() => "");
  await page.screenshot({ path: screenshotFile, fullPage: true, animations: "disabled" }).catch(() => {});
  const record = {
    name,
    url: page.url(),
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => [])),
    dialogs: compact(await page.locator('[role="dialog"]').allInnerTexts().catch(() => []), 80),
    controls: await getControls(page),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 220))
        .catch(() => []),
      220,
    ),
    links: await page
      .locator("a")
      .evaluateAll((els) =>
        els
          .map((a) => ({ text: a.textContent?.trim().replace(/\s+/g, " ") || "", href: a.href || "" }))
          .filter((a) => a.text || a.href)
          .slice(0, 260),
      )
      .catch(() => []),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(PDF|納品書|出荷|#IO|エクスポート|ダウンロード|完了|失敗|実行|ステータス|開始|終了|配送|メール|ヤマト|B2|CSV|アイテムが見つかりません|存在しない|予期せぬ|入力してください|選択してください)/.test(line),
        ),
      360,
    ),
    classification: {
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      notFound: text.includes("このページは存在しないようです"),
      empty: text.includes("アイテムが見つかりませんでした"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} url=${record.url} empty=${record.classification.empty}`);
  shotIndex += 1;
  return record;
}

async function tryOpenOutboundPdfMenu(page) {
  await goto(page, targets.outbound);
  await snapshot(page, "01-outbound-detail-before-menu");

  const menuButtons = [
    page.getByRole("button", { name: /その他|操作|アクション|メニュー|PDF|納品書/ }),
    page.locator('button[aria-label*="その他"], button[aria-label*="操作"], button[aria-label*="メニュー"], button[aria-label*="PDF"], button[aria-label*="納品書"]'),
  ];

  for (const locator of menuButtons) {
    const count = await locator.count().catch(() => 0);
    for (let index = 0; index < count; index += 1) {
      const item = locator.nth(index);
      if (!(await item.isVisible().catch(() => false))) continue;
      const disabled = await item.evaluate((el) => el.disabled || el.getAttribute("aria-disabled") === "true").catch(() => true);
      if (disabled) continue;
      await item.click({ timeout: 12000 }).catch(() => {});
      await settle(page);
      await snapshot(page, `02-outbound-menu-candidate-${index}`);
      const body = await page.locator("body").innerText().catch(() => "");
      if (/PDF|納品書|エクスポート/.test(body)) {
        const pdfItem = page.getByText(/PDF|納品書/).last();
        if (await pdfItem.isVisible().catch(() => false)) {
          await pdfItem.click({ timeout: 12000 }).catch(() => {});
          await settle(page);
          await snapshot(page, `03-outbound-pdf-action-after-click-${index}`);
          return;
        }
      }
    }
  }
}

async function fillYamatoExport(page) {
  await goto(page, targets.yamatoExport);
  await snapshot(page, "05-yamato-b2-export-form-before-submit");

  const inputs = page.locator("input");
  const count = await inputs.count().catch(() => 0);
  for (let index = 0; index < count; index += 1) {
    const input = inputs.nth(index);
    const type = await input.getAttribute("type").catch(() => "");
    const placeholder = await input.getAttribute("placeholder").catch(() => "");
    const labelText = await input
      .locator("xpath=ancestor::*[self::div][1]")
      .innerText()
      .catch(() => "");
    if (type === "datetime-local" || /開始日時/.test(labelText + placeholder)) {
      await input.fill("2026-06-09T00:00").catch(() => {});
    } else if (/終了日時/.test(labelText + placeholder)) {
      await input.fill("2026-06-10T00:00").catch(() => {});
    }
  }

  const selects = page.locator("select");
  const selectCount = await selects.count().catch(() => 0);
  for (let index = 0; index < selectCount; index += 1) {
    const select = selects.nth(index);
    const options = await select.locator("option").allInnerTexts().catch(() => []);
    if (options.some((option) => option.includes("出荷完了"))) {
      await select.selectOption({ label: "出荷完了" }).catch(async () => {
        const optionIndex = options.findIndex((option) => option.includes("出荷完了"));
        if (optionIndex >= 0) await select.selectOption({ index: optionIndex });
      });
    }
  }
  await settle(page);
  await snapshot(page, "06-yamato-b2-export-form-filled");

  const beforeUrl = page.url();
  await page.getByRole("button", { name: "実行する", exact: true }).click({ timeout: 20000 });
  await settle(page, 2500);
  await snapshot(page, "07-yamato-b2-export-after-submit", { beforeUrl });
}

async function inspectPdfListAndDownloads(page, name) {
  await goto(page, targets.pdfList);
  const listRecord = await snapshot(page, name);
  const downloadLinks = listRecord.links.filter((link) => /ダウンロード|download|PDF|pdf/i.test(`${link.text} ${link.href}`));
  const downloaded = [];
  for (const link of downloadLinks.slice(0, 3)) {
    const locator = page.locator(`a[href="${link.href}"]`).first();
    if (!(await locator.isVisible().catch(() => false))) continue;
    const downloadPromise = page.waitForEvent("download", { timeout: 10000 }).catch(() => null);
    await locator.click({ timeout: 10000 }).catch(() => {});
    const download = await downloadPromise;
    if (!download) continue;
    const suggested = download.suggestedFilename();
    const target = path.join(DOWNLOAD_DIR, suggested || `download-${Date.now()}.pdf`);
    await download.saveAs(target);
    downloaded.push({ text: link.text, href: link.href, suggestedFilename: suggested, savedAs: path.relative(ROOT, target) });
  }
  if (downloaded.length) {
    await snapshot(page, `${name}-after-download`, { downloaded });
  }
  return downloaded;
}

async function pollPdfListAndDownloads(page, attempts = 5) {
  const allDownloads = [];
  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    const downloaded = await inspectPdfListAndDownloads(page, `09-pdf-packing-slip-list-after-yamato-poll-${attempt}`);
    allDownloads.push(...downloaded);
    const body = await page.locator("body").innerText().catch(() => "");
    if (downloaded.length || !body.includes("アイテムが見つかりませんでした")) break;
    await page.waitForTimeout(15000);
  }
  return allDownloads;
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  ignoreHTTPSErrors: true,
  acceptDownloads: true,
});
const page = await context.newPage();
page.setDefaultTimeout(25000);
page.on("console", (msg) => {
  if (["error", "warning"].includes(msg.type())) {
    consoleLogs.push({ type: msg.type(), text: msg.text() });
  }
});
page.on("pageerror", (error) => {
  consoleLogs.push({ type: "pageerror", text: error.message });
});

let failed = null;
try {
  await tryOpenOutboundPdfMenu(page);
  await goto(page, targets.pdfTop);
  await snapshot(page, "04-pdf-export-top");
  await inspectPdfListAndDownloads(page, "04b-pdf-packing-slip-list-before-yamato");
  await fillYamatoExport(page);
  await goto(page, targets.yamatoExport);
  await snapshot(page, "08-yamato-b2-export-list-after-submit");
  const downloaded = await pollPdfListAndDownloads(page);
  await snapshot(page, "10-pdf-packing-slip-final-download-summary", { downloaded });
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "pdf-packing-slip-export-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), targets, failed, consoleLogs, records }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
