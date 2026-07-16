# Personalization Segment Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `CMS`
- Model title: `PersonalizationSegment`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `368a3581-c8c4-4960-901a-9587864226f3`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 52 |
| Database-marked properties | 21 |
| Lava-marked properties | 36 |
| Lava-marked non-database properties | 15 |
| Related model links | 2 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalFilterConfiguration |  |  | yes |  |  | Configuration for the Additional Segment Filters |
| AdditionalFilterJson | yes | yes |  |  |  | Gets or sets the additional filter json. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Categories |  | yes | yes |  |  | Gets or sets the collection of Categories that this Personalization Segment is associated with. NOTE: Since changes to Categories isn't tracked by ChangeTracker, set the ModifiedDateTime if Categories are modified. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description of the segment. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FilterDataView |  | yes | yes |  |  | Gets or sets the filter data view. |
| FilterDataViewId | yes | yes |  |  |  | Gets or sets the filter data view identifier. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is active. |
| IsDirty | yes | yes |  |  |  | Gets or sets a value indicating whether the Personalization Segment values is considered dirty. If it is dirty then it should be assumed that a calculation is being run on it is yet to be completed. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the name. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersistedLastRefreshDateTime | yes | yes |  |  |  | Gets or sets the last refresh datetime for persistence. |
| PersistedLastRunDurationMilliseconds | yes | yes |  |  |  | Gets or sets the last run duration in milliseconds for persistence. |
| PersistedSchedule |  | yes | yes |  |  | Gets or sets the persisted schedule. |
| PersistedScheduleId | yes | yes |  |  |  | Gets or sets the schedule id for persistence. |
| PersistedScheduleIntervalMinutes | yes | yes |  |  |  | Gets or sets the interval in minutes for persistence. |
| PersonalizationSegmentAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| SegmentKey | yes | yes |  |  |  | Gets or sets the segment key. |
| SupportedActions |  |  | yes |  |  |  |
| TimeToUpdateDurationMilliseconds | yes | yes |  |  |  | Gets or sets the duration in milliseconds it takes to update the segment. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Categories | Gets or sets the collection of Categories that this Personalization Segment is associated with. NOTE: Since changes to Categories isn't tracked by ChangeTracker, set the ModifiedDateTime if Categories are modified. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| FilterDataView | Gets or sets the filter data view. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersistedSchedule | Gets or sets the persisted schedule. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Categories | Categories | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| Categories | [Personalization Segment](personalization-segment.md) | 368a3581-c8c4-4960-901a-9587864226f3 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
