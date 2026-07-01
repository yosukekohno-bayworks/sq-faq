# 2026-07-01 セール価格CSVエクスポート 実機確認

## 対象

- 作成画面: `/admin/csv_export/csv_export_operation_product_price_rule_sale_prices/create`
- 履歴画面: `/admin/csv_export/csv_export_operation_product_price_rule_sale_prices`

## フォーム確認

- フォーム項目は `販売価格ルール` と `エクスポートを開始する`。
- 販売価格ルールは通常のセレクトボックス。
- 候補:
  - `TEST_FAQ_販売価格ルール (JPY)`
  - `TEST_FAQ_販売価格ルール_遷移確認_20260607 (JPY)`
  - `TEST_FAQ_DEEP_202606080340_販売価格ルール (JPY)`
  - `TEST_FAQ_20260624_販売価格_100908 (USD)`
  - `年末セール価格 (JPY)`

## 実行結果

- 選択ルール: `年末セール価格 (JPY)`
- 作成時刻表示: `2026年07月01日 15:03`
- 履歴一覧の列: `作成日時 / 販売価格ルール / ステータス / ダウンロード`
- 開始直後: `注意 処理中`
- 完了後: `成功 完了` と `ダウンロード` リンクを表示
- CSV行数: 2（ヘッダー + セール価格1件）
- CSVサイズ: 198 bytes

## CSVヘッダー

```csv
ProductVariantID,ExternalID,PriceAmount,PriceAmountAfterTaxes,CurrencyCode,StartsAt,EndsAt
```

## サンプル行

```csv
505ffa58-952d-5932-9a5b-57036ea7eb39_ProductVariant,,1000,1100,JPY,2026-06-30 15:00:00,2026-07-07 14:59:00
```

## 注意点

- 履歴一覧ではルール名は `年末セール価格` と表示され、通貨コードは表示されない。
- CSVのデータ行はSKU文字列ではなく `ProductVariantID` をキーとして出力される。

## ドキュメント反映先

- `04-notion/22-CSV・PDF・データ移行.md`
- `01-by-feature/CSVエクスポート・PDFエクスポート.md`
- `02-by-task/データをCSV・PDFでエクスポートする.md`
- `03-faq/CSVインポート・エクスポートのよくある質問.md`
- `_analysis/NOTION-LIVE-VERIFICATION-LEDGER-2026-06-27.md`
- `_analysis/WBS-JULY-END-SCOPE-REVIEW-2026-06-21.md`
