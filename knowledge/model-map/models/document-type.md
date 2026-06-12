# Document Type Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `DocumentType`
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
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BinaryFileType |  | yes | yes |  |  | Gets or sets the BinaryFileType of the document type. |
| BinaryFileTypeId | yes | yes |  |  |  | Gets or sets the id of the BinaryFileType that this document type belongs to. |
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
| EntityType |  | yes | yes |  |  | Gets or sets the EntityType of the entities that Notes of this DocumentType |
| EntityTypeId | yes | yes |  | yes |  | Gets or sets the Id of the EntityType that this DocumentType is used for. A DocumentType can only be associated with a single EntityType and will only contain notes for entities of this type. This property is required. |
| EntityTypeQualifierColumn | yes | yes |  |  |  | Gets or sets the name of the qualifier column/property on the EntityType that this Docuement Type applies to. If this is not provided, the document type can be used on all entities of the provided EntityType. |
| EntityTypeQualifierValue | yes | yes |  |  |  | Gets or sets the qualifier value in the qualifier column that this document type applies to. For instance this note type and related notes will only be applicable to entity if the value in the EntityTypeQualiferColumn matches this value. This property should not be populated without also populating the EntityTypeQualifierColumn property. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the CSS class that is used for a vector/CSS icon. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsImage | yes | yes |  | yes |  | Gets or sets the IsImage flag for the DocumentType. |
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
| BinaryFileType | Gets or sets the BinaryFileType of the document type. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the EntityType of the entities that Notes of this DocumentType |
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
| BinaryFileType | [BinaryFileType](binary-file-type.md) |  |
| BinaryFileTypeId | [BinaryFileType](binary-file-type.md) |  |
| EntityType | [EntityType](entity-type.md) |  |
| EntityType | Notes |  |
| EntityTypeId | [EntityType](entity-type.md) |  |
| EntityTypeQualifierColumn | [EntityType](entity-type.md) |  |
| IsImage | [DocumentType](document-type.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
