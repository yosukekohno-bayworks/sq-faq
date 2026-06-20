# Playwright実画面 深掘り検証レビュー（2026-06-08）

> 方針: 元のClaude作成mdは変更しない。現在のSQ staging実画面と公開ヘルプをPlaywrightで開き、表示・URL・フォーム挙動・主要フロー証跡を別ファイルとして残す。

## まず訂正

前回の「全部確認」は表現が強すぎた。  
その時点で実施済みだったのは、管理画面URL巡回、公開ヘルプ再クロール、一部重要フローの実操作であり、md全行の主張を全部Playwrightで潰し切ったわけではなかった。

今回追加で、Playwrightによる実画面確認を以下まで増やした。

## 今回の実施範囲

| 種別 | 実施内容 | 件数 | 証跡 |
|:--|:--|--:|:--|
| 管理画面URL確認 | mdに出てくる静的 `/admin/...` URLを実際に開き、h1/本文/ボタン/フォームラベル/404/TODO/空状態/スクショを保存 | 159 URL | `deep-screen-verification-20260608/admin-screen-records.json` |
| 管理画面スクショ | 上記159 URLのフルページスクショ | 159枚 | `deep-screen-verification-20260608/admin-screenshots/` |
| フォーム挙動 | 主要作成/接続フォームを空のまま保存・作成・連携ボタン押下し、バリデーションと遷移有無を確認 | 32フォーム | `deep-screen-verification-20260608/form-validation-records.json` |
| フォームスクショ | バリデーション後スクショ | 32枚 | `deep-screen-verification-20260608/form-validation-screenshots/` |
| 公開ヘルプ | `/docs/guide/...` を内部リンク込みで実クロールし、h1/本文量/画像数/ステータス/スクショを保存 | 55 URL | `deep-screen-verification-20260608/public-help-screen-records.json` |
| 公開ヘルプスクショ | 公開ヘルプのフルページスクショ | 55枚 | `deep-screen-verification-20260608/public-help-screenshots/` |
| 実操作フロー | 在庫依頼→確保→移動伝票→出荷→入荷→在庫反映、発注伝票作成エラー | 実施済み | `CODEX-SCREEN-REVIEW-2026-06-08.md` |

## 管理画面の実測結果

- 開いた管理画面URL: 159件。
- スクショ保存: 159枚。
- 404: 9件。
- アプリ内「予期せぬエラー」: 11件。
- TODO表示: 2件。
- 空状態表示: 53件。

### 404確認済み

- `/admin/b2b/create`
- `/admin/csv_import/csv_export_operation_inventory_logical_available_quantities`
- `/admin/csv_import/csv_import_settings_suppliers`
- `/admin/customer_ranks`
- `/admin/inventory_suppliers`
- `/admin/inventory_suppliers/create`
- `/admin/order_returns/create`
- `/admin/sale_change_line_items/create`
- `/admin/settings/company_locations`

### TODO確認済み

- `/admin/analytics`: h1「分析」、本文TODO。
- `/admin/b2b`: h1「卸売」、本文TODO。

### 古い/省略IDでエラーになったURL

以下は、md内に例として書かれた省略ID・古いID・仮URLが現在の実画面では「予期せぬエラー」になる。

- `/admin/catalogs/e2a819ab-`
- `/admin/catalogs/e2a819ab-.../catalog_product_variants`
- `/admin/omnibus_core_integrations/.../`
- `/admin/omnibus_core_integrations/TEST_MAKER_001`
- `/admin/products/2c32fb97`
- `/admin/products/2c32fb97-.../variants/ee869106-..._ProductVariant`
- `/admin/products/2c32fb97.../variants/create`
- `/admin/settings/brands/9db91120-..._Brand`
- `/admin/settings/brands/new`

## 重要な現在状態の修正

前回レビューで「現在空が多い」と書いたが、今回のPlaywright実画面では一部訂正が必要。

- `/admin/products` は空ではない。UNIQLO系商品と `TEST_FAQ_非公開ステータス確認用` が見える。
- `/admin/inventory_items` は空ではない。UNIQLO系SKUが多数見える。列は `商品 / 品番(SKU) / 販売不可 / 確定済み / 販売可能 / 手持ち`。
- `/admin/settings/suppliers` は空ではない。`TEST_FAQ_Supplier` と `TEST_FAQ_Supplier2` が見える。
- `/admin/product_price_rules` は空ではない。`TEST_FAQ_販売価格ルール` 系が見える。
- `/admin/order_price_adjustment_rules` は空ではない。`TEST_FAQ_ディスカウント_対象商品テスト` が見える。
- 一方、注文・返品・発注・入荷/出荷/在庫依頼・顧客など、実注文系は空状態が多い。

