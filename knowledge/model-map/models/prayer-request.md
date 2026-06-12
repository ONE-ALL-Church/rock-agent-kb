# Prayer Request Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Prayer`
- Model title: `PrayerRequest`
- EntityType GUID: `f13c8fd2-7702-4c79-a6a9-86440dd5de13`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 69 |
| Database-marked properties | 33 |
| Lava-marked properties | 51 |
| Lava-marked non-database properties | 18 |
| Related model links | 6 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowComments | yes | yes |  |  |  | Gets or sets a flag indicating whether or not comments can be made against the request. |
| Answer | yes | yes |  |  |  | Gets or sets a description of the way that God has answered the prayer. |
| ApprovedByPersonAlias |  | yes | yes |  |  | Gets or sets the approved by person alias. |
| ApprovedByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonId of the Person who approved this prayer request. |
| ApprovedOnDateTime | yes | yes |  |  |  | Gets or sets the date this prayer request was approved. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the campus. |
| CampusId | yes | yes |  |  |  | Gets or sets the campus identifier. |
| Category |  | yes | yes |  |  | Gets or sets the Category that this prayer request belongs to. |
| CategoryId | yes | yes |  |  |  | Gets or sets the CategoryId of the Category that the PrayerRequest belongs to. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Email | yes | yes |  |  |  | Gets or sets the email address of the person requesting prayer. |
| EncryptedKey |  |  | yes |  |  |  |
| EnteredDateTime | yes | yes |  |  |  | Gets or sets the date that this prayer request was entered. |
| EntityStringValue |  | yes | yes |  |  |  |
| ExpirationDate | yes | yes |  |  |  | Gets or sets the date that the prayer request expires. |
| FirstName | yes | yes |  | yes |  | Gets or sets the First Name of the person that this prayer request is about. This property is required. |
| FlagCount | yes | yes |  |  |  | Gets or sets the number of times this request has been flagged. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FullName |  |  | yes |  |  | Gets full name of the person for who the prayer request is about. |
| FullNameReversed |  |  | yes |  |  | Gets the full name of the person who this prayer request is about in Last Name, First Name format. |
| Group |  | yes | yes |  |  | TODO: GET CONFIRMATION AND DOCUMENT -CSF Gets or sets the group. |
| GroupId | yes | yes |  |  |  | TODO: GET CLARIFICATION AND DOCUMENT Gets or sets the group id. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if this prayer request is active. |
| IsApproved | yes | yes |  |  |  | Gets or sets a flag indicating if the prayer request has been approved. |
| IsPublic | yes | yes |  |  |  | Gets or sets the flag indicating whether or not the request is public. |
| IsUrgent | yes | yes |  |  |  | Gets or sets a flag indicating if this is an urgent prayer request. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LanguageValue |  | yes | yes |  |  | Gets or sets the Language DefinedValue for this prayer request. |
| LanguageValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the DefinedValue that represents the Language for this prayer request. |
| LastName | yes | yes |  |  |  | Gets or sets the Last Name of the person that this prayer request is about. This property is required. |
| ModerationFlags | yes | yes |  |  |  | Gets or sets the bitmask of moderation flags for the PrayerRequest. This is a hard coded list of values defined in the code as an enumeration. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name |  |  | yes |  |  | Gets the name of the prayer request. The format for this is the EnteredDate - FullName. This is required to implement ICategorized |
| OriginalRequest | yes | yes |  |  |  | Gets or sets the Original Text of the PrayerRequest. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PrayerCount | yes | yes |  |  |  | Gets or sets the number of times that this prayer request has been prayed for. |
| PrayerRequestAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| RequestedByPersonAlias |  | yes | yes |  |  | Gets or sets the requested by person alias. |
| RequestedByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonId of the Person who is submitting the PrayerRequest |
| SentimentEmotionValueId | yes | yes |  |  |  | Gets or sets the identified emotional sentiment DefinedValueId (if any). |
| SupportedActions |  |  | yes |  |  |  |
| Text | yes | yes |  | yes |  | Gets or sets the text/content of the request. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ApprovedByPersonAlias | Gets or sets the approved by person alias. |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the campus. |
| Category | Gets or sets the Category that this prayer request belongs to. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| Group | TODO: GET CONFIRMATION AND DOCUMENT -CSF Gets or sets the group. |
| IdKey |  |
| LanguageValue | Gets or sets the Language DefinedValue for this prayer request. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RequestedByPersonAlias | Gets or sets the requested by person alias. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ApprovedByPersonAliasId | [Person](person.md) |  |
| Category | [Category](category.md) |  |
| CategoryId | [Category](category.md) |  |
| LanguageValue | [DefinedValue](defined-value.md) |  |
| LanguageValueId | [DefinedValue](defined-value.md) |  |
| RequestedByPersonAliasId | [Person](person.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
