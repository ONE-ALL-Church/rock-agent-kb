# Note Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Core`
- Model title: `Note`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `35`
- Obsolete methods: `4`
- EntityType GUID: `53dc1e78-14a5-44de-903f-6a2cb02164e7`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 66 |
| Database-marked properties | 26 |
| Lava-marked properties | 51 |
| Lava-marked non-database properties | 25 |
| Related model links | 2 |
| Method signatures | 35 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| ApprovalStatus | yes | yes |  |  |  | Gets or sets the approval status. This is a hard coded list of values defined in the code as an enumeration. |
| ApprovalUrl |  | yes | yes |  | yes | Gets the approval URL. |
| ApprovalsSent | yes | yes |  |  | yes | Gets or sets a value indicating whether [approvals sent]. |
| ApprovedByPersonAliasId | yes | yes |  |  | yes | Gets or sets the PersonAliasId of the Person who either approved or declined the Note. If no approval action has been performed on this Note, this value will be null. |
| ApprovedDateTime | yes | yes |  |  |  | Gets or sets the approved date. |
| Attachments |  | yes | yes |  |  | Gets or sets the note attachments. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Caption | yes | yes |  |  |  | Gets or sets the caption |
| ChildNotes |  | yes | yes |  |  | Gets or sets the child notes. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedByPersonPhotoUrl |  | yes | yes |  |  | Gets the created by person photo URL. |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EditedByPersonAlias |  | yes | yes |  |  | Gets or sets the person alias that last edited the note text. Use this instead of ModifiedByPersonAlias to determine the last person to edit the note text |
| EditedByPersonAliasId | yes | yes |  |  |  | Gets or sets the person alias that last edited the note text. Use this instead of ModifiedByPersonAliasId to determine the last person to edit the note text |
| EditedByPersonName |  | yes | yes |  |  | Gets the name of the person that last edited the note text. Use this instead of ModifiedByPersonName to determine the last person to edit the note text |
| EditedDateTime | yes | yes |  |  |  | Gets or sets the last time the note text was edited. Use this instead of ModifiedDateTime to determine the last time a person edited a note |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  | Gets or sets the Id of the entity that this note is related to. |
| EntityName |  | yes | yes |  |  | Gets the name of the entity (If it is a Note on a Person, it would be the person's name, etc) |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsAlert | yes | yes |  |  |  | Gets or sets a flag indicating if this note is an alert. |
| IsCurrentPersonWatching |  | yes | yes |  |  | Gets a value indicating whether the currently logged in person is watching this specific note |
| IsPinned | yes | yes |  |  |  | Gets or sets a flag indicating if this note should be pinned to top |
| IsPrivateNote | yes | yes |  |  |  | Gets or sets a value indicating whether this note is viewable to only the person that created the note |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this note is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| NoteAnchorId |  | yes | yes |  |  | Gets the id to use in the note's anchor tag |
| NoteAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| NoteType |  | yes | yes |  |  | Gets or sets the Note Type |
| NoteTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Note Type. This property is required. |
| NoteUrl | yes | yes |  |  |  | Gets or sets the URL where the Note was created. Use NoteUrl with a hash anchor of the Note.NoteAnchorId so that Notifications and Approvals can know where to view the note |
| NotificationsSent | yes | yes |  |  |  | Gets or sets a value indicating whether [notifications sent]. |
| ParentAuthority |  |  | yes |  |  | Gets the parent security authority of this Note. Where security is inherited from. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ParentNote |  | yes | yes |  |  | Gets or sets the parent note. |
| ParentNoteId | yes | yes |  |  |  | Gets or sets the parent note identifier. |
| SupportedActions |  |  | yes |  |  |  |
| Text | yes | yes |  |  |  | Gets or sets the text/body of the note. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| ViewableChildNotes |  | yes | yes |  |  | Gets the childs note that the current person is allowed to view |
| ViewableDescendentsCount |  | yes | yes |  |  | Gets the count of that are descendants (replies) of this note. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ApprovalUrl | Gets the approval URL. |
| Attachments | Gets or sets the note attachments. |
| AttributeValues |  |
| Attributes |  |
| ChildNotes | Gets or sets the child notes. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| CreatedByPersonPhotoUrl | Gets the created by person photo URL. |
| EditedByPersonAlias | Gets or sets the person alias that last edited the note text. Use this instead of ModifiedByPersonAlias to determine the last person to edit the note text |
| EditedByPersonName | Gets the name of the person that last edited the note text. Use this instead of ModifiedByPersonName to determine the last person to edit the note text |
| EntityName | Gets the name of the entity (If it is a Note on a Person, it would be the person's name, etc) |
| EntityStringValue |  |
| IdKey |  |
| IsCurrentPersonWatching | Gets a value indicating whether the currently logged in person is watching this specific note |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| NoteAnchorId | Gets the id to use in the note's anchor tag |
| NoteType | Gets or sets the Note Type |
| ParentNote | Gets or sets the parent note. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| ViewableChildNotes | Gets the childs note that the current person is allowed to view |
| ViewableDescendentsCount | Gets the count of that are descendants (replies) of this note. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ApprovedByPersonAliasId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| NoteTypeId | [Note Type](note-type.md) | 337eed57-d4ab-4eed-bbdb-0cb3a467dbcc |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
