# Report Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Reporting`
- Model title: `Report`
- EntityType GUID: `f1f22d3e-fefa-4c84-9ffa-9e8ace60fce7`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 51 |
| Database-marked properties | 20 |
| Lava-marked properties | 36 |
| Lava-marked non-database properties | 16 |
| Related model links | 6 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Category |  | yes | yes |  |  | Gets or sets the Category that this Report belongs to. |
| CategoryId | yes | yes |  |  |  | Gets or sets the CategoryId of the Category that the Report belongs to. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DataView |  | yes | yes |  |  | Gets or sets the base/root DataView that this Report is based on. |
| DataViewId | yes | yes |  |  |  | Gets or the DataViewId of the root DataView that this Report is based on. |
| Description | yes | yes |  |  |  | Gets or sets the Report's Description. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the EntityType that is being reported on. |
| EntityTypeId | yes | yes |  |  |  | Gets or sets the EntityTypeId of the EntityType that is being reported on. |
| FetchTop | yes | yes |  |  |  | Gets or sets the number of records to fetch in the report. Null means all records. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Report is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastRunDateTime | yes | yes |  |  |  | Gets or sets the last run date time. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the Report. This property is required. |
| ParentAuthority |  |  | yes |  |  | Gets the parent security authority for the Report which is its Category |
| ParentAuthorityPre |  |  | yes |  |  |  |
| QueryHint | yes | yes |  |  |  | Gets or sets the query hint that is included in the SQL that is executed on the database server |
| ReportAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ReportFields |  | yes | yes |  |  | Gets or sets the report fields. |
| RunCount | yes | yes |  |  |  | Gets or sets the persisted last run duration in mulliseconds. |
| SupportedActions |  |  | yes |  |  |  |
| TimeToRunDurationMilliseconds | yes | yes |  |  |  | The amount of time in milliseconds that it took to run the DataView |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the Category that this Report belongs to. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DataView | Gets or sets the base/root DataView that this Report is based on. |
| EntityStringValue |  |
| EntityType | Gets or sets the EntityType that is being reported on. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ReportFields | Gets or sets the report fields. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Category | [Category](category.md) |  |
| CategoryId | [Category](category.md) |  |
| DataView | [DataView](data-view.md) |  |
| DataViewId | [DataView](data-view.md) |  |
| EntityType | [EntityType](entity-type.md) |  |
| EntityTypeId | [EntityType](entity-type.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
