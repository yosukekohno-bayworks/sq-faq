# CRM 会員ランク算出タイミング設定 実機確認 2026-06-28

- 対象ルール: `TEST_FAQ_会員ランク算出ルール`
- 詳細URL: `https://www.sqstackstaging.com/admin/customer_rank_calculation_rules/37f5da19-1289-5ff2-99ac-1b39ed8dfeaa_CustomerRankCalculationRule`
- 編集URL: `https://www.sqstackstaging.com/admin/customer_rank_calculation_rules/37f5da19-1289-5ff2-99ac-1b39ed8dfeaa_CustomerRankCalculationRule/update`

## 結果

| 確認項目 | 結果 |
|:--|:--|
| 詳細に `算出タイミング` が表示 | `True` |
| 詳細の値が `リアルタイムに算出` | `True` |
| 編集フォームに `算出タイミング` 入力欄あり | `False` |
| 編集フォームに `リアルタイム` 入力欄あり | `False` |
| 算出方法ラジオは購入金額固定 | `True` |
| 算出方法ラジオの獲得ポイントはdisabled | `True` |

## 編集フォームのラベル

- `タイトル`
- `購入金額`
- `獲得ポイント`
- `税抜き価格でランクを算出する`
- `期間`

## 判断

- 詳細画面には `算出タイミング` / `リアルタイムに算出` が表示される。
- 編集フォームには `算出タイミング` や `リアルタイム` を変更する入力欄は表示されない。
- 現行UIでは、算出タイミングは管理者が選択する設定ではなく固定表示として案内する。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/18-crm-rank-realtime-setting-20260628.json`
- 詳細スクリーンショット: `_analysis/complete-live-verification-2026-06-28/18-crm-rank-realtime-detail-20260628.png`
- 編集スクリーンショット: `_analysis/complete-live-verification-2026-06-28/18-crm-rank-realtime-update-20260628.png`
