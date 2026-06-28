# 販売閾値ルール 保存・削除確認 2026-06-28

## 検証データ

- ルール名: `TEST_FAQ_THRESHOLD_20260628063313`
- SKU: `TEST_E2E_20260622_GU_1905_NAVY_M`

## 結果

| 項目 | 結果 |
|:--|:--|
| 作成フォームのラベル | `['ルール名', 'デフォルトの閾値を設定する']` |
| デフォルト閾値ON時の初期値 | `0` |
| 作成後に一覧へ戻る | `True` |
| 詳細画面の主要導線 | `['自動追加ルール', '閾値を追加する']` |
| SKU別閾値フォーム初期値 | `0` |
| SKU選択行 | `アイテムを選択する productVariant thumbnail TEST_E2E_20260622 GU検証Tシャツ 1905 NAVY / M TEST_E2E_20260622_GU_1905 TEST_E2E_20260622_GU_1905_NAVY_M` |
| SKU別閾値保存後の行 | `[{'id': 'f1b69a46-f901-5835-852b-ac2ea3d3398e_InventoryThresholdRuleProductVariant', 'text': 'アイテムを選択する product variant thumbnail NAVY / M TEST_E2E_20260622 GU検証Tシャツ 1905 TEST_E2E_20260622_GU_1905_NAVY_M TEST_E2E_20260622_GU_1905 3'}]` |
| SKU別閾値削除 | `True` |
| ルール本体削除 | `True` |
| UI上の到達時説明 | `False` |

## 判断

- 販売閾値ルールは現行stagingでも作成でき、保存後は詳細ではなく一覧へ戻る。
- ルール詳細から `閾値を追加する` へ進み、SKU別の閾値を保存できる。
- SKU別閾値は行選択後の削除確認ダイアログで削除でき、ルール本体も一覧行選択後に削除できる。
- 管理画面UIには、閾値に達したときの売り止め/通知/連携先反映を説明する文言は確認できない。実効はリテールポータル等の接続環境で別検証が必要。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/11-inventory-threshold-rule-save-cleanup-20260628.json`
