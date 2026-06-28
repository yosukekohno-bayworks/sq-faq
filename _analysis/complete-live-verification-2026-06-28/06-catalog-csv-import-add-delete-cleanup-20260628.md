# 06 カタログCSVインポート NEW/DELETE 実行確認 2026-06-28

## 対象

- 商品コード: `TEST_FAQ_CATCSV_20260628_082508`
- 商品名: `TEST_FAQ_CATCSV_20260628_082508_商品`
- カタログ: `TEST_FAQ_CATCSV_20260628_082508_カタログ`
- ADD CSV: `_analysis/complete-live-verification-2026-06-28/06-catalog-csv-import-add-20260628_082508.csv`
- DELETE CSV: `_analysis/complete-live-verification-2026-06-28/06-catalog-csv-import-delete-20260628_082508.csv`
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/06-catalog-csv-import-add-delete-cleanup-20260628.json`

## 結果

- NEW検証成功: `確認`
- NEW実行成功: `確認`
- NEW後のカタログ反映: `確認`
- DELETE検証成功: `確認`
- DELETE実行成功: `確認`
- DELETE後のカタログ除外: `確認`
- 商品削除: `確認`
- カタログ削除: `確認`

## 判定

- カタログ商品CSVは `product_code,command` の2列で、`NEW` により対象商品をカタログへ追加できる。
- 同じ形式で `DELETE` を実行すると、対象商品をカタログから外せる。
- NEW/DELETEとも検証成功後に確認ダイアログを経て実行され、実行ステータスは `成功 完了` になる。
- 検証用の商品・カタログは削除済み。

## ステップ

### connected-cdp

- URL: `about:blank`

### product-created

- URL: `https://www.sqstackstaging.com/admin/products/8f534fe4-6243-5fb7-b49d-cf5556610317_Product`
- 商品管理
- カタログ
- 未完了の在庫依頼 3件
- TEST_FAQ_CATCSV_20260628_082508_商品。このページの準備が整いました
- TEST_FAQ_CATCSV_20260628_082508_商品
- 商品コード
- TEST_FAQ_CATCSV_20260628_082508
- 商品名
- 商品分類
- 商品タイプ
- 商品を作成しました

### catalog-created

- URL: `https://www.sqstackstaging.com/admin/catalogs/6f694266-98e8-5ad1-8ad2-633dcd780670_Catalog`
- 商品管理
- カタログ
- 未完了の在庫依頼 3件
- TEST_FAQ_CATCSV_20260628_082508_カタログ。このページの準備が整いました
- TEST_FAQ_CATCSV_20260628_082508_カタログ
- インポート
- 商品
- 商品を追加する
- 商品コードで検索する
- 商品を作成しました

### add-form-filled

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products/create`
- 商品管理
- 未完了の在庫依頼 3件
- カタログ商品をCSVでインポートする。このページの準備が整いました
- カタログ商品をCSVでインポートする
- カタログ
- カタログを選択してください
- TEST_FAQ_カタログ001
- TEST_FAQ_CATCSV_20260628_082508_カタログ

### add-after-submit

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products/create`
- 商品管理
- 未完了の在庫依頼 3件
- カタログ商品をCSVでインポートする。このページの準備が整いました
- カタログ商品をCSVでインポートする
- カタログ
- カタログを選択してください
- TEST_FAQ_カタログ001
- TEST_FAQ_CATCSV_20260628_082508_カタログ

### add-detail-after-validation

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products/3ef4eed8-c5da-5002-8f7a-d5f1984cdc92_CSVImportOperationCatalogProduct`
- 商品管理
- 未完了の在庫依頼 3件
- CSVインポート操作の詳細。このページの準備が整いました
- CSVインポート操作の詳細
- 実行する
- 検証ステータス
- 成功 完了
- 完了
- 実行ステータス
- 未実行
- 検証成功
- 1件の商品
- 検証失敗
- 0件の商品

### resume-connected-cdp

- URL: `about:blank`

### add-resume-detail-before-execution

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products/3ef4eed8-c5da-5002-8f7a-d5f1984cdc92_CSVImportOperationCatalogProduct`
- 商品管理
- 未完了の在庫依頼 3件
- CSVインポート操作の詳細。このページの準備が整いました
- CSVインポート操作の詳細
- 実行する
- 検証ステータス
- 成功 完了
- 完了
- 実行ステータス
- 未実行
- 検証成功
- 1件の商品
- 検証失敗
- 0件の商品

### add-resume-execute-dialog

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products/3ef4eed8-c5da-5002-8f7a-d5f1984cdc92_CSVImportOperationCatalogProduct`
- 商品管理
- 未完了の在庫依頼 3件
- CSVインポート操作の詳細。このページの準備が整いました
- CSVインポート操作の詳細
- 実行する
- 検証ステータス
- 成功 完了
- 完了
- 実行ステータス
- 未実行
- 検証成功
- 1件の商品
- 検証失敗
- 0件の商品
- カタログに商品を一括登録するCSVの取り込み処理を実行しますか？
- 1件のカタログ商品を登録します。この操作は巻き戻すことができません。

### add-resume-detail-after-execution

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products/3ef4eed8-c5da-5002-8f7a-d5f1984cdc92_CSVImportOperationCatalogProduct`
- 商品管理
- 未完了の在庫依頼 3件
- CSVインポート操作の詳細。このページの準備が整いました
- CSVインポート操作の詳細
- 実行する
- 検証ステータス
- 成功 完了
- 完了
- 実行ステータス
- 検証成功
- 1件の商品
- 検証失敗
- 0件の商品

### catalog-after-add

