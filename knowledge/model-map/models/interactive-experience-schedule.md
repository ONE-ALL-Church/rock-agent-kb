# Interactive Experience Schedule Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Event`
- Model title: `InteractiveExperienceSchedule`
- EntityType GUID: `d23b4dcf-545a-490f-aead-ba78a8fb4028`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 47 |
| Database-marked properties | 14 |
| Lava-marked properties | 32 |
| Lava-marked non-database properties | 18 |
| Related model links | 10 |
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
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DataView |  | yes | yes |  |  | Gets or sets the DataView. |
| DataViewId | yes | yes |  |  |  | Gets or sets the DataView identifier. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Group. |
| GroupId | yes | yes |  |  |  | Gets or sets the Group identifier. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InteractiveExperience |  | yes | yes |  |  | Gets or sets the InteractiveExperience that the InteractiveExperienceSchedule belongs to. |
| InteractiveExperienceId | yes | yes |  | yes |  | Gets or sets the Id of the InteractiveExperience that this InteractiveExperienceSchedule is associated with. This property is required. |
| InteractiveExperienceOccurrences |  | yes | yes |  |  | Gets or sets the occurrences for this Interactive Experience Schedule. |
| InteractiveExperienceScheduleAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| InteractiveExperienceScheduleCampuses |  | yes | yes |  |  | Gets or sets the InteractiveExperienceScheduleCampuses for this Interactive Experience Schedule. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Schedule |  | yes | yes |  |  | Gets or sets the Schedule that is associated with this Interactive Experience. |
| ScheduleId | yes | yes |  | yes |  | Gets or sets the Id of the Schedule that is associated with this Interactive Experience. This property is required. |
| ScheduleSettingsJson | yes | yes |  |  |  | Gets or sets the JSON representing the additional settings. |
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
| DataView | Gets or sets the DataView. |
| EntityStringValue |  |
| Group | Gets or sets the Group. |
| IdKey |  |
| InteractiveExperience | Gets or sets the InteractiveExperience that the InteractiveExperienceSchedule belongs to. |
| InteractiveExperienceOccurrences | Gets or sets the occurrences for this Interactive Experience Schedule. |
| InteractiveExperienceScheduleCampuses | Gets or sets the InteractiveExperienceScheduleCampuses for this Interactive Experience Schedule. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Schedule | Gets or sets the Schedule that is associated with this Interactive Experience. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| DataView | [DataView](data-view.md) |  |
| DataViewId | [DataView](data-view.md) |  |
| Group | [Group](group.md) |  |
| GroupId | [Group](group.md) |  |
| InteractiveExperience | [InteractiveExperience](interactive-experience.md) |  |
| InteractiveExperienceId | [InteractiveExperience](interactive-experience.md) |  |
| InteractiveExperienceOccurrences | occurrences |  |
| InteractiveExperienceScheduleCampuses | InteractiveExperienceScheduleCampuses |  |
| Schedule | [Schedule](schedule.md) |  |
| ScheduleId | [Schedule](schedule.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
