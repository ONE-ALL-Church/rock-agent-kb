# Metric YTD Data Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Reporting`
- Model title: `MetricYTDData`
- Table name: `Metric`
- Obsolete: `no`
- Method signatures: `35`
- Obsolete methods: `4`
- EntityType GUID: `7c878afd-df74-4cdf-8491-31671559bd30`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 72 |
| Database-marked properties | 36 |
| Lava-marked properties | 57 |
| Lava-marked non-database properties | 21 |
| Related model links | 0 |
| Method signatures | 35 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdminPersonAlias |  | yes | yes |  |  | Gets or sets the admin person alias. |
| AdminPersonAliasId | yes | yes |  |  |  | Gets or sets the admin person alias identifier. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AutoPartitionOnPrimaryCampus | yes | yes |  |  |  | If set to true this feature will auto partition the individuals in the data view based on their primary campus. |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CumulativeValue | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DataView |  | yes | yes |  |  | Gets or sets the data view. |
| DataViewId | yes | yes |  |  |  | Gets or sets the data view identifier. |
| Description | yes | yes |  |  |  | Gets or sets a user defined description of the Metric. |
| EnableAnalytics | yes | yes |  |  |  | Gets or sets a value indicating whether [enable analytics]. If this is enabled, a SQL View named 'AnalyticsFactMetric{{Metric.Name}}' will be made available that can be used by Analytic tools, such as Power BI |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GoalValue | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsCumulative | yes | yes |  |  |  | Gets or sets a value indicating whether [is cumulative]. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Metric is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastRunDateTime | yes | yes |  |  |  | For SQL or DataView based Metrics, this is the DateTime that the MetricValues where scheduled to be updated according to Schedule |
| LastValue | yes | yes |  |  |  |  |
| LastValueDate | yes | yes |  |  |  |  |
| MeasurementClassificationValue |  | yes | yes |  |  | Gets or sets the measurement classification value. |
| MeasurementClassificationValueId | yes | yes |  |  |  | Gets or sets the measurement classification value identifier. |
| MetricAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| MetricCategories |  | yes | yes |  |  | Gets or sets the metric categories. |
| MetricChampionPersonAlias |  | yes | yes |  |  | Gets or sets the metric champion person alias. |
| MetricChampionPersonAliasId | yes | yes |  |  |  | Gets or sets the metric champion person alias identifier. |
| MetricPartitions |  | yes | yes |  |  | Gets or sets the metric partitions. |
| MetricValues |  | yes | yes |  |  | Gets or sets the metric values. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| NumericDataType | yes | yes |  |  |  | Gets or sets the type of the numeric data that the values represent. Although all values are stored as a decimal, specifying the type here allows entry screens to use appropriate controls/validation when entering values. This is a hard coded list of values defined in the code as an enumeration. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PreviousValue | yes | yes |  |  |  |  |
| PreviousValueDate | yes | yes |  |  |  |  |
| Schedule |  | yes | yes |  |  | Gets or sets the schedule. |
| ScheduleId | yes | yes |  |  |  | Gets or sets the schedule identifier. |
| SourceLava | yes | yes |  |  |  | Gets or sets the Lava code that returns the data for the Metric. |
| SourceSql | yes | yes |  |  |  | Gets or sets the SQL query that returns the data for the Metric. |
| SourceValueType |  | yes | yes |  |  | Gets or sets the type of the source value. |
| SourceValueTypeId | yes | yes |  |  |  | Gets or sets the source value type identifier. |
| Subtitle | yes | yes |  |  |  | Gets or sets the Subtitle of the Metric. |
| SupportedActions |  |  | yes |  |  |  |
| Title | yes | yes |  | yes |  | Gets or sets the Title of this Metric. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UnitType | yes | yes |  |  |  | Gets or sets the type of the unit. This is a hard coded list of values defined in the code as an enumeration. |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| XAxisLabel | yes | yes |  |  |  | Gets or sets the x axis label. Note that in Rock, graphs typically actually use the MetricValue.MetricValueDateTime as the graph's X Axis. Therefore, in most cases, Metric.XAxisLabel and MetricValue.XAxis are NOT used |
| YAxisLabel | yes | yes |  |  |  | Gets or sets the y axis label. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AdminPersonAlias | Gets or sets the admin person alias. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DataView | Gets or sets the data view. |
| EntityStringValue |  |
| IdKey |  |
| MeasurementClassificationValue | Gets or sets the measurement classification value. |
| MetricCategories | Gets or sets the metric categories. |
| MetricChampionPersonAlias | Gets or sets the metric champion person alias. |
| MetricPartitions | Gets or sets the metric partitions. |
| MetricValues | Gets or sets the metric values. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Schedule | Gets or sets the schedule. |
| SourceValueType | Gets or sets the type of the source value. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
