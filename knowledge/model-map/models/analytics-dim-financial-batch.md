# Analytics Dim Financial Batch Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Reporting`
- Model title: `AnalyticsDimFinancialBatch`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `f970ff85-f3ed-41bd-90d9-5511baced928`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 26 |
| Database-marked properties | 14 |
| Lava-marked properties | 18 |
| Lava-marked non-database properties | 5 |
| Related model links | 3 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AccountingSystemCode | yes | yes |  |  |  | Gets or sets an optional transaction code from an accounting system that batch is associated with |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BatchEndDateTime | yes | yes |  |  |  | Gets or sets end of the posting date and time range for FinancialTransactions that are included in this batch. Transactions that post before or on this date and time and after the BatchStartDateTime can be included in this batch. |
| BatchId | yes |  |  |  |  | Gets or sets the batch identifier. |
| BatchStartDateTime | yes | yes |  |  |  | Gets or sets the start posting date and time range of FinancialTransactions that are included in this batch. Transactions that post on or after this date and time and before the BatchEndDateTime can be included in this batch. |
| Campus | yes | yes |  |  |  | Gets or sets the campus. |
| ContextKey |  |  | yes |  |  |  |
| ControlAmount | yes | yes |  |  |  | Gets or sets the control amount. This should match the total value of all FinancialTransactions that are included in the batch. |
| Count | yes | yes |  |  |  | Gets or sets the count. NOTE: This always has a (hard-coded) value of 1. It is stored in the table to assist with analytics calculations. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the batch. |
| Status | yes | yes |  |  |  | Gets or sets the status of the batch. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| BatchEndDateTime | FinancialTransactions | 2c1cb26b-ab22-42d0-8164-aedee0dae667 |
| BatchStartDateTime | FinancialTransactions | 2c1cb26b-ab22-42d0-8164-aedee0dae667 |
| ControlAmount | FinancialTransactions | 2c1cb26b-ab22-42d0-8164-aedee0dae667 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
