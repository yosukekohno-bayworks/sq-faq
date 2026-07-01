# 2026-07-01 在庫CSVエクスポート 実機確認

## 対象

- 作成画面: `/admin/csv_export/csv_export_operation_inventory_logical_quantities/create`
- 履歴画面: `/admin/csv_export/csv_export_operation_inventory_logical_quantities`

## フォーム確認

- フォーム項目は `ロケーション` と `エクスポートを開始する` のみ。
- `カタログ` など商品集合を指定する項目はない。
- ロケーション選択ダイアログは `すべて / 店舗 / 倉庫` タブ、列は `名前 / 場所コード`。
- 2026-07-01実機確認では、`ユニクロ物流倉庫` を1件チェックすると、別行の `ユニクロ - 銀座店` のチェックボックスがdisabledになり、2件目をチェックできなかった。そのため在庫CSVエクスポートは実質1ロケーション指定として扱う。

## 実行結果

- 選択ロケーション: `ユニクロ物流倉庫`
- 作成時刻表示: `2026年07月01日 14:51`
- 履歴一覧の列: `作成日 / 店舗 / ステータス / ダウンロード`
- 開始直後: `注意 処理中`
- 完了後: `成功 完了` と `ダウンロード` リンクを表示
- CSV行数: 98
- CSVサイズ: 12,939 bytes

## CSVヘッダー

```csv
SKU,ProductVariantID,InventoryItemID,Incoming,Available,Committed,Reserved,Damaged,SafetyStock,QualityControl,OnHand
```

## サンプル行

```csv
486125-31-XL,21d354c4-8757-54c6-ae20-3cc20db613dd_ProductVariant,30c999b0-145d-5304-b522-c4e3cda1abd5_InventoryItem,0,-1,0,0,0,0,0,-1
486102-70-S,505ffa58-952d-5932-9a5b-57036ea7eb39_ProductVariant,0d5dab1c-5889-5963-966f-01aa6a4c588c_InventoryItem,0,-1,0,0,0,0,0,-1
```

## 注意点

- CSV本体にはロケーション名・場所コード列がない。選択ロケーションは履歴一覧の `店舗` 列で確認する。
- `Available` や `OnHand` にはマイナス値も出る。
- 本機能はCSVエクスポートであり、外部在庫同期の対象商品指定ではない。カタログ指定はこのフォームにはない。

## ドキュメント反映先

- `04-notion/22-CSV・PDF・データ移行.md`
- `01-by-feature/CSVエクスポート・PDFエクスポート.md`
- `02-by-task/データをCSV・PDFでエクスポートする.md`
- `03-faq/CSVインポート・エクスポートのよくある質問.md`
- `_analysis/NOTION-LIVE-VERIFICATION-LEDGER-2026-06-27.md`
- `_analysis/WBS-JULY-END-SCOPE-REVIEW-2026-06-21.md`
