# ヤマトB2クラウド出荷実績CSV 追加検証 2026-07-01

対象環境: `https://www.sqstackstaging.com/admin`

## 対象データ

- 注文: `FAQ-YAMATO-CSV-20260701134406`
- 注文ID: `16cc169a-468b-53a1-8455-aa7c5863ff27_Order`
- 作成方法: 内部GraphQL `orderCreate`
- 注文条件:
  - `inventoryBehavior = DECREMENT`
  - `requiresFulfillment = true`
  - `paymentStatus = PAID`
  - 作成直後 `fulfillmentStatus = UNFULFILLED`
- 出荷指示: `#IO-1048`
- 出荷指示ID: `fe9c2dbb-4ca5-54bb-afb9-f864659c2d4f_InventoryOutboundOrder`
- 作成直後の一覧行: `情報 未完了 / 出荷待ち`、引当ステータス `情報 未完了 / 引当待ち`
- SKU: `TEST_E2E_20260622_GU_1905_NAVY_M`
- 出荷場所: `TEST_E2E_20260622_GU倉庫_ON_1905`

## CSV取込

- CSV: `_analysis/live-notion-verification-2026-07-01/yamato-b2-import-io-nohash-20260701.csv`
- `お客様管理番号`: `IO-1048`
- `伝票番号`: `FAQYB2202607011048A`
- `出荷日`: `2026-07-01`
- アップロード方法: 画面のDropZoneへドラッグ&ドロップ

結果:

- DropZone経由ではファイル名が表示され、`保存する` でインポート詳細が作成された。
- 詳細URL: `/admin/csv_import/csv_import_operation_fulfillment_by_yamato_b2_clouds/257523da-22f9-5086-9db8-4a01a9a76e4f_CSVImportOperationFulfillmentByYamatoB2Cloud`
- 画面上は `CSVのバリデーションを実行しています`、`検証成功 0件の出荷結果`、`検証失敗 0件の出荷結果`、`実行ステータス 未実行` と表示され続ける。
- 内部GraphQLでは以下の状態だった。
  - `isRunningValidationJob = false`
  - `isCompletedValidationJob = false`
  - `isFailedValidationJob = true`
  - `validationSuccessCount = 0`
  - `validationFailureCount = 0`
  - `validationFailures.nodes = []`
  - `validationSuccesses.nodes = []`
- 2026-06-28の `#IO-1032` 取込履歴も内部GraphQLでは同じく `isFailedValidationJob = true`、成功0件/失敗0件だった。

結論:

- 少なくとも検証用CSV（`#IO-1032`、`IO-1048`）では、ヤマトB2出荷実績CSVのバリデーションジョブが内部的に失敗し、実行可能状態にならない。
- UIは失敗状態を明示せず、バリデーション中の文言を出し続ける。画面表示だけを見て「処理中」と案内しない。
- CSV取込による `#IO-1048` の出荷完了遷移・配送キャリア/追跡コード反映は確認できなかった。

## 後処理

CSVで完了できなかったため、検証用出荷指示 `#IO-1048` は手動で出荷実績を登録した。

- 配送キャリア: `FAQCarrier-YamatoCSVFallback-20260701`
- 追跡コード: `FAQ-YB2-FALLBACK-1048`
- 登録後の一覧行: `成功 完了 / 出荷完了`
- 出荷待ちタブ: `新規 0`
- 注文 `FAQ-YAMATO-CSV-20260701134406` は内部GraphQLで `fulfillmentStatus = FULFILLED`、`fulfilledAt = 2026-07-01T13:53:52Z`

この後処理はCSV取込結果ではなく、未完了データを残さないための手動登録。
