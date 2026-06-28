# orderCreate最小注文（inventoryBehavior=BYPASS） 2026-06-28

- 作成方法: 内部GraphQL `orderCreate`
- inventoryBehavior: `BYPASS`
- 注文ID: `4c7e4e96-6d5b-5c73-bf86-9693cf7c4734_Order`
- 管理コード: `FAQ-ORDER-BYPASS-20260628100919`
- 管理番号: `1`
- 顧客: `検証顧客ユニクロ095318FAQ` / `sq-faq-uniqlo-customer-20260628095318@example.invalid`
- SKU: `TEST_E2E_20260622_GU_1905_NAVY_M`
- 注文一覧に表示: `True`
- 注文詳細に表示: `True`
- 顧客詳細の注文履歴に表示: `True`
- 売上実績一覧に表示: `True`
- paymentStatus: `PAID`
- fulfillmentStatus: `FULFILLED`
- merchantCancellable/refundable/returnable/fulfillable: `False` / `False` / `True` / `None`
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/16-order-create-bypass-minimal-20260628.json`

## 注意

- この注文は在庫を動かさない `BYPASS` で作成したため、注文詳細・顧客履歴・売上表示の確認用です。
- `orderCreate` の必須条件を満たすため、fulfillmentロケーションは `ユニクロ物流倉庫`、`requiresFulfillment=false` を指定しています。
- 注文レコードは後続のキャンセル/返品/ステータス確認に使うため、このスクリプトでは削除・キャンセルしていません。
