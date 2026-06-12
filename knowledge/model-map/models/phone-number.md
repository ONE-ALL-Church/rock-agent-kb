# Phone Number Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `CRM`
- Model title: `PhoneNumber`
- EntityType GUID: `ad7e27cb-036d-40c6-b352-81b38bfae798`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 53 |
| Database-marked properties | 23 |
| Lava-marked properties | 37 |
| Lava-marked non-database properties | 15 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CountryCode | yes | yes |  |  |  | Gets or sets the country code. |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets an optional description of the PhoneNumber. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| Extension | yes | yes |  |  |  | Gets or sets the extension (if any) that would need to be dialed to contact the owner. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FullNumber | yes | yes |  | yes |  | Gets the full phone number (country code and number). This should really only be used for queries and comparisons. NOTE: If Number is a partial number (for example, no area code), then FullNumber isn't really the full number, and neither is NumberFormatted. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsMessagingEnabled | yes | yes |  | yes |  | Gets or sets a flag indicating whether the number has been opted in for SMS |
| IsMessagingOptedOut | yes | yes |  |  |  | Gets or sets a flag indicating whether the phone number has opted out of messages through the SMS provider. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if the PhoneNumber is part of the Rock core system/framework. This property is required. |
| IsUnlisted | yes | yes |  |  |  | Gets or sets a flag indicating whether the PhoneNumber is unlisted or not. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MessagingOptedOutDateTime | yes | yes |  |  |  | Gets or sets the date and time when the phone number opted out of messaging. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Number | yes | yes |  | yes |  | Gets or sets the phone number without country code. The number is stored without any string formatting. (i.e. (502) 555-1212 will be stored as 5025551212). This property is required. |
| NumberFormatted | yes | yes |  |  |  | Gets or sets the formatted number. Note: value is recalculated on every add/modify of entity during context's default SaveChanges() method. |
| NumberFormattedWithCountryCode |  | yes | yes |  |  | Gets the number formatted with country code. |
| NumberReversed | yes |  |  |  |  | Gets or sets the phone number reversed. This is the fastest way to search by phone number ending in xxxx. |
| NumberTypeValue |  | yes | yes |  |  | Gets or sets the Phone Number's NumberType DefinedValue |
| NumberTypeValueId | yes | yes |  |  |  | Gets the Phone Number's Number Type DefinedValue Id. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Person |  | yes | yes |  |  | Gets or sets the Person who the PhoneNumber belongs to. |
| PersonId | yes | yes |  | yes |  | Gets or sets the PersonId of the Person that the PhoneNumber belongs to. This property is required. |
| PhoneNumberAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
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
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| NumberFormattedWithCountryCode | Gets the number formatted with country code. |
| NumberTypeValue | Gets or sets the Phone Number's NumberType DefinedValue |
| Person | Gets or sets the Person who the PhoneNumber belongs to. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| NumberTypeValue | [DefinedValue](defined-value.md) |  |
| NumberTypeValueId | [DefinedValue](defined-value.md) |  |
| Person | [Person](person.md) |  |
| PersonId | [Person](person.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
