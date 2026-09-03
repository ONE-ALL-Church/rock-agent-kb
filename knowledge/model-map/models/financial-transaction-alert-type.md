# Financial Transaction Alert Type Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Finance`
- Model title: `FinancialTransactionAlertType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `2e237b04-5b2a-40f1-8cd3-52673c104305`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 69 |
| Database-marked properties | 33 |
| Lava-marked properties | 52 |
| Lava-marked non-database properties | 21 |
| Related model links | 7 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AccountParticipantSystemCommunication |  | yes | yes |  |  | Gets or sets the System Communication that will be sent to any Account Participants. Account Participants are stored as Related Entity with RelatedEntity.PurposeKey of RelatedEntityPurposeKey.FinancialAccountGivingAlert. |
| AccountParticipantSystemCommunicationId | yes |  |  |  |  | Gets or sets the System Communication that will be sent to any Account Participants. Account Participants are stored as Related Entity with RelatedEntity.PurposeKey of RelatedEntityPurposeKey.FinancialAccountGivingAlert. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AlertSummaryNotificationGroup |  | yes | yes |  |  | Gets or sets the alert summary notification group. |
| AlertSummaryNotificationGroupId | yes | yes |  |  |  | Gets or sets the alert summary notification group identifier. |
| AlertType | yes | yes |  |  |  | Gets or sets the alert type. This is a hard coded list of values defined in the code as an enumeration. |
| AmountSensitivityScale | yes | yes |  |  |  | Gets or sets the amount sensitivity scale. This determines the point where a transaction amount is considered significantly larger or smaller than usual. See notes on AlertType to see how this value is used for Gratitude vs Follow-Up alert types. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the campus that this financial transaction alert type is associated with. |
| CampusId | yes | yes |  |  |  | Gets or sets the campus identifier. |
| ConnectionOpportunity |  | yes | yes |  |  | Gets or sets the connection opportunity. |
| ConnectionOpportunityId | yes | yes |  |  |  | Gets or sets the connection opportunity identifier. |
| ContextKey |  |  | yes |  |  |  |
| ContinueIfMatched | yes | yes |  |  |  | Gets or sets a value indicating whether [continue if matched]. |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DataView |  | yes | yes |  |  | Gets or sets the Data View that this financial transaction alert type is based on. |
| DataViewId | yes | yes |  |  |  | Gets or sets the data view identifier. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FinancialAccount |  | yes | yes |  |  | Gets or sets the financial account. |
| FinancialAccountId | yes | yes |  |  |  | Gets or sets the financial account identifier. |
| FinancialTransactionAlertTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| FinancialTransactionAlerts |  | yes | yes |  |  | Gets or sets the financial transaction alerts. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FrequencySensitivityScale | yes | yes |  |  |  | Gets or sets the frequency sensitivity scale. This determines the point where a transaction is considered significantly later or earlier than usual. See notes on AlertType to see how this value is used for Gratitude vs Follow-Up alert types. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IncludeChildFinancialAccounts | yes | yes |  |  |  | Gets or sets a value indicating whether [include child financial accounts]. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MaximumDaysSinceLastGift | yes | yes |  |  |  | Gets or sets the maximum days since last gift. |
| MaximumGiftAmount | yes | yes |  |  |  | Gets or sets the maximum gift amount. |
| MaximumMedianGiftAmount | yes | yes |  |  |  | Gets or sets the maximum median gift amount. |
| MinimumGiftAmount | yes | yes |  |  |  | Gets or sets the minimum gift amount. |
| MinimumMedianGiftAmount | yes | yes |  |  |  | Gets or sets the minimum median gift amount. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the name. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RepeatPreventionDuration | yes | yes |  |  |  | Gets or sets the repeat prevention duration (days). |
| RunDays | yes | yes |  |  | yes | Gets or sets the run days for this alert type. Null means all days of the week are run days. This is a hard coded list of values defined in the code as an enumeration. |
| RunDaysOfWeek | yes |  |  |  |  | Gets or sets the run days for this alert type. Null means all days of the week are run days. This is a hard coded list of values defined in the code as an enumeration. |
| SendBusEvent | yes | yes |  |  |  | Gets or sets a value indicating whether [send bus event]. |
| SupportedActions |  |  | yes |  |  |  |
| SystemCommunication |  | yes | yes |  |  | Gets or sets the System Communication that will be sent to the Donor (FinancialTransaction.AuthorizedPersonAlias). |
| SystemCommunicationId | yes | yes |  |  |  | Gets or sets the System Communication that will be sent to the Donor (FinancialTransaction.AuthorizedPersonAlias). |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowType |  | yes | yes |  |  | Gets or sets the type of the workflow. |
| WorkflowTypeId | yes | yes |  |  |  | Gets or sets the workflow type identifier. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AccountParticipantSystemCommunication | Gets or sets the System Communication that will be sent to any Account Participants. Account Participants are stored as Related Entity with RelatedEntity.PurposeKey of RelatedEntityPurposeKey.FinancialAccountGivingAlert. |
| AlertSummaryNotificationGroup | Gets or sets the alert summary notification group. |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the campus that this financial transaction alert type is associated with. |
| ConnectionOpportunity | Gets or sets the connection opportunity. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DataView | Gets or sets the Data View that this financial transaction alert type is based on. |
| EntityStringValue |  |
| FinancialAccount | Gets or sets the financial account. |
| FinancialTransactionAlerts | Gets or sets the financial transaction alerts. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| SystemCommunication | Gets or sets the System Communication that will be sent to the Donor (FinancialTransaction.AuthorizedPersonAlias). |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WorkflowType | Gets or sets the type of the workflow. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AccountParticipantSystemCommunication | [Related Entity](related-entity.md) | bd29e403-ba47-4688-be29-45a38ce8bd03 |
| AccountParticipantSystemCommunication | [System Communication](system-communication.md) | d0cad7c0-10fe-41ef-b89d-e6f0d22456c4 |
| AccountParticipantSystemCommunicationId | [Related Entity](related-entity.md) | bd29e403-ba47-4688-be29-45a38ce8bd03 |
| AccountParticipantSystemCommunicationId | [System Communication](system-communication.md) | d0cad7c0-10fe-41ef-b89d-e6f0d22456c4 |
| DataView | [Data View](data-view.md) | 57f8fa29-dcf1-4f74-8553-87e90f234139 |
| SystemCommunication | [System Communication](system-communication.md) | d0cad7c0-10fe-41ef-b89d-e6f0d22456c4 |
| SystemCommunicationId | [System Communication](system-communication.md) | d0cad7c0-10fe-41ef-b89d-e6f0d22456c4 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
