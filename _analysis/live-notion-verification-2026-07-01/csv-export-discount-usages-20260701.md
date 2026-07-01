# 2026-07-01 ディスカウント利用履歴CSVエクスポート 実機確認

## 対象

- 作成画面: `/admin/csv_export/csv_export_operation_order_price_adjustment_usages/create`
- 履歴画面: `/admin/csv_export/csv_export_operation_order_price_adjustment_usages`

## フォーム確認

- フォーム項目は `ディスカウント` と `エクスポートを開始する`。
- 選択ダイアログは `タイトル / ステータス` 列で、有効な候補が2件表示された。
- `TEST_FAQ_ディスカウント_対象商品テスト` を1件チェックすると、他候補のチェックボックスがdisabledになったため、ディスカウントは実質1件指定。

## 実行結果

- 選択ディスカウント: `TEST_FAQ_ディスカウント_対象商品テスト`
- 作成時刻表示: `2026年07月01日 14:59`
- 履歴一覧の列: `作成日 / ディスカウント / ステータス / ダウンロード`
- 開始直後: `注意 処理中`
- 完了後: `成功 完了` と `ダウンロード` リンクを表示
- CSV行数: 1（ヘッダーのみ）
- CSVサイズ: 27 bytes

## CSVヘッダー

```csv
顧客ID,顧客外部ID,店舗名,店舗コード,利用日時
```

## 注意点

- 利用履歴が0件でも空レスポンスではなく、ヘッダーのみのCSVがダウンロードされる。
- 実際に注文でディスカウントが使われた場合のデータ行は未確認。

## ドキュメント反映先

- `04-notion/22-CSV・PDF・データ移行.md`
- `01-by-feature/CSVエクスポート・PDFエクスポート.md`
- `02-by-task/データをCSV・PDFでエクスポートする.md`
- `03-faq/CSVインポート・エクスポートのよくある質問.md`
- `_analysis/NOTION-LIVE-VERIFICATION-LEDGER-2026-06-27.md`
- `_analysis/WBS-JULY-END-SCOPE-REVIEW-2026-06-21.md`
