# Communication Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Communication`
- Model title: `Communication`
- EntityType GUID: `c4ccbd91-1264-48bf-bc33-92751c8948b5`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 94 |
| Database-marked properties | 53 |
| Lava-marked properties | 76 |
| Lava-marked non-database properties | 24 |
| Related model links | 11 |
| Pre-alpha changes touching this model | 2 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalMergeFields |  | yes | yes |  |  | Gets or sets the additional merge field list. When a communication is created from a grid, the grid may add additional merge fields that will be available for the communication. |
| AdditionalMergeFieldsJson | yes | yes |  |  |  | Gets or sets a JSON string containing any additional merge fields for the Communication. |
| Attachments |  | yes | yes |  |  | Gets or sets the attachments. NOTE: In most cases, you should use GetAttachments( CommunicationType ) instead. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BCCEmails | yes | yes |  |  |  | Gets or sets a comma separated list of BCC'ed email addresses. |
| CCEmails | yes | yes |  |  |  | Gets or sets a comma separated list of CC'ed email addresses. |
| CommunicationAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| CommunicationTemplate |  | yes | yes |  |  | Gets or sets the CommunicationTemplate that was used to compose this communication |
| CommunicationTemplateId | yes |  |  |  |  | Gets or sets the CommunicationTemplate that was used to compose this communication |
| CommunicationTopicValue |  | yes | yes |  |  | Gets or sets the communication topic defined value. |
| CommunicationTopicValueId | yes | yes |  |  |  | Gets or sets the communication topic defined value. |
| CommunicationType | yes | yes |  | yes |  | Gets or sets the communication type value identifier. This is a hard coded list of values defined in the code as an enumeration. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EmailAttachmentBinaryFileIds |  |  | yes |  |  | Gets or sets a list of email binary file ids |
| EmailMetricsReminderOffsetDays | yes | yes |  |  |  | Gets or sets the number of days to wait after the communication is sent to send the email metrics reminder communication. |
| EmailMetricsReminderSentDateTime | yes | yes |  |  |  | Gets or sets the datetime that the email metrics reminder communication was sent. |
| EnabledLavaCommands | yes | yes |  |  |  | Gets or sets a comma-delimited list of enabled LavaCommands |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExcludeDuplicateRecipientAddress | yes | yes |  |  |  | Option to prevent communications from being sent to people with the same email/SMS addresses. This will mean two people who share an address will not receive a personalized communication, only one of them will. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FromEmail | yes | yes |  |  |  | Gets or sets from email address. |
| FromName | yes | yes |  |  |  | Gets or sets from name. |
| FutureSendDateTime | yes | yes |  |  |  | Gets or sets the future send date for the communication. This allows a user to schedule when a communication is sent and the communication will not be sent until that date and time. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsBulkCommunication | yes | yes |  |  |  | Gets or sets the is bulk communication. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ListGroup |  | yes | yes |  |  | Gets or sets the list Group. |
| ListGroupId | yes | yes |  |  |  | Gets or sets the list that email is being sent to. |
| Message | yes | yes |  |  |  | Gets or sets the message. |
| MessageMetaData | yes | yes |  |  |  | Gets or sets the message meta data. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the name of the Communication |
| ParentAuthority |  |  | yes |  |  | A parent authority. If a user is not specifically allowed or denied access to this object, Rock will check the default authorization on the current type, and then the authorization on the Rock.Security.GlobalDefault entity |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonalizationSegments | yes | yes |  |  |  | Gets or sets the personalization segments that list is being filtered to. |
| PushData | yes | yes |  |  |  | Gets or sets the push data. |
| PushImageBinaryFileId | yes | yes |  |  |  | Gets or sets the push image file identifier. |
| PushMessage | yes | yes |  |  |  | Gets or sets the message. |
| PushOpenAction | yes | yes |  |  |  | Gets or sets the push open action. This is a hard coded list of values defined in the code as an enumeration. |
| PushOpenMessage | yes | yes |  |  |  | Gets or sets the push open message. |
| PushOpenMessageJson | yes | yes |  |  |  | Gets or sets the push open message structured content JSON. |
| PushSound | yes | yes |  |  |  | Gets or sets push sound. |
| PushTitle | yes | yes |  |  |  | Gets or sets the push notification title. |
| Recipients |  | yes | yes |  |  | Gets or sets a collection containing the CommunicationRecipients for the Communication. |
| ReplyToEmail | yes | yes |  |  |  | Gets or sets the reply to email address. |
| ReviewedDateTime | yes | yes |  |  |  | Gets or sets the date and time stamp of when the Communication was reviewed. |
| ReviewerNote | yes | yes |  |  |  | Gets or sets the note that was entered by the reviewer. |
| ReviewerPersonAlias |  | yes | yes |  |  | Gets or sets the reviewer PersonAlias. |
| ReviewerPersonAliasId | yes | yes |  |  |  | Gets or sets the reviewer person alias identifier. |
| SMSAttachmentBinaryFileIds |  |  | yes |  |  | Gets or sets a list of sms binary file ids |
| SMSFromDefinedValue |  | yes | yes |  |  | [Obsoleted in v15] Use SmsFromSystemPhoneNumber instead. Gets or sets the SMS from defined value. |
| SMSFromDefinedValueId | yes | yes |  |  |  | [Obsoleted in v15] Use SmsFromSystemPhoneNumberId instead. Gets or sets the SMS from number. |
| SMSMessage | yes | yes |  |  |  | Gets or sets the message. |
| SegmentCriteria | yes | yes |  |  |  | Gets or sets if communication is targeted to people in all selected segments or any selected segments. This is a hard coded list of values defined in the code as an enumeration. |
| Segments | yes | yes |  |  |  | Gets or sets the segments that list is being filtered to (comma-delimited list of dataview guids). |
| SendDateKey | yes | yes |  |  |  | Gets the send date key. |
| SendDateTime | yes | yes |  |  |  | Gets or sets the datetime that communication was sent. This also indicates that communication shouldn't attempt to send again. |
| SendSourceDate |  | yes | yes |  |  | Gets or sets the send source date. |
| SenderPersonAlias |  | yes | yes |  |  | Gets or sets the sender PersonAlias. |
| SenderPersonAliasId | yes | yes |  |  |  | Gets or sets the sender PersonAlias identifier. |
| SmsFromSystemPhoneNumber |  | yes | yes |  |  | Gets or sets the system phone number used for SMS sending. |
| SmsFromSystemPhoneNumberId | yes | yes |  |  |  | Gets or sets the system phone number identifier used for SMS sending. |
| Status | yes | yes |  |  |  | Gets or sets the status of the Communication. This is a hard coded list of values defined in the code as an enumeration. |
| Subject | yes | yes |  |  |  | Gets or sets the name of the Communication |
| Summary | yes | yes |  |  |  | Gets or sets the summary of the Communication |
| SupportedActions |  |  | yes |  |  |  |
| SystemCommunication |  | yes | yes |  |  | Gets or sets the SystemCommunication that this communication is associated with. |
| SystemCommunicationId | yes | yes |  |  |  | Gets or sets the SystemCommunication that this communication is associated with. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| UrlReferrer | yes | yes |  |  |  | Gets or sets the URL from where this communication was created (grid) |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AdditionalMergeFields | Gets or sets the additional merge field list. When a communication is created from a grid, the grid may add additional merge fields that will be available for the communication. |
| Attachments | Gets or sets the attachments. NOTE: In most cases, you should use GetAttachments( CommunicationType ) instead. |
| AttributeValues |  |
| Attributes |  |
| CommunicationTemplate | Gets or sets the CommunicationTemplate that was used to compose this communication |
| CommunicationTopicValue | Gets or sets the communication topic defined value. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ListGroup | Gets or sets the list Group. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Recipients | Gets or sets a collection containing the CommunicationRecipients for the Communication. |
| ReviewerPersonAlias | Gets or sets the reviewer PersonAlias. |
| SMSFromDefinedValue | [Obsoleted in v15] Use SmsFromSystemPhoneNumber instead. Gets or sets the SMS from defined value. |
| SendSourceDate | Gets or sets the send source date. |
| SenderPersonAlias | Gets or sets the sender PersonAlias. |
| SmsFromSystemPhoneNumber | Gets or sets the system phone number used for SMS sending. |
| SystemCommunication | Gets or sets the SystemCommunication that this communication is associated with. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Attachments | attachments |  |
| CommunicationTemplate | [CommunicationTemplate](communication-template.md) |  |
| CommunicationTemplateId | [CommunicationTemplate](communication-template.md) |  |
| ListGroup | [Group](group.md) |  |
| ListGroupId | list |  |
| PushImageBinaryFileId | image file |  |
| Recipients | CommunicationRecipients |  |
| ReviewerPersonAlias | [PersonAlias](person-alias.md) |  |
| SendSourceDate | send source date |  |
| SenderPersonAlias | [PersonAlias](person-alias.md) |  |
| SenderPersonAliasId | [PersonAlias](person-alias.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_removed | SMSFromDefinedValue |  |
| property_removed | SMSFromDefinedValueId |  |
