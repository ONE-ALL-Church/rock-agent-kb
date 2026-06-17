# Group Demographic Value Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Group`
- Model title: `GroupDemographicValue`
- EntityType GUID: `c9ced7b0-88bf-40d1-83d1-a58b3c57a2e1`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 48 |
| Database-marked properties | 18 |
| Lava-marked properties | 33 |
| Lava-marked non-database properties | 15 |
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
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the group. |
| GroupDemographicType |  | yes | yes |  |  | Gets or sets the type of the group demographic. |
| GroupDemographicTypeId | yes | yes |  | yes |  | Gets or sets the GroupDemographicType ID that this GroupDemographicValue is for. |
| GroupDemographicValueAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupId | yes | yes |  | yes |  | Gets or sets the Group ID that this GroupDemographicValue is for. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastCalculatedDateTime | yes | yes |  |  |  | Gets or sets the last date and time when this GroupDemographicValue was calculated. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RelatedEntityId | yes | yes |  |  |  | Gets or sets the related entity identifier. e.g. the ID of the DefinedValue |
| RelatedEntityType |  | yes | yes |  |  | Gets or sets the type of the related entity. |
| RelatedEntityTypeId | yes | yes |  |  |  | Gets or sets the related EntityTypeID this value if for. e.g. DefinedValue. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| Value | yes | yes |  |  |  | Gets or sets the value. |
| ValueAsBoolean | yes | yes |  |  |  | Gets or sets the value as boolean. |
| ValueAsGuid | yes | yes |  |  |  | Gets or sets the value as GUID. |
| ValueAsNumeric | yes | yes |  |  |  | Gets or sets the value as numeric. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| Group | Gets or sets the group. |
| GroupDemographicType | Gets or sets the type of the group demographic. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RelatedEntityType | Gets or sets the type of the related entity. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
