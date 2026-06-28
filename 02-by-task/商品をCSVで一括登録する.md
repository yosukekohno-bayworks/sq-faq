---
title: 商品をCSVで一括登録する
type: 作業別
task: CSV一括登録
feature: [CSVインポート, 商品管理]
action: [CSVインポート, 商品一括登録, 商品一括更新]
role: [運営者, 管理者]
status: 確定
tags: [csv, インポート, 商品, 一括登録, 一括更新]
last_verified: 2026-06-22
---

# 商品をCSVで一括登録する

> 対象ユーザー: 運営者・管理者　|　所要: 10〜30分（データ量による）　|　最終確認: 2026-06-22

---

## このドキュメントのスコープ

商品一覧（`/admin/products`）の「インポート」メニューから開ける5カテゴリを使って、商品・バリエーション・画像・メタフィールド値を一括で登録・更新する手順をまとめています。

個別に1件ずつ登録する場合は [商品を作成する](./商品を作成する.md) を参照してください。

---

## 商品一覧のインポート5カテゴリと使い分け

商品一覧右上の「インポート」ドロップダウンには以下の5カテゴリがあります。目的に合ったカテゴリを選んでください。

| カテゴリ（UIラベル） | 遷移先URL | できること |
|:--|:--|:--|
| 商品 | `/admin/csv_import/csv_import_operation_products` | 商品を一括で登録・更新する |
| 商品画像 | `/admin/csv_import/csv_import_operation_product_images` | 商品画像を一括で追加・上書きする |
| 商品バリエーション | `/admin/csv_import/csv_import_operation_product_variants` | SKUを一括で登録・更新する |
| 商品メタフィールド | `/admin/csv_import/csv_import_operation_product_metafields` | 商品メタフィールド値を一括で登録・更新する |
| 商品バリエーションメタフィールド | `/admin/csv_import/csv_import_operation_product_variant_metafields` | SKUメタフィールド値を一括で登録・更新する |

> **CSVインポートトップとの違い:** CSVインポートトップ（`/admin/csv_import`）の「商品」グループは `商品 / 商品バリエーション / 商品画像 / 商品バリエーション画像 / カタログ` です。商品一覧の「インポート」メニューは、商品バリエーション画像・カタログではなく、商品メタフィールド・商品バリエーションメタフィールドを含む5項目です。

---

## 「商品」カテゴリの基本的な流れ

以下の手順は「商品」カテゴリ（`/admin/csv_import/csv_import_operation_products`）を代表例として説明します。他のカテゴリも同様のフローで操作します（フォームの構成のみ異なる場合があります）。

### ステップ 1: テンプレートを入手する

1. 左メニューから「CSVインポート」をクリックしてCSVインポートトップ画面（`/admin/csv_import`）を開く。
2. 商品一覧の「インポート」メニューから「商品」を選ぶ、またはCSVインポートトップの「商品」グループから「商品」をクリックする。商品インポートの一覧画面（`/admin/csv_import/csv_import_operation_products`）へ遷移する。
3. 「テンプレート」ボタンをクリックする。Googleスプレッドシートのテンプレートが別タブで開く。

