# Financial Transaction Refund Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Finance`
- Model title: `FinancialTransactionRefund`
- EntityType GUID: `7616e2af-cef2-44a5-b27f-3e70ec8b70fa`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 42 |
| Database-marked properties | 12 |
| Lava-marked properties | 27 |
| Lava-marked non-database properties | 15 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
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
| FinancialTransaction |  | yes | yes |  |  | Gets or sets the FinancialTransaction. |
| FinancialTransactionRefundAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
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
| OriginalTransaction |  | yes | yes |  |  | Gets or sets the original transaction. |
| OriginalTransactionId | yes | yes |  |  |  | Gets or sets the original transaction identifier. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RefundReasonSummary | yes | yes |  |  |  | Gets or sets a detailed summary of the circumstances surrounding why a refund was issued. |
| RefundReasonValue |  | yes | yes |  |  | Gets or sets the refund reason DefinedValue indicating the reason for the refund. |
| RefundReasonValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the return reason DefinedValue indicating the reason why a refund was issued for the original transaction. These are found in the "Refund Reason" Defined Type. |
| SupportedActions |  |  | yes |  |  |  |
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
| FinancialTransaction | Gets or sets the FinancialTransaction. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| OriginalTransaction | Gets or sets the original transaction. |
| RefundReasonValue | Gets or sets the refund reason DefinedValue indicating the reason for the refund. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| FinancialTransaction | [FinancialTransaction](financial-transaction.md) |  |
| OriginalTransaction | transaction |  |
| RefundReasonValue | [DefinedValue](defined-value.md) |  |
| RefundReasonValueId | [DefinedValue](defined-value.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
