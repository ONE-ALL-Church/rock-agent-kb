# Campus Schedule Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Core`
- Model title: `CampusSchedule`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `134b8879-cd7c-4872-8065-882aa3721c2d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 43 |
| Database-marked properties | 13 |
| Lava-marked properties | 28 |
| Lava-marked non-database properties | 15 |
| Related model links | 7 |
| Method signatures | 36 |
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
| Campus |  | yes | yes |  |  | Gets or sets the Campus that is associated with this CampusSchedule. |
| CampusId | yes | yes |  |  |  | Gets or sets the Id of the Campus that is associated with this CampusSchedule. This property is required. |
| CampusScheduleAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Order | yes | yes |  | yes |  | Gets or sets the display order of the CampusSchedule in the campus schedule list. The lower the number the higher the display priority this CampusSchedule has. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Schedule |  | yes | yes |  |  | Gets or sets the Schedule that is associated with this CampusSchedule. |
| ScheduleId | yes | yes |  |  |  | Gets or sets the Id of the Schedule that is associated with this CampusSchedule. This property is required. |
| ScheduleTypeValue |  | yes | yes |  |  | Gets or sets the Schedule Type Defined Value of this CampusSchedule. |
| ScheduleTypeValueId | yes | yes |  |  |  | The Id of the ScheduleType Defined Value that is used to identify the type of Campus Schedule that this is. This property is required. These are found in the Schedule Type Defined Type. |
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
| Campus | Gets or sets the Campus that is associated with this CampusSchedule. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Schedule | Gets or sets the Schedule that is associated with this CampusSchedule. |
| ScheduleTypeValue | Gets or sets the Schedule Type Defined Value of this CampusSchedule. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Campus | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| CampusId | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| Schedule | [Schedule](schedule.md) | 0b2c38a7-d79c-4f85-9757-f1b045d32c8a |
| ScheduleId | [Schedule](schedule.md) | 0b2c38a7-d79c-4f85-9757-f1b045d32c8a |
| ScheduleTypeValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| ScheduleTypeValueId | [Campus Schedule](campus-schedule.md) | 134b8879-cd7c-4872-8065-882aa3721c2d |
| ScheduleTypeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
