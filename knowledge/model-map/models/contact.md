# Contact Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Engagement`
- Model title: `Contact`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `a2fbb846-2511-4760-b912-928775bfc6d6`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 69 |
| Database-marked properties | 40 |
| Lava-marked properties | 54 |
| Lava-marked non-database properties | 14 |
| Related model links | 2 |
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
| BaptismDay | yes | yes |  |  |  | Gets or sets the baptism day. |
| BaptismMonth | yes | yes |  |  |  | Gets or sets the baptism month. |
| BaptismYear | yes | yes |  |  |  | Gets or sets the baptism year. |
| BirthDay | yes | yes |  |  |  | Gets ro sets the birth day. |
| BirthMonth | yes | yes |  |  |  | Gets or sets the birth month. |
| BirthYear | yes | yes |  |  |  | Gets or sets the birth year of the individual. |
| ConnectionCadence | yes | yes |  |  |  | Gets or sets the connection cadence. This is a hard coded list of values defined in the code as an enumeration. |
| ContactAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ContactNote | yes | yes |  |  |  | Gets or sets the prayer note. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Email | yes | yes |  |  |  | Gets or sets the email. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FacebookProfileUrl | yes | yes |  |  |  | Gets or sets the Facebook profile URL. |
| FirstName | yes | yes |  |  |  | Gets or sets the last name. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Gender | yes | yes |  |  |  | Gets or sets the gender. This is a hard coded list of values defined in the code as an enumeration. |
| Guid | yes | yes |  |  |  |  |
| HasAcceptedJesus | yes | yes |  |  |  | Gets or sets a value indicating whether this contact has accepted Jesus as their personal savior. |
| HasBeenBaptized | yes | yes |  |  |  | Gets or sets a value indicating whether this contact has been baptized. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InstagramProfileUrl | yes | yes |  |  |  | Gets or sets the Instagram profile URL. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastName | yes | yes |  |  |  | Gets or sets the last name. |
| LinkedInProfileUrl | yes | yes |  |  |  | Gets or sets the LinkedIn profile URL. |
| MobilePhone | yes | yes |  |  |  | Gets or sets the phone number. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| OwnerPersonAlias |  | yes | yes |  |  | Gets or sets the owner Person Alias. |
| OwnerPersonAliasId | yes | yes |  |  |  | Gets or sets the owner person alias identifier. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Photo |  | yes | yes |  |  | Gets or sets the photo Binary File. |
| PhotoId | yes | yes |  |  |  | Gets or sets the photo identifier. |
| PrayerCadence | yes | yes |  |  |  | Gets or sets the prayer cadence. This is a hard coded list of values defined in the code as an enumeration. |
| RelationshipFocus | yes | yes |  |  |  | Gets or sets the relationship focus. This is a hard coded list of values defined in the code as an enumeration. |
| RelationshipStrength | yes | yes |  |  |  | Gets or sets the relationship strength. This is a hard coded list of values defined in the code as an enumeration. |
| SalvationDay | yes | yes |  |  |  | Gets or sets the day of the salvation day. |
| SalvationMonth | yes | yes |  |  |  | Gets or sets the month of the salvation month. |
| SalvationYear | yes | yes |  |  |  | Gets or sets the year of the salvation year. |
| SupportedActions |  |  | yes |  |  |  |
| TikTokProfileUrl | yes | yes |  |  |  | Gets or sets the TikTok profile URL. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WeddingDay | yes | yes |  |  |  | Gets or sets the wedding Day. |
| WeddingMonth | yes | yes |  |  |  | Gets or sets the wedding month. |
| WeddingYear | yes | yes |  |  |  | Gets or sets the wedding year. |
| XProfileUrl | yes | yes |  |  |  | Gets or sets the X (formerly Twitter) profile URL. |

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
| OwnerPersonAlias | Gets or sets the owner Person Alias. |
| Photo | Gets or sets the photo Binary File. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| OwnerPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| Photo | [Binary File](binary-file.md) | 9bb1a349-5998-47c1-97d5-d6cc00275662 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
