# Document Type Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Core`
- Model title: `DocumentType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `18cf366f-46b6-49ca-b557-bcabd6bbd175`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 50 |
| Database-marked properties | 21 |
| Lava-marked properties | 35 |
| Lava-marked non-database properties | 14 |
| Related model links | 7 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 3 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BinaryFileType |  | yes | yes |  |  | Gets or sets the Binary File Type of the document type. |
| BinaryFileTypeId | yes | yes |  |  |  | Gets or sets the id of the Binary File Type that this document type belongs to. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefaultDocumentNameTemplate | yes | yes |  |  |  | Gets or sets the default document name template. |
| DocumentTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the Entity Type of the entities that Notes of this DocumentType |
| EntityTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Entity Type that this DocumentType is used for. A DocumentType can only be associated with a single Entity Type and will only contain notes for entities of this type. This property is required. |
| EntityTypeQualifierColumn | yes | yes |  |  |  | Gets or sets the name of the qualifier column/property on the Entity Type that this Docuement Type applies to. If this is not provided, the document type can be used on all entities of the provided Entity Type. |
| EntityTypeQualifierValue | yes | yes |  |  |  | Gets or sets the qualifier value in the qualifier column that this document type applies to. For instance this note type and related notes will only be applicable to entity if the value in the EntityTypeQualiferColumn matches this value. This property should not be populated without also populating the EntityTypeQualifierColumn property. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the CSS class that is used for a vector/CSS icon. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsImage | yes | yes |  | yes |  | Gets or sets the IsImage flag for the Document Type. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this DocumentType is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MaxDocumentsPerEntity | yes | yes |  |  |  | Gets or sets the maximum documents per entity. This would limit the documents of that type per entity. A blank value means no limit. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the given Name of the DocumentType. |
| Order | yes | yes |  | yes |  | Gets or sets the display order of this DocumentType. The lower the number the higher the display priority. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| UserSelectable | yes | yes |  |  |  | Gets or sets a value indicating whether the type is user selectable. |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| BinaryFileType | Gets or sets the Binary File Type of the document type. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the Entity Type of the entities that Notes of this DocumentType |
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
| BinaryFileType | [Binary File Type](binary-file-type.md) | 62af597f-f193-412b-94ea-291cf713327d |
| BinaryFileTypeId | [Binary File Type](binary-file-type.md) | 62af597f-f193-412b-94ea-291cf713327d |
| EntityType | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| EntityType | Notes | 7cefa340-9d98-4b2c-b462-313c61944b6c |
| EntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| EntityTypeQualifierColumn | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| IsImage | [Document Type](document-type.md) | 18cf366f-46b6-49ca-b557-bcabd6bbd175 |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | EntityTypeId | description |
| property_changed | EntityTypeQualifierColumn | description |
| property_changed | EntityTypeQualifierValue | description |
