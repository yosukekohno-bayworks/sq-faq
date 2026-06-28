# 06 カタログ: 自動追加ルールの既存商品・遅延反映再確認 2026-06-28

## 対象

- 検証ID: `20260628_075426`
- カタログ: `TEST_FAQ_RETRO_CATALOG_20260628_075426`
- ルール: `製造元 / 一致する / TEST_VENDOR_RETRO_20260628_075426`
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/06-catalog-auto-rule-existing-delayed-recheck-20260628.json`

## 検証商品

- `rule_before_existing_matching`: `TEST_FAQ_RETRO_EXISTING_MATCH_UPDATED_20260628_075426` / 製造元 `TEST_VENDOR_RETRO_20260628_075426`
- `rule_before_existing_changed_to_match`: `TEST_FAQ_RETRO_EXISTING_NONMATCH_20260628_075426` / 製造元 `TEST_VENDOR_OTHER_20260628_075426`
- `rule_after_new_matching`: `TEST_FAQ_RETRO_NEW_MATCH_20260628_075426` / 製造元 `TEST_VENDOR_RETRO_20260628_075426`

## チェック結果

- `after_rule_immediate`（待機 0秒）: TEST_FAQ_RETRO_EXISTING_MATCH_20260628_075426=なし, TEST_FAQ_RETRO_EXISTING_NONMATCH_20260628_075426=なし
- `after_rule_reload_10s`（待機 10秒）: TEST_FAQ_RETRO_EXISTING_MATCH_20260628_075426=なし, TEST_FAQ_RETRO_EXISTING_NONMATCH_20260628_075426=なし
- `after_rule_reload_60s`（待機 60秒）: TEST_FAQ_RETRO_EXISTING_MATCH_20260628_075426=なし, TEST_FAQ_RETRO_EXISTING_NONMATCH_20260628_075426=なし
- `after_matching_existing_name_update`（待機 5秒）: TEST_FAQ_RETRO_EXISTING_MATCH_UPDATED_20260628_075426=あり, TEST_FAQ_RETRO_EXISTING_NONMATCH_20260628_075426=なし
- `after_nonmatching_existing_vendor_update_5s`（待機 5秒）: TEST_FAQ_RETRO_EXISTING_MATCH_UPDATED_20260628_075426=あり, TEST_FAQ_RETRO_EXISTING_NONMATCH_20260628_075426=あり
- `after_nonmatching_existing_vendor_update_30s`（待機 30秒）: TEST_FAQ_RETRO_EXISTING_MATCH_UPDATED_20260628_075426=あり, TEST_FAQ_RETRO_EXISTING_NONMATCH_20260628_075426=あり
- `after_new_matching_product_create_5s`（待機 5秒）: TEST_FAQ_RETRO_EXISTING_MATCH_UPDATED_20260628_075426=あり, TEST_FAQ_RETRO_EXISTING_NONMATCH_20260628_075426=あり, TEST_FAQ_RETRO_NEW_MATCH_20260628_075426=あり
- `after_new_matching_product_create_30s`（待機 30秒）: TEST_FAQ_RETRO_EXISTING_MATCH_UPDATED_20260628_075426=あり, TEST_FAQ_RETRO_EXISTING_NONMATCH_20260628_075426=あり, TEST_FAQ_RETRO_NEW_MATCH_20260628_075426=あり

## 操作結果

- matching_existing_product_name_update_after_rule: 成功
- nonmatching_existing_product_vendor_changed_to_match_after_rule: 保存後の本文待機は `TimeoutError`。ただし、その後のカタログ商品タブで当該商品が表示されたため、ルール再評価・追加は確認済み。

## 後片付け

- 商品削除: 全件確認済み
- カタログ削除: 確認済み

## 判定

- ルール作成前から製造元が一致していた既存商品は、作成直後・10秒後・60秒後の再読み込みではカタログに追加されなかった。
- 既存の一致商品は、商品名更新後にカタログへ追加された。
- ルール作成前から存在した不一致商品を、作成後に製造元一致へ変更して保存するとカタログへ追加された。
- ルール作成後に新規作成した一致商品はカタログへ追加された。
