# Analytics Source Financial Transaction Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Reporting`
- Model title: `AnalyticsSourceFinancialTransaction`
- EntityType GUID: `68e1bb08-b30b-49e2-993e-0b5352bb97c5`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 51 |
| Database-marked properties | 36 |
| Lava-marked properties | 44 |
| Lava-marked non-database properties | 8 |
| Related model links | 0 |
| Pre-alpha changes touching this model | 2 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| Account |  | yes | yes |  |  |  |
| AccountId | yes | yes |  |  |  |  |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Amount | yes | yes |  |  |  |  |
| AuthorizedCurrentPersonKey | yes | yes |  |  |  |  |
| AuthorizedFamilyId | yes | yes |  |  |  |  |
| AuthorizedPersonAliasId | yes | yes |  |  |  |  |
| AuthorizedPersonKey | yes | yes |  |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Batch |  | yes | yes |  |  |  |
| BatchId | yes | yes |  |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| Count | yes | yes |  |  |  |  |
| CreditCardTypeValueId | yes | yes |  |  |  | These are found in the Credit Card Type Defined Type. |
| CurrencyTypeValueId | yes | yes |  |  |  | These are found in the Currency Type Defined Type. |
| DaysSinceLastTransactionOfType | yes | yes |  |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityTypeId | yes | yes |  |  |  |  |
| FinancialGatewayId | yes | yes |  |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GivingGroupId | yes | yes |  |  |  |  |
| GivingId | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsFirstTransactionOfType | yes | yes |  |  |  |  |
| IsScheduled | yes | yes |  |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ProcessedByPersonAliasId | yes | yes |  |  |  |  |
| ProcessedDateTime | yes | yes |  |  |  |  |
| SourceTypeValueId | yes | yes |  |  |  | These are found in the Transaction Source Defined Type. |
| Summary | yes | yes |  |  |  |  |
| TransactionCode | yes | yes |  |  |  |  |
| TransactionDate |  | yes | yes |  |  |  |
| TransactionDateKey | yes | yes |  |  |  |  |
| TransactionDateTime | yes | yes |  |  |  |  |
| TransactionDetailId | yes | yes |  |  |  |  |
| TransactionFrequency | yes | yes |  |  |  |  |
| TransactionId | yes | yes |  |  |  |  |
| TransactionKey | yes | yes |  |  |  |  |
| TransactionTypeValueId | yes | yes |  |  |  | These are found in the Transaction Type Defined Type. |
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

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | CurrencyTypeValueId | enum_values |
| property_changed | SourceTypeValueId | enum_values |
