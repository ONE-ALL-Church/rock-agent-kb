# Web Farm Node Metric Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `WebFarm`
- Model title: `WebFarmNodeMetric`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `3194a5e3-f352-4cd0-a585-f1dd37008b9c`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 43 |
| Database-marked properties | 15 |
| Lava-marked properties | 28 |
| Lava-marked non-database properties | 13 |
| Related model links | 2 |
| Method signatures | 34 |
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
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
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
| MetricType | yes | yes |  | yes |  | Gets or sets the type of the metric. This is a hard coded list of values defined in the code as an enumeration. |
| MetricValue | yes | yes |  | yes |  | Gets or sets the metric value. |
| MetricValueDateKey | yes | yes |  |  |  | Gets the metric value date key. |
| MetricValueDateTime | yes | yes |  |  |  | Gets or sets the metric value date time. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Note | yes | yes |  |  |  | Gets or sets the note. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WebFarmNode |  | yes | yes |  |  | Gets or sets the Web Farm Node. |
| WebFarmNodeId | yes | yes |  | yes |  | Gets or sets the Web Farm Node identifier. |
| WebFarmNodeMetricAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
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
| WebFarmNode | Gets or sets the Web Farm Node. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| WebFarmNode | [Web Farm Node](web-farm-node.md) | 2338d5c3-e808-408f-b000-e8a7d8a4858c |
| WebFarmNodeId | [Web Farm Node](web-farm-node.md) | 2338d5c3-e808-408f-b000-e8a7d8a4858c |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
