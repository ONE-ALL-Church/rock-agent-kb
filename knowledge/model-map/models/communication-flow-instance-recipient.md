# Communication Flow Instance Recipient Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Communication`
- Model title: `CommunicationFlowInstanceRecipient`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `f615ac08-8acd-48f9-b42e-2f4ce02d4206`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 45 |
| Database-marked properties | 15 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 15 |
| Related model links | 0 |
| Method signatures | 36 |
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
| CommunicationFlowInstance |  | yes | yes |  |  | Gets or sets the Communication Flow Instance. |
| CommunicationFlowInstanceId | yes | yes |  | yes |  | Gets or sets the identifier of the Communication Flow Instance. |
| CommunicationFlowInstanceRecipientAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
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
| InactiveReason | yes | yes |  |  |  | Gets or sets the inactive reason for this Communication Flow Instance Recipient. This is a hard coded list of values defined in the code as an enumeration. |
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
| RecipientPersonAlias |  | yes | yes |  |  | Gets or sets the recipient Person Alias. |
| RecipientPersonAliasId | yes | yes |  | yes |  | Gets or sets the identifier of the recipient Person Alias. |
| Status | yes | yes |  |  |  | Gets or sets the status for this Communication Flow Instance Recipient. This is a hard coded list of values defined in the code as an enumeration. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UnsubscribeCommunicationRecipient |  | yes | yes |  |  | Gets or sets the Communication Recipient that was unsubscribed. |
| UnsubscribeCommunicationRecipientId | yes | yes |  |  |  | Gets or sets the identifier of the Communication Recipient that was unsubscribed. |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WasConversionGoalPreMet | yes | yes |  |  |  | Gets or sets a value indicating whether the conversion goal was pre-met for this recipient when the instance was created. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CommunicationFlowInstance | Gets or sets the Communication Flow Instance. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RecipientPersonAlias | Gets or sets the recipient Person Alias. |
| TypeId |  |
| TypeName |  |
| UnsubscribeCommunicationRecipient | Gets or sets the Communication Recipient that was unsubscribed. |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
