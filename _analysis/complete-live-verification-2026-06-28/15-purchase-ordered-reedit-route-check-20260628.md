# 発注済み伝票の差し戻し・再編集導線 実機確認

- 実行日時: 2026-06-27T21:57:32.839605+00:00
- 確認範囲: 発注済み未入荷 `#IP-1013`、入荷完了済み `#IP-1007`、比較用下書き `#IP-1010`
- 確認内容: 詳細画面、`その他の操作`、直接 `/update` / `/edit` URL

## 結果

### #IP-1013 (ordered_without_inbound_created)

- 発注済み表示: `True` / 下書き表示: `False`
- 詳細画面に `保存`: `False`
- 詳細画面に `発注する`: `False`
- 詳細画面に `入荷指示を作成する`: `True`
- 詳細画面に編集/再編集/差し戻し/下書き戻し系文言: `False`
- その他の操作に `キャンセルする`: `True`
- その他の操作に編集/再編集/差し戻し/下書き戻し系文言: `False`
- 直接 `/update`: `https://www.sqstackstaging.com/admin/inventory_purchase_orders/697d403b-4112-562b-9982-f07bb643872f_InventoryPurchaseOrder/update` / h1 `['このページは存在しないようです']` / 編集系文言 `False`
- 直接 `/edit`: `https://www.sqstackstaging.com/admin/inventory_purchase_orders/697d403b-4112-562b-9982-f07bb643872f_InventoryPurchaseOrder/edit` / h1 `['このページは存在しないようです']` / 編集系文言 `False`

### #IP-1007 (ordered_after_inbound_completed)

- 発注済み表示: `True` / 下書き表示: `False`
- 詳細画面に `保存`: `False`
- 詳細画面に `発注する`: `False`
- 詳細画面に `入荷指示を作成する`: `True`
- 詳細画面に編集/再編集/差し戻し/下書き戻し系文言: `False`
- その他の操作に `キャンセルする`: `True`
- その他の操作に編集/再編集/差し戻し/下書き戻し系文言: `False`
- 直接 `/update`: `https://www.sqstackstaging.com/admin/inventory_purchase_orders/536f9387-9a2b-59da-aab8-131ca9b82a3b_InventoryPurchaseOrder/update` / h1 `['このページは存在しないようです']` / 編集系文言 `False`
- 直接 `/edit`: `https://www.sqstackstaging.com/admin/inventory_purchase_orders/536f9387-9a2b-59da-aab8-131ca9b82a3b_InventoryPurchaseOrder/edit` / h1 `['このページは存在しないようです']` / 編集系文言 `False`

### #IP-1010 (draft_comparison)

- 発注済み表示: `False` / 下書き表示: `True`
- 詳細画面に `保存`: `False`
- 詳細画面に `発注する`: `True`
- 詳細画面に `入荷指示を作成する`: `False`
- 詳細画面に編集/再編集/差し戻し/下書き戻し系文言: `False`
- その他の操作に `キャンセルする`: `True`
- その他の操作に編集/再編集/差し戻し/下書き戻し系文言: `False`
- 直接 `/update`: `https://www.sqstackstaging.com/admin/inventory_purchase_orders/c5ebeb3b-241c-55b6-92b6-f665b47e37d8_InventoryPurchaseOrder/update` / h1 `['このページは存在しないようです']` / 編集系文言 `False`
- 直接 `/edit`: `https://www.sqstackstaging.com/admin/inventory_purchase_orders/c5ebeb3b-241c-55b6-92b6-f665b47e37d8_InventoryPurchaseOrder/edit` / h1 `['このページは存在しないようです']` / 編集系文言 `False`

## 結論

- 発注済み伝票では、詳細画面・その他の操作・直接URLの確認範囲で、下書きへ差し戻して再編集する導線は確認できませんでした。
- 発注済み未入荷の `#IP-1013` は `入荷指示を作成する` と `キャンセルする` が主な導線です。
- 入荷完了済みの `#IP-1007` は `キャンセルする` がdisabledで、再編集・差し戻し導線も確認できませんでした。

## 証跡

- JSON: `_analysis/complete-live-verification-2026-06-28/15-purchase-ordered-reedit-route-check-20260628.json`
