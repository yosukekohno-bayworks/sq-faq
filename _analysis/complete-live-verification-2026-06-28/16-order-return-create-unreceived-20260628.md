# 注文返品を内部GraphQLで作成（未受領） 2026-06-28

- 元注文: `FAQ-ORDER-BYPASS-20260628100919` / `4c7e4e96-6d5b-5c73-bf86-9693cf7c4734_Order`
- 返品ID: `f2c59ab8-81e6-57a4-8f32-a5859b1778fb_OrderReturn`
- 返品管理コード: `FAQ-ORDER-BYPASS-20260628100919-R1`
- 作成時status: `WAITING`
- receivable/completable/cancellable: `True` / `False` / `True`
- 数量: total `1` / received `0`
- 返品一覧に表示: `True`
- 返品詳細に表示: `False`
- 注文側 hasActiveOrderReturns: `True`
- 注文側 totalReturnableQuantity: `0`
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/16-order-return-create-unreceived-20260628.json`

## 注意

- `received=false` で作成したため、受領・返金・在庫戻しの完了挙動はこのスクリプトでは実行していません。
