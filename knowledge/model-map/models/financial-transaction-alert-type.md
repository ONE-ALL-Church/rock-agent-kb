# Financial Transaction Alert Type Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Finance`
- Model title: `FinancialTransactionAlertType`
- EntityType GUID: `2e237b04-5b2a-40f1-8cd3-52673c104305`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 68 |
| Database-marked properties | 32 |
| Lava-marked properties | 52 |
| Lava-marked non-database properties | 21 |
| Related model links | 7 |
| Pre-alpha changes touching this model | 4 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AccountParticipantSystemCommunication |  | yes | yes |  |  | Gets or sets the SystemCommunication that will be sent to any Account Participants. Account Participants are stored as RelatedEntity with RelatedEntity.PurposeKey of . |
| AccountParticipantSystemCommunicationId | yes |  |  |  |  | Gets or sets the SystemCommunication that will be sent to any Account Participants. Account Participants are stored as RelatedEntity with RelatedEntity.PurposeKey of . |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AlertSummaryNotificationGroup |  | yes | yes |  |  | Gets or sets the alert summary notification group. |
| AlertSummaryNotificationGroupId | yes | yes |  |  |  | Gets or sets the alert summary notification group identifier. |
| AlertType | yes | yes |  |  |  | Gets or sets the alert type. This is a hard coded list of values defined in the code as an enumeration. |
| AmountSensitivityScale | yes | yes |  |  |  | Gets or sets the amount sensitivity scale. This determines the point where a transaction amount is considered significantly larger or smaller than usual. See notes on Alert Type to see how this value is used for Gratitude vs Follow-Up alert types. |
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
| DataView |  | yes | yes |  |  | Gets or sets the DataView that this financial transaction alert type is based on. |
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
| FrequencySensitivityScale | yes | yes |  |  |  | Gets or sets the frequency sensitivity scale. This determines the point where a transaction is considered significantly later or earlier than usual. See notes on Alert Type to see how this value is used for Gratitude vs Follow-Up alert types. |
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
| RunDays | yes | yes |  |  |  | Gets or sets the run days for this alert type. Null means all days of the week are run days. This is a hard coded list of values defined in the code as an enumeration. |
| SendBusEvent | yes | yes |  |  |  | Gets or sets a value indicating whether [send bus event]. |
| SupportedActions |  |  | yes |  |  |  |
| SystemCommunication |  | yes | yes |  |  | Gets or sets the SystemCommunication that will be sent to the Donor (FinancialTransaction.AuthorizedPersonAlias). |
| SystemCommunicationId | yes | yes |  |  |  | Gets or sets the SystemCommunication that will be sent to the Donor (FinancialTransaction.AuthorizedPersonAlias). |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowType |  | yes | yes |  |  | Gets or sets the type of the workflow. |
| WorkflowTypeId | yes | yes |  |  |  | Gets or sets the workflow type identifier. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AccountParticipantSystemCommunication | Gets or sets the SystemCommunication that will be sent to any Account Participants. Account Participants are stored as RelatedEntity with RelatedEntity.PurposeKey of . |
| AlertSummaryNotificationGroup | Gets or sets the alert summary notification group. |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the campus that this financial transaction alert type is associated with. |
| ConnectionOpportunity | Gets or sets the connection opportunity. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DataView | Gets or sets the DataView that this financial transaction alert type is based on. |
| EntityStringValue |  |
| FinancialAccount | Gets or sets the financial account. |
| FinancialTransactionAlerts | Gets or sets the financial transaction alerts. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| SystemCommunication | Gets or sets the SystemCommunication that will be sent to the Donor (FinancialTransaction.AuthorizedPersonAlias). |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WorkflowType | Gets or sets the type of the workflow. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AccountParticipantSystemCommunication | [RelatedEntity](related-entity.md) |  |
| AccountParticipantSystemCommunication | [SystemCommunication](system-communication.md) |  |
| AccountParticipantSystemCommunicationId | [RelatedEntity](related-entity.md) |  |
| AccountParticipantSystemCommunicationId | [SystemCommunication](system-communication.md) |  |
| DataView | [DataView](data-view.md) |  |
| SystemCommunication | [SystemCommunication](system-communication.md) |  |
| SystemCommunicationId | [SystemCommunication](system-communication.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | RunDaysOfWeek |  |
| property_changed | AccountParticipantSystemCommunication | description |
| property_changed | AccountParticipantSystemCommunicationId | description |
| property_changed | RunDays | is_obsolete |
