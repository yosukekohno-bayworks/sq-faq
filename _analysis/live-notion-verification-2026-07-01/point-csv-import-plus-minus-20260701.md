# ポイント一括加算・減算CSV 実データ取込検証（2026-07-01）

## 対象

- ポイント一括加算: `/admin/csv_import/csv_import_operation_point_pluses`
- ポイント一括減算: `/admin/csv_import/csv_import_operation_point_minuses`
- ポイント変動履歴CSV: `/admin/csv_export/csv_export_operation_point_changes`

## テンプレート確認

### 一括加算

- フォーマットCSVヘッダー: `customer_id,title,points,available_date,expires_date,note`
- 定義:
  - `customer_id`: 必須。SQが発番した顧客ID、またはShopifyなど外部システムの顧客ID。
  - `title`: 必須。
  - `points`: 必須。1ポイント以上。
  - `available_date`: 任意。指定する場合はインポート実行日以降。
  - `expires_date`: 必須。インポート実行日以降。
  - `note`: 任意。

### 一括減算

- フォーマットCSVヘッダー: `customer_id,title,points,note`
- 定義:
  - `customer_id`: 必須。テンプレート定義ではShopify customer ID。
  - `title`: 必須。
  - `points`: 必須。正の整数で指定する。マイナス値ではなく、減算したい値を正数で入れる。
  - `note`: 任意。

## 検証対象顧客

- 顧客: `検証顧客ユニクロ095318FAQ`
- SQ顧客ID: `e284db39-9ba1-587e-a3b1-aa0700076c2e_PurchasingCustomer`
- 外部ID: `FAQ_E2E_UNIQLO_CUSTOMER_20260628095318`
- 会員番号: `FAQUNI0628095318`
- テナント: `ユニクロ`
- 加算前の顧客詳細: `保有ポイント 0 ポイント`, `付与予定 0 ポイント`, `ポイント履歴はありません`

## 一括加算

CSV:

```csv
customer_id,title,points,available_date,expires_date,note
e284db39-9ba1-587e-a3b1-aa0700076c2e_PurchasingCustomer,FAQ_POINT_PLUS_20260701,5,,2026-07-31,FAQ verification plus 20260701
```

フォーム:

- テナント: `ユニクロ`
- 顧客IDの種別: `SQが発番した顧客ID`
- ファイル: `point-plus-import-20260701.csv`

結果:

- 操作詳細: `/admin/csv_import/csv_import_operation_point_pluses/3f05c6af-c0c6-537c-af1d-706cb823039d_CSVImportOperationPointPlus`
- 作成日時: `2026年07月01日 21:06`
- 検証結果: `成功 成功`, `検証成功 (1件)`, `検証失敗 (0件)`
- 実行確認ダイアログ: `1件のポイント付与を実行します。この操作は巻き戻すことができません。`
- 実行結果: `成功 成功`, `実行成功 (1件)`, `実行失敗 (0件)`
- 実行開始/終了: `2026年07月01日 21:07` / `2026年07月01日 21:08`
- 顧客詳細反映: `保有ポイント 5 ポイント`, `付与予定 0 ポイント`
- 顧客詳細の履歴行: `FAQ_POINT_PLUS_20260701`, `5`, `2026年07月01日 21:08`, `2026年07月01日 21:08`, `2026年07月31日`

補足:

- 別テナント所属の顧客IDを `ユニクロ` で加算した場合、検証は成功するが実行で失敗した。
- 失敗理由は `tenantID or purchasingCustomerID is incorrect`。顧客名は検証成功側で解決されても、テナント不一致は実行時に落ちる。

## 一括減算

SQ顧客IDで試したCSV:

```csv
customer_id,title,points,note
e284db39-9ba1-587e-a3b1-aa0700076c2e_PurchasingCustomer,FAQ_POINT_MINUS_20260701,2,FAQ verification minus 20260701
```

結果:

- 操作詳細: `/admin/csv_import/csv_import_operation_point_minuses/7a5cfe4c-4c2d-566d-b952-3840cce50730_CSVImportOperationPointMinus`
- 検証結果: `重大 失敗`, `検証成功 (0件)`, `検証失敗 (1件)`
- 検証失敗詳細: `2 customer_id: 指定された顧客IDの顧客が存在しません`

外部IDで再実行したCSV:

```csv
customer_id,title,points,note
FAQ_E2E_UNIQLO_CUSTOMER_20260628095318,FAQ_POINT_MINUS_20260701,2,FAQ verification minus 20260701
```

フォーム:

- テナント: `ユニクロ`
- ファイル: `point-minus-import-20260701.csv`
- 顧客IDの種別フィールド: なし

結果:

- 操作詳細: `/admin/csv_import/csv_import_operation_point_minuses/313f5a20-9b68-5434-81f2-fc65e34d589e_CSVImportOperationPointMinus`
- 作成日時: `2026年07月01日 21:14`
- 検証結果: `成功 成功`, `検証成功 (1件)`, `検証失敗 (0件)`
- 実行確認ダイアログ: `1件のポイント減算を実行します。この操作は巻き戻すことができません。`
- 実行結果: `成功 成功`, `実行成功 (1件)`, `実行失敗 (0件)`
- 実行開始/終了: `2026年07月01日 21:16` / `2026年07月01日 21:17`
- 顧客詳細反映: `保有ポイント 3 ポイント`, `付与予定 0 ポイント`
- 顧客詳細の履歴行: `FAQ_POINT_MINUS_20260701`, `-2`, `2026年07月01日 21:17`, `2026年07月01日 21:17`, 失効日空欄

## ポイント変動履歴CSV

加算後のエクスポート:

- 作成日時: `2026年07月01日 21:10`
- テナント: `ユニクロ`
- 対象期間: `2026年07月01日 00:00 〜 2026年07月01日 23:59`
- ステータス: `注意 処理中` → `成功 完了`
- 実ファイル: `point-change-after-plus-20260701-2110.csv`
- 行数: 2行（ヘッダー + 加算1行）
- 加算行: `FAQ_POINT_PLUS_20260701`, `Delta=5`, `PointChangeActivityType=EARNED`

減算後のエクスポート:

- 作成日時: `2026年07月01日 21:19`
- テナント: `ユニクロ`
- 対象期間: `2026年07月01日 00:00 〜 2026年07月01日 23:59`
- ステータス: `注意 処理中` → `成功 完了`
- 実ファイル: `point-change-after-minus-20260701-2119.csv`
- 行数: 3行（ヘッダー + 加算1行 + 減算1行）
- ヘッダー: `PointChangeID,PurchasingCustomerID,PurchasingCustomerBarcode,Title,Delta,AvailableAt,ExpiresDate,PointChangeCreatedAt,PointChangeActivityType,Note`
- 加算行: `FAQ_POINT_PLUS_20260701`, `Delta=5`, `PointChangeActivityType=EARNED`, `Note=FAQ verification plus 20260701`
- 減算行: `FAQ_POINT_MINUS_20260701`, `Delta=-2`, `PointChangeActivityType=USED`, `Note=FAQ verification minus 20260701`

## 結論

- 一括加算は、フォームで顧客IDの種別を指定できる。今回のSQ顧客ID指定では検証・実行とも成功した。
- 一括減算は、フォームに顧客IDの種別がない。SQ顧客IDでは検証失敗し、外部IDでは検証・実行とも成功した。
- 減算CSVの `points` は正数で入れるが、顧客詳細とポイント変動履歴CSVでは `-2` として反映される。
- ポイント変動履歴CSVは、実績0件ではヘッダーのみ、実績ありでは加算/減算行を出力する。加算は `EARNED`、減算は `USED`。
