# 注文管理 未完了件数と決済状態 追加検証 2026-06-28

- JSON証跡: `_analysis/complete-live-verification-2026-06-28/16-order-payment-status-count-20260628.json`
- 作成注文: `FAQ-REMAINING-AUTHONLY-20260628140300`
- transaction kind: `AUTHORIZATION`
- paymentStatus / fulfillmentStatus / requiresFulfillment: `PAID` / `FULFILLED` / `False`
- 出荷指示: `[{'id': 'cc490d87-c8f8-585a-ad50-30334908a9e4_InventoryOutboundOrder', 'managementCode': '#IO-1039', 'kind': 'ORDER', 'workingStatus': 'COMPLETE', 'totalQuantity': 1}]`

## 件数差分

| 区分 | before | after | diff |
|:--|--:|--:|--:|
| `WAITING` | 1 | 1 | 0 |
| `ON_HOLD` | 0 | 0 | 0 |
| `REQUESTED` | 0 | 0 | 0 |
| `IN_PROGRESS` | 0 | 0 | 0 |
| `REJECTED` | 0 | 0 | 0 |
| `NON_TERMINAL` | 1 | 1 | 0 |
| `COMPLETE` | 3 | 4 | 1 |
| `CANCELLED` | 0 | 0 | 0 |

## 判断

- `AUTHORIZATION` 取引だけで投入しても、この内部 `orderCreate` では `paymentStatus=PAID` になった。非PAID状態はこの経路では再現できていない。
- `requiresFulfillment=false` のため、紐づく出荷指示は `COMPLETE` で作成された。
- 非完了ステータス（WAITING/ON_HOLD/REQUESTED/IN_PROGRESS/REJECTED）の件数は増えない。加えて `OrderCountFilter` に paymentStatus 条件はないため、未完了件数は決済状態ではなく出荷指示の未完了ステータスで数えると判断する。
