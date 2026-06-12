# Persisted Dataset Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `CMS`
- Model title: `PersistedDataset`
- EntityType GUID: `9c3064c0-cf9c-4549-9a80-022514b7ff83`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 38 |
| Database-marked properties | 24 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 6 |
| Related model links | 2 |
| Pre-alpha changes touching this model | 22 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AccessKey | yes | yes |  |  |  | Gets or sets the unique key to use to access this persisted dataset. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowManualRefresh | yes | yes |  |  |  | Gets or sets a value indicating whether [allow manual refresh]. |
| AvailableKeys |  |  | yes |  |  |  |
| BuildScript | yes | yes |  |  |  | Gets or sets the build script. See BuildScriptType. |
| BuildScriptType | yes | yes |  |  |  | Gets or sets the type of the build script. This is a hard coded list of values defined in the code as an enumeration. |
| ContextKey |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a user defined description of the PersistedDataset. |
| EnabledLavaCommands | yes | yes |  |  |  | Gets or sets a comma-delimited list of enabled LavaCommands. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the type of the entity. |
| EntityTypeId | yes | yes |  |  |  | Gets or sets the Id of the EntityTypeCache (EntityType) that this PersistedDataset is used for. |
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
| Name | yes | yes |  | yes |  | Gets or sets the Name of the PersistedDataset. |
| PersistedSchedule |  |  | yes |  |  | Gets or sets the schedule associated with this PersistedDataset. |
| PersistedScheduleId | yes | yes |  |  |  | Gets or sets the ID of the schedule for this PersistedDataset. |
| PersistedScheduleIntervalMinutes | yes | yes |  |  |  | Gets or sets the persisted schedule interval minutes. If this is null, then the DataView is not persisted. |
| RefreshIntervalMinutes | yes | yes |  |  |  | Gets or sets the refresh interval minutes. |
| ResultData | yes | yes |  |  |  | Gets or sets the serialized data of the dataset. See ResultFormat. |
| ResultFormat | yes | yes |  |  |  | Gets or sets the result format. This is a hard coded list of values defined in the code as an enumeration. |
| TimeToBuildMS | yes | yes |  |  |  | The amount of time that it took to persist the ResultData. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| EntityType | Gets or sets the type of the entity. |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| EntityTypeId | [EntityType](entity-type.md) |  |
| EntityTypeId | EntityTypeCache |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | Attributes |  |
| property_added | AttributeValueDefaults |  |
| property_added | AttributeValues |  |
| property_added | CreatedByPersonAlias |  |
| property_added | CreatedByPersonAliasId |  |
| property_added | CreatedByPersonId |  |
| property_added | CreatedByPersonName |  |
| property_added | CreatedDateTime |  |
| property_added | CustomSortValue |  |
| property_added | ModifiedAuditValuesAlreadyUpdated |  |
| property_added | ModifiedByPersonAlias |  |
| property_added | ModifiedByPersonAliasId |  |
| property_added | ModifiedByPersonId |  |
| property_added | ModifiedByPersonName |  |
| property_added | ModifiedDateTime |  |
| property_added | ParentAuthority |  |
| property_added | ParentAuthorityPre |  |
| property_added | PersistedDatasetAttributeValues |  |
| property_added | SupportedActions |  |
| property_changed | EntityTypeId | related_entity_links |
| property_changed | PersistedScheduleIntervalMinutes | description |
| property_changed | RefreshIntervalMinutes | is_obsolete |
