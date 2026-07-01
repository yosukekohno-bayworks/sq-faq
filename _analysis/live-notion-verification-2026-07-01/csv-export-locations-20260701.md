# 2026-07-01 ロケーションCSVエクスポート 実機確認

## 対象

- 作成画面: `/admin/csv_export/csv_export_operation_location_by_location_group/create`
- 履歴画面: `/admin/csv_export/csv_export_operation_location_by_location_group`

## フォーム確認

- フォーム項目は `ロケーショングループ` と `エクスポートを開始する`。
- 選択ダイアログには `テスト`, `TEST_FAQ_20260624_LG_171810`, `ユニクログループ`, `GU グループ` が表示された。
- `ユニクログループ` を1件チェックすると他グループのチェックボックスがdisabledになったため、ロケーショングループは実質1件指定。

## 実行結果

- 選択グループ: `ユニクログループ`
- 作成時刻表示: `2026年07月01日 14:55`
- 履歴一覧の列: `作成日 / ロケーショングループ / ステータス / ダウンロード`
- 開始直後: `注意 処理中`
- 完了後: `成功 完了` と `ダウンロード` リンクを表示
- CSV行数: 4（ヘッダー + ロケーション3件）
- CSVサイズ: 465 bytes

## CSVヘッダー

```csv
Name,DisplayName,ExternalID,IsListedPublic,IsArchived,LocationCode,Tags,Email,LocationType,PointApplicationType,IsLocalPickupEnabled,IsInventoryAllocationRequestEnabled,MapURL,Phone,CountryCode,PostalCode,Province,City,Address1,Address2
```

## サンプル行

```csv
ユニクロEC,ユニクロEC,,true,false,TESTEC01,,,RETAIL,DISCOUNT,false,false,,,,,,,,
ユニクロ物流倉庫,ユニクロ物流倉庫,,true,false,W0001,,,WAREHOUSE,DISCOUNT,false,false,,,,,,,,
ユニクロ - 銀座店,ユニクロ - 銀座店,,true,false,R0001,,,RETAIL,DISCOUNT,false,false,,,,,,,,
```

## 注意点

- `LocationType` は `RETAIL` / `WAREHOUSE` として出力される。
- `IsLocalPickupEnabled` と `IsInventoryAllocationRequestEnabled` も列として出力される。
- ロケーショングループ名はCSV本体には含まれず、履歴一覧の `ロケーショングループ` 列で確認する。

## ドキュメント反映先

- `04-notion/22-CSV・PDF・データ移行.md`
- `01-by-feature/CSVエクスポート・PDFエクスポート.md`
- `02-by-task/データをCSV・PDFでエクスポートする.md`
- `03-faq/CSVインポート・エクスポートのよくある質問.md`
- `_analysis/NOTION-LIVE-VERIFICATION-LEDGER-2026-06-27.md`
- `_analysis/WBS-JULY-END-SCOPE-REVIEW-2026-06-21.md`
