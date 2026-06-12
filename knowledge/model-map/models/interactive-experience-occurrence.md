# Interactive Experience Occurrence Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Event`
- Model title: `InteractiveExperienceOccurrence`
- EntityType GUID: `2d1263a1-a3e7-4568-aa4b-c1234824188d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 46 |
| Database-marked properties | 16 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 15 |
| Related model links | 7 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the Campus that is associated with this Interactive Experience Occurrence. |
| CampusId | yes | yes |  |  |  | Gets or sets the Id of the Campus that is associated with this Interactive Experience Occurrence. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CurrentlyShownAction |  | yes | yes |  |  | Gets or sets the InteractiveExperienceAction that is currently being displayed. |
| CurrentlyShownActionId | yes | yes |  |  |  | Gets or sets the InteractiveExperienceAction identifier that is currently being displayed. |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InteractiveExperienceOccurrenceAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| InteractiveExperienceSchedule |  | yes | yes |  |  | Gets or sets the InteractiveExperienceSchedule that the InteractiveExperienceOccurrence belongs to. |
| InteractiveExperienceScheduleId | yes | yes |  | yes |  | Gets or sets the Id of the InteractiveExperienceSchedule that this InteractiveExperienceOccurrence is associated with. This property is required. |
| IsOccurrenceActive | yes |  |  |  |  | Gets a value indicating whether this occurrence is active right now. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| OccurrenceDateKey | yes | yes |  |  |  | Gets the occurrence date key used for indexing. Only the date portion of OccurrenceDateTime is used when calculating this. |
| OccurrenceDateTime | yes | yes |  |  |  | Gets or sets the DateTime for when this occurrence started. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| StateJson | yes | yes |  |  |  | Gets or sets the state json. This is used to store general state information about this occurrence that will be defined later. |
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
| Campus | Gets or sets the Campus that is associated with this Interactive Experience Occurrence. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| CurrentlyShownAction | Gets or sets the InteractiveExperienceAction that is currently being displayed. |
| EntityStringValue |  |
| IdKey |  |
| InteractiveExperienceSchedule | Gets or sets the InteractiveExperienceSchedule that the InteractiveExperienceOccurrence belongs to. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Campus | [Campus](campus.md) |  |
| CampusId | [Campus](campus.md) |  |
| CurrentlyShownAction | [InteractiveExperienceAction](interactive-experience-action.md) |  |
| CurrentlyShownActionId | [InteractiveExperienceAction](interactive-experience-action.md) |  |
| InteractiveExperienceSchedule | [InteractiveExperienceSchedule](interactive-experience-schedule.md) |  |
| InteractiveExperienceScheduleId | [InteractiveExperienceSchedule](interactive-experience-schedule.md) |  |
| OccurrenceDateTime | DateTime |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | OccurrenceDateTime | related_entity_links |
