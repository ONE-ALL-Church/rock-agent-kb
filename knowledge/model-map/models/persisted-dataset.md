# Persisted Dataset Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `CMS`
- Model title: `PersistedDataset`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `37`
- Obsolete methods: `4`
- EntityType GUID: `9c3064c0-cf9c-4549-9a80-022514b7ff83`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 57 |
| Database-marked properties | 28 |
| Lava-marked properties | 41 |
| Lava-marked non-database properties | 13 |
| Related model links | 1 |
| Method signatures | 37 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AccessKey | yes | yes |  |  |  | Gets or sets the unique key to use to access this persisted dataset. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowManualRefresh | yes | yes |  |  |  | Gets or sets a value indicating whether [allow manual refresh]. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BuildScript | yes | yes |  |  |  | Gets or sets the build script. See BuildScriptType. |
| BuildScriptType | yes | yes |  |  |  | Gets or sets the type of the build script. This is a hard coded list of values defined in the code as an enumeration. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a user defined description of the PersistedDataset. |
| EnabledLavaCommands | yes | yes |  |  |  | Gets or sets a comma-delimited list of enabled LavaCommands. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the type of the entity. |
| EntityTypeId | yes | yes |  |  |  | Gets or sets the Id of the EntityTypeCache (Entity Type) that this PersistedDataset is used for. |
| ExpireDateTime | yes | yes |  |  |  | The DateTime when to stop updating the ResultData. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  | yes |  | Gets or sets a value indicating whether this instance is active. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating that this PersistedDataset is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastRefreshDateTime | yes | yes |  |  |  | Gets or sets the persisted last refresh date time. |
| MemoryCacheDurationMS | yes | yes |  |  |  | Gets or sets the memory cache duration ms. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the PersistedDataset. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersistedDatasetAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| PersistedSchedule |  |  | yes |  |  | Gets or sets the schedule associated with this PersistedDataset. |
| PersistedScheduleId | yes | yes |  |  |  | Gets or sets the ID of the schedule for this PersistedDataset. |
| PersistedScheduleIntervalMinutes | yes | yes |  |  |  | Gets or sets the persisted schedule interval minutes. If this is null, then the DataView is not persisted by an interval but it might be persisted by a PersistedSchedule. |
| RefreshIntervalMinutes | yes | yes |  |  | yes | Gets or sets the refresh interval minutes. |
| ResultData | yes | yes |  |  |  | Gets or sets the serialized data of the dataset. See ResultFormat. |
| ResultFormat | yes | yes |  |  |  | Gets or sets the result format. This is a hard coded list of values defined in the code as an enumeration. |
| SupportedActions |  |  | yes |  |  |  |
| TimeToBuildMS | yes | yes |  |  |  | The amount of time that it took to persist the ResultData. |
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
| EntityType | Gets or sets the type of the entity. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| EntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | Status |  |
