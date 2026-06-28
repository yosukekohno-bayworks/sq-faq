# 09/10 翻訳・採寸 再確認 2026-06-28

- 実行日時: 2026-06-27T22:26:28.217709+00:00
- JSON: `_analysis/complete-live-verification-2026-06-28/09-10-translation-measurement-readonly-recheck-20260628.json`
- エラー数: `0`

## 結果

- 翻訳トップ/ルール一覧/作成/詳細で、手動実行系ボタン（`実行` / `再実行` / `翻訳する` / `生成`）の一致数: `0`
- 翻訳詳細URL: `/admin/settings/translation/translation_rules/19b42234-5a07-55fa-812f-4e483d8f2a99_TranslationRule`
- 採寸詳細URL: `/admin/settings/product_measurement_rules/50bec65a-f55f-53c6-9a3e-b4496f09d1ba_ProductMeasurementRule`
- 商品詳細 `486125` の採寸/測定/measurementキーワード: `[]`
- 商品詳細 `482787` の採寸/測定/measurementキーワード: `[]`

## 採寸ルール詳細の入力状態

| ラベル | tag | disabled | readonly |
|:--|:--|:--|:--|
| ルール名 | input | `False` | `True` |
| 採寸単位 | input | `False` | `True` |
| 採寸項目1 | input | `False` | `True` |
| 採寸項目2 | input | `False` | `True` |
| 採寸項目3 | input | `False` | `True` |
| 採寸項目4 | input | `False` | `True` |
| 採寸項目5 | input | `False` | `True` |

## 判断

- 翻訳は、確認範囲の管理画面UIに手動実行ボタンがない。
- 採寸ルールは詳細の入力がreadonlyで、テンプレート定義の確認画面として扱う。
- 商品詳細2件では採寸・測定・measurement系の表示がなく、個別商品への紐づけ導線は管理画面UI上では確認できない。
- 実際の翻訳生成結果、採寸情報の外部/API経由適用、ストアフロント/チャネル反映はこのUI確認だけでは確定できない。