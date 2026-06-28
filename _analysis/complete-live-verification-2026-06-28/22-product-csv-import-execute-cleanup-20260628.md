# 22 商品CSVインポート実行・削除確認 2026-06-28

## 対象

- CSV: `_analysis/complete-live-verification-2026-06-28/22-product-csv-import-execute-cleanup-20260628_081405.csv`
- 商品コード: `TEST_FAQ_CSV_EXEC_20260628_081405`
- 商品名: `TEST_FAQ_CSV_EXEC_20260628_081405_商品`
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/22-product-csv-import-execute-cleanup-20260628.json`

## 結果

- 検証成功件数: `1個の商品`
- 実行確認ダイアログ: `確認`
- 実行ステータス: `成功 完了`
- 商品一覧/詳細反映: `確認`
- 商品削除: `確認`

## 判定

- 商品CSVインポートは、CSVアップロード後に検証ステータスが成功完了となり、`実行する` で確認ダイアログを経て実行される。
- 確認ダイアログには `この操作は巻き戻すことができません` が表示される。
- 実行ステータスは時間差で `成功 完了` になり、検証用商品は商品一覧/詳細に反映された。
- 検証用商品は商品詳細から削除でき、削除後は該当Productなし表示になった。

## ステップ

### connected-cdp

- URL: `about:blank`

### create-before-upload

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products/create`
- 商品管理
- 未完了の在庫依頼 3件
- 商品をCSVでインポートする。このページの準備が整いました
- 商品をCSVでインポートする
- CSVファイル
- ファイルをアップロード
- ファイルを選択する
- 保存する

### create-file-selected

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products/create`
- 商品管理
- 未完了の在庫依頼 3件
- 商品をCSVでインポートする。このページの準備が整いました
- 商品をCSVでインポートする
- CSVファイル
- 保存する

### after-submit

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products/create`
- 商品管理
- 未完了の在庫依頼 3件
- 商品をCSVでインポートする。このページの準備が整いました
- 商品をCSVでインポートする
- CSVファイル
- 保存する
- CSVインポートの検証を開始しました

### detail-after-validation-poll

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products/183e9028-641f-5c13-8686-716bca2ad990_CSVImportOperationProduct`
- 商品管理
- 未完了の在庫依頼 3件
- CSVインポート操作の詳細。このページの準備が整いました
- CSVインポート操作の詳細
- 実行する
- 作成日
- 検証ステータス
- 成功 完了
- 完了
- 実行ステータス
- 未実行
- 検証成功
- 1個の商品
- 検証失敗
- 0個の商品

### execute-dialog

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products/183e9028-641f-5c13-8686-716bca2ad990_CSVImportOperationProduct`
- 商品管理
- 未完了の在庫依頼 3件
- CSVインポート操作の詳細。このページの準備が整いました
- CSVインポート操作の詳細
- 実行する
- 作成日
- 検証ステータス
- 成功 完了
- 完了
- 実行ステータス
- 未実行
- 検証成功
- 1個の商品
- 検証失敗
- 0個の商品
- CSVの取り込み処理を実行しますか？
- 1件の商品を登録します。この操作は巻き戻すことができません。

### after-confirm-execute

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products/183e9028-641f-5c13-8686-716bca2ad990_CSVImportOperationProduct`
- 商品管理
- 未完了の在庫依頼 3件
- CSVインポート操作の詳細。このページの準備が整いました
- CSVインポート操作の詳細
- 実行する
- 作成日
- 検証ステータス
- 成功 完了
- 完了
- 実行ステータス
- 未実行
- 検証成功
- 1個の商品
- 検証失敗
- 0個の商品
- CSVの取り込み処理を実行しますか？
- 1件の商品を登録します。この操作は巻き戻すことができません。

### detail-after-execution-poll

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products/183e9028-641f-5c13-8686-716bca2ad990_CSVImportOperationProduct`
- 商品管理
- 未完了の在庫依頼 3件
- CSVインポート操作の詳細。このページの準備が整いました
- CSVインポート操作の詳細
- 実行する
- 作成日
- 検証ステータス
- 成功 完了
- 完了
- 実行ステータス
- 未実行
- 検証成功
- 1個の商品
- 検証失敗
- 0個の商品
- CSVの取り込み処理を実行しますか？
- 1件の商品を登録します。この操作は巻き戻すことができません。

### products-search-after-execute

- URL: `https://www.sqstackstaging.com/admin/products`
- 商品管理
- 未完了の在庫依頼 3件
- 商品管理。このページの準備が整いました
- インポート
- 商品を作成する
- 商品
- ステータス
- 商品コード
- 商品タイプ
- TEST_E2E_20260622 GU検証Tシャツ 1905
- TEST_E2E_20260622 GU検証Tシャツ 1845
- TEST_E2E_20260622 GU検証Tシャツ 1830
- TEST_E2E_20260622 GU検証Tシャツ 1755
- TEST_E2E_20260622 GU検証Tシャツ 1740
- 成功
- TEST_FAQ_CSV_RECHECK_20260608_01
- 検証

### detail-recheck-execution-success

- URL: `https://www.sqstackstaging.com/admin/csv_import/csv_import_operation_products/183e9028-641f-5c13-8686-716bca2ad990_CSVImportOperationProduct`
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
- 1個の商品
- 検証失敗
- 0個の商品

### product-detail-before-delete-recheck

- URL: `https://www.sqstackstaging.com/admin/products/cc121063-9f9d-54ee-81f6-dfa3b2f9676c_Product`
- 商品管理
- 未完了の在庫依頼 3件
- TEST_FAQ_CSV_EXEC_20260628_081405_商品。このページの準備が整いました
- TEST_FAQ_CSV_EXEC_20260628_081405_商品
- 商品コード
- TEST_FAQ_CSV_EXEC_20260628_081405
- 商品名
- 商品分類
- 商品タイプ
- TEST_FAQ_CSV_EXEC

### delete-dialog-recheck

- URL: `https://www.sqstackstaging.com/admin/products/cc121063-9f9d-54ee-81f6-dfa3b2f9676c_Product`
- 商品管理
- 未完了の在庫依頼 3件
- TEST_FAQ_CSV_EXEC_20260628_081405_商品。このページの準備が整いました
- TEST_FAQ_CSV_EXEC_20260628_081405_商品
- 商品コード
- TEST_FAQ_CSV_EXEC_20260628_081405
- 商品名
- 商品分類
- 商品タイプ
- TEST_FAQ_CSV_EXEC
- 商品を削除しますか？
- この商品を削除しますか？
- この処理は巻き戻すことができません。
- 削除する

### product-detail-after-delete-recheck

- URL: `https://www.sqstackstaging.com/admin/products/cc121063-9f9d-54ee-81f6-dfa3b2f9676c_Product`
- 商品管理
- 未完了の在庫依頼 3件
- 該当するProductが見つかりませんでした。
- 再実行

