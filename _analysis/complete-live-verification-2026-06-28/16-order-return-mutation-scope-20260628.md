# 注文返品/返金mutation一覧 2026-06-28

- JSON証跡: `_analysis/complete-live-verification-2026-06-28/16-order-return-mutation-scope-20260628.json`

## orderRefundCreate
- `input`: `OrderRefundCreateInput!`
## orderReturnCreate
- `input`: `OrderReturnCreateInput!`
## orderReturnAddLineItems
- `input`: `OrderReturnAddLineItemsInput!`
## orderReturnRemoveLineItems
- `input`: `OrderReturnRemoveLineItemsInput!`
## orderReturnLineItemsRemovedQuantityUpdate
- `input`: `OrderReturnLineItemsRemovedQuantityUpdateInput!`
## orderReturnProcess
- `input`: `OrderReturnProcessInput!`
## orderReturnCancel
- `input`: `OrderReturnCancelInput!`
## orderReturnReceive
- `input`: `OrderReturnReceiveInput!`
## orderReturnCreateExchangeInventoryOutboundOrder
- `input`: `OrderReturnCreateExchangeInventoryOutboundOrderInput!`

## input types
### OrderRefundCreateInput
- `orderID`: `ID!`
- `externalID`: `String`
- `orderRefundLineItems`: `[OrderRefundLineItemInput!]!`
- `notifyCustomer`: `Boolean!`
### OrderReturnCreateInput
- `orderID`: `ID!`
- `orderReturnLineItems`: `[OrderReturnLineItemCreateInput!]`
- `exchangeInventoryLocationID`: `ID`
- `externalID`: `String`
- `received`: `Boolean!`
### OrderReturnAddLineItemsInput
- `orderReturnID`: `ID!`
- `orderReturnLineItems`: `[OrderReturnAddLineItemInput!]!`
### OrderReturnRemoveLineItemsInput
- `orderReturnID`: `ID!`
- `orderReturnLineItemIDs`: `[ID!]!`
### OrderReturnLineItemsRemovedQuantityUpdateInput
- `orderReturnID`: `ID!`
- `orderReturnLineItems`: `[OrderReturnLineItemRemovedQuantityUpdateInput!]`
### OrderReturnProcessInput
- `orderReturnID`: `ID!`
- `refundLineItems`: `[OrderReturnProcessRefundLineItemInput!]`
- `notifyCustomer`: `Boolean!`
- `refundsShipping`: `Boolean!`
- `restockInventoryLocationID`: `ID`
### OrderReturnCancelInput
- `orderReturnID`: `ID!`
### OrderReturnReceiveInput
- `orderReturnID`: `ID!`
- `orderReturnLineItems`: `[OrderReturnLineItemReceiveInput!]`
### OrderReturnCreateExchangeInventoryOutboundOrderInput
- `orderReturnID`: `ID!`
### OrderRefundLineItemInput
- `orderLineItemID`: `ID!`
- `quantity`: `Int!`
- `price`: `OrderRefundLineItemPriceInput`
- `restock`: `Boolean!`
### OrderReturnLineItemCreateInput
- `externalID`: `String`
- `orderLineItemID`: `ID!`
- `quantity`: `Int!`
- `reason`: `String`
- `exchangeLineItem`: `OrderReturnLineItemCreateExchangeLineItemInput`
### OrderReturnAddLineItemInput
- `orderLineItemID`: `ID!`
- `quantity`: `Int!`
- `reason`: `String`
### OrderReturnLineItemRemovedQuantityUpdateInput
- `orderReturnLineItemID`: `ID!`
- `removedQuantity`: `Int!`
### OrderReturnProcessRefundLineItemInput
- `orderLineItemID`: `ID!`
- `refundedPrice`: `MoneyInput!`
- `refundedTaxPrice`: `MoneyInput!`
### OrderReturnLineItemReceiveInput
- `orderReturnLineItemID`: `ID!`
- `receivedQuantity`: `Int!`
### OrderRefundLineItemPriceInput
- `price`: `MoneyInput!`
- `taxPrice`: `MoneyInput!`
### OrderReturnLineItemCreateExchangeLineItemInput
- `productVariantID`: `ID!`
### MoneyInput
- `amount`: `Decimal!`
- `currencyCode`: `CurrencyCode!`
