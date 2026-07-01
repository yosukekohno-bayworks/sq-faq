# Shopify側確認メモ 2026-06-29

## ストア基本状態

- Shopify管理画面URL: `https://admin.shopify.com/store/stack-ps-yosuke`
- ストア名: `stack-ps-yosuke`
- 管理画面タイトル: `stack-ps-yosuke · ホーム · Shopify Plus`

## 商品一覧

- URL: `/products`
- 2026-06-29の商品一覧は17件。
- SQ側UNIQLOカタログの未連携5商品は、商品情報一括同期前にはShopify商品一覧に存在しなかった。
- SQ側で商品情報一括同期を実行してProductSet認証情報不足で失敗した後も、Shopify商品一覧は17件のまま。UNIQLO 5商品は作成されておらず、部分作成も確認されなかった。

一覧に表示されていた商品:

- The Collection Snowboard: Liquid
- The Multi-managed Snowboard
- The 3p Fulfilled Snowboard
- The Collection Snowboard: Oxygen
- The Multi-location Snowboard
- Selling Plans Ski Wax
- The Out of Stock Snowboard
- The Compare at Price Snowboard
- The Minimal Snowboard
- The Draft Snowboard
- The Collection Snowboard: Hydrogen
- The Videographer Snowboard
- The Hidden Snowboard
- The Archived Snowboard
- The Complete Snowboard
- Gift Card
- The Inventory Not Tracked Snowboard

## ロケーション

- URL: `/settings/locations`
- Active locations: `2 of 200`
- Default location: `Shop location`
- Shopify側ロケーション:
  - `My Custom Location`（POS Pro、アクティブ）
  - `Shop location`（POS Pro、アクティブ）
- App/custom fulfillment location:
  - `Shopify Test Data` app / `Snow City Warehouse`

SQ側のShopifyロケーション接続では、`ユニクロEC` が Shopify の `My Custom Location` に接続されている。

## インストール済みアプリ

- URL: `/settings/apps`
- インストール済みアプリ: `erp-stg`
- Shopify側アプリ詳細では、開発者は `Stack Inc`、2日前にインストール済み。
- アクティビティと権限には `商品管理` / `顧客管理` / `注文管理` / `オンラインストア` / `カスタムデータ` / `ディスカウント` などが表示される。
- 個人データアクセスあり。対象には名前、メールアドレス、電話番号、住所、デバイスとアクティビティデータ等が含まれる。
- アプリプロキシURL: `https://stack-ps-yosuke.myshopify.com/apps/sq-api`

## アプリ開発画面

- URL: `/settings/apps/development`
- 表示される主な導線は `Dev Dashboardでアプリを開発・管理` と `レガシーカスタムアプリを作成`。
- この画面では、SQ側アクセストークンに入力する `ProductSet` / `InventorySet` 等のクライアントID/シークレットを発行・表示する導線は確認できなかった。

## Shopify内アプリ画面

- URL: `/apps/erp-stg/app`
- 表示名: `SQ (エス・キュー)`
- 埋め込み先は staging 用の `sq.stackservicestaging.com`。
- 画面本文:
  - 見出し: `連携されるデータ`
  - 説明: ストアが正常に連携されている場合、SQからデータが連携され、制御はSQの管理画面で行う旨が表示される。
  - 連携データ種別: `商品データ` / `価格データ` / `在庫データ` / `注文データ` / `顧客データ`
  - データ連携状況: `成功 完了` / `正常`
  - カタログ: `UNIQLO - 5点の商品が連携されます。`

このShopify内アプリ画面には、ProductSet用クライアントID/シークレットを発行・表示するUIは確認できなかった。

## ログイン後の再確認

- 2026-06-29、Shopify管理画面ログイン後に商品一覧を再読み込みし、SQ側UNIQLO 5商品の商品名が存在しないことを確認した。
- 同時点の商品一覧は17件で、サンプル商品（Snowboard系、Gift Card、Ski Wax）のみ。
- `erp-stg` のアプリ詳細、アプリ開発画面、埋め込みアプリのいずれにも、SQ側アクセストークン用のクライアントID/シークレット発行・表示導線は確認できなかった。
