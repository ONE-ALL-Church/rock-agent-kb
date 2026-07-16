# Communication Recipient Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Communication`
- Model title: `CommunicationRecipient`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `37`
- Obsolete methods: `4`
- EntityType GUID: `3ec89b90-6692-451e-a48f-0d2adeba05bc`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 62 |
| Database-marked properties | 28 |
| Lava-marked properties | 43 |
| Lava-marked non-database properties | 16 |
| Related model links | 6 |
| Method signatures | 37 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| ActivityList |  |  | yes |  |  | Gets a list of activities. |
| ActivityListHtml |  |  | yes |  |  | Gets a list of activities. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalMergeValues |  | yes | yes |  |  | Gets or sets a dictionary containing the Additional Merge values for this communication |
| AdditionalMergeValuesJson | yes | yes |  |  |  | Gets or sets the AdditionalMergeValues as a Json string. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Communication |  | yes | yes |  |  | Gets or sets the Communication. |
| CommunicationId | yes | yes |  |  |  | Gets or sets the CommunicationId of the Communication. |
| CommunicationRecipientAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DeliveredDateTime | yes | yes |  |  |  | Gets or sets the datetime that communication was delivered to the recipient. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FirstSendAttemptDateTime | yes | yes |  |  |  | Gets or sets the datetime that communication was first attempted. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MediumEntityType |  | yes | yes |  |  | Gets or sets the type of the medium entity. |
| MediumEntityTypeId | yes | yes |  |  |  | Gets or sets the medium entity type identifier. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| OpenedClient | yes | yes |  |  |  | Gets or sets type of client that the recipient used to open the communication. |
| OpenedDateTime | yes | yes |  |  |  | Gets or sets the datetime that communication was opened by the recipient. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the Person who is receiving the Communication. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the PersonId of the Person who is being sent the Communication. |
| PersonalDevice |  |  | yes |  |  | Gets or sets the personal device. |
| PersonalDeviceId | yes |  |  |  |  | Gets or sets the personal device identifier. |
| ResponseCode | yes | yes |  |  |  | The response code from 100-99999 (excluding 666 and 911) with a prefix of '@'. For example, '@126345' Note: this numeric portion must be between 3 and 5 digits due to a regex that parses the message to find response codes |
| SendDateTime | yes | yes |  |  |  | Gets or sets the datetime that communication was sent. |
| SentMessage | yes | yes |  |  |  | Gets or sets the message as it was sent to the recipient (i.e. after lava merge). |
| SpamComplaintDateTime | yes | yes |  |  |  | Gets or sets the datetime when the recipient marked this communication as spam. |
| Status | yes | yes |  |  |  | Gets or sets the status of the Communication submission to the recipient. This is a hard coded list of values defined in the code as an enumeration. |
| StatusNote | yes | yes |  |  |  | Gets or sets the status note. |
| SupportedActions |  |  | yes |  |  |  |
| TransportEntityTypeName | yes | yes |  |  |  | Gets or sets the transport entity type identifier. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UniqueMessageId | yes | yes |  |  |  | Gets or sets the unique message identifier. |
| UnsubscribeDateTime | yes | yes |  |  |  | Gets or sets the datetime when the recipient unsubscribed. |
| UnsubscribeLevel | yes | yes |  |  |  | Gets or sets the unsubscribe level. This is a hard coded list of values defined in the code as an enumeration. |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AdditionalMergeValues | Gets or sets a dictionary containing the Additional Merge values for this communication |
| AttributeValues |  |
| Attributes |  |
| Communication | Gets or sets the Communication. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| MediumEntityType | Gets or sets the type of the medium entity. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the Person who is receiving the Communication. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Communication | [Communication](communication.md) | c4ccbd91-1264-48bf-bc33-92751c8948b5 |
| CommunicationId | [Communication](communication.md) | c4ccbd91-1264-48bf-bc33-92751c8948b5 |
| PersonAlias | [Communication](communication.md) | c4ccbd91-1264-48bf-bc33-92751c8948b5 |
| PersonAlias | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| PersonAliasId | [Communication](communication.md) | c4ccbd91-1264-48bf-bc33-92751c8948b5 |
| PersonAliasId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
