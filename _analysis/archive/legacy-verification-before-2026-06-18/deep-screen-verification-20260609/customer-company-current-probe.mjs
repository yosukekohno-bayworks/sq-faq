import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "customer-company-current-screenshots");
await fs.rm(SCREEN_DIR, { recursive: true, force: true });
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const base = "https://www.sqstackstaging.com";
const knownCompanyUrl = `${base}/admin/companies/9481aa92-6e9d-5c81-9aca-68be833882c3_Company`;
const knownContactUrl = `${knownCompanyUrl}/contacts/b7732de6-f920-5983-af16-e7959b0a62e5_CompanyContact`;
const records = [];
const network = [];
const consoleLogs = [];
let shotIndex = 1;

function compact(items, limit = 280) {
  return [...new Set(items.map((item) => (item || "").trim()).filter(Boolean))].slice(0, limit);
}

function slugify(value) {
  return value.replace(/[^A-Za-z0-9_-]+/g, "__").replace(/^_+|_+$/g, "").slice(0, 150) || "screen";
}

function safeUrl(url) {
  try {
    const parsed = new URL(url);
    if (parsed.hostname.includes("clerk")) parsed.search = "";
    if (parsed.searchParams.has("__session")) parsed.searchParams.set("__session", "[redacted]");
    return parsed.toString();
  } catch {
    return url;
  }
}

