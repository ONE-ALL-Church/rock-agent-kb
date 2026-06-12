# Defined Value Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `DefinedValue`
- EntityType GUID: `53d4bf38-c49e-4a52-8b0e-5e016fb9574e`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 46 |
| Database-marked properties | 17 |
| Lava-marked properties | 31 |
| Lava-marked non-database properties | 14 |
| Related model links | 1 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Category |  | yes | yes |  |  | Gets or sets the Category that this Defined Value belongs to. |
| CategoryId | yes | yes |  |  |  | Gets or sets the category identifier. This property is ignored if DefinedType.CategorizedValuesEnabled is disabled. |
| CategoryName | yes | yes |  |  |  | Gets the Category Name if a Category is associated with the Defined Type. Otherwise returns an empty string. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefinedType |  | yes | yes |  |  | Gets or sets the Defined Type that this DefinedValue belongs to. |
| DefinedTypeId | yes | yes |  | yes |  | Gets or sets the DefinedTypeId of the DefinedType that this DefinedValue belongs to. This property is required. |
| DefinedValueAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Description | yes | yes |  |  |  | Gets or sets the Description of the DefinedValue. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  | yes |  | Gets or sets a value indicating whether this DefinedValue is active. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this DefinedValue is part of the Rock core system/framework. this property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Order | yes | yes |  | yes |  | Gets or sets the sort and display order of the DefinedValue. This is an ascending order, so the lower the value the higher the sort priority. |
| ParentAuthority |  |  | yes |  |  | Gets the parent security authority for this DefinedValue. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| Value | yes | yes |  | yes |  | Gets or sets the Value of the DefinedValue. This property is required. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the Category that this Defined Value belongs to. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DefinedType | Gets or sets the Defined Type that this DefinedValue belongs to. |
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
| DefinedTypeId | [DefinedType](defined-type.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
