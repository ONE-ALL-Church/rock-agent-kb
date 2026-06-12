# Binary File Type Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `BinaryFileType`
- EntityType GUID: `62af597f-f193-412b-94ea-291cf713327d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 56 |
| Database-marked properties | 25 |
| Lava-marked properties | 38 |
| Lava-marked non-database properties | 13 |
| Related model links | 7 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowAnonymous | yes | yes |  |  |  | If true then the file type allows anonymous uploads. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BinaryFileTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| CacheControlHeader |  |  | yes |  |  | Gets the cache control header. |
| CacheControlHeaderSettings | yes | yes |  |  |  | Gets or sets the cache control header settings. |
| CacheToServerFileSystem | yes | yes |  |  |  | Gets or sets a flag indicating whether the file on any BinaryFile child entities should be cached to the server. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a description of the BinaryFileType. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FileCount |  |  | yes |  |  | Gets the count of BinaryFile entities that are children of this BinaryFileType. |
| FileQuery |  |  | yes |  |  | Gets a queryable collection of BinaryFile entities that are children of this BinaryFileType. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the CSS class that is used for a vector/CSS icon. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this BinaryFileType is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MaxFileSizeBytes | yes | yes |  |  |  | Gets or sets the maximum file size bytes. |
| MaxHeight | yes | yes |  |  |  | Gets or sets a value indicating the maximum height of a file type. |
| MaxWidth | yes | yes |  |  |  | Gets or sets a value indicating the maximum width of a file type. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the given Name of the BinaryFileType. This value is an alternate key and is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PreferredColorDepth | yes | yes |  |  |  | Gets or sets the preferred color depth of the file type. This is a hard coded list of values defined in the code as an enumeration. |
| PreferredFormat | yes | yes |  |  |  | Gets or sets the preferred format of the file type. This is a hard coded list of values defined in the code as an enumeration. |
| PreferredRequired | yes | yes |  |  |  | Gets or sets a value indicating whether the preferred attributes of the file type are required |
| PreferredResolution | yes | yes |  |  |  | Gets or sets the preferred resolution of the file type. This is a hard coded list of values defined in the code as an enumeration. |
| RequiresViewSecurity | yes | yes |  |  |  | Gets or sets a value indicating whether security should be checked when displaying files of this type |
| StorageEntityType |  | yes | yes |  |  | Gets or sets the storage mode EntityType. |
| StorageEntityTypeId | yes | yes |  |  |  | Gets or sets the Id of the storage service EntityType that is used to store files of this type. |
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
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| StorageEntityType | Gets or sets the storage mode EntityType. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| CacheToServerFileSystem | [BinaryFile](binary-file.md) |  |
| FileCount | [BinaryFile](binary-file.md) |  |
| FileCount | [BinaryFileType](binary-file-type.md) |  |
| FileQuery | [BinaryFile](binary-file.md) |  |
| FileQuery | [BinaryFileType](binary-file-type.md) |  |
| StorageEntityType | [EntityType](entity-type.md) |  |
| StorageEntityTypeId | [EntityType](entity-type.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
