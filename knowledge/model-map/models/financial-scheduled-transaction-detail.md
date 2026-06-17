# Financial Scheduled Transaction Detail Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Finance`
- Model title: `FinancialScheduledTransactionDetail`
- EntityType GUID: `a206615f-3fb5-48df-b606-86ae8716fd57`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 47 |
| Database-marked properties | 16 |
| Lava-marked properties | 31 |
| Lava-marked non-database properties | 15 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| Account |  | yes | yes |  |  | Gets or sets the Financial Account/account that the Amount of this transaction detail will be credited toward. |
| AccountId | yes | yes |  |  |  | Gets or sets the AccountId of the Financial Account/account that that the transaction detail Amount should be directed toward. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Amount | yes | yes |  |  |  | Gets or sets the purchase/gift amount. |
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
| FeeCoverageAmount | yes | yes |  |  |  | Gets or sets the fee coverage amount. |
| FinancialScheduledTransactionDetailAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HistoryChangeList |  |  | yes |  | yes | Gets or sets the history change list. |
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
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ScheduledTransaction |  | yes | yes |  |  | Gets or sets the Financial Scheduled Transaction that this transaction detail belongs to. |
| ScheduledTransactionId | yes | yes |  |  |  | Gets or sets the ScheduledTransactionId of the Financial Scheduled Transaction that this detail item belongs to. |
| Summary | yes | yes |  |  |  | Gets or sets the summary of this scheduled transaction detail. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Account | Gets or sets the Financial Account/account that the Amount of this transaction detail will be credited toward. |
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
| ScheduledTransaction | Gets or sets the Financial Scheduled Transaction that this transaction detail belongs to. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Account | [Financial Account](financial-account.md) | 798bce48-6aa7-4983-9214-f9bcefb4521d |
| AccountId | [Financial Account](financial-account.md) | 798bce48-6aa7-4983-9214-f9bcefb4521d |
| ScheduledTransaction | [Financial Scheduled Transaction](financial-scheduled-transaction.md) | 76824e8a-ccc4-4085-84d9-8af8c0807e20 |
| ScheduledTransactionId | [Financial Scheduled Transaction](financial-scheduled-transaction.md) | 76824e8a-ccc4-4085-84d9-8af8c0807e20 |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_removed | HistoryChangeList |  |
