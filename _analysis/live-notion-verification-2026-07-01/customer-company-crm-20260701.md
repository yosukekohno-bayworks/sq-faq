# 顧客・会社 / CRM 追加実機検証 2026-07-01

対象環境: `https://www.sqstackstaging.com/admin`

## 18 CRM: ポイントキャンペーンのチャネル候補

- 対象画面: `/admin/point_campaign_order_rules/create`
- 種別選択前: タイトル、開始日時、終了日時、ポイントキャンペーン種別のみ表示。
- 種別 `なし` / `会員ランク` / `購入金額` / `商品` を選ぶと、ポイント付与方法、対象の注文ポイント付与ルール、適用条件が表示される。
- Shopify接続済み状態のチャネル候補:
  - `FAQ_INTERNAL_GRAPHQL_ORDER_SHIP_FLOW`
  - `stack-ps-yosuke.myshopify.com`
- 検証用キャンペーン: `TEST_FAQ_20260701_1201_POINT_CAMPAIGN_SHOPIFY_CHANNEL`
- 保存条件: 種別 `なし`、ポイント倍率 `1`、対象の注文ポイント付与ルール `TEST_FAQ_注文ポイント付与ルール`、チャネル `stack-ps-yosuke.myshopify.com`
- 保存結果:
  - 詳細URL: `/admin/point_campaign_order_rules/5fc227fb-9dbd-53e1-91b5-f1098bdf8451_PointCampaignOrderRule`
  - 詳細表示: `チャネル stack-ps-yosuke.myshopify.com`
  - 対象店舗: `キャンペーンの対象となる店舗が登録されていません`
- 削除結果:
  - 一覧で行選択すると `ルールを削除する` が表示。
  - 確認ダイアログ: `ポイントキャンペーンを削除しますか？` / `選択されている1件のポイントキャンペーンを削除します。この処理は巻き戻すことができません。`
  - 削除後、一覧から検証用キャンペーンが消え、`ポイントキャンペーンを削除しました` が表示。

## 17 顧客・会社: 会社ID/会社ロケーションID付き注文

- 対象会社: `TEST_FAQ_20260624_COMPANY_102911`
- 会社ID: `16fb446c-e284-593e-a19e-7ec339e48a7a_Company`
- 会社ロケーション: `TEST_FAQ_20260624_COMPANY_LOC_102911`
- 会社ロケーションID: `176ee231-d367-5840-8b53-9d65f9d68cec_CompanyLocation`
- 検証注文: `FAQ-COMPANY-ORDER-202607011221`
- 注文ID: `4ef54db1-f0ad-500d-b54a-3ab38f4991ed_Order`
- 作成方法: 内部GraphQL `orderCreate`
- `OrderCreatePurchasingCompanyInput`:
  - `companyID`: 必須
  - `companyLocationID`: 必須
  - `companyContactID`: 任意
- 注文作成結果:
  - `purchasingCompany.company.name = TEST_FAQ_20260624_COMPANY_102911`
  - `purchasingCompany.location.name = TEST_FAQ_20260624_COMPANY_LOC_102911`
  - `paymentStatus = PAID`
  - `fulfillmentStatus = FULFILLED`
  - `inventoryBehavior = BYPASS`
  - 注文詳細の配送先住所/請求先住所には会社名 `TEST_FAQ_20260624_COMPANY_102911` が表示。
- 会社詳細の反映:
  - 作成前: `直近の注文 この会社はまだ注文していません`、ロケーション行 `売上 ¥0` / `注文 0`
  - 作成後: 同じく `直近の注文 この会社はまだ注文していません`、ロケーション行 `売上 ¥0` / `注文 0`
- 会社ロケーション詳細の反映:
  - 作成前: `直近の注文 このロケーションからはまだ注文がありません`
  - 作成後: 同じく `直近の注文 このロケーションからはまだ注文がありません`
- 画面GraphQL:
  - 会社詳細の `Company` query は会社名、外部ID、メモ、ロケーション、担当者、メタフィールドだけを取得。注文/売上は取得していない。
  - ロケーション詳細の `CompanyLocation` query はロケーション名、外部ID、コード、住所、会社IDだけを取得。注文/売上は取得していない。

結論: 会社ID/会社ロケーションIDは注文データには保存されるが、現行の会社詳細/会社ロケーション詳細UIの注文履歴・売上・注文数には反映されない。
