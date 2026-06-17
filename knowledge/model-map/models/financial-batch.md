# Financial Batch Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Finance`
- Model title: `FinancialBatch`
- EntityType GUID: `bdd09c8e-2c52-4d08-9062-be7d52d190c2`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 51 |
| Database-marked properties | 22 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 14 |
| Related model links | 6 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AccountingSystemCode | yes | yes |  |  |  | Gets or sets an optional transaction code from an accounting system that batch is associated with |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BatchEndDateTime | yes | yes |  |  |  | Gets or sets end of the posting date and time range for FinancialTransactions that are included in this batch. Transactions that post before or on this date and time and after the BatchStartDateTime can be included in this batch. |
| BatchStartDateTime | yes | yes |  |  |  | Gets or sets the start posting date and time range of FinancialTransactions that are included in this batch. Transactions that post on or after this date and time and before the BatchEndDateTime can be included in this batch. |
| Campus |  | yes | yes |  |  | Gets or sets the Campus that this batch is associated with. |
| CampusId | yes | yes |  |  |  | Gets or sets the CampusId of the Campus that this batch is associated with. If the batch is not linked to a campus, this value will be null. |
| ContextKey |  |  | yes |  |  |  |
| ControlAmount | yes | yes |  |  |  | Gets or sets the control amount. This should match the total value of all FinancialTransactions that are included in the batch. Use FinancialBatchService.IncrementControlAmount(System.Int32,System.Decimal,History.HistoryChangeList)() if you are incrementing the control amount based on a transaction amount. |
| ControlItemCount | yes | yes |  |  |  | Gets or sets the control item count. |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FinancialBatchAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsAutomated | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is automated. If IsAutomated is True, the UI should not allow the status of Pending to be changed to Open or Closed ( an external process will be in change of changing the status ) |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the batch. |
| Note | yes | yes |  |  |  | Gets or sets the note. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RemoteSettlementAmount | yes |  |  |  |  | Gets or sets the external system's settlement batch amount. |
| RemoteSettlementBatchKey | yes |  |  |  |  | Gets or sets the Batch Key for tracking an external system's settlement batch id/key |
| RemoteSettlementBatchUrl | yes | yes |  |  |  | Gets or sets the URL to view the remote settlement information of the batch. This is usually set by gateways to view the related information on the back-end gateway's site. |
| Status | yes | yes |  |  |  | Gets or sets the status of the batch. This is a hard coded list of values defined in the code as an enumeration. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| Transactions |  | yes | yes |  |  | Gets or sets a collection that contains the FinancialTransactions that are included in the batch. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the Campus that this batch is associated with. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Transactions | Gets or sets a collection that contains the FinancialTransactions that are included in the batch. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| BatchEndDateTime | FinancialTransactions | 2c1cb26b-ab22-42d0-8164-aedee0dae667 |
| BatchStartDateTime | FinancialTransactions | 2c1cb26b-ab22-42d0-8164-aedee0dae667 |
| Campus | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| CampusId | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| ControlAmount | FinancialTransactions | 2c1cb26b-ab22-42d0-8164-aedee0dae667 |
| Transactions | FinancialTransactions | 2c1cb26b-ab22-42d0-8164-aedee0dae667 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
