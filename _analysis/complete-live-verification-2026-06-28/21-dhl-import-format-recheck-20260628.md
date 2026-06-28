# 21 DHL出荷実績CSVインポート フォーマット表示 実機確認 2026-06-28

## 対象

- 一覧: `/admin/csv_import/csv_import_operation_fulfillment_by_dhls`
- 作成: `/admin/csv_import/csv_import_operation_fulfillment_by_dhls/create`

## 操作

1. DHL出荷実績CSVインポート一覧を開いた。
2. 一覧内のテンプレートリンク/ボタン有無を確認した。
3. 新規インポート作成画面を開いた。
4. 作成画面内の入力項目、テンプレート表記、空保存エラーを確認した。

## 結果

| 確認項目 | 結果 |
|:--|:--|
| 一覧h1 | `DHLの出荷実績をCSVでインポートする` |
| 一覧の主導線 | `新規インポート` |
| 一覧のテンプレート表記 | なし |
| 一覧のデータ状態 | `アイテムが見つかりませんでした` |
| 作成フォームh1 | `DHLの出荷実績をCSVでインポートする` |
| 作成フォーム入力 | `CSVファイル` のfile inputのみ |
| 作成フォームのテンプレート表記 | なし |
| ファイル未選択保存 | `ファイルを選択してください` |

## 判断

- DHL出荷実績CSVはインポート導線とファイルアップロード欄は確認できる。
- 2026-06-28時点の管理画面UIには、DHLのテンプレートリンク、列数、必須列、列名説明は表示されない。
- DHL CSVの正確なフォーマットは、実CSVサンプルまたは開発元確認が必要。ヤマトB2クラウドの10列/必須3列仕様をDHLへ流用して案内しない。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/21-dhl-import-format-recheck-20260628.json`
- 実行スクリプト: `_analysis/complete-live-verification-2026-06-28/21-dhl-import-format-recheck-20260628.py`
