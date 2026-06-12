# Metric Value Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Reporting`
- Model title: `MetricValue`
- EntityType GUID: `dd0e6f39-3e07-44d0-be7b-b1ab75afed2d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 18 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 16 |
| Related model links | 0 |
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
| DateTimeStamp | yes | yes |  |  |  | Gets the metric value datetime as a javascript time stamp (handy for chart apis) |
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
| Metric |  | yes | yes |  |  | Gets or sets the metric. |
| MetricId | yes | yes |  | yes |  | Gets or sets the MetricId. |
| MetricValueAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| MetricValueDateKey | yes | yes |  |  |  | Gets the metric value date key. |
| MetricValueDateTime | yes | yes |  |  |  | Gets or sets the metric value date time. |
| MetricValuePartitionEntityIds |  | yes | yes |  |  | Gets the metric value partitions as a comma-delimited list of EntityTypeId\|EntityId |
| MetricValuePartitions |  | yes | yes |  |  | Gets or sets the metric value partitions. |
| MetricValueSourceDate |  | yes | yes |  |  | Gets or sets the metric value source date. |
| MetricValueType | yes | yes |  |  |  | Gets or sets the type of the metric value. This is a hard coded list of values defined in the code as an enumeration. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Note | yes | yes |  |  |  | Gets or sets the note. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SeriesName | yes | yes |  |  |  | Gets or sets the name of the series. This will be the default name of the series if MetricValuePartitionEntityIds can't be resolved |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| XValue | yes | yes |  |  |  | Gets or sets the X axis value. Note that in Rock, graphs typically actually use the MetricValue.MetricValueDateTime as the graph's X Axis. Therefore, in most cases, Metric.XAxisLabel and MetricValue.XAxis are NOT used |
| YValue | yes | yes |  |  |  | Gets or sets the Y axis value. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| Metric | Gets or sets the metric. |
| MetricValuePartitionEntityIds | Gets the metric value partitions as a comma-delimited list of EntityTypeId\|EntityId |
| MetricValuePartitions | Gets or sets the metric value partitions. |
| MetricValueSourceDate | Gets or sets the metric value source date. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