![「商品をCSVでインポートする」一覧画面。右上に「テンプレート」「新規インポート」ボタン、下に実行履歴の一覧](https://raw.githubusercontent.com/yosukekohno-bayworks/sq-faq/main/_analysis/screenshots/03-csv-import-products.png)
4. スプレッドシートをダウンロードまたはコピーして、CSVファイルとして保存する。

> CSVのカラム順・ヘッダー名はテンプレートに準拠する必要があります。列の順番を変えたり、ヘッダー名を変更したりすると取り込みに失敗します。

---

### ステップ 2: CSVファイルを作成する

テンプレートのヘッダー行に従ってデータを入力し、CSVファイルとして保存します。

### 5カテゴリのテンプレート必須列

各カテゴリの一覧画面には「テンプレート」ボタンがあります。テンプレートはGoogleスプレッドシートで、主に `定義書` と `フォーマット` シートに分かれています。

| カテゴリ | フォーマット列 | 必須列 |
|:--|:--|:--|
| 商品 | `command`, `product_code`, `title`, `description`, `product_status`, `brand_code`, `product_vendor`, `product_type`, `tags`, `option1_name`, `option1_type`, `option2_name`, `option2_type`, `option3_name`, `option3_type`, `seo_title`, `seo_description`, `is_outlet`, `sale_start_date`, `sale_end_date` | `command`, `product_code`, `title`, `product_status`, `option1_name` |
| 商品画像 | `product_code`, `image_url`, `position`, `alt`, `filename` | `product_code`, `image_url` |
| 商品バリエーション | `command`, `sku`, `product_code`, `supplier_sku`, `option1_value`, `option1_value_code`, `option1_value_index`, `option2_value`, `option2_value_code`, `option2_value_index`, `option3_value`, `option3_value_code`, `option3_value_index`, `price`, `price_currency_code`, `weight_value`, `weight_unit`, `inventory_policy`, `is_tracked`, `requires_shipping`, `barcode`, `jan`, `upc`, `harmonized_system_code`, `country_code_of_origin` | `command`, `sku`, `product_code`, `option1_value`, `price`, `price_currency_code` |
| 商品メタフィールド | `product_code`, `namespace`, `key`, `value_type`, `value` | 全列 |
| 商品バリエーションメタフィールド | `sku`, `namespace`, `key`, `value_type`, `value` | 全列 |

> **商品バリエーションの在庫系列:** `inventory_policy` は「在庫切れの場合でも販売を続ける」、`is_tracked` は「在庫を追跡する」です。両者は別項目です。

---

### ステップ 3: 新規インポートを開始する

1. 商品インポートの一覧画面（`/admin/csv_import/csv_import_operation_products`）で「新規インポート」ボタンをクリックする。インポート実行フォーム（`/admin/csv_import/csv_import_operation_products/create`）へ遷移する。

---

### ステップ 4: CSVファイルをアップロードする

1. 「CSVファイル」のアップロードエリアが表示されている。
2. 次のいずれかの方法でCSVファイルを選択する。
   - 「ファイルを選択する」ボタンをクリックしてファイル選択ダイアログを開き、作成したCSVファイルを選択する。
   - アップロードエリアにCSVファイルをドラッグ&ドロップする。

---

### ステップ 5: 「保存する」ボタンをクリックする

1. ファイル選択後、「保存する」ボタンをクリックする。
2. 処理が開始され、インポート一覧画面に実行履歴が表示される。

---

### ステップ 6: 実行履歴で検証ステータスを確認する

「保存する」を押した後、インポートは「検証」→「実行」の2段階で処理されます。

1. 商品インポートの一覧画面（`/admin/csv_import/csv_import_operation_products`）で実行履歴を確認する。
2. 実行した行をクリックして詳細画面を開く。
3. 以下の項目を確認する。

   | 項目（UIラベル） | 内容 |
   |:--|:--|
   | 検証ステータス | CSVの検証結果（例: 完了） |
   | 実行ステータス | データ反映の結果（例: 完了） |
   | 検証成功 | 成功した件数（例: 6個の商品） |
   | 検証失敗 | 失敗した件数。クリックで失敗詳細画面（「検証失敗」）へ移動できる |

![「CSVインポート操作の詳細」画面。検証ステータス・実行ステータス・検証成功・検証失敗の各項目](https://raw.githubusercontent.com/yosukekohno-bayworks/sq-faq/main/_analysis/screenshots/gap-csv-import-detail-success.png)

---

### ステップ 7: 検証成功後に「実行する」ボタンをクリックする

1. 検証ステータスが「完了」で、「検証失敗」が0件であることを確認する。
2. 「実行する」ボタンをクリックしてデータをシステムに反映させる。

2026-06-28の実機確認では、商品CSV1件の検証成功後に「CSVの取り込み処理を実行しますか？」が表示され、本文は「1件の商品を登録します。この操作は巻き戻すことができません。」でした。確定後は実行ステータスが「成功 完了」になり、商品一覧/詳細に反映されました。検証用商品は削除済みです。

> 「実行する」ボタンは成功完了後は無効（disabled）になります。一度実行したインポートは再実行できません。

---

### 検証失敗があった場合

1. 詳細画面の「検証失敗」の件数リンクをクリックする。
2. 「検証失敗」画面（`/{id}/validation_failure`）でエラーの内容を確認する。
3. CSVファイルを修正して、再度「新規インポート」から手順をやり直す。

<!-- 残課題: 検証失敗詳細画面に表示される列構成：行番号・エラー理由等 -->

---

## 「商品画像」カテゴリの注意点

「商品画像」のインポートフォームでは、ファイルアップロードの前に画像の処理方法をラジオボタンで選択します。

| 選択肢（UIラベル） | 動作 |
|:--|:--|
| 画像を追加する（デフォルト） | 既存の画像を残したまま新しい画像を追加する |
| 画像を上書きする | 既存の画像を削除して新しい画像に置き換える |

1. 目的に合った処理方法をラジオボタンで選択する。
2. CSVファイルをアップロードする。
3. 「保存する」ボタンをクリックする。

---

## うまくいかないとき

**「テンプレート」ボタンが見当たらない**
- 商品一覧の「インポート」5カテゴリでは、各カテゴリの一覧画面に「テンプレート」ボタンがあります。CSVインポート全体では、テンプレートがないカテゴリもあります。

**「保存する」を押してもエラーになる**
- CSVのヘッダー行がテンプレートと異なっている可能性があります。テンプレートの列名・列順に合わせてCSVを修正してください。

**検証失敗が発生した**
- 詳細画面の「検証失敗」リンクをクリックしてエラー行を確認し、CSVを修正して再インポートしてください。

---

## 関連

- 機能の説明: [CSVインポート](../01-by-feature/CSVインポート.md)
- 機能の説明: [商品管理](../01-by-feature/商品管理.md)
- 関連作業: [商品を作成する](./商品を作成する.md)
- 関連作業: [CSVで在庫を一括更新する](./CSVで在庫を一括更新する.md)
