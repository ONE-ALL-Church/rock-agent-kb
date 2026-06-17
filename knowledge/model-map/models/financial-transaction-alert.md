# Financial Transaction Alert Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Finance`
- Model title: `FinancialTransactionAlert`
- EntityType GUID: `0e60f95e-70b5-4a06-9bee-80ed9f12f25a`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 54 |
| Database-marked properties | 24 |
| Lava-marked properties | 39 |
| Lava-marked non-database properties | 15 |
| Related model links | 2 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AlertDateKey | yes | yes |  |  |  | Gets or sets the alert date key. |
| AlertDateTime | yes | yes |  |  |  | Gets or sets the alert date time. |
| AlertTypeId | yes | yes |  |  |  | Gets or sets the financial transaction alert type identifier. |
| Amount | yes | yes |  |  |  | Gets or sets the amount of financial transaction |
| AmountCurrentIqr | yes | yes |  |  |  | Gets or sets the amount current interquartile range. |
| AmountCurrentMedian | yes | yes |  |  |  | Gets or sets the amount current median |
| AmountIqrMultiplier | yes | yes |  |  |  | Gets or sets the amount interquartile range multiplier. |
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
| EntityStringValue |  | yes | yes |  |  |  |
| FinancialTransaction |  | yes | yes |  |  | Gets or sets the transaction that this financial transaction alert is associated with. |
| FinancialTransactionAlertAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| FinancialTransactionAlertType |  | yes | yes |  |  | Gets or sets the type of the financial transaction alert. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FrequencyCurrentMean | yes | yes |  |  |  | Gets or sets the frequency current mean. |
| FrequencyCurrentStandardDeviation | yes | yes |  |  |  | Gets or sets the frequency current standard deviation. |
| FrequencyDifferenceFromMean | yes | yes |  |  |  | Gets or sets the frequency difference from mean. |
| FrequencyZScore | yes | yes |  |  |  | Gets or sets the frequency Z score. |
| GivingId | yes | yes |  |  |  | Gets or sets the giving identifier. |
| Guid | yes | yes |  |  |  |  |
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
| PersonAlias |  | yes | yes |  |  | Gets or sets the person alias Person associated with the financial transaction alert. |
| PersonAliasId | yes | yes |  | yes |  | Gets or sets the Id of the person Person who is associated with the transaction. |
| ReasonsKey | yes | yes |  |  |  | Gets or sets the reason key. |
| SupportedActions |  |  | yes |  |  |  |
| TransactionId | yes | yes |  |  |  | Gets or sets the transaction identifier. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| FinancialTransaction | Gets or sets the transaction that this financial transaction alert is associated with. |
| FinancialTransactionAlertType | Gets or sets the type of the financial transaction alert. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the person alias Person associated with the financial transaction alert. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| PersonAlias | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| PersonAliasId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
