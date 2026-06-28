# 注文残件検証向けGraphQL型・サポートデータ確認 2026-06-28

- JSON証跡: `_analysis/complete-live-verification-2026-06-28/16-remaining-order-introspection-20260628.json`
- 対象SKU: `TEST_E2E_20260622_GU_1905_NAVY_M`
- variant id: `9d94e684-4882-5ebc-bbbb-513915a8bfc7_ProductVariant`
- inventory item id: `137c461d-51a3-545e-8c58-2402bae9fef7_InventoryItem`
- active location count: `15`

## enum

- OrderPaymentStatus: `UNPAID, PENDING, AUTHORIZED, PARTIALLY_PAID, PAID, PARTIALLY_REFUNDED, REFUNDED, VOIDED`
- OrderFulfillmentStatus: `UNFULFILLED, REJECTED, CANCELLED, PARTIALLY_FULFILLED, FULFILLED`

## key input fields

### OrderFilter
- `tenantID`: `ID`
- `managementCode`: `String`
- `tag`: `String`
- `tagNot`: `String`
- `purchasingCustomerID`: `ID`
- `source`: `String`

### OrderCountFilter
- `inventoryOutboundOrderWorkingStatuses`: `[InventoryOutboundOrderWorkingStatus!]`
- `retailLocationID`: `ID`
- `isCancelled`: `Boolean`

### OrderReturnLineItemCreateInput
- `externalID`: `String`
- `orderLineItemID`: `ID!`
- `quantity`: `Int!`
- `reason`: `String`
- `exchangeLineItem`: `OrderReturnLineItemCreateExchangeLineItemInput`

## active locations

- `W0001` / `ユニクロ物流倉庫` / `WAREHOUSE` / `8b7c4983-7e88-549c-b23a-6fafc2c4d52c_Location`
- `R0001` / `ユニクロ - 銀座店` / `RETAIL` / `b12adcce-247e-5b58-b65a-4d7397be8f79_Location`
- `TESTEC01` / `ユニクロEC` / `RETAIL` / `8046cfc4-14d2-5fd3-9603-868d5e79f3ae_Location`
- `TFCLOC3698` / `GU 倉庫` / `WAREHOUSE` / `8b3bd7b3-3efe-549b-a1c5-6352492dbdc7_Location`
- `12456789098765` / `GU 銀座店` / `RETAIL` / `0f856b5d-5c17-5880-9583-a0f351ba9f7f_Location`
- `FLAGOFF01` / `TEST_FLAGOFF_20260621` / `RETAIL` / `45ffa873-a7f2-5581-8117-5758f5a45c73_Location`
- `TEST_E2E_20260622_STORE_1740` / `TEST_E2E_20260622_GU店舗_OFF_1740` / `RETAIL` / `1f0fd500-ee41-50b5-afb9-217ab8af9db3_Location`
- `TEST_E2E_20260622_WH_1740` / `TEST_E2E_20260622_GU倉庫_ON_1740` / `WAREHOUSE` / `78ae0d92-71dc-56e9-8fc5-a01216b37db1_Location`
- `TEST_E2E_20260622_WH_1755` / `TEST_E2E_20260622_GU倉庫_ON_1755` / `WAREHOUSE` / `960d77a3-59f8-586e-9087-fd1ee6a719ee_Location`
- `TEST_E2E_20260622_STORE_1830` / `TEST_E2E_20260622_GU店舗_OFF_1830` / `RETAIL` / `cbe47a67-ca31-507c-865d-6968d4e12187_Location`
- `TEST_E2E_20260622_WH_1830` / `TEST_E2E_20260622_GU倉庫_ON_1830` / `WAREHOUSE` / `eca69a97-1e36-5dfa-8496-44e1c51fd96b_Location`
- `TEST_E2E_20260622_STORE_1845` / `TEST_E2E_20260622_GU店舗_OFF_1845` / `RETAIL` / `6dd32852-58dd-5f7a-a496-ea0c8bc03623_Location`
- `TEST_E2E_20260622_WH_1845` / `TEST_E2E_20260622_GU倉庫_ON_1845` / `WAREHOUSE` / `6241e39d-9ed7-5004-9b1d-d2d3f280fa68_Location`
- `TEST_E2E_20260622_STORE_1905` / `TEST_E2E_20260622_GU店舗_OFF_1905` / `RETAIL` / `4f100847-e242-5aaf-b97a-eb47683a7c95_Location`
- `TEST_E2E_20260622_WH_1905` / `TEST_E2E_20260622_GU倉庫_ON_1905` / `WAREHOUSE` / `d018dd79-47b6-5a93-a1bf-0e12cac23d3e_Location`
