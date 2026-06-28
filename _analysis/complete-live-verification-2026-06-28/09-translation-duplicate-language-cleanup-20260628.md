# 翻訳ルール 同一言語・自動生成保存・削除確認 2026-06-28

## 検証データ

- ルールA: `TEST_FAQ_TRANSLATION_DUP_A_20260628063821`（英語、自動生成ON）
- ルールB: `TEST_FAQ_TRANSLATION_DUP_B_20260628063821`（英語、自動生成OFF）

## 結果

| 項目 | 結果 |
|:--|:--|
| 作成フォームの言語選択肢 | `['選択してください', '日本語', '英語', '中国語（簡体字）', '中国語（繁体字）', '韓国語', 'スペイン語', 'フランス語', 'ドイツ語', 'ヒンディー語', 'タイ語']` |
| 既存の英語ルール数 | `2` |
| 同一言語2件の新規作成 | `True` |
| 自動生成ONの保存状態 | `{'index': 2, 'tag': 'input', 'type': 'checkbox', 'placeholder': '', 'value': 'true', 'checked': True, 'disabled': False, 'readOnly': False, 'label': '翻訳データを自動で作成する', 'options': []}` |
| 自動生成OFFの保存状態 | `{'index': 2, 'tag': 'input', 'type': 'checkbox', 'placeholder': '', 'value': 'false', 'checked': False, 'disabled': False, 'readOnly': False, 'label': '翻訳データを自動で作成する', 'options': []}` |
| 手動実行ボタン | `{'noneFound': True, 'hits': []}` |
| 検証用ルール削除 | `True` |

## 判断

- 2026-06-28時点の現行UIでは、同じ言語（英語）の翻訳ルールを複数作成できる。一覧にも同一言語の複数行が並ぶ。
- `翻訳データを自動で作成する` は保存後の詳細画面でもチェック状態が残る。
- 翻訳トップ/一覧/作成フォーム/詳細画面の確認範囲では、手動の `実行` / `再実行` / `翻訳する` / `生成` ボタンは見当たらない。
- 検証用翻訳ルール2件は一覧の行選択後 `削除する` で削除済み。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/09-translation-duplicate-language-cleanup-20260628.json`
