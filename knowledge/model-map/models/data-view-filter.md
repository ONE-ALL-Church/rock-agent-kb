# Data View Filter Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Reporting`
- Model title: `DataViewFilter`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `40`
- Obsolete methods: `4`
- EntityType GUID: `507e646b-9943-4dd6-8fb7-8ba9f95e6bd0`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 48 |
| Database-marked properties | 15 |
| Lava-marked properties | 31 |
| Lava-marked non-database properties | 16 |
| Related model links | 1 |
| Method signatures | 40 |
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
| ChildFilters |  | yes | yes |  |  | Gets or sets the child DataViewFilters. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DataView |  |  | yes |  |  | Gets or sets the data view that owns this record. |
| DataViewFilterAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| DataViewId | yes | yes |  |  |  | Gets or sets the id of the Data View that owns this record. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the EntityType of the DataFilterComponent that this filter is using. |
| EntityTypeId | yes | yes |  |  |  | Gets or sets the EntityTypeId of the DataFilterComponent that this filter is using. |
| Expanded |  | yes | yes |  |  | Gets or sets a value indicating whether this Data View Filter is currently expanded. This property is only used by the DataView ui to track which filters are currently expanded |
| ExpressionType | yes | yes |  |  |  | Gets or sets the expression type of this DataViewFilter. This is a hard coded list of values defined in the code as an enumeration. |
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
| Parent |  | yes | yes |  |  | Gets or sets sets the parent DataViewFilter. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ParentId | yes | yes |  |  |  | Gets or sets the DataViewFilterId of the parent DataViewFilter. |
| RelatedDataView |  |  | yes |  |  | Gets or sets the data view that this record uses to filter. |
| RelatedDataViewId | yes | yes |  |  |  | Gets or sets the id of the data view that this record uses for filtering. |
| Selection | yes | yes |  |  |  | Gets or sets the value that the DataViewFilter is filtering by. |
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
| ChildFilters | Gets or sets the child DataViewFilters. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the EntityType of the DataFilterComponent that this filter is using. |
| Expanded | Gets or sets a value indicating whether this Data View Filter is currently expanded. This property is only used by the DataView ui to track which filters are currently expanded |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Parent | Gets or sets sets the parent DataViewFilter. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Expanded | [Data View Filter](data-view-filter.md) | 507e646b-9943-4dd6-8fb7-8ba9f95e6bd0 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
