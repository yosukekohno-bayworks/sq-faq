# 店舗受取SKU選択 実機確認 2026-06-28

- 対象: `/admin/local_pickup_product_variants`
- 検索語: `TEST_E2E`
- 追加前件数: 20
- 追加対象としてチェックしたSKU: `TEST_E2E_20260622_GU_1830_NAVY_M`
- 未チェックで残したSKU: `TEST_E2E_20260622_GU_1845_NAVY_M`
- 追加後件数: 21
- チェックしたSKUが追加された: True
- 未チェックSKUが追加されなかった: True
- 削除後件数: 20
- 追加分のクリーンアップ完了: True
- 追加ダイアログ内にカタログ項目あり: False

## 候補行

- `TEST_E2E_20260622_GU_1830_NAVY_M`: アイテムを選択する productVariant thumbnail TEST_E2E_20260622 GU検証Tシャツ 1830 NAVY / M TEST_E2E_20260622_GU_1830 TEST_E2E_20260622_GU_1830_NAVY_M
- `TEST_E2E_20260622_GU_1845_NAVY_M`: アイテムを選択する productVariant thumbnail TEST_E2E_20260622 GU検証Tシャツ 1845 NAVY / M TEST_E2E_20260622_GU_1845 TEST_E2E_20260622_GU_1845_NAVY_M
- `TEST_E2E_20260622_GU_1905_NAVY_M`: アイテムを選択する productVariant thumbnail TEST_E2E_20260622 GU検証Tシャツ 1905 NAVY / M TEST_E2E_20260622_GU_1905 TEST_E2E_20260622_GU_1905_NAVY_M

## 結論

- 商品管理 > 店舗受取の追加ダイアログでは、チェックしたSKUだけが店舗受取対象一覧に追加され、未チェックのSKUは追加されない。
- この商品側UIはSKU直接指定であり、追加ダイアログ内にカタログ選択項目は表示されない。
- カタログで束ねた商品集合との優先関係は、この画面単体では判定できない。リテールポータル/販売チャネル接続後の挙動として残す。
