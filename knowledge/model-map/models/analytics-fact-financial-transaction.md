# Analytics Fact Financial Transaction Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Reporting`
- Model title: `AnalyticsFactFinancialTransaction`
- EntityType GUID: `6447497f-c40f-41b9-ab5b-a1f14f80dd18`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 63 |
| Database-marked properties | 48 |
| Lava-marked properties | 56 |
| Lava-marked non-database properties | 8 |
| Related model links | 0 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| Account |  | yes | yes |  |  |  |
| AccountId | yes | yes |  |  |  |  |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Amount | yes | yes |  |  |  |  |
| AuthorizedCurrentFamilyKey | yes | yes |  |  |  | This is the FamilyKey (AnalyticsDimFamilyCurrent.Id) of the family of the Authorized Person that did this transaction Note that this is the family that the person is in now To see what GivingGroup they were part of when the Transaction occurred, see GivingUnitKey |
| AuthorizedCurrentPersonKey | yes | yes |  |  |  |  |
| AuthorizedFamilyId | yes | yes |  |  |  |  |
| AuthorizedFamilyKey | yes | yes |  |  |  | This is the FamilyKey (AnalyticsDimFamilyCurrent.Id) of the family of the Authorized Person that did this transaction Note that this is the family that the person was in at the time of the transaction To see what GivingGroup they were part of when the Transaction occurred, see GivingUnitKey |
| AuthorizedPersonAliasId | yes | yes |  |  |  |  |
| AuthorizedPersonKey | yes | yes |  |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Batch |  | yes | yes |  |  |  |
| BatchId | yes | yes |  |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| Count | yes | yes |  |  |  |  |
| CreditCardType | yes | yes |  |  |  | Gets or sets the type of the credit card. |
| CreditCardTypeValueId | yes | yes |  |  |  | These are found in the "Credit Card Type" Defined Type. |
| CurrencyType | yes | yes |  |  |  | Gets or sets the type of the currency. |
| CurrencyTypeValueId | yes | yes |  |  |  | These are found in the "Currency Type" Defined Type. |
| DaysSinceLastTransactionOfType | yes | yes |  |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityTypeId | yes | yes |  |  |  |  |
| EntityTypeName | yes | yes |  |  |  | Gets or sets the entity type identifier. |
| FinancialGateway | yes | yes |  |  |  | Gets or sets the gateway identifier. |
| FinancialGatewayId | yes | yes |  |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GivingGroupId | yes | yes |  |  |  |  |
| GivingId | yes | yes |  |  |  |  |
| GivingUnitCurrentKey | yes | yes |  |  |  | Gets or sets the current giving unit key, which is the GivingGroup the person is in now |
| GivingUnitKey | yes | yes |  |  |  | Gets or sets the giving unit key, which is the GivingGroup the person was in at the time of the transaction |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsFirstTransactionOfType | yes | yes |  |  |  |  |
| IsScheduled | yes | yes |  |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ProcessedByPersonAliasId | yes | yes |  |  |  |  |
| ProcessedByPersonKey | yes | yes |  |  |  | Gets or sets the processed by person key. |
| ProcessedDateTime | yes | yes |  |  |  |  |
| ScheduleType | yes | yes |  |  |  | Gets or sets the type of the schedule. (Scheduled or Non-Scheduled) |
| SourceTypeValueId | yes | yes |  |  |  | These are found in the "Transaction Source" Defined Type. |
| Summary | yes | yes |  |  |  |  |
| TransactionCode | yes | yes |  |  |  |  |
| TransactionDate |  | yes | yes |  |  |  |
| TransactionDateKey | yes | yes |  |  |  |  |
| TransactionDateTime | yes | yes |  |  |  |  |
| TransactionDetailId | yes | yes |  |  |  |  |
| TransactionFrequency | yes | yes |  |  |  |  |
| TransactionId | yes | yes |  |  |  |  |
| TransactionKey | yes | yes |  |  |  |  |
| TransactionSource | yes | yes |  |  |  | Gets or sets the transaction source. |
| TransactionType | yes | yes |  |  |  | Gets or sets the type of the transaction. |
| TransactionTypeValueId | yes | yes |  |  |  | These are found in the "Transaction Type" Defined Type. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Account |  |
| Batch |  |
| EntityStringValue |  |
| IdKey |  |
| TransactionDate |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