async function settle(page, extraMs = 800) {
  await page.waitForLoadState("domcontentloaded", { timeout: 60000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(extraMs);
}

async function goto(page, url) {
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await settle(page);
}

async function waitForBodyText(page, pattern, timeoutMs = 30000) {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    const text = await page.locator("body").innerText({ timeout: 5000 }).catch(() => "");
    if (pattern.test(text)) return true;
    await page.waitForTimeout(500);
  }
  return false;
}

async function getControls(page) {
  return await page
    .locator("button, a, input, select, textarea")
    .evaluateAll((els) =>
      els.slice(0, 620).map((el) => {
        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);
        return {
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute("type") || "",
          role: el.getAttribute("role") || "",
          text: el.textContent?.trim().replace(/\s+/g, " ") || "",
          ariaLabel: el.getAttribute("aria-label") || "",
          title: el.getAttribute("title") || "",
          href: el.href || "",
          placeholder: el.getAttribute("placeholder") || "",
          value: String(el.value || "").slice(0, 420),
          checked: el.checked || false,
          disabled: el.disabled || el.getAttribute("aria-disabled") === "true" || false,
          visible:
            style.visibility !== "hidden" &&
            style.display !== "none" &&
            rect.width > 0 &&
            rect.height > 0,
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
        value: select.value || "",
        disabled: select.disabled,
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
    h1: compact(await page.locator("h1").allInnerTexts().catch(() => []), 40),
    h2: compact(await page.locator("h2").allInnerTexts().catch(() => []), 160),
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
    buttons: controls.filter((control) => control.tag === "button").map((control) => ({ text: control.text, ariaLabel: control.ariaLabel, disabled: control.disabled, visible: control.visible })),
    checkedInputs: controls.filter((control) => control.checked).map((control) => ({ type: control.type, value: control.value, text: control.text, ariaLabel: control.ariaLabel })),
    selectOptions: await getSelectOptions(page),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(顧客|会社|担当者|ロケーション|注文|売上|販売合計|作成日|インポート|ポイント一括付与|メールアドレス|会員証|メタフィールド|会社名|会社ID|配送先住所|請求先住所|配送先住所と同じ|国\/地域|都道府県|市区町村|住所|電話番号|保存する|キャンセル|アイテムが見つかりません|注文が見つかりません|このページの準備が整いました|予期せぬエラー|このページは存在しない|TODO|UUID|未設定|メモ)/.test(
            line,
          ),
        ),
      560,
    ),
    classification: {
      empty: text.includes("アイテムが見つかりませんでした") || text.includes("注文が見つかりませんでした"),
      notFound: text.includes("このページは存在しないようです"),
      unexpectedError: text.includes("予期せぬエラーが発生しました") || text.includes("Application error"),
      readyMessage: text.includes("このページの準備が整いました"),
    },
    screenshot: path.relative(ROOT, screenshotFile),
    ...extra,
  };
  records.push(record);
  console.log(`${record.name}: h1=${record.h1.join(" / ")} url=${record.url} empty=${record.classification.empty} notFound=${record.classification.notFound} unexpected=${record.classification.unexpectedError}`);
  shotIndex += 1;
  return record;
}

async function clickButton(page, nameRe, name) {
  const locator = page.getByRole("button", { name: nameRe }).first();
  if (!(await locator.isVisible().catch(() => false))) return false;
  await locator.click({ timeout: 5000 }).catch(() => {});
  await settle(page, 500);
  console.log(`clicked: ${name}`);
  return true;
}

async function clickText(page, textRe, name) {
  const locator = page.getByText(textRe).first();
  if (!(await locator.isVisible().catch(() => false))) return false;
  await locator.click({ timeout: 5000 }).catch(() => {});
  await settle(page, 700);
  console.log(`clicked: ${name}`);
  return true;
}

async function firstHref(page, pattern, exclude = []) {
  const hrefs = await page.locator("a").evaluateAll((els) => els.map((el) => el.href).filter(Boolean)).catch(() => []);
  return [...new Set(hrefs)].find((href) => pattern.test(href) && exclude.every((item) => !href.includes(item))) || null;
}

const context = await chromium.launchPersistentContext(profileDir, {
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
  viewport: { width: 1440, height: 1100 },
  locale: "ja-JP",
  timezoneId: "Asia/Tokyo",
  acceptDownloads: false,
});

context.on("page", (page) => {
  page.on("console", (message) => {
    if (message.type() === "error") consoleLogs.push({ type: message.type(), text: message.text().slice(0, 600) });
  });
  page.on("response", (response) => {
    if (response.status() >= 400) network.push({ status: response.status(), url: safeUrl(response.url()), method: response.request().method() });
  });
});

const page = context.pages()[0] || (await context.newPage());
page.on("console", (message) => {
  if (message.type() === "error") consoleLogs.push({ type: message.type(), text: message.text().slice(0, 600) });
});
page.on("response", (response) => {
  if (response.status() >= 400) network.push({ status: response.status(), url: safeUrl(response.url()), method: response.request().method() });
});

try {
  await goto(page, `${base}/admin/purchasing_customers`);
  await snapshot(page, "customers-list", `${base}/admin/purchasing_customers`);
  await clickButton(page, /^インポート$/, "customers-import");
  await snapshot(page, "customers-import-opened", `${base}/admin/purchasing_customers`, { action: "open-import" });
  await page.keyboard.press("Escape").catch(() => {});
  await settle(page, 300);
  await clickButton(page, /検索と絞り込みの結果/, "customers-filter");
  await snapshot(page, "customers-filter-opened", `${base}/admin/purchasing_customers`, { action: "open-filter" });
  await clickButton(page, /絞り込みを追加/, "customers-add-filter");
  await snapshot(page, "customers-filter-menu-opened", `${base}/admin/purchasing_customers`, { action: "open-filter-menu" });
  await goto(page, `${base}/admin/purchasing_customers/create`);
  await snapshot(page, "customers-create-direct", `${base}/admin/purchasing_customers/create`);

  await goto(page, `${base}/admin/companies`);
  await snapshot(page, "companies-list", `${base}/admin/companies`);
  await clickButton(page, /^インポート$/, "companies-import");
  await snapshot(page, "companies-import-clicked", `${base}/admin/companies`, { action: "click-import" });
  await goto(page, `${base}/admin/companies/create`);
  await snapshot(page, "company-create", `${base}/admin/companies/create`);
  const sameAddress = page.getByLabel(/配送先住所と同じ/).first();
  if (await sameAddress.isVisible().catch(() => false)) {
    await sameAddress.click({ timeout: 5000 }).catch(() => {});
    await settle(page, 500);
    await snapshot(page, "company-create-billing-expanded", `${base}/admin/companies/create`, { action: "toggle-billing-address" });
  }

  await goto(page, `${base}/admin/companies`);
  await clickText(page, /TEST_FAQ_株式会社テスト|TEST_FAQ/, "company-row");
  if (!/\/admin\/companies\/[^/?#]+$/.test(page.url())) {
    const companyHref = await firstHref(page, /\/admin\/companies\/[^/?#]+$/, ["/create"]);
    if (companyHref) await goto(page, companyHref);
  }
  await waitForBodyText(page, /直近の注文|会社ID|担当者を追加|ロケーションを追加/, 30000);
  await snapshot(page, "company-detail-first", page.url());
  const companyUrl = page.url();

  await clickButton(page, /担当者を追加/, "company-add-contact");
  await waitForBodyText(page, /担当者を作成する|メールアドレス|発注の確認メール/, 15000);
  await snapshot(page, "company-add-contact-dialog-opened", companyUrl, { action: "open-add-contact" });

  await goto(page, companyUrl);
  await waitForBodyText(page, /直近の注文|会社ID|担当者を追加|ロケーションを追加/, 30000);
  const locationHref = await firstHref(page, /\/admin\/companies\/[^/?#]+\/locations\/[^/?#]+$/, ["/create"]);
  if (locationHref) {
    await goto(page, locationHref);
    await waitForBodyText(page, /ロケーションID|配送先住所|請求先住所|直近の注文/, 30000);
    await snapshot(page, "company-location-detail-first", locationHref);
  } else {
    records.push({ name: "company-location-detail-first", note: "No company location detail link found.", url: companyUrl });
  }

  await goto(page, `${companyUrl}/locations/create`);
  await waitForBodyText(page, /新しいロケーション|ロケーション名|配送先住所|請求先住所/, 30000);
  await snapshot(page, "company-location-create", `${companyUrl}/locations/create`);

  await goto(page, companyUrl);
  await waitForBodyText(page, /直近の注文|会社ID|担当者を追加|ロケーションを追加/, 30000);
  const contactHref = await firstHref(page, /\/admin\/companies\/[^/?#]+\/contacts\/[^/?#]+$/, ["/create"]);
  if (contactHref) {
    await goto(page, contactHref);
    await waitForBodyText(page, /CompanyContact|担当|作成/, 30000);
    await snapshot(page, "company-contact-detail-first", contactHref);
  } else {
    await clickText(page, /TEST_FAQ_担当|担当/, "company-contact-row");
    if (/\/admin\/companies\/[^/?#]+\/contacts\/[^/?#]+$/.test(page.url())) {
      await waitForBodyText(page, /CompanyContact|担当|作成/, 30000);
      await snapshot(page, "company-contact-detail-first", page.url());
    } else {
      records.push({ name: "company-contact-detail-first", note: "No company contact detail link found.", url: companyUrl });
    }
  }

  await goto(page, knownCompanyUrl);
  await waitForBodyText(page, /TEST_FAQ_株式会社テスト|直近の注文|会社ID|担当者を追加|ロケーションを追加/, 30000);
  await snapshot(page, "company-detail-known-direct", knownCompanyUrl, { purpose: "recheck-06-customers-known-company" });

  await clickButton(page, /担当者を追加/, "known-company-add-contact");
  await waitForBodyText(page, /担当者を作成する|姓|名|メールアドレス|電話番号|発注の確認メール/, 15000);
  await snapshot(page, "company-add-contact-known-dialog", knownCompanyUrl, { action: "open-add-contact-known-company" });

  await goto(page, knownContactUrl);
  await waitForBodyText(page, /TEST_FAQ_担当太郎|CompanyContact|作成/, 30000);
  await snapshot(page, "company-contact-known-direct", knownContactUrl, { purpose: "recheck-known-company-contact-detail" });
} catch (error) {
  records.push({ name: "failure", message: error.message, stack: error.stack });
  await snapshot(page, "failure-state", page.url(), { error: error.message }).catch(() => {});
  throw error;
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "customer-company-current-records.json"),
    JSON.stringify(
      {
        generatedAt: new Date().toISOString(),
        failed: records.find((record) => record.name === "failure")?.message || null,
        records,
        network,
        console: consoleLogs,
      },
      null,
      2,
    ),
  );
  await context.close();
}
