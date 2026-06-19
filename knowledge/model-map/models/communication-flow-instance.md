# Communication Flow Instance Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Communication`
- Model title: `CommunicationFlowInstance`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `7b487d88-0667-4aff-bc6c-1fc8482392c8`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 43 |
| Database-marked properties | 13 |
| Lava-marked properties | 26 |
| Lava-marked non-database properties | 15 |
| Related model links | 0 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CommunicationFlow |  | yes | yes |  |  | Gets or sets the Communication Flow. |
| CommunicationFlowId | yes | yes |  | yes |  | Gets or sets the identifier of the Communication Flow. |
| CommunicationFlowInstanceAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| CommunicationFlowInstanceCommunications |  | yes | yes |  |  | Gets or sets the communications for this Communication Flow Instance. |
| CommunicationFlowInstanceRecipients |  | yes | yes |  |  | Gets or sets the recipients for this Communication Flow Instance. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsConversionGoalTrackingCompleted | yes |  |  |  |  | Gets or sets a value indicating whether this flow instance has finished all conversion goal tracking and no further evaluation is required. |
| IsMessagingCompleted | yes |  |  |  |  | Gets or sets a value indicating whether this flow instance has finished scheduling or sending all configured communications. |
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
| StartDate | yes | yes |  |  |  | Gets or sets the date when this Communication Flow Instance starts. |
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
| CommunicationFlow | Gets or sets the Communication Flow. |
| CommunicationFlowInstanceCommunications | Gets or sets the communications for this Communication Flow Instance. |
| CommunicationFlowInstanceRecipients | Gets or sets the recipients for this Communication Flow Instance. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
