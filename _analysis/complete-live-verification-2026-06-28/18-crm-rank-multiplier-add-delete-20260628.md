# CRM 会員ランク倍率 追加/削除 実機確認 2026-06-28

- 対象ルール: `TEST_FAQ_注文ポイント付与ルール`
- 対象URL: `https://www.sqstackstaging.com/admin/point_calculation_rules/4d73fe29-07c9-5370-80a2-61c3ad3aadfa_PointCalculationRule/rank_multipliers`
- 追加対象: `Bronze` / `2倍`

## 結果

| 確認項目 | 結果 |
|:--|:--|
| 追加ダイアログに会員ランクと倍率が表示 | `True` |
| `Bronze` が選択可能 | `True` |
| 追加後一覧に `Bronze` が表示 | `True` |
| 追加後一覧に `2倍` が表示 | `True` |
| 削除確認ダイアログを確認 | `True` |
| 削除後一覧から `Bronze` が消える | `True` |

## 削除確認ダイアログ

会員ランク倍率を削除しますか？ 選択された1件の会員ランク倍率を削除します。この処理は巻き戻すことができません。 キャンセル 削除する

## 判断

- 注文ポイント付与ルール詳細の `会員ランク倍率` タブでは、会員ランクを選択し倍率を保存できる。
- 保存後は会員ランク名と倍率が一覧に反映される。
- 行選択後の `削除する` で削除確認ダイアログを経て削除でき、リロード後も一覧から消える。
- 実注文に対する倍率計算結果は、注文/顧客/ポイント実績が必要なため未確認。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/18-crm-rank-multiplier-add-delete-20260628.json`
- 追加後スクリーンショット: `_analysis/complete-live-verification-2026-06-28/18-crm-rank-multiplier-after-add-20260628.png`
- 削除後スクリーンショット: `_analysis/complete-live-verification-2026-06-28/18-crm-rank-multiplier-after-delete-20260628.png`
