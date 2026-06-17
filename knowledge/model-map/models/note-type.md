# Note Type Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `NoteType`
- EntityType GUID: `337eed57-d4ab-4eed-bbdb-0cb3a467dbcc`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 62 |
| Database-marked properties | 33 |
| Lava-marked properties | 47 |
| Lava-marked non-database properties | 14 |
| Related model links | 5 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  | Gets or sets the additional settings json. |
| AllowsAttachments | yes | yes |  |  |  | Gets or sets a value indicating whether attachments are allowed for this note type. |
| AllowsReplies | yes | yes |  |  |  | Gets or sets a value indicating whether [allows replies]. |
| AllowsWatching | yes | yes |  |  |  | Gets or sets a value indicating whether [allows watching]. |
| ApprovalUrlTemplate | yes | yes |  |  | yes | A optional Lava Template that can be used to general a URL where Notes of this type can be approved If this is left blank, the Approval URL will be a URL to the page (including a hash anchor to the note) where the note was originally created |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AutoWatchAuthors | yes | yes |  |  |  | Gets or sets a value indicating whether [automatic watch authors]. |
| AvailableKeys |  |  | yes |  |  |  |
| BackgroundColor | yes | yes |  |  | yes | Gets or sets the background color of each note |
| BinaryFileType |  | yes | yes |  |  | Gets or sets the Binary File Type that will be used for attachments. |
| BinaryFileTypeId | yes | yes |  |  |  | Gets or sets the binary file type identifier used when saving attachments. |
| BorderColor | yes | yes |  |  | yes | Gets or sets the border color of each note |
| Color | yes | yes |  |  |  | Gets or sets the base color to use when calculating the color pair for notes of this type. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the Entity Type of the entities that Notes of this NoteType |
| EntityTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Entity Type that this NoteType is used for. A NoteType can only be associated with a single Entity Type and will only contain notes for entities of this type. This property is required. |
| EntityTypeQualifierColumn | yes | yes |  |  |  | Gets or sets the name of the qualifier column/property on the Entity Type that this NoteType applies to. If this is not provided, the note type can be used on all entities of the provided Entity Type. |
| EntityTypeQualifierValue | yes | yes |  |  |  | Gets or sets the qualifier value in the qualifier column that this note type applies to. For instance this note type and related notes will only be applicable to entity if the value in the EntityTypeQualiferColumn matches this value. This property should not be populated without also populating the EntityTypeQualifierColumn property. |
| FontColor | yes | yes |  |  | yes | Gets or sets the font color of the note text |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FormatType | yes | yes |  |  |  | Gets or sets the format the note text is stored in. This is a hard coded list of values defined in the code as an enumeration. |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the name of an icon CSS class. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsMentionEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether notes of this type allow person mentions to be embedded in the text. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating that this NoteType is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MaxReplyDepth | yes | yes |  |  |  | Gets or sets the maximum reply depth. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the NoteType. This property is required. |
| NoteTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RequiresApprovals | yes | yes |  |  |  | Gets or sets a value indicating whether [requires approvals]. |
| SendApprovalNotifications | yes | yes |  |  | yes | Gets or sets a value indicating whether [send approval notifications]. |
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
| BinaryFileType | Gets or sets the Binary File Type that will be used for attachments. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the Entity Type of the entities that Notes of this NoteType |
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
| EntityType | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| EntityType | Notes | 53dc1e78-14a5-44de-903f-6a2cb02164e7 |
| EntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| EntityTypeQualifierColumn | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
