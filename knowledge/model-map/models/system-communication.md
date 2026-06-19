# System Communication Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Communication`
- Model title: `SystemCommunication`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `d0cad7c0-10fe-41ef-b89d-e6f0d22456c4`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 64 |
| Database-marked properties | 33 |
| Lava-marked properties | 49 |
| Lava-marked non-database properties | 16 |
| Related model links | 0 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 2 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Bcc | yes | yes |  |  |  | Gets or sets the email addresses that should be sent a BCC or blind carbon copy of an email using this template. If there is not a predetermined distribution list; this property can remain empty. |
| Body | yes | yes |  | yes |  | Gets or sets the Body template that is used for emails that use this template. |
| Category |  | yes | yes |  |  | Gets or sets the category. |
| CategoryId | yes | yes |  |  |  | Gets or sets the category identifier. |
| Cc | yes | yes |  |  |  | Gets or sets the email addresses that should be sent a CC or carbon copy of an email using this template. If there is not a predetermined distribution list, this property can remain empty. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CssInliningEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether CSS styles should be inlined in the message body to ensure compatibility with oldere HTML rendering engines. |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| From | yes | yes |  |  |  | Gets or sets the From email address. |
| FromName | yes | yes |  |  |  | Gets or sets from name. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if this item is available for use. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if the email template is part of the Rock core system/framework. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LavaFields |  | yes | yes |  |  | A Dictionary of Key,DefaultValue for Lava MergeFields that can be used when processing Lava in the SystemCommunication. By convention, a Key with a 'Color' suffix will indicate that the Value is selected using a ColorPicker - otherwise, it is just text. |
| LavaFieldsJson | yes | yes |  |  |  | The internal storage for CommunicationTemplate.LavaFields |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PushData | yes | yes |  |  |  | Gets or sets the push data. |
| PushImageBinaryFileId | yes | yes |  |  |  | Gets or sets the push image file identifier. |
| PushMessage | yes | yes |  |  |  | Gets or sets the message text. |
| PushOpenAction | yes | yes |  |  |  | Gets or sets the push open action. This is a hard coded list of values defined in the code as an enumeration. |
| PushOpenMessage | yes | yes |  |  |  | Gets or sets the push open message. |
| PushOpenMessageJson | yes | yes |  |  |  | Gets or sets the push open message structured content JSON. |
| PushSound | yes | yes |  |  |  | Gets or sets the name of the sound alert to use for the notification. |
| PushTitle | yes | yes |  |  |  | Gets or sets the title of the notification. |
| SMSFromDefinedValue |  | yes | yes |  | yes | Gets or sets the SMS from defined value. |
| SMSFromDefinedValueId | yes | yes |  |  | yes | Gets or sets the SMS from number. |
| SMSMessage | yes | yes |  |  |  | Gets or sets the SMS message content. |
| SmsFromSystemPhoneNumber |  | yes | yes |  |  | Gets or sets the system phone number used for SMS sending. |
| SmsFromSystemPhoneNumberId | yes | yes |  |  |  | Gets or sets the system phone number identifier used for SMS sending. |
| Subject | yes | yes |  | yes |  | Gets or sets the subject of an email that uses this template. |
| SupportedActions |  |  | yes |  |  |  |
| SystemCommunicationAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Title | yes | yes |  | yes |  | Gets or sets the Title of the EmailTemplate |
| To | yes | yes |  |  |  | Gets or sets the To email addresses that emails using this template should be delivered to. If there is not a predetermined distribution list, this property can remain empty. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the category. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| LavaFields | A Dictionary of Key,DefaultValue for Lava MergeFields that can be used when processing Lava in the SystemCommunication. By convention, a Key with a 'Color' suffix will indicate that the Value is selected using a ColorPicker - otherwise, it is just text. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| SMSFromDefinedValue | Gets or sets the SMS from defined value. |
| SmsFromSystemPhoneNumber | Gets or sets the system phone number used for SMS sending. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_removed | SMSFromDefinedValue |  |
| property_removed | SMSFromDefinedValueId |  |
