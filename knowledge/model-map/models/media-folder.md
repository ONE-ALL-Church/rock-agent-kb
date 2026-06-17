# Media Folder Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `CMS`
- Model title: `MediaFolder`
- EntityType GUID: `b28fc79f-9fee-4be4-801d-96b9246e6043`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 53 |
| Database-marked properties | 21 |
| Lava-marked properties | 38 |
| Lava-marked non-database properties | 17 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContentChannel |  | yes | yes |  |  | Gets or sets the content channel. |
| ContentChannelAttribute |  | yes | yes |  |  | Gets or sets the content channel attribute. |
| ContentChannelAttributeId | yes | yes |  |  |  | Gets or sets the synced content channel item attribute identifier to store the Guid value into. |
| ContentChannelId | yes | yes |  |  |  | Gets or sets the content channel identifier. |
| ContentChannelItemStatus | yes | yes |  |  |  | Gets or sets the ContentChannelItemStatus Content channel Item status. This is a hard coded list of values defined in the code as an enumeration. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a description of the MediaFolder. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsContentChannelSyncEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether the content channel sync is enabled. |
| IsPublic | yes | yes |  |  |  | Gets or sets a value indicating if this Media Folder is public. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MediaAccount |  | yes | yes |  |  | Gets or sets the Media Account that this MediaFolder belongs to. |
| MediaAccountId | yes | yes |  | yes |  | Gets or sets the MediaAccountId of the Media Account that this MediaFolder belongs to. This property is required. |
| MediaElements |  | yes | yes |  |  | Gets or sets a collection containing the Elements that belong to this Folder. |
| MediaFolderAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| MetricData | yes | yes |  |  |  | Gets or sets the custom provider metric data for this instance. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the MediaFolder. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SourceData | yes | yes |  |  |  | Gets or sets the custom provider data for this instance. |
| SourceKey | yes | yes |  |  |  | Gets or sets the provider's unique identifier for this instance. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowType |  | yes | yes |  |  | Gets or sets the type of the workflow that will be launched when a new Media Element is added. |
| WorkflowTypeId | yes | yes |  |  |  | Gets or sets the workflow type identifier. This workflow is launched whenever a new Media Element is added to the system. The Media Element is passed as the Entity object to the workflow. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| ContentChannel | Gets or sets the content channel. |
| ContentChannelAttribute | Gets or sets the content channel attribute. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| MediaAccount | Gets or sets the Media Account that this MediaFolder belongs to. |
| MediaElements | Gets or sets a collection containing the Elements that belong to this Folder. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WorkflowType | Gets or sets the type of the workflow that will be launched when a new Media Element is added. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| MediaAccountId | [Media Account](media-account.md) | cd35f034-ac18-40d5-b703-6bf16d79c51c |
| MediaElements | Elements | f4506b5d-f22c-4d3f-8205-fe48a9b7584b |
| WorkflowType | [Media Element](media-element.md) | f4506b5d-f22c-4d3f-8205-fe48a9b7584b |
| WorkflowTypeId | [Media Element](media-element.md) | f4506b5d-f22c-4d3f-8205-fe48a9b7584b |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
