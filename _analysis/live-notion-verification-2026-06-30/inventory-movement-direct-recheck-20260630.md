# 2026-06-30 Inventory Movement Direct Recheck

## Scope

- Area: `12-在庫状態・在庫数`
- Purpose: Re-run the inventory movement sequence in the current SQ staging UI without using an inventory allocation request.
- SKU: `TEST_E2E_20260622_GU_1905_NAVY_M`
- Source: `TEST_E2E_20260622_GU倉庫_ON_1905`
- Destination: `TEST_E2E_20260622_GU店舗_OFF_1905`
- Quantity: `1`

## Records Created

- Movement order: `#IM-1033`
- Outbound order: `#IO-1041`
- Inbound order: `#II-1035`

## Observed Inventory Changes

| Step | Source | Destination | Notes |
|:--|:--|:--|:--|
| Before | available 1 / allocated 0 / reserved 0 / on hand 1 | available 11 / allocated 0 / reserved 0 / on hand 11 | Inventory list checked per location |
| Movement created | available 0 / allocated 0 / reserved 1 / on hand 1 | `情報 入荷予定`; major columns remain 11/0/0/11 | `#IO-1041` and `#II-1035` auto-created |
| Shipment registered | available 0 / allocated 0 / reserved 0 / on hand 0 | `情報 積送中`; major columns remain 11/0/0/11 | `#IO-1041` became `成功 完了 / 出荷完了`; shipped 0 -> 1 |
| Receipt registered | available 0 / allocated 0 / reserved 0 / on hand 0 | available 12 / allocated 0 / reserved 0 / on hand 12 | `#II-1035` and parent `#IM-1033` became `成功 完了 / 入荷完了` |

## UI Details

- The product reference button became enabled after both source and destination were selected.
- The product selection dialog showed the target SKU inventory as `1個`.
- The movement line quantity defaulted to `0`; it had to be changed to `1` before saving.
- The outbound registration modal accepted blank carrier and tracking code.
- After outbound completion, the page showed `成功 完了 / 出荷完了` and shipped count `1`, but a secondary `情報 未完了 / 引当待ち` display remained.
- The inbound receive screen showed `今回受領` default `0`; it had to be changed to `1`.

## Conclusion

Direct movement order creation produced the same inventory transitions as the 2026-06-27 allocation-request-based flow:

1. Movement creation moves stock at the source from available to reserved and places an incoming marker at the destination.
2. Shipment reduces source reserved and on-hand stock, and changes the destination marker from incoming to in-transit.
3. Receipt increases destination available and on-hand stock.
