# Content Collection Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `CMS`
- Model title: `ContentCollection`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `ad7b9219-1b47-4164-9dd1-90f0af588cb8`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 21 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 13 |
| Related model links | 1 |
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
| CollectionKey | yes | yes |  |  |  | Gets or sets the collection key. |
| ContentCollectionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ContentCollectionSources |  | yes | yes |  |  | Gets or sets the content collection sources. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description. |
| EnableRequestFilters | yes | yes |  |  |  | Gets or sets a value indicating whether personalization request filters should be enabled. |
| EnableSegments | yes | yes |  |  |  | Gets or sets a value indicating whether personalization segments should be enabled. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FilterSettings | yes | yes |  |  |  | Gets or sets the filter settings. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastIndexDateTime | yes | yes |  |  |  | Gets or sets the last index date time. |
| LastIndexItemCount | yes | yes |  |  |  | Gets or sets the last index item count. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the Content Collection. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SupportedActions |  |  | yes |  |  |  |
| TrendingEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether trending is enabled for this content collection. |
| TrendingGravity | yes | yes |  | yes |  | Gets or sets the trending gravity to apply more weight to items that are newer. |
| TrendingMaxItems | yes | yes |  | yes |  | Gets or sets the trending max items. |
| TrendingWindowDay | yes | yes |  | yes |  | Gets or sets the trending window day. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| ContentCollectionSources | Gets or sets the content collection sources. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
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
| Name | [Content Collection](content-collection.md) | ad7b9219-1b47-4164-9dd1-90f0af588cb8 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