## フォーム挙動確認

32フォームで空保存/空作成を実行し、全件フォームに留まった。データ作成・外部接続には進んでいない。

代表的な実測バリデーション:

- 商品作成: `商品コードを入力してください`、`商品名を入力してください`。
- カタログ作成: `タイトルを入力してください`。
- 会社作成: `会社名を入力してください`、`ロケーション名を入力してください`、住所系必須。
- 取引先作成: `取引先名を入力してください`。
- 発注伝票作成: `取引先を選択してください`、`テナントを選択してください`、`商品を1つ以上追加してください`。
- 在庫依頼作成: `商品バリエーションを選択してください`、`1以上の数量を入力してください`、`移動先ロケーションを選択してください`。
- 移動伝票作成: `配送元を選択してください`、`配送先を選択してください`、`商品を1つ以上追加してください`。
- 調整伝票作成: `ロケーションを選択してください`、`理由を選択してください`、`商品を1つ以上追加してください`。
- 販売上限作成: `販売上限ルール名を入力してください`、`チャネルを選択してください`。
- ディスカウント作成: `タイトルを入力してください`、`クーポンコードを入力してください`、`テナントを選択してください`、開始/終了日時必須。
- Shopify連携作成: `ストア名を入力してください`、`ショップドメインを入力してください`、`shop.myshopify.com の形式で入力してください`、テナント/カタログ/ロケーショングループ必須。

## 公開ヘルプの実測結果

- クロールURL: 55件。
- 200: 52件。
- 404: 3件。
- スクショ保存: 55枚。
- `/docs/guide/...` が正規。
- `/guide/...` は404。
- `/docs/llms.txt` と `/docs/llms-full.txt` は200。
- `/llms.txt` と `/llms-full.txt` は404。

### 公開ヘルプ内リンク切れ

- `https://docs.sqstack.com/docs/guide/data-management/create-location`
- `https://docs.sqstack.com/docs/guide/data-management/create-location-group`
- `https://docs.sqstack.com/docs/guide/data-management/metafields`

### 既存mdのヘルプ評価への影響

`01-helpcenter-coverage-gap.md` と `02-helpcenter-pages.md` の「13ページ中12ページがthin」「Shopifyだけmedium」は現在の実公開ヘルプ全体とは合わない。  
トップページ群は薄いものが多いが、子ページには商品作成、カタログ追加、CSV入出力、ポイント、会員ランク、ロケーション、リテールポータルなどの手順ページが存在する。

## ファイル別の最新判定

