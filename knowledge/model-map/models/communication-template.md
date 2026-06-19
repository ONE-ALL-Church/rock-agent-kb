# Communication Template Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Communication`
- Model title: `CommunicationTemplate`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `39`
- Obsolete methods: `4`
- EntityType GUID: `a9493afe-4316-4651-800d-5028e4c7444d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 80 |
| Database-marked properties | 41 |
| Lava-marked properties | 63 |
| Lava-marked non-database properties | 22 |
| Related model links | 2 |
| Method signatures | 39 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 2 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Attachments |  | yes | yes |  |  | Gets or sets the attachments. NOTE: In most cases, you should use GetAttachments( CommunicationType ) instead. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BCCEmails | yes | yes |  |  |  | Gets or sets the BCC emails. |
| CCEmails | yes | yes |  |  |  | Gets or sets the cc emails. |
| Category |  | yes | yes |  |  | Gets or sets the category. |
| CategoryId | yes | yes |  |  |  | Gets or sets the category identifier. |
| CommunicationTemplateAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CssInliningEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether [CSS inlining enabled]. |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description. |
| EmailAttachmentBinaryFileIds |  |  | yes |  |  | Gets or sets a list of email binary file ids |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FromEmail | yes | yes |  |  |  | Gets or sets from email. |
| FromName | yes | yes |  |  |  | Gets or sets from name. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| ImageFile |  | yes | yes |  |  | Gets or sets the image file for the Template Preview Image |
| ImageFileId | yes | yes |  |  |  | Gets or sets the image file identifier for the Template Preview Image |
| IsActive | yes | yes |  | yes |  | Gets or sets a flag indicating if this is an active communication template. This value is required. |
| IsPersonal |  | yes | yes |  |  | Gets a value indicating whether this instance is personal (has a SenderPersonAliasId value) or not |
| IsStarter | yes | yes |  |  |  | Gets or sets a flag indicating if this is a starter communication template. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this PageContext is a part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LavaFields |  | yes | yes |  |  | A Dictionary of Key,DefaultValue for Lava MergeFields that can be used when processing Lava in the CommunicationTemplate By convention, a Key with a 'Color' suffix will indicate that the Value is selected using a ColorPicker. Otherwise,it is just text |
| LavaFieldsJson | yes | yes |  |  |  | The internal storage for LavaFields |
| LogoBinaryFile |  | yes | yes |  |  | Gets or sets the logo binary file that email messages using this template can use for the logo in the message content |
| LogoBinaryFileId | yes | yes |  |  |  | Gets or sets the logo binary file identifier that email messages using this template can use for the logo in the message content |
| Message | yes | yes |  |  |  | Gets or sets the message. |
| MessageMetaData | yes | yes |  |  |  | Gets or sets the message meta data. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the Communication Template |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  | When checking for security, if a template does not have specific rules, first check the category it belongs to, but then check the default entity security for templates. |
| PushData | yes | yes |  |  |  | Gets or sets the push data. |
| PushImageBinaryFile |  | yes | yes |  |  | Gets or sets the push image file. |
| PushImageBinaryFileId | yes | yes |  |  |  | Gets or sets the push image file identifier. |
| PushMessage | yes | yes |  |  |  | Gets or sets the message. |
| PushOpenAction | yes | yes |  |  |  | Gets or sets the push open action. This is a hard coded list of values defined in the code as an enumeration. |
| PushOpenMessage | yes | yes |  |  |  | Gets or sets the push open message. |
| PushOpenMessageJson | yes | yes |  |  |  | Gets or sets the push open message structured content JSON. |
| PushSound | yes | yes |  |  |  | Gets or sets from number. |
| PushTitle | yes | yes |  |  |  | Gets or sets from number. |
| ReplyToEmail | yes | yes |  |  |  | Gets or sets the reply to email. |
| SMSAttachmentBinaryFileIds |  |  | yes |  |  | Gets or sets a list of sms binary file ids |
| SMSFromDefinedValue |  | yes | yes |  | yes | Gets or sets the SMS from defined value. |
| SMSFromDefinedValueId | yes | yes |  |  | yes | Gets or sets from number. |
| SMSMessage | yes | yes |  |  |  | Gets or sets the message. |
| SenderPersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias of the Communication's sender. |
| SenderPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonId of the Person who is the sender of the Communication |
| SmsFromSystemPhoneNumber |  | yes | yes |  |  | Gets or sets the system phone number used for SMS sending. |
| SmsFromSystemPhoneNumberId | yes | yes |  |  |  | Gets or sets the system phone number identifier used for SMS sending. |
| Subject | yes | yes |  |  |  | Gets or sets the name of the Communication |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| UsageType | yes | yes |  |  |  | Gets or sets the Communication Template usage type. This is a hard coded list of values defined in the code as an enumeration. |
| ValidationResults |  |  | yes |  |  |  |
| Version | yes | yes |  |  |  | Gets or sets the communication template version. This is a hard coded list of values defined in the code as an enumeration. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Attachments | Gets or sets the attachments. NOTE: In most cases, you should use GetAttachments( CommunicationType ) instead. |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the category. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ImageFile | Gets or sets the image file for the Template Preview Image |
| IsPersonal | Gets a value indicating whether this instance is personal (has a SenderPersonAliasId value) or not |
| LavaFields | A Dictionary of Key,DefaultValue for Lava MergeFields that can be used when processing Lava in the CommunicationTemplate By convention, a Key with a 'Color' suffix will indicate that the Value is selected using a ColorPicker. Otherwise,it is just text |
| LogoBinaryFile | Gets or sets the logo binary file that email messages using this template can use for the logo in the message content |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PushImageBinaryFile | Gets or sets the push image file. |
| SMSFromDefinedValue | Gets or sets the SMS from defined value. |
| SenderPersonAlias | Gets or sets the Person Alias of the Communication's sender. |
| SmsFromSystemPhoneNumber | Gets or sets the system phone number used for SMS sending. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| SenderPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| SenderPersonAliasId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_removed | SMSFromDefinedValue |  |
| property_removed | SMSFromDefinedValueId |  |
