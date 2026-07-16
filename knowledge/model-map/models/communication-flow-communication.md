# Communication Flow Communication Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Communication`
- Model title: `CommunicationFlowCommunication`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `07d0cecc-066f-45a8-95bc-7c8f5199d53c`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 47 |
| Database-marked properties | 17 |
| Lava-marked properties | 32 |
| Lava-marked non-database properties | 15 |
| Related model links | 0 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CommunicationFlow |  | yes | yes |  |  | Gets or sets the Communication Flow. |
| CommunicationFlowCommunicationAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| CommunicationFlowId | yes | yes |  | yes |  | Gets or sets the Communication Flow identifier. |
| CommunicationFlowInstanceCommunications |  | yes | yes |  |  | Gets or sets the Communication Flow Instances that use this Communication Flow Communication. |
| CommunicationTemplate |  | yes | yes |  |  | Gets or sets the Communication Template. |
| CommunicationTemplateId | yes | yes |  | yes |  | Gets or sets the Communication Template identifier used to create the communications that will be sent to recipients. |
| CommunicationType | yes | yes |  |  |  | Gets or sets the communication type for this communication flow communication. This is a hard coded list of values defined in the code as an enumeration. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DaysToWait | yes | yes |  |  |  | Gets or sets the number of days to wait to send since the last communication in this flow. |
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
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the Communication Flow Communication (maximum 100 characters). |
| Order | yes | yes |  |  |  | Gets or sets the order of this communication in the communication flow. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SupportedActions |  |  | yes |  |  |  |
| TimeToSend | yes | yes |  |  |  | Gets or sets the time to send this communication flow communication. |
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
| CommunicationFlowInstanceCommunications | Gets or sets the Communication Flow Instances that use this Communication Flow Communication. |
| CommunicationTemplate | Gets or sets the Communication Template. |
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
