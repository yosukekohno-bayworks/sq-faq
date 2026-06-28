# 注文残件追加検証（通常注文・未完了件数・交換返品） 2026-06-28

- 実行日時: `2026-06-28T05:01:17.316755+00:00`
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/16-order-remaining-normal-exchange-20260628.json`
- 対象SKU: `TEST_E2E_20260622_GU_1905_NAVY_M`
- 対象ロケーション: `TEST_E2E_20260622_GU倉庫_ON_1905`

## DECREMENT注文

- 管理コード: `FAQ-REMAINING-DECREMENT-20260628135953`
- paymentStatus / fulfillmentStatus / requiresFulfillment: `PAID` / `UNFULFILLED` / `True`
- inventoryBehavior: `DECREMENT`
- 出荷指示数: `1`
  - `#IO-1034` / `WAITING` / allocated=`False` / allocationStatus=`WAITING`

### 在庫差分（注文前 → DECREMENT注文後）

| 区分 | before | after | diff |
|:--|--:|--:|--:|
| `available` | 1 | 0 | -1 |
| `committed` | 0 | 1 | 1 |
| `damaged` | 0 | 0 | 0 |
| `inTransit` | 0 | 0 | 0 |
| `incoming` | 0 | 0 | 0 |
| `onHand` | 1 | 1 | 0 |
| `qualityControl` | 0 | 0 | 0 |
| `reserved` | 0 | 0 | 0 |
| `safetyStock` | 0 | 0 | 0 |
| `sellableQuantity` | 1 | 0 | -1 |
| `locationAvailability.inventoryQuantity` | 1 | 0 | -1 |

## 未完了件数/決済状態

| タイミング | WAITING | NON_TERMINAL |
|:--|--:|--:|
| 作成前 | 0 | 0 |
| DECREMENT注文後 | 1 | 1 |
| 未払い・出荷不要注文後 | 1 | 1 |
| 交換返品後 | 1 | 1 |

- 未払い・出荷不要注文: `FAQ-REMAINING-UNPAID-NOFULFILL-20260628140117` / paymentStatus=`PAID` / fulfillmentStatus=`FULFILLED` / requiresFulfillment=`False`
- `OrderCountFilter` は `inventoryOutboundOrderWorkingStatuses` / `retailLocationID` / `isCancelled` のみを受け付け、paymentStatus条件を持たない。

## 交換返品

- 元注文: `FAQ-REMAINING-EXCHANGE-20260628140117` / paymentStatus=`PAID` / fulfillmentStatus=`FULFILLED`
- 返品管理コード: `FAQ-REMAINING-EXCHANGE-20260628140117-R1`
- status: `WAITING`
- hasExchangeLineItems / exchangeLineItemCount: `True` / `1`
- exchange outbound: `None` / `None` / qty=`None`

## 判断

- `DECREMENT` 注文は在庫を動かし、出荷指示を持つ注文として作成できる。
- `OrderCountFilter` の形と実測差分から、未完了件数は決済状態ではなく未完了の出荷指示ステータスに紐づく。
- 取引なし・出荷不要の内部 `orderCreate` は paymentStatus=`PAID` になった。非PAID状態はこの経路では再現できていない。
- 交換返品は `exchangeLineItem` と `exchangeInventoryLocationID` を指定して作成でき、返品データに交換明細が紐づく。ただし作成直後の `exchangeInventoryOutboundOrder` は `null`。
