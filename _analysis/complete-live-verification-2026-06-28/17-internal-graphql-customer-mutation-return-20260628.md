# purchasingCustomerCreate 戻り値確認 2026-06-28

- return type: `PurchasingCustomerCreatePayload`
- JSON証跡: `_analysis/complete-live-verification-2026-06-28/17-internal-graphql-customer-mutation-return-20260628.json`

## fields

- `purchasingCustomer`: `PurchasingCustomer!`
- `pubSubPublishObjects`: `[PubSubPublishObject!]!`

## PurchasingCustomer

- `id`: `ID!`
- `barcode`: `String!`
- `firstName`: `String!`
- `lastName`: `String!`
- `fullName`: `String!`
- `email`: `String!`
- `phone`: `String!`
- `note`: `String!`
- `externalID`: `String!`
- `source`: `String!`
- `emailMarketingConsentState`: `EmailMarketingConsentState!`
- `gender`: `Gender!`
- `birthDate`: `DateTime`
- `externalTags`: `[String!]!`
- `internalTags`: `[String!]!`
- `tags`: `[String!]!`
- `hasAnyTags`: `Boolean!`
- `tenant`: `Tenant!`
- `orders`: `OrderConnection!`
- `orderCount`: `Int!`
- `orderFirst`: `Order`
- `orderFirstPaid`: `Order`
- `orderLast`: `Order`
- `orderLastPaid`: `Order`
- `metafield`: `Metafield`
- `metafieldDefinitions`: `MetafieldDefinitionConnection!`
- `orderPriceAdjustmentRules`: `OrderPriceAdjustmentRuleConnection!`
- `orderPriceAdjustmentRuleCount`: `Int!`
- `orderPriceAdjustmentRuleApplicable`: `Boolean!`
- `orderRetailReturns`: `OrderRetailReturnConnection!`
- `isPointCalculationDisabled`: `Boolean!`
- `isBirthdayPointDisabled`: `Boolean!`
- `pointsApproved`: `Int!`
- `pointsApprovedByLabel`: `Int!`
- `pointsExpiring`: `Int!`
- `pointExpirations`: `[PointExpiration!]!`
- `pointExpirationsByLabel`: `[PointExpiration!]!`
- `pointsPending`: `Int!`
- `pointChangeActivities`: `PointChangeActivityConnection!`
- `estimatedOrderPoint`: `EstimatedOrderPoint!`
- `miles`: `Int!`
- `milesLifetime`: `Int!`
- `mileChangeActivities`: `MileChangeActivityConnection!`
- `shopifyMileOrders`: `ShopifyMileOrderConnection!`
- `currentCustomerRank`: `CustomerRank`
- `customerMinimumRank`: `CustomerRankRule`
- `customerRankCalculationPurchasePriceChanges`: `CustomerRankCalculationPurchasePriceChangeConnection!`
- `estimatedCustomerRank`: `CustomerRank!`
- `shippingAddresses`: `PurchasingCustomerShippingAddressConnection!`
- `sourceURL`: `URL`
- `isMerged`: `Boolean!`
- `mergedTo`: `PurchasingCustomer`
- `mergedFrom`: `[PurchasingCustomer!]!`
- `visitedRetailLocations`: `LocationConnection!`
- `customerSharing`: `CustomerSharing`
- `isDisabled`: `Boolean!`
- `smsVerified`: `Boolean!`
- `smsVerifiedPhone`: `String!`
- `smsVerifiedAt`: `DateTime`
- `createdAt`: `DateTime!`
- `updatedAt`: `DateTime!`

## PubSubPublishObject

- `objectID`: `ID!`
- `topic`: `PubSubTopic!`
- `publishesAt`: `DateTime!`
