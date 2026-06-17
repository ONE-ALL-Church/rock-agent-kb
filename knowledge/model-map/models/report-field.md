# Report Field Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Reporting`
- Model title: `ReportField`
- EntityType GUID: `6b541baa-44b7-48ba-937a-543866905689`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 20 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 14 |
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
| ColumnHeaderText | yes | yes |  |  |  | Gets or sets the column header text. |
| ColumnOrder | yes | yes |  |  |  | Gets or sets the column order of this field |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DataSelectComponentEntityType |  | yes | yes |  |  | Gets or sets the EntityType of the DataSelectComponent that this report field is using. |
| DataSelectComponentEntityTypeId | yes | yes |  |  |  | Gets or sets the EntityTypeId of the DataSelectComponent that this report field is using. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsCommunicationMergeField | yes | yes |  |  |  | Gets or sets the is communication merge field. |
| IsCommunicationRecipientField | yes | yes |  |  |  | Gets or sets the is recipient field. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Report |  | yes | yes |  |  | Gets or sets the report. |
| ReportFieldAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ReportFieldType | yes | yes |  | yes |  | Gets or sets the type of the report field. This is a hard coded list of values defined in the code as an enumeration. |
| ReportId | yes | yes |  | yes |  | Gets or sets the report identifier. |
| Selection | yes | yes |  |  |  | Selection is where the FieldType stores specific parameter values If ReportFieldType is Column or Attribute, it is the Column or Attribute name If ReportFieldType is DataSelectComponent, it will be some values of whatever the DataSelectComponent implements for specific parameters |
| ShowInGrid | yes | yes |  | yes |  | Gets or sets a value indicating whether [show in grid]. |
| SortDirection | yes | yes |  |  |  | Gets or sets the sort direction. This is a hard coded list of values defined in the code as an enumeration. |
| SortOrder | yes | yes |  |  |  | Gets or sets the sort order (ORDER BY). NULL means don't sort by this field |
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
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DataSelectComponentEntityType | Gets or sets the EntityType of the DataSelectComponent that this report field is using. |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Report | Gets or sets the report. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
