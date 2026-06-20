import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "/Users/kounoyousuke/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs";

const ROOT = process.cwd();
const OUT_DIR = path.join(ROOT, "faq/_analysis/deep-screen-verification-20260609");
const SCREEN_DIR = path.join(OUT_DIR, "crm-points-current-screenshots");
await fs.mkdir(SCREEN_DIR, { recursive: true });

const profileDir = process.argv[2];
if (!profileDir) throw new Error("Pass Chrome profile directory.");

const base = "https://www.sqstackstaging.com";

const targets = [
  { name: "discount-list", url: `${base}/admin/order_price_adjustment_rules`, action: "list-menu" },
  { name: "discount-create", url: `${base}/admin/order_price_adjustment_rules/create` },
  { name: "point-rules-list", url: `${base}/admin/point_calculation_rules` },
  { name: "point-rules-create", url: `${base}/admin/point_calculation_rules/create` },
  { name: "birthday-point-list", url: `${base}/admin/point_calculation_birthday_rules` },
  { name: "birthday-point-create", url: `${base}/admin/point_calculation_birthday_rules/create` },
  { name: "point-campaign-list", url: `${base}/admin/point_campaign_order_rules` },
  { name: "point-campaign-create", url: `${base}/admin/point_campaign_order_rules/create`, action: "campaign-create-variants" },
  { name: "point-excluded-products-list", url: `${base}/admin/point_application_excluded_products` },
  { name: "point-excluded-products-create", url: `${base}/admin/point_application_excluded_products/create`, action: "open-picker" },
  { name: "point-expiration-list", url: `${base}/admin/point_expiration_notification_rule` },
  { name: "point-expiration-create", url: `${base}/admin/point_expiration_notification_rule/create` },
  { name: "customer-rank-list", url: `${base}/admin/customer_rank_calculation_rules` },
  { name: "customer-rank-create", url: `${base}/admin/customer_rank_calculation_rules/create`, action: "rank-periods" },
  { name: "customer-ranks-standalone", url: `${base}/admin/customer_ranks` },
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

function uniq(items) {
  return [...new Set(items.filter(Boolean))];
}

function absoluteUrl(url) {
  if (!url) return "";
  if (url.startsWith("http")) return url;
  return `${base}${url.startsWith("/") ? "" : "/"}${url}`;
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
      els.slice(0, 460).map((el) => {
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
          value: el.value || "",
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
      selects.slice(0, 70).map((select, index) => {
        const label =
          select.closest("label")?.textContent?.trim().replace(/\s+/g, " ") ||
          select.getAttribute("aria-label") ||
          select.getAttribute("name") ||
          "";
        const context = select.closest("fieldset, section, form, div")?.textContent?.trim().replace(/\s+/g, " ").slice(0, 700) || "";
        return {
          index,
          name: select.getAttribute("name") || "",
          label,
          value: select.value || "",
          context,
          disabled: select.disabled,
          options: Array.from(select.options).map((option) => ({
            text: option.textContent?.trim().replace(/\s+/g, " ") || "",
            value: option.value || "",
            disabled: option.disabled,
          })),
        };
      }),
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
    h2: compact(await page.locator("h2").allInnerTexts().catch(() => []), 100),
    h3: compact(await page.locator("h3").allInnerTexts().catch(() => []), 120),
    dialogs: compact(await page.locator('[role="dialog"], [role="menu"]').allInnerTexts().catch(() => []), 120),
    rows: compact(
      await page
        .locator("tr, [role=row]")
        .evaluateAll((els) => els.map((el) => el.textContent?.trim().replace(/\s+/g, " ") || "").filter(Boolean).slice(0, 340))
        .catch(() => []),
      340,
    ),
    controls,
    links: controls.filter((control) => control.tag === "a" && control.href).map((control) => ({ text: control.text, href: control.href })),
    selectOptions: await getSelectOptions(page),
    checkedInputs: controls
      .filter((control) => control.checked)
      .map((control) => ({
        type: control.type,
        name: control.name,
        text: control.text,
        ariaLabel: control.ariaLabel,
        value: control.value,
        disabled: control.disabled,
      })),
    disabledInputs: controls
      .filter((control) => control.disabled && /(radio|checkbox|button|select)/.test(`${control.type} ${control.tag}`))
      .map((control) => ({
        tag: control.tag,
        type: control.type,
        name: control.name,
        text: control.text,
        ariaLabel: control.ariaLabel,
        value: control.value,
      })),
    importantLines: compact(
      text
        .split(/\n+/)
        .map((line) => line.trim())
        .filter((line) =>
          /(ディスカウント|クーポン|割引|適用条件|対象商品|対象顧客|対象店舗|利用回数|有効|スケジュール|期限切れ|ポイント|注文ポイント|キャンペーン|誕生日|利用外商品|失効|通常|追加|付与|倍率|会員ランク|算出|購入金額|獲得ポイント|除外商品|開始月|直近365日|無期限|1年間|税抜き|月初|持ち越|チャネル|店舗|ロケーション|商品|保存|作成|編集|追加|選択|アイテムが見つかりません|このページの準備が整いました|このページは存在しない|予期せぬエラー|Application error|エラー)/.test(
            line,
          ),
        ),
      460,
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

async function selectOptionByText(page, optionRe, contextRe = null) {
  const selects = page.locator("select");
  const candidates = [];
  const count = await selects.count().catch(() => 0);
  for (let index = 0; index < count; index += 1) {
    const select = selects.nth(index);
    if (!(await select.isVisible().catch(() => false))) continue;
    const options = await select.evaluate((node) =>
      Array.from(node.options).map((option) => ({
        text: option.textContent?.trim().replace(/\s+/g, " ") || "",
        value: option.value,
        disabled: option.disabled,
      })),
    );
    const context = await select
      .evaluate(
        (node) =>
          node.closest("label")?.textContent?.trim().replace(/\s+/g, " ") ||
          node.closest("fieldset, section, form, div")?.textContent?.trim().replace(/\s+/g, " ").slice(0, 700) ||
          "",
      )
      .catch(() => "");
    const option = options.find((item) => !item.disabled && optionRe.test(item.text));
    if (option) candidates.push({ select, option, index, context, contextMatch: contextRe ? contextRe.test(context) : true });
  }
  const chosen = candidates.find((item) => item.contextMatch) || candidates[0];
  if (!chosen) return null;
  await chosen.select.selectOption({ value: chosen.option.value });
  await settle(page, 1200);
  return { selected: chosen.option, selectIndex: chosen.index, context: chosen.context, contextMatch: chosen.contextMatch };
}

async function selectOptionByValue(page, value) {
  const selects = page.locator("select");
  const count = await selects.count().catch(() => 0);
  for (let index = 0; index < count; index += 1) {
    const select = selects.nth(index);
    if (!(await select.isVisible().catch(() => false))) continue;
    const values = await select.evaluate((node) => Array.from(node.options).map((option) => option.value));
    if (!values.includes(value)) continue;
    await select.selectOption(value);
    await settle(page, 1200);
    return { selectIndex: index, value };
  }
  return null;
}

async function selectFirstPointRule(page) {
  return await selectOptionByText(page, /TEST_FAQ_注文ポイント付与ルール|注文ポイント付与ルール/);
}

async function selectAdditionalPointMethod(page) {
  return await selectOptionByText(page, /通常.*ポイント.*追加|通常.*付与.*追加|指定.*ポイント.*追加|追加.*ポイント/);
}

async function selectMultiplierMethod(page) {
  return await selectOptionByText(page, /倍率/);
}

async function clickSafeButton(page, buttonRe) {
  const buttons = page.locator("button").filter({ hasText: buttonRe });
  const count = await buttons.count().catch(() => 0);
  for (let index = 0; index < count; index += 1) {
    const button = buttons.nth(index);
    if (!(await button.isVisible().catch(() => false))) continue;
    const label = await button.textContent().catch(() => "");
    if (/保存|削除|連携|実行|確定|送信/.test(label || "")) continue;
    const disabled = await button.evaluate((el) => el.disabled || el.getAttribute("aria-disabled") === "true").catch(() => true);
    if (disabled) continue;
    await button.click({ timeout: 12000 }).catch(() => {});
    await settle(page, 1000);
    return true;
  }
  return false;
}

async function openPicker(page, targetName, requestedUrl) {
  const opened =
    (await clickSafeButton(page, /選択|検索/)) ||
    (await page
      .locator('button[aria-label*="選択"], button[aria-label*="検索"]')
      .first()
      .click({ timeout: 8000 })
      .then(async () => {
        await settle(page, 1000);
        return true;
      })
      .catch(() => false));
  if (opened) {
    await snapshot(page, `${targetName}-picker-opened`, requestedUrl, { action: "open-picker" });
    await page.keyboard.press("Escape").catch(() => {});
    await settle(page, 500);
  }
  return opened;
}

async function openTopIconMenu(page, targetName, requestedUrl) {
  const buttons = page.locator("button");
  const count = await buttons.count().catch(() => 0);
  for (let index = 0; index < Math.min(count, 18); index += 1) {
    const button = buttons.nth(index);
    if (!(await button.isVisible().catch(() => false))) continue;
    const meta = await button
      .evaluate((el) => {
        const rect = el.getBoundingClientRect();
        return {
          text: el.textContent?.trim().replace(/\s+/g, " ") || "",
          ariaLabel: el.getAttribute("aria-label") || "",
          title: el.getAttribute("title") || "",
          disabled: el.disabled || el.getAttribute("aria-disabled") === "true",
          rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
        };
      })
      .catch(() => null);
    if (!meta || meta.disabled) continue;
    const label = `${meta.text} ${meta.ariaLabel} ${meta.title}`;
    if (/保存|削除|作成|追加|前|次|すべて|有効|スケジュール|期限切れ|キャンセル|stack-ps-yosuke/.test(label)) continue;
    if (meta.rect.y > 280 && !/表示|メニュー|More|その他|列|絞り込み|フィルタ/.test(label)) continue;
    if (meta.rect.width > 90 && meta.text) continue;
    await button.click({ timeout: 12000 }).catch(() => {});
    await settle(page, 1000);
    await snapshot(page, `${targetName}-menu-opened`, requestedUrl, { action: "open-menu", clickedButton: meta });
    await page.keyboard.press("Escape").catch(() => {});
    await settle(page, 500);
    return true;
  }
  return false;
}

function firstLink(record, re) {
  const link = record.links.find((item) => re.test(item.href) && !/\/create(?:[/?#]|$)/.test(item.href));
  return link ? link.href : "";
}

function extractIdsFromNetwork() {
  const result = {
    discounts: [],
    pointCampaigns: [],
    customerRankRules: [],
  };
  for (const item of network) {
    if (!item.body) continue;
    let parsed = null;
    try {
      parsed = JSON.parse(item.body);
    } catch {
      continue;
    }
    for (const node of parsed?.data?.orderPriceAdjustmentRules?.nodes || []) {
      if (node?.id) result.discounts.push({ id: node.id, title: node.title || "" });
    }
    for (const node of parsed?.data?.pointCampaignOrderRules?.nodes || []) {
      if (node?.id) result.pointCampaigns.push({ id: node.id, title: node.title || "", targetType: node.targetType || "" });
    }
    for (const node of parsed?.data?.customerRankCalculationRules?.nodes || []) {
      if (node?.id) result.customerRankRules.push({ id: node.id, title: node.title || "" });
    }
  }
  return {
    discounts: Array.from(new Map(result.discounts.map((item) => [item.id, item])).values()),
    pointCampaigns: Array.from(new Map(result.pointCampaigns.map((item) => [item.id, item])).values()),
    customerRankRules: Array.from(new Map(result.customerRankRules.map((item) => [item.id, item])).values()),
  };
}

async function runCampaignCreateVariant(page, value, label, target) {
  await goto(page, target.url);
  await snapshot(page, `${target.name}-${label}-initial`, target.url, { action: "campaign-create-variant", value });
  const selectedType = await selectOptionByValue(page, value);
  await snapshot(page, `${target.name}-${label}-type-selected`, target.url, { selectedType });
  const selectedPointRule = await selectFirstPointRule(page);
  await snapshot(page, `${target.name}-${label}-point-rule-selected`, target.url, { selectedPointRule });
  const selectedAdditional = await selectAdditionalPointMethod(page);
  await snapshot(page, `${target.name}-${label}-additional-point-method`, target.url, { selectedAdditional });
  const selectedMultiplier = await selectMultiplierMethod(page);
  await snapshot(page, `${target.name}-${label}-multiplier-method`, target.url, { selectedMultiplier });
  records.push({ name: `${target.name}-${label}-summary`, selectedType, selectedPointRule, selectedAdditional, selectedMultiplier });
}

async function runCampaignCreateVariants(page, target) {
  records.push({ name: "mutation-boundary", note: "Opened forms, dropdowns, menus, and pickers only. No save/delete/connect/execute buttons were clicked." });
  await runCampaignCreateVariant(page, "NONE", "none", target);
  await runCampaignCreateVariant(page, "CUSTOMER_RANK", "customer-rank", target);
  await runCampaignCreateVariant(page, "PURCHASE_PRICE", "purchase-price", target);
  await runCampaignCreateVariant(page, "PRODUCT", "product", target);
}

async function runRankPeriodActions(page, target) {
  const selectedRecent = await selectOptionByText(page, /^直近365日$/);
  await snapshot(page, `${target.name}-period-recent365`, target.url, { selectedRecent });
  const selectedUnlimited = await selectOptionByText(page, /^無期限$/);
  await snapshot(page, `${target.name}-period-unlimited`, target.url, { selectedUnlimited });
  const selectedOneYear = await selectOptionByText(page, /^1年間$/);
  await snapshot(page, `${target.name}-period-one-year-restored`, target.url, { selectedOneYear });
}

async function runCustomerRankSubRuleFlow(page, namePrefix, url) {
  const selectedRule = await selectOptionByText(page, /TEST_FAQ_会員ランク算出ルール|会員ランク算出ルール/);
  await snapshot(page, `${namePrefix}-calculation-rule-selected`, url, { selectedRule });
  const selectedRank = await selectOptionByText(page, /Bronze|Silver|Gold|会員ランク/);
  await snapshot(page, `${namePrefix}-rank-selected`, url, { selectedRank });
}

async function inspectDiscount(page, url, namePrefix) {
  await goto(page, url);
  await snapshot(page, namePrefix, url);
  await openTopIconMenu(page, `${namePrefix}-actions`, url);
  for (const subpath of ["product_variants", "customers", "locations", "usages"]) {
    const subUrl = `${url.replace(/\/$/, "")}/${subpath}`;
    await goto(page, subUrl);
    await snapshot(page, `${namePrefix}-${subpath}`, subUrl);
  }
}

async function inspectPointCampaign(page, url, campaign, index) {
  const namePrefix = `point-campaign-detail-${index}-${slugify(campaign.title || campaign.id)}`;
  await goto(page, url);
  await snapshot(page, namePrefix, url, { campaign });
  await openTopIconMenu(page, `${namePrefix}-actions`, url);
  for (const subpath of ["update", "customer_ranks/create", "retail_locations/create"]) {
    const subUrl = `${url.replace(/\/$/, "")}/${subpath}`;
    await goto(page, subUrl);
    await snapshot(page, `${namePrefix}-${subpath.replaceAll("/", "-")}`, subUrl, { campaign });
    if (subpath === "customer_ranks/create") {
      await runCustomerRankSubRuleFlow(page, `${namePrefix}-customer-ranks-create`, subUrl);
    }
    if (subpath === "retail_locations/create") {
      await openPicker(page, `${namePrefix}-retail-locations-create`, subUrl);
    }
  }
}

async function inspectCustomerRankRule(page, url, rule, index) {
  const namePrefix = `customer-rank-detail-${index}-${slugify(rule.title || rule.id)}`;
  await goto(page, url);
  const detail = await snapshot(page, namePrefix, url, { rule });
  await openTopIconMenu(page, `${namePrefix}-actions`, url);

  const rankRuleHref = firstLink(detail, /\/admin\/customer_rank_calculation_rules\/[^/]+\/customer_rank_rules\/[^/?#]+/);
  if (rankRuleHref) {
    await goto(page, absoluteUrl(rankRuleHref));
    await snapshot(page, `${namePrefix}-rank-rule-detail`, absoluteUrl(rankRuleHref), { rule });
  }

  for (const subpath of ["update", "exclude_products", "exclude_products/create", "customer_rank_rules/create"]) {
    const subUrl = `${url.replace(/\/$/, "")}/${subpath}`;
    await goto(page, subUrl);
    await snapshot(page, `${namePrefix}-${subpath.replaceAll("/", "-")}`, subUrl, { rule });
    if (subpath === "exclude_products/create") {
      await openPicker(page, `${namePrefix}-exclude-products-create`, subUrl);
    }
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
  if (
    !/graphql|order_price_adjustment_rules|point_calculation|point_campaign|point_application|point_expiration|customer_rank/.test(url) &&
    response.status() < 400
  ) {
    return;
  }
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
  const listRecords = {};

  for (const target of targets) {
    await goto(page, target.url);
    const record = await snapshot(page, target.name, target.url);
    listRecords[target.name] = record;

    if (target.action === "list-menu") {
      await openTopIconMenu(page, target.name, target.url);
    }
    if (target.action === "campaign-create-variants") {
      await runCampaignCreateVariants(page, target);
    }
    if (target.action === "open-picker") {
      await openPicker(page, target.name, target.url);
    }
    if (target.action === "rank-periods") {
      await runRankPeriodActions(page, target);
    }
  }

  const ids = extractIdsFromNetwork();
  const discountUrls = uniq([
    firstLink(listRecords["discount-list"], /\/admin\/order_price_adjustment_rules\/[^/?#]+/),
    ...ids.discounts.map((item) => `${base}/admin/order_price_adjustment_rules/${item.id}`),
  ]).map(absoluteUrl);
  const campaignUrls = ids.pointCampaigns.map((item) => ({
    ...item,
    url: `${base}/admin/point_campaign_order_rules/${item.id}`,
  }));
  const rankRuleUrls = ids.customerRankRules.map((item) => ({
    ...item,
    url: `${base}/admin/customer_rank_calculation_rules/${item.id}`,
  }));

  records.push({ name: "discovered-current-ids", ids, discountUrls, campaignUrls, rankRuleUrls });

  for (let index = 0; index < Math.min(discountUrls.length, 2); index += 1) {
    await inspectDiscount(page, discountUrls[index], `discount-detail-${index + 1}`);
  }

  for (let index = 0; index < campaignUrls.length; index += 1) {
    await inspectPointCampaign(page, campaignUrls[index].url, campaignUrls[index], index + 1);
  }

  for (let index = 0; index < rankRuleUrls.length; index += 1) {
    await inspectCustomerRankRule(page, rankRuleUrls[index].url, rankRuleUrls[index], index + 1);
  }
} catch (error) {
  failed = { message: error.message, stack: error.stack };
  await snapshot(page, "99-failure-state", page.url(), { failed });
  console.error(error);
} finally {
  await fs.writeFile(
    path.join(OUT_DIR, "crm-points-current-records.json"),
    JSON.stringify({ generatedAt: new Date().toISOString(), targets, failed, consoleLogs, network, records }, null, 2),
  );
  await context.close().catch(() => {});
}

if (failed) process.exitCode = 1;
