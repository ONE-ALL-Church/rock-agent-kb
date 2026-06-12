# Streak Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Engagement`
- Model title: `Streak`
- EntityType GUID: `d953b0a5-0065-4624-8844-10010de01e5c`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 53 |
| Database-marked properties | 22 |
| Lava-marked properties | 38 |
| Lava-marked non-database properties | 16 |
| Related model links | 8 |
| Pre-alpha changes touching this model | 2 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
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
| CurrentStreakCount | yes | yes |  |  |  | The current number of non excluded occurrences attended in a row |
| CurrentStreakStartDate | yes | yes |  |  |  | The date that the current streak began |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EngagementCount | yes | yes |  |  |  | The number of engagements on occurrences |
| EngagementMap | yes | yes |  |  |  | The sequence of bits that represent engagement. The least significant bit (right side) is representative of the StreakType's StartDate. More significant bits (going left) are more recent dates. |
| EnrollmentDate | yes | yes |  | yes |  | Gets or sets the DateTime when the person was enrolled in the streak type. This is not the Streak Type start date. |
| EntityStringValue |  | yes | yes |  |  |  |
| ExclusionMap | yes | yes |  |  |  | The sequence of bits that represent exclusions exclusive to this streak. The least significant bit (right side) is representative of the StreakType's StartDate. More significant bits (going left) are more recent dates. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InactiveDateTime | yes | yes |  |  |  | Gets or sets the DateTime when the person deactivated their Streak. If null, the Streak is active. |
| IsActive |  | yes | yes |  |  | Gets or sets the IsActive. |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. |
| Item |  |  | yes |  |  |  |
| Location |  | yes | yes |  |  | Gets or sets the Location. |
| LocationId | yes | yes |  |  |  | Gets or sets the Location identifier by which the person's exclusions will be sourced. |
| LongestStreakCount | yes | yes |  |  |  | The longest number of non excluded occurrences attended in a row |
| LongestStreakEndDate | yes | yes |  |  |  | The date the longest streak ended |
| LongestStreakStartDate | yes | yes |  |  |  | The date the longest streak began |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias. |
| PersonAliasId | yes | yes |  | yes |  | Gets or sets the PersonAlias identifier. |
| StreakAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| StreakType |  | yes | yes |  |  | Gets or sets the StreakType. |
| StreakTypeId | yes | yes |  | yes |  | Gets or sets the Id of the StreakType to which this Streak belongs. This property is required. |
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
| IsActive | Gets or sets the IsActive. |
| Location | Gets or sets the Location. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the PersonAlias. |
| StreakType | Gets or sets the StreakType. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| EnrollmentDate | DateTime |  |
| InactiveDateTime | DateTime |  |
| Location | [Location](location.md) |  |
| LocationId | [Location](location.md) |  |
| PersonAlias | [PersonAlias](person-alias.md) |  |
| PersonAliasId | [PersonAlias](person-alias.md) |  |
| StreakType | [StreakType](streak-type.md) |  |
| StreakTypeId | [StreakType](streak-type.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | EnrollmentDate | related_entity_links |
| property_changed | InactiveDateTime | related_entity_links |
