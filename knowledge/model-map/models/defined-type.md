# Defined Type Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `DefinedType`
- EntityType GUID: `6028d502-79f4-4a74-9323-525e90f900c7`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 19 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 15 |
| Related model links | 5 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CategorizedValuesEnabled | yes | yes |  |  |  | Gets or sets a flag indicating if the Defined Values associated with this Defined Type can be grouped into categories. |
| Category |  | yes | yes |  |  | Gets or sets the category. |
| CategoryId | yes | yes |  |  |  | Gets or sets the category identifier. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefinedTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| DefinedValues |  | yes | yes |  |  | Gets or sets a collection containing the DefinedValues that belong to this DefinedType. |
| Description | yes | yes |  |  |  | Gets or sets a user defined description of the DefinedType. |
| EnableSecurityOnValues | yes | yes |  |  |  | Gets or sets a value indicating whether the DefinedValues for this DefinedType should allow security settings. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FieldType |  | yes | yes |  |  | Gets or sets the Field Type that is used to set/select, and at times display the DefinedValues that are associated with this DefinedType. |
| FieldTypeId | yes | yes |  |  |  | Gets or sets the FieldTypeId of the Field Type that is used to set/select, and at times display the DefinedValues that are associated with NOTE: Currently, Text is the only supported fieldType for DefinedTypes. this DefinedType. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HelpText | yes | yes |  |  |  | Gets or sets the help text for the defined type. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  | yes |  | Gets or sets a value indicating whether this Defined Type is active. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this DefinedType is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the DefinedType. |
| Order | yes | yes |  | yes |  | Gets or sets the display order of this DefinedType. The lower the number the higher the display priority. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
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
| Category | Gets or sets the category. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DefinedValues | Gets or sets a collection containing the DefinedValues that belong to this DefinedType. |
| EntityStringValue |  |
| FieldType | Gets or sets the Field Type that is used to set/select, and at times display the DefinedValues that are associated with this DefinedType. |
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
| DefinedValues | DefinedValues | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| FieldType | DefinedValues | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| FieldType | [Field Type](field-type.md) | 54018eb6-868c-477d-8b6a-455a6115b30b |
| FieldTypeId | DefinedValues | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| FieldTypeId | [Field Type](field-type.md) | 54018eb6-868c-477d-8b6a-455a6115b30b |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