- URL: `https://www.sqstackstaging.com/admin/catalogs/6f694266-98e8-5ad1-8ad2-633dcd780670_Catalog`
- 商品管理
- カタログ
- 未完了の在庫依頼 3件
- TEST_FAQ_CATCSV_20260628_082508_カタログ。このページの準備が整いました
- TEST_FAQ_CATCSV_20260628_082508_カタログ
- インポート
- 商品
- 商品を追加する
- 商品コードで検索する
- 商品コード
- TEST_FAQ_CATCSV_20260628_082508_商品
- TEST_FAQ_CATCSV_20260628_082508

### delete-form-filled

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products/create`
- 商品管理
- 未完了の在庫依頼 3件
- カタログ商品をCSVでインポートする。このページの準備が整いました
- カタログ商品をCSVでインポートする
- カタログ
- カタログを選択してください
- TEST_FAQ_カタログ001
- TEST_FAQ_CATCSV_20260628_082508_カタログ

### delete-after-submit

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products/create`
- 商品管理
- 未完了の在庫依頼 3件
- カタログ商品をCSVでインポートする。このページの準備が整いました
- カタログ商品をCSVでインポートする
- カタログ
- カタログを選択してください
- TEST_FAQ_カタログ001
- TEST_FAQ_CATCSV_20260628_082508_カタログ

### delete-detail-after-validation

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products/823cab58-77e6-5fff-a9ef-a681d782fb46_CSVImportOperationCatalogProduct`
- 商品管理
- 未完了の在庫依頼 3件
- CSVインポート操作の詳細。このページの準備が整いました
- CSVインポート操作の詳細
- 実行する
- 検証ステータス
- 成功 完了
- 完了
- 実行ステータス
- 未実行
- 検証成功
- 1件の商品
- 検証失敗
- 0件の商品

### delete-execute-dialog

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products/823cab58-77e6-5fff-a9ef-a681d782fb46_CSVImportOperationCatalogProduct`
- 商品管理
- 未完了の在庫依頼 3件
- CSVインポート操作の詳細。このページの準備が整いました
- CSVインポート操作の詳細
- 実行する
- 検証ステータス
- 成功 完了
- 完了
- 実行ステータス
- 未実行
- 検証成功
- 1件の商品
- 検証失敗
- 0件の商品
- カタログに商品を一括登録するCSVの取り込み処理を実行しますか？
- 1件のカタログ商品を登録します。この操作は巻き戻すことができません。

### delete-detail-after-execution

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_catalog_products/823cab58-77e6-5fff-a9ef-a681d782fb46_CSVImportOperationCatalogProduct`
- 商品管理
- 未完了の在庫依頼 3件
- CSVインポート操作の詳細。このページの準備が整いました
- CSVインポート操作の詳細
- 実行する
- 検証ステータス
- 成功 完了
- 完了
- 実行ステータス
- 検証成功
- 1件の商品
- 検証失敗
- 0件の商品

### catalog-after-delete-import

- URL: `https://www.sqstackstaging.com/admin/catalogs/6f694266-98e8-5ad1-8ad2-633dcd780670_Catalog`
- 商品管理
- カタログ
- 未完了の在庫依頼 3件
- TEST_FAQ_CATCSV_20260628_082508_カタログ。このページの準備が整いました
- TEST_FAQ_CATCSV_20260628_082508_カタログ
- インポート
- 商品
- 商品を追加する
- 商品コードで検索する

### product-delete-dialog

- URL: `https://www.sqstackstaging.com/admin/products/8f534fe4-6243-5fb7-b49d-cf5556610317_Product`
- 商品管理
- カタログ
- 未完了の在庫依頼 3件
- TEST_FAQ_CATCSV_20260628_082508_商品。このページの準備が整いました
- TEST_FAQ_CATCSV_20260628_082508_商品
- 商品コード
- TEST_FAQ_CATCSV_20260628_082508
- 商品名
- 商品分類
- 商品タイプ
- 商品を削除しますか？
- この商品を削除しますか？
- この処理は巻き戻すことができません。
- 削除する

### product-after-delete

- URL: `https://www.sqstackstaging.com/admin/products/8f534fe4-6243-5fb7-b49d-cf5556610317_Product`
- 商品管理
- カタログ
- 未完了の在庫依頼 3件
- 該当するProductが見つかりませんでした。
- 再実行

### resume-connected-cdp

- URL: `about:blank`

### catalog-after-delete-import

- URL: `https://www.sqstackstaging.com/admin/catalogs/6f694266-98e8-5ad1-8ad2-633dcd780670_Catalog`
- 商品管理
- カタログ
- 未完了の在庫依頼 3件
- TEST_FAQ_CATCSV_20260628_082508_カタログ。このページの準備が整いました
- TEST_FAQ_CATCSV_20260628_082508_カタログ
- インポート
- 商品
- 商品を追加する
- 商品コードで検索する

### catalog-delete-dialog

- URL: `https://www.sqstackstaging.com/admin/catalogs/6f694266-98e8-5ad1-8ad2-633dcd780670_Catalog`
- 商品管理
- カタログ
- 未完了の在庫依頼 3件
- TEST_FAQ_CATCSV_20260628_082508_カタログ。このページの準備が整いました
- TEST_FAQ_CATCSV_20260628_082508_カタログ
- インポート
- 商品
- 商品を追加する
- 商品コードで検索する
- カタログを削除する
- カタログを削除します。この処理は巻き戻すことができません。
- 削除する

### catalog-after-delete

- URL: `https://www.sqstackstaging.com/admin/catalogs/6f694266-98e8-5ad1-8ad2-633dcd780670_Catalog`
- 商品管理
- カタログ
- 未完了の在庫依頼 3件
- 該当するCatalogが見つかりませんでした。
- 再実行

