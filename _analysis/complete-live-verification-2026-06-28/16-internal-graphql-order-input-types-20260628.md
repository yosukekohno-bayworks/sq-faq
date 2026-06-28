# 内部GraphQL 入力型確認 2026-06-28

- 対象mutation: `orderCreate, orderReturnCreate, orderRefundCreate, saleChangeCreate, purchasingCustomerCreate, inventoryOutboundOrderComplete`
- mutation確認数: `6`
- input型確認数: `43`
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/16-internal-graphql-order-input-types-20260628.json`

## mutation args

### inventoryOutboundOrderComplete
- `input`: `InventoryOutboundOrderCompleteInput!`
- `option`: `InventoryOutboundOrderCompleteOptionInput`
### orderCreate
- `input`: `OrderCreateInput!`
- `option`: `OrderCreateOptionInput!`
### orderRefundCreate
- `input`: `OrderRefundCreateInput!`
### orderReturnCreate
- `input`: `OrderReturnCreateInput!`
### purchasingCustomerCreate
- `input`: `PurchasingCustomerCreateInput!`
### saleChangeCreate
- `input`: `SaleChangeCreateInput!`
- `option`: `SaleChangeCreateOptionInput`

## input fields

### InventoryOutboundOrderCompleteInput
- `inventoryOutboundOrderID`: `ID!`
- `fulfilledAt`: `DateTime`
- `shippingCarrier`: `String!`
- `trackingCodes`: `[String!]`
- `packages`: `[InventoryOutboundOrderCompleteShippingPackageInput!]`
- `lineItems`: `[InventoryOutboundOrderCompleteLineItemInput!]`

### InventoryOutboundOrderCompleteOptionInput
- `skipsToSyncIntegration`: `Boolean!`

### OrderCreateInput
- `externalID`: `String`
- `managementCode`: `String!`
- `receiptNumber`: `String`
- `source`: `String!`
- `tenantID`: `ID!`
- `currencyCode`: `CurrencyCode!`
- `purchasingCustomer`: `OrderCreatePurchasingCustomerInput`
- `purchasingCompany`: `OrderCreatePurchasingCompanyInput`
- `tags`: `[String!]`
- `purchasedAt`: `DateTime!`
- `cancelledAt`: `DateTime`
- `deliveryDate`: `DateTime`
- `isLocked`: `Boolean`
- `isEditable`: `Boolean!`
- `isDeletable`: `Boolean`
- `note`: `String`
- `billingAddress`: `OrderCreateBillingAddressInput`
- `shippingAddress`: `OrderCreateShippingAddressInput`
- `email`: `String`
- `attributes`: `[OrderCreateAttributeInput!]`
- `metafields`: `[MetafieldInput!]`
- `lineItems`: `[OrderCreateLineItemInput!]!`
- `shippingLines`: `[OrderCreateShippingLineInput!]`
- `taxesIncluded`: `Boolean!`
- `fulfillment`: `OrderCreateFulfillmentInput`
- `inventoryOutboundOrders`: `[OrderCreateInventoryOutboundOrderInput!]`
- `retail`: `OrderCreateRetailInput`
- `retailStaffMember`: `OrderCreateRetailStaffMemberInput`
- `transactions`: `[OrderCreateTransactionInput!]`
- `additionalFees`: `[OrderCreateAdditionalFeeInput!]`
- `discounts`: `[OrderCreateDiscountInput!]`
- `useDiscountAllocationInput`: `Boolean!`
- `pointApplication`: `OrderCreatePointApplicationInput`
- `priceAdjustmentUsages`: `OrderCreatePriceAdjustmentUsagesInput`

### OrderCreateOptionInput
- `inventoryBehavior`: `InventoryBehavior!`
- `integrationsToSync`: `OrderCreateOptionIntegrationsToSyncInput`
- `bypassesPointCalculation`: `Boolean`
- `excludesFromCustomerRankCalculation`: `Boolean`
- `excludesFromSalesRecording`: `Boolean`
- `createInventoryOutboundOrderAsOnHold`: `Boolean`

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

### PurchasingCustomerCreateInput
- `tenantID`: `ID!`
- `externalID`: `String!`
- `source`: `String!`
- `barcode`: `String`
- `firstName`: `String!`
- `lastName`: `String!`
- `email`: `String!`
- `phone`: `String!`
- `gender`: `Gender`
- `tags`: `[String!]`

### SaleChangeCreateInput
- `externalID`: `String`
- `sourceResourceID`: `String`
- `tenantID`: `ID!`
- `processedAt`: `DateTime`
- `currencyCode`: `CurrencyCode!`
- `taxesIncluded`: `Boolean!`
- `lineItems`: `[SaleChangeCreateLineItemInput!]!`
- `orderLevelDiscountPrice`: `Decimal`
- `shippingPrice`: `Decimal`
- `shippingTaxPrice`: `Decimal`
- `shippingDiscountPrice`: `Decimal`
- `pointApplicationPrice`: `Decimal`
- `metafields`: `[MetafieldInput!]`

### SaleChangeCreateOptionInput
- `orderID`: `ID`

### InventoryOutboundOrderCompleteShippingPackageInput
- `managementCode`: `String!`
- `lineItems`: `[InventoryOutboundOrderCompleteShippingPackageLineItemInput!]!`

### InventoryOutboundOrderCompleteLineItemInput
- `inventoryOutboundOrderLineItemID`: `ID!`
- `quantity`: `Int!`

### OrderCreatePurchasingCustomerInput
- `customerID`: `ID!`

### OrderCreatePurchasingCompanyInput
- `companyID`: `ID!`
- `companyLocationID`: `ID!`
- `companyContactID`: `ID`

### OrderCreateBillingAddressInput
- `firstName`: `String!`
- `lastName`: `String!`
- `company`: `String!`
- `address1`: `String!`
- `address2`: `String!`
- `city`: `String!`
- `postalCode`: `String!`
- `provinceCode`: `String!`
- `countryCode`: `CountryCode!`
- `phone`: `String!`

### OrderCreateShippingAddressInput
- `firstName`: `String!`
- `lastName`: `String!`
- `company`: `String!`
- `address1`: `String!`
- `address2`: `String!`
- `city`: `String!`
- `postalCode`: `String!`
- `provinceCode`: `String!`
- `countryCode`: `CountryCode!`
- `phone`: `String!`

### OrderCreateAttributeInput
- `name`: `String!`
- `value`: `String!`

### MetafieldInput
- `namespace`: `String!`
- `key`: `String!`
- `valueType`: `MetafieldValueType!`
- `value`: `String!`

### OrderCreateLineItemInput
- `productTitle`: `String`
- `variantTitle`: `String`
- `externalID`: `String`
- `sku`: `String!`
- `quantity`: `Int!`
- `unitPrice`: `MoneyInput!`
- `isBackOrder`: `Boolean`
- `taxLines`: `[OrderCreateLineItemTaxLineInput!]`
- `discounts`: `[OrderCreateLineItemDiscountInput!]`
- `discountAllocations`: `[OrderCreateLineItemDiscountAllocationInput!]`
- `pointApplicationAllocation`: `OrderCreateLineItemPointAllocationInput`
- `excludesFromPointCalculation`: `Boolean`

### OrderCreateShippingLineInput
- `title`: `String!`
- `externalID`: `String`
- `price`: `MoneyInput!`
- `taxLines`: `[OrderCreateShippingLineTaxLineInput!]`
- `discounts`: `[OrderCreateShippingLineDiscountInput!]`

### OrderCreateFulfillmentInput
- `locationID`: `ID!`
- `requiresFulfillment`: `Boolean!`

### OrderCreateInventoryOutboundOrderInput
- `locationID`: `ID!`
- `isFulfilled`: `Boolean!`
- `lineItems`: `[OrderCreateInventoryOutboundOrderLineItemInput!]!`

### OrderCreateRetailInput
- `locationID`: `ID!`

### OrderCreateRetailStaffMemberInput
- `code`: `String!`

### OrderCreateTransactionInput
- `externalID`: `String`
- `paymentID`: `String!`
- `kind`: `OrderTransactionKind!`
- `gateway`: `String!`
- `price`: `MoneyInput!`
- `orderTransactionCreatedAt`: `DateTime!`
- `authorizationExpiresAt`: `DateTime`

### OrderCreateAdditionalFeeInput
- `name`: `String!`
- `price`: `MoneyInput!`
- `taxPrice`: `MoneyInput`

### OrderCreateDiscountInput
- `allocationKey`: `String`
- `title`: `String!`
- `code`: `String`
- `price`: `MoneyInput!`

### OrderCreatePointApplicationInput
- `point`: `Decimal!`
- `pointApplicationType`: `PointApplicationType!`
- `usePointAllocationInput`: `Boolean!`

### OrderCreatePriceAdjustmentUsagesInput
- `codes`: `[String!]!`

### OrderCreateOptionIntegrationsToSyncInput
- `shopifyIntegrationIDs`: `[ID!]`
- `sendReceipt`: `Boolean!`
- `sendFulfillmentReceipt`: `Boolean!`

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

### SaleChangeCreateLineItemInput
- `externalID`: `String`
- `sku`: `String!`
- `quantity`: `Int!`
- `salePrice`: `Decimal!`
- `taxPrice`: `Decimal`
- `discountPrice`: `Decimal`

### InventoryOutboundOrderCompleteShippingPackageLineItemInput
- `productVariantID`: `ID!`
- `quantity`: `Int!`

### MoneyInput
- `amount`: `Decimal!`
- `currencyCode`: `CurrencyCode!`

### OrderCreateLineItemTaxLineInput
- `title`: `String!`
- `price`: `MoneyInput!`
- `rate`: `Decimal!`

### OrderCreateLineItemDiscountInput
- `title`: `String!`
- `code`: `String`
- `price`: `MoneyInput!`

### OrderCreateLineItemDiscountAllocationInput
- `key`: `String!`
- `price`: `MoneyInput!`

### OrderCreateLineItemPointAllocationInput
- `point`: `Decimal!`

### OrderCreateShippingLineTaxLineInput
- `title`: `String!`
- `price`: `MoneyInput!`
- `rate`: `Decimal!`

### OrderCreateShippingLineDiscountInput
- `title`: `String!`
- `code`: `String`
- `price`: `MoneyInput!`

### OrderCreateInventoryOutboundOrderLineItemInput
- `sku`: `String!`
- `quantity`: `Int!`

### OrderRefundLineItemPriceInput
- `price`: `MoneyInput!`
- `taxPrice`: `MoneyInput!`

### OrderReturnLineItemCreateExchangeLineItemInput
- `productVariantID`: `ID!`
