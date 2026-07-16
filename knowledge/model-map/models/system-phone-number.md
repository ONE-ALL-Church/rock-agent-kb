# System Phone Number Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Communication`
- Model title: `SystemPhoneNumber`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `66d62a9f-13cd-4160-8653-211b2a4abf16`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 54 |
| Database-marked properties | 23 |
| Lava-marked properties | 39 |
| Lava-marked non-database properties | 16 |
| Related model links | 1 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AssignedToPersonAlias |  | yes | yes |  |  | Gets or sets the person alias who should receive responses to the SMS number. This person must have a phone number with SMS enabled or no response will be sent. |
| AssignedToPersonAliasId | yes | yes |  |  |  | Gets or sets the identifier of the person alias who should receive responses to the SMS number. This person must have a phone number with SMS enabled or no response will be sent. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description. |
| DisableSmsOptInOutTracking | yes | yes |  |  |  | Gets or sets whether to prevent Rock from updating an individual's SMS status when they opt in or out of receiving SMS messages. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this phone number is active. |
| IsSmsEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this instance support SMS. |
| IsSmsForwardingEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this phone number will forward incoming messages to AssignedToPersonAliasId. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MobileApplicationSite |  | yes | yes |  |  | Gets or sets the SMS mobile application site. This is used when determining what devices to send push notifications to. |
| MobileApplicationSiteId | yes | yes |  |  |  | Gets or sets the mobile application site identifier. This is used when determining what devices to send push notifications to. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the friendly name of the phone number. |
| Number | yes | yes |  | yes |  | Gets or sets the phone number. This should be in E.123 format, such as +16235553324. |
| Order | yes | yes |  | yes |  | Gets or sets the sort and display order of the System Phone Number. This is an ascending order, so the lower the value the higher the sort priority. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ProviderIdentifier | yes | yes |  |  |  | Gets or sets the provider identifier. |
| SmsNotificationGroup |  | yes | yes |  |  | Gets or sets the SMS notification group. Active members of this group will be notified when a new SMS message comes in to this phone number. |
| SmsNotificationGroupId | yes | yes |  |  |  | Gets or sets the notification group identifier. Active members of this group will be notified when a new SMS message comes in to this phone number. |
| SmsReceivedWorkflowType |  | yes | yes |  |  | Gets or sets the workflow type that will be launched when an SMS message is received on this number. |
| SmsReceivedWorkflowTypeId | yes | yes |  |  |  | Gets or sets the identifier of the workflow type that will be launched when an SMS message is received on this number. |
| SupportedActions |  |  | yes |  |  |  |
| SuppressSmsOptInOutAutoReplies | yes | yes |  |  |  | Gets or sets whether to prevent Rock from sending automatic SMS replies to opt-in or opt-out messages. |
| SystemPhoneNumberAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AssignedToPersonAlias | Gets or sets the person alias who should receive responses to the SMS number. This person must have a phone number with SMS enabled or no response will be sent. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| MobileApplicationSite | Gets or sets the SMS mobile application site. This is used when determining what devices to send push notifications to. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| SmsNotificationGroup | Gets or sets the SMS notification group. Active members of this group will be notified when a new SMS message comes in to this phone number. |
| SmsReceivedWorkflowType | Gets or sets the workflow type that will be launched when an SMS message is received on this number. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Order | [System Phone Number](system-phone-number.md) | 66d62a9f-13cd-4160-8653-211b2a4abf16 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
