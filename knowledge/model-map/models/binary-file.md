# Binary File Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `BinaryFile`
- EntityType GUID: `9bb1a349-5998-47c1-97d5-d6cc00275662`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 59 |
| Database-marked properties | 25 |
| Lava-marked properties | 41 |
| Lava-marked non-database properties | 17 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalInformation | yes | yes |  |  |  | Gets or sets additional information for the file. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BinaryFileAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| BinaryFileType |  | yes | yes |  |  | Gets or sets the Binary File Type of the file. |
| BinaryFileTypeId | yes | yes |  |  |  | Gets or sets the id of the Binary File Type that this file belongs to. |
| ContentLastModified | yes | yes |  |  |  | Gets or sets the content last modified. |
| ContentStream |  |  | yes |  |  | Gets or sets the content stream. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DatabaseData |  | yes | yes |  |  | Gets or sets a Binary File Data that contains the content of the file. This object can be used for temporary storage or be persisted to the database. |
| Description | yes | yes |  |  |  | Gets or sets a user defined description of the file. |
| Document |  | yes | yes |  |  | Gets or sets the document. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FileName | yes | yes |  | yes |  | Gets or sets the name of the file, including any extensions. This name is usually captured when the file is uploaded to Rock and this same name will be used when the file is downloaded. This property is required. |
| FileSize | yes | yes |  |  |  | Gets or sets the size of the file (in bytes) |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Height | yes | yes |  |  |  | Gets or sets a value indicating the height of a file type. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this file is part of the Rock core system/framework. |
| IsTemporary | yes | yes |  | yes |  | Gets or sets a flag indicating if this is a temporary file. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MimeType | yes | yes |  | yes |  | Gets or sets the Mime Type for the file. This property is required |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ParentEntityId | yes | yes |  |  |  | Gets or sets the parent Entity ID to determine security access. |
| ParentEntityTypeId | yes | yes |  |  |  | Gets or sets the Parent EntityType ID to determine security access. |
| Path | yes | yes |  |  |  | Gets or sets a path to the file that is understandable by the storage provider. |
| StorageEntitySettings | yes |  |  |  |  | Gets or sets the storage entity settings. |
| StorageEntityTypeId | yes | yes |  |  |  | Gets the Id of the Storage Service Entity Type that is used to store this file. |
| StorageProvider |  | yes | yes |  |  | Gets the storage provider. |
| StorageSettings |  |  | yes |  |  | Gets the storage settings. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| Url |  | yes | yes |  |  | Gets the URL. |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| Width | yes | yes |  |  |  | Gets or sets a value indicating the width of a file type. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| BinaryFileType | Gets or sets the Binary File Type of the file. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DatabaseData | Gets or sets a Binary File Data that contains the content of the file. This object can be used for temporary storage or be persisted to the database. |
| Document | Gets or sets the document. |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| StorageProvider | Gets the storage provider. |
| TypeId |  |
| TypeName |  |
| Url | Gets the URL. |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| BinaryFileType | [Binary File Type](binary-file-type.md) | 62af597f-f193-412b-94ea-291cf713327d |
| BinaryFileTypeId | [Binary File Type](binary-file-type.md) | 62af597f-f193-412b-94ea-291cf713327d |
| DatabaseData | [Binary File Data](binary-file-data.md) | ea647542-1e0f-4dae-9537-65e3ffee8792 |
| StorageEntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
