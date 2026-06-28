# 検索・絞り込み 実機再確認（2026-06-27）

## きっかけ

`04-notion/02-アカウント・権限.md` に「管理メンバー一覧の絞り込み条件はメールアドレスのみ」と書いていたが、実機ではキーワード検索欄に `河野` を入れると名前で検索できた。

## 管理メンバー一覧の確定事項

対象URL: `/admin/settings/users`

| 操作 | 実機結果 | 証跡 |
|:--|:--|:--|
| キーワード検索 `河野` | `河野陽介 / yosuke.kohno@bay-works.com` の1件に絞り込み。URLは `?query=河野` | `account02-users-keyword-search-name-kono.*` |
| キーワード検索 `陽介` | 同じく1件に絞り込み | `account02-users-keyword-search-given-yosuke.*` |
| キーワード検索 `kohno` | メールアドレス断片で1件に絞り込み | `account02-users-keyword-search-email-kohno.*` |
| キーワード検索 `特権管理者` | 0件。権限グループ名はキーワード検索対象外 | `account02-users-keyword-search-permission-admin.*` |
| 「絞り込みを追加」メニュー | 選択肢は `メールアドレス` のみ | `account02-users-filter-menu-20260627-recheck.*` |
| メールアドレスフィルタ `kohno` | `メールアドレスの形式が正しくありません`。断片検索ではない | `account02-users-email-filter-kohno.*` |
| メールアドレスフィルタ `yosuke.kohno@bay-works.com` | 1件に絞り込み。URLは `?email=yosuke.kohno%40bay-works.com` | `account02-users-email-filter-exact-email.*` |

## 修正文言

「キーワード検索」は姓・名・メールアドレス断片に効く。  
「絞り込みを追加」の条件はメールアドレスのみで、これはキーワード検索とは別のメール形式フィルタ。

2026-06-28追記: 管理メンバー一覧を再確認し、`河野` / `陽介` / `kohno` は各1件、`特権管理者` / `河野 kohno` / 存在しない語は0件になった。複数語をAND/ORとして扱う検索ではなく、キーワード欄は単一語・断片検索として案内する。

## 横断クロール

主要42画面について、初期状態・検索/絞り込みパネル展開後・絞り込みメニュー表示後の状態を保存した。

- 出力先: `_analysis/live-notion-verification-2026-06-27/search-filter-audit/`
- 集計JSON: `_analysis/search-filter-live-audit-summary-2026-06-27.json`
- 抽出元の文書検索結果: `_analysis/search-filter-claims-rg-2026-06-27.txt`

注意: Polaris UIの一部入力欄は通常DOM抽出だけではplaceholderが取れず、`browser-use state` 側で確認する必要がある。したがって、修正前には各画面の `*-initial.md` / `*-filter-menu.json` を併読する。

## 追加で優先確認する画面

1. 商品一覧・在庫一覧・発注の商品選択ダイアログ: `商品コードのみ` / `SKUコードのみ` の断定。
2. 設定マスタ一覧: ロケーション/取引先/ブランドなどで一覧検索があるか、タブだけか。

## 追加で確定した画面

| 画面 | 実機結果 | 証跡 |
|:--|:--|:--|
| 商品一覧 `/admin/products` | `F` で検索パネルが開く。検索欄は `商品コードで検索する`。追加フィルタは表示されない | `search-filter-audit/products-search-panel-key-f.md` |
| 在庫一覧 `/admin/inventory_items` | 検索欄は `SKUコードで検索する`。`絞り込みを追加` の候補は `商品コード` のみ | `search-filter-audit/inventory-items-search-panel-retry.md`, `inventory-items-filter-menu-manual.md` |
| 注文一覧 `/admin/orders` | 検索欄は `注文番号で検索する`。フィルタ候補は `テナント` / `タグ付けされている` / `タグ付けされていません` / `チャネル` | `search-filter-audit/orders-search-panel-key-f.md`, `orders-filter-menu-manual.md` |
| 下書き注文 `/admin/draft_orders` | 検索欄は `注文番号で検索する`。追加フィルタは表示されない | `search-filter-audit/draft-orders-search-panel-key-f.md` |
| 返品 `/admin/order_returns` | 検索欄は表示されず、フィルタ候補は `キャンセル` / `交換出荷` | `search-filter-audit/order-returns-search-panel-key-f.md`, `order-returns-filter-menu-manual.md` |
| 顧客管理 `/admin/purchasing_customers` | 検索欄は `メールアドレスで検索する`。フィルタ候補は `テナント` / `メタフィールド` / `会員証バーコード` | `search-filter-audit/purchasing-customers-search-panel-key-f.md`, `purchasing-customers-filter-menu-manual.md` |
| 販売閾値 `/admin/inventory_threshold_rules` | 正URLは `/admin/inventory_threshold_rules`。一覧列は `名前` のみ | `search-filter-audit/threshold-rules-initial.*` |
| 採寸ルール `/admin/settings/product_measurement_rules` | 正URLは `/admin/settings/product_measurement_rules`。一覧列は `ルール名` / `単位` / `採寸項目` | `search-filter-audit/measurement-rules-initial.*` |

2026-06-28追記: `23-search-filter-cross-check-20260628.*` で主要8画面を再確認。商品/在庫/ロケーション/出荷/入荷は `F` で検索パネルが開く。カタログ/移動伝票は今回の方法では検索パネルなし。商品検索は商品コード、在庫検索はSKUコード、ロケーション検索は場所コード、出荷/入荷検索は `#` 付き管理番号に一致し、名前・ステータス名・複数語の汎用検索では0件になる。
