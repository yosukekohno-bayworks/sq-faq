# ポイント変動履歴CSVエクスポート実ファイル検証（2026-07-01）

## 対象

- 画面: `/admin/csv_export/csv_export_operation_point_changes/create`
- 一覧: `/admin/csv_export/csv_export_operation_point_changes`
- カテゴリ: CSVエクスポート > ポイント > ポイント変動履歴

## フォーム

- 見出し: `ポイント変動履歴をCSVでエクスポートする`
- 項目:
  - `テナント*`
  - `開始日時*`
  - `終了日時*`
- テナント候補:
  - `ユニクロ`
  - `TEST_FAQ_COVERAGE_20260615_テナント_EDIT`
  - `テストテナント`
  - `TEST_FAQ_20260624_TENANT_170037`

## 実行条件

- テナント: `ユニクロ`
- 開始日時: `2026-06-01T00:00`
- 終了日時: `2026-07-01T23:59`

## 一覧履歴

- 実行直後:
  - 作成日: `2026年07月01日 19:37`
  - テナント: `ユニクロ`
  - 対象期間: `2026年06月01日 00:00 〜 2026年07月01日 23:59`
  - ステータス: `注意 処理中`
  - ダウンロード: 空
- 再読み込み後:
  - ステータス: `成功 完了`
  - ダウンロード: `ダウンロード` リンク表示

## CSV本体

- ファイル名: `20260701-1937.csv`
- サイズ: 147 bytes
- 行数: 1行（ヘッダーのみ）
- ヘッダー:

```csv
PointChangeID,PurchasingCustomerID,PurchasingCustomerBarcode,Title,Delta,AvailableAt,ExpiresDate,PointChangeCreatedAt,PointChangeActivityType,Note
```

## 判断

- ポイント変動履歴CSVは、対象期間にポイント実績が0件でも空ファイルではなくヘッダーのみのCSVとしてダウンロードできる。
- 実績0件時の挙動はこの時点ではヘッダーのみでした。後続の `_analysis/live-notion-verification-2026-07-01/point-csv-import-plus-minus-20260701.md` で、ポイント一括加算/減算後の実績データ行（加算 `EARNED`、減算 `USED`）まで確認済みです。
- 一覧履歴の列は `作成日 / テナント / 対象期間 / ステータス / ダウンロード`。