| ファイル | 最新判定 | 理由 |
|:--|:--|:--|
| `00-admin-sitemap.md` | 一部修正要 | サイドナビ構造は概ね一致。ただし `全39画面` は古い。今回だけで159 URLを実画面確認。分析/卸売TODOは一致。 |
| `01-helpcenter-coverage-gap.md` | 要改訂 | 公開ヘルプは55 URL拾え、52件200。子ページを含める必要あり。 |
| `02-helpcenter-pages.md` | 要改訂 | `/docs/guide/...` 正規、`/guide/...` 404は一致。ただし13ページ前提は古い。内部リンク切れ3件も追記が必要。 |
| `02-home.md` | 概ね一致 | ホームh1、サイドナビ、カード導線は実画面と一致。 |
| `03-products.md` | 一部修正要 | 商品一覧は現在空ではない。UNIQLO系商品とTEST商品が見える。省略IDの詳細URLはエラー。商品作成フォーム/必須エラーは実測済み。 |
| `04-inventory.md` | 一部修正要 | 在庫一覧は現在空ではなく、4区分列とSKU一覧が見える。単純な最終在庫反映は実操作済み。ただし在庫計算式全体は未実証。 |
| `05-orders.md` | 概ね一致/未実証多 | 注文一覧は空、返品createは404、下書きcreateは予期せぬエラー。注文詳細・返品起票は実データ不足。 |
| `06-customers.md` | 一部修正要 | 会社/担当者TEST詳細は存在。購買顧客一覧は空、`/admin/purchasing_customers/create` は予期せぬエラー。 |
| `07-purchase-orders.md` | 重要点一致 | 発注作成フォーム、取引先/テナント/通貨、空保存バリデーションを確認。`inventory_suppliers` は404。発注保存後の入荷連携は未実証。 |
| `08-sales-settings.md` | かなり一致/外部依存あり | 価格/予約/上限/閾値フォームと空保存エラー確認。販売上限はチャネル必須。外部チャネル連携後の実挙動は未実証。 |
| `09-accounting.md` | 概ね一致 | 売上実績一覧は空、createは404。会計連動・請求/入金/返金は未実証。 |
| `10-analytics.md` | 一致 | `/admin/analytics` はTODO。 |
| `11-operations.md` | 中核フローは実証済み | 入荷/出荷/在庫依頼/確保済み/移動/調整フォームは存在。社内在庫移動は完了まで実操作済み。発注経由入荷は未実証。 |
| `12-crm.md` | 一部修正要 | ディスカウントTESTデータは現在も見える。ポイント/会員ランク系の公開ヘルプ子ページが存在。実注文・返品・ポイント履歴は未実証。 |
| `13-channels.md` | 一部修正要 | Shopify/OmnibusCore/スマレジ/リテールポータルフォームは確認。B2BはTODO/create404。外部同期後の動作は未実証。 |
| `14-settings.md` | 一部修正要 | 設定系フォームと必須エラーは広く確認済み。取引先/権限/決済など一部TESTデータが現存。`company_locations` は404。 |
| `15-csv-pdf.md` | 概ね一致/一部修正要 | CSV/PDF主要画面は存在。誤URL `csv_import/csv_export_operation_inventory_logical_available_quantities` は404。ファイル投入・エクスポート実行は未実施。 |
| `COMPLEX-OPERATIONS.md` | 方針は妥当 | 社内在庫移動は実証済み。外部連携、予約販売相殺、実注文起点は未実証。 |
| `CONFIRMATION-LIST.md` | 追記推奨 | 実データ不足/外部依存/書き込み必要の分類は有効。今回のPlaywright証跡を追加すべき。 |
| `SUMMARY.md` | 要改訂 | ヘルプ評価、画面数、現在データ状態が古い。最新根拠は本ファイルとJSON証跡。 |
| `SQ-調査報告.html` | 要再生成 | 古いSUMMARY由来のため、今回のPlaywright結果を反映して再生成が必要。 |

## フロー別の深掘り状況

| フロー | 状態 | 根拠 |
|:--|:--|:--|
| 社内在庫移動 | 実操作完了 | 在庫依頼→確保→移動伝票→出荷→入荷→最終在庫反映まで確認。 |
| 在庫調整 | フォーム/必須エラー確認 | 空保存でロケーション/理由/商品必須を確認。実在庫変更は追加実施せず。 |
| 発注伝票 | フォーム/必須エラー確認、保存エラーは既存証跡 | 空保存で取引先/テナント/商品必須。既存実操作ではGraphQLエラーで保存不可。 |
| 注文/下書き/返品 | 実データ不足 | 注文一覧空、下書きcreateエラー、返品create404。注文詳細起点の返品は確認不可。 |
| 商品/カタログ | 一覧/フォーム/既存TEST詳細確認 | 商品一覧あり、商品作成必須エラー、カタログ詳細TESTあり。新規商品保存は未実施。 |
| 販売設定 | フォーム/既存TESTデータ確認 | 販売価格/予約販売/閾値/上限フォーム確認。チャネル必須も確認。外部反映は未実証。 |
| CRM | フォーム/既存TESTデータ/公開ヘルプ確認 | ディスカウントTESTあり、ポイント/ランク公開ヘルプあり。実注文連動は未実証。 |
| CSV/PDF | 画面/フォーム確認 | CSV/PDF画面と一部createフォーム確認。ファイルアップロード/実行は未実施。 |
| 外部連携 | 接続フォーム確認 | Shopify/OmnibusCore/スマレジ/Recustomer/リテールポータルのフォームと必須エラー確認。実接続は未実施。 |

## FAQ化で使える/使えない

### 使ってよい

- URLの存在/404/TODO。
- 画面h1、ボタン名、フォームラベル、空保存時の必須エラー。
- 現在画面に見えているTESTデータやUNIQLO系データ。ただし「環境例」として扱う。
- 社内在庫移動フローの実操作結果。

### 注記付きで使う

- 既存TESTデータを使った詳細画面の観察。
- 公開ヘルプの手順。管理画面の現在UIと一致するかは個別照合が必要。
- 空状態の一覧。データ投入後の列や操作は別検証が必要。

### 断定しない

- 実注文起点の返品/会計/ポイント反映。
- 発注保存後の入荷連携。
- Shopify/OmnibusCore/スマレジ/Recustomer接続後の同期挙動。
- 在庫4区分/7区分の全計算式。
- CSVアップロード/エクスポート実行後のファイル内容。
