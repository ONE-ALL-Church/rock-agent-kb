# Media Element Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `CMS`
- Model title: `MediaElement`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `f4506b5d-f22c-4d3f-8205-fe48a9b7584b`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 54 |
| Database-marked properties | 24 |
| Lava-marked properties | 37 |
| Lava-marked non-database properties | 13 |
| Related model links | 1 |
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
| CloseCaption | yes | yes |  |  |  | The close captioning data for the media element. This should be in the format of WebVTT for use by Rock. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefaultFileUrl | yes | yes |  |  |  | Gets the default file URL to use for media playback. This value is calculated at run time but also stored on the database so it is available in SQL and LINQ queries as well. |
| DefaultThumbnailUrl | yes | yes |  |  |  | Gets the default thumbnail URL. This value is calculated at run time but also stored on the database so it is available in SQL and LINQ queries as well. |
| Description | yes | yes |  |  |  | Gets or sets a description of the Element. |
| DurationSeconds | yes | yes |  |  |  | Gets or set the duration in seconds of media element. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FileData |  |  | yes |  |  | Gets or sets the media element file data. This contains all the information about the different file URLs available for the user to stream or download. |
| FileDataJson | yes | yes |  |  |  | Gets or sets the file data JSON content that will be stored in the database. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MediaElementAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| MediaFolder |  | yes | yes |  |  | Gets or sets the Media Folder that this Element belongs to. |
| MediaFolderId | yes | yes |  | yes |  | Gets or sets the MediaFolderId of the Media Folder that this MediaElement belongs to. This property is required. |
| MetricData | yes | yes |  |  |  | Gets or sets the custom provider metric data for this instance. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the Element. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SourceCreatedDateTime | yes | yes |  |  |  | Gets or sets the DateTime this instance was created on the provider. |
| SourceData | yes | yes |  |  |  | Gets or sets the custom provider data for this instance. |
| SourceKey | yes | yes |  |  |  | Gets or sets the provider's unique identifier for this instance. |
| SourceModifiedDateTime | yes | yes |  |  |  | Gets or sets the DateTime this instance was modified on the provider. |
| SupportedActions |  |  | yes |  |  |  |
| ThumbnailData |  |  | yes |  |  | Gets or sets the thumbnail data. |
| ThumbnailDataJson | yes | yes |  |  |  | Gets or sets the thumbnail data JSON content that will stored in the database. |
| TranscriptionText | yes | yes |  |  |  | Transcripts Text |
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
| MediaFolder | Gets or sets the Media Folder that this Element belongs to. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| MediaFolderId | [Media Folder](media-folder.md) | b28fc79f-9fee-4be4-801d-96b9246e6043 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
