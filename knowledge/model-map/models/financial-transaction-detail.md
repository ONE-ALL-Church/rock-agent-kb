# Financial Transaction Detail Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Finance`
- Model title: `FinancialTransactionDetail`
- EntityType GUID: `ac4ac28b-8e7e-4d7e-85db-dffb4f3adcce`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 18 |
| Lava-marked properties | 33 |
| Lava-marked non-database properties | 15 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| Account |  | yes | yes |  |  | Gets or sets the FinancialAccount that is affected by this detail line item. |
| AccountId | yes | yes |  |  |  | Gets or sets the AccountId of the FinancialAccount/account that the Amount of this detail line item should be credited towards. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Amount | yes | yes |  |  |  | Gets or sets the total amount of the transaction detail. This total amount includes any associated fees. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  | Gets or sets the entity id. |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the type of the entity. |
| EntityTypeId | yes | yes |  |  |  | Gets or sets the entity. |
| FeeAmount | yes | yes |  |  |  | Gets or sets the fee amount of the transaction detail, which is a subset of the Amount. |
| FeeCoverageAmount | yes | yes |  |  |  | Gets or sets the fee coverage amount. |
| FinancialTransactionDetailAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ForeignCurrencyAmount | yes | yes |  |  |  | Gets or sets the foreign currency amount. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HistoryChangeList |  |  | yes |  |  | [Obsoleted in v14] Does nothing. No longer needed. We replaced this with a private property under the SaveHook class for this entity. Gets or sets the history change list. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  | A parent authority. If a user is not specifically allowed or denied access to this object, Rock will check the default authorization on the current type, and then the authorization on the Rock.Security.GlobalDefault entity |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Summary | yes | yes |  |  |  | Gets or sets the summary of the transaction detail. |
| SupportedActions |  |  | yes |  |  |  |
| Transaction |  | yes | yes |  |  | Gets or sets the FinancialTransaction that this detail item belongs to. |
| TransactionId | yes | yes |  |  |  | Gets or sets the TransactionId of the FinancialTransaction that this detail item is a part of. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Account | Gets or sets the FinancialAccount that is affected by this detail line item. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the type of the entity. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Transaction | Gets or sets the FinancialTransaction that this detail item belongs to. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Account | [FinancialAccount](financial-account.md) |  |
| AccountId | [FinancialAccount](financial-account.md) |  |
| Transaction | [FinancialTransaction](financial-transaction.md) |  |
| TransactionId | [FinancialTransaction](financial-transaction.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_removed | HistoryChangeList |  |
