# 交換返品の受領・完了処理 2026-06-28

- JSON証跡: `_analysis/complete-live-verification-2026-06-28/16-order-exchange-return-receive-process-20260628.json`
- 返品 externalID: `FAQ_EXCHANGE_RETURN_20260628140117`

## 状態推移

| タイミング | status | receivable | completable | received | exchange outbound |
|:--|:--|:--|:--|--:|:--|
| 作成直後 | `WAITING` | `True` | `False` | 0 | `None` / `None` |
| 受領後 | `RECEIVED` | `False` | `True` | 1 | `None` / `None` |
| 完了試行後 | `REFUNDED` | `False` | `False` | 1 | `#IO-1040` / `WAITING` |

## 交換明細

- hasExchangeLineItems: `True`
- exchangeLineItemCount: `1`

## 完了処理

- process skipped: `None`
- process errors: `None`

## 判断

- 交換明細付き返品は作成でき、受領すると `RECEIVED` になる。
- 作成直後・受領後は `exchangeInventoryOutboundOrder` が `null` のまま。
- `orderReturnProcess` 完了後、`ORDER_EXCHANGE` の交換出荷指示 `#IO-1040` が `WAITING` で生成された。
