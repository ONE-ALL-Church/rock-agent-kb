# Data View Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Reporting`
- Model title: `DataView`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `45`
- Obsolete methods: `4`
- EntityType GUID: `57f8fa29-dcf1-4f74-8553-87e90f234139`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 60 |
| Database-marked properties | 28 |
| Lava-marked properties | 45 |
| Lava-marked non-database properties | 17 |
| Related model links | 9 |
| Method signatures | 45 |
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
| Category |  | yes | yes |  |  | Gets or sets the Category that this DataView belongs to |
| CategoryId | yes | yes |  |  |  | Gets or sets the CategoryId of the Category that this DataView belongs to. If there is no Category, this value will be null. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DataViewAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| DataViewFilter |  | yes | yes |  |  | Gets or sets the base Data View Filter that is used to generate this DataView. |
| DataViewFilterId | yes | yes |  |  |  | Gets or sets the DataViewFilterId of the root/base Data View Filter that is used to generate this DataView. |
| Description | yes | yes |  |  |  | Gets or sets the user defined description of the DataView |
| DisableUseOfReadOnlyContext | yes | yes |  |  |  | Gets or sets whether using a read-only Rock Context is disabled. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the Entity Type (Rock.Data.IEntity) that this DataView reports on. |
| EntityTypeId | yes | yes |  | yes |  | Gets or sets the EntityTypeId of the Entity Type (Rock.Data.IEntity) that this DataView reports on. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HighlightColor | yes | yes |  |  |  | Gets or sets the highlight color for the IconCssClass. |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class for entities returned by this DataView. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IncludeDeceased | yes | yes |  |  |  | Gets or sets a value indicating whether deceased should be included. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this DataView is part of the Rock core system/framework. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastRunDateTime | yes | yes |  |  |  | Gets or sets the last run date time. This is only updated when the data view is actually executed, not when we access the persisted values directly. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the DataView. |
| ParentAuthority |  |  | yes |  |  | Gets the parent security authority for the DataView which is its Category |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersistedLastRefreshDateTime | yes | yes |  |  |  | Gets or sets the persisted last refresh date time. |
| PersistedLastRunDurationMilliseconds | yes | yes |  |  |  | Gets or sets the persisted last run duration in milliseconds. |
| PersistedSchedule |  | yes | yes |  |  | Gets or sets the persisted Schedule that belongs to this DataView. |
| PersistedScheduleId | yes | yes |  |  |  | Gets or sets the Persisted Schedule Id. If this is null, then the DataView does not have a persisted schedule. |
| PersistedScheduleIntervalMinutes | yes | yes |  |  |  | Gets or sets the persisted schedule interval minutes. If this is null, then the DataView is not persisted. |
| RunCount | yes | yes |  |  |  | Gets or sets the run count. This is only updated when the data view is actually executed, not when we access the persisted values directly. |
| RunCountLastRefreshDateTime | yes | yes |  |  |  | Gets or sets the DateTime that the Run Count was last reset to 0. |
| SupportedActions |  |  | yes |  |  |  |
| TimeToRunDurationMilliseconds | yes | yes |  |  |  | Gets or sets the amount of time in milliseconds that it took to run the Data View. This is only updated when the data view is actually executed, not when we access the persisted values directly. |
| TransformEntityType |  | yes | yes |  |  | Gets or sets the entity type (MEF Component) used for an optional transformation |
| TransformEntityTypeId | yes | yes |  |  |  | Gets or sets the EntityTypeId of the Entity Type (MEF Component) that is used for an optional transformation on this DataView. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the Category that this DataView belongs to |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DataViewFilter | Gets or sets the base Data View Filter that is used to generate this DataView. |
| EntityStringValue |  |
| EntityType | Gets or sets the Entity Type (Rock.Data.IEntity) that this DataView reports on. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersistedSchedule | Gets or sets the persisted Schedule that belongs to this DataView. |
| TransformEntityType | Gets or sets the entity type (MEF Component) used for an optional transformation |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Category | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| CategoryId | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| DataViewFilter | [Data View Filter](data-view-filter.md) | 507e646b-9943-4dd6-8fb7-8ba9f95e6bd0 |
| DataViewFilterId | [Data View Filter](data-view-filter.md) | 507e646b-9943-4dd6-8fb7-8ba9f95e6bd0 |
| EntityType | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| EntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| PersistedSchedule | [Schedule](schedule.md) | 0b2c38a7-d79c-4f85-9757-f1b045d32c8a |
| TimeToRunDurationMilliseconds | [Data View](data-view.md) | 57f8fa29-dcf1-4f74-8553-87e90f234139 |
| TransformEntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
