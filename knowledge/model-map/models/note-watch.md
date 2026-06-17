# Note Watch Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `NoteWatch`
- EntityType GUID: `a5c129c2-e64d-4b72-b94d-dba6da6ac2e3`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 52 |
| Database-marked properties | 20 |
| Lava-marked properties | 35 |
| Lava-marked non-database properties | 17 |
| Related model links | 0 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowOverride | yes | yes |  |  |  | Set AllowOverride to False to prevent people from adding an IsWatching=False on NoteWatch with the same filter that is marked as IsWatching=True In other words, if a group is configured a NoteWatch, an individual shouldn't be able to add an un-watch if AllowOverride=False (and any un-watches that may have been already added would be ignored) |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  | Set EntityTypeId and EntityId to watch all notes for a specific entity NOTE: If EntityType is Person, make sure to watch the Person's PersonAlias' Persons |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the type of the entity. |
| EntityTypeId | yes | yes |  |  |  | Set EntityTypeId and EntityId to watch all notes for a specific entity |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  | Returns true if ... is valid. |
| IsValidWatchFilter | yes |  |  |  |  | Returns true if this NoteWatch has valid "Watch Filter" parameters |
| IsValidWatcher | yes |  |  |  |  | Returns true if this NoteWatch has valid "Watcher" parameters |
| IsWatching | yes | yes |  |  |  | Set IsWatching to False to disable this NoteWatch (or specifically don't watch based on the notewatch criteria) |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Note |  | yes | yes |  |  | Gets or sets the note. |
| NoteId | yes | yes |  |  |  | Set NoteId to watch a specific note |
| NoteType |  | yes | yes |  |  | Gets or sets the type of the note. |
| NoteTypeId | yes | yes |  |  |  | Set NoteTypeId to watch all notes of a specific note type Set NoteTypeId and EntityId to watch all notes of a specific type as it relates to a specific entity |
| NoteWatchAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WatchReplies | yes | yes |  |  |  | Gets or sets a value indicating whether [watch replies]. |
| WatcherGroup |  | yes | yes |  |  | Gets or sets the group that is watching this note watch |
| WatcherGroupId | yes | yes |  |  |  | Gets or sets the group that is watching this note watch |
| WatcherPersonAlias |  | yes | yes |  |  | Gets or sets the person alias of the person watching this note watch |
| WatcherPersonAliasId | yes | yes |  |  |  | Gets or sets the person alias id of the person watching this note watch |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the type of the entity. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Note | Gets or sets the note. |
| NoteType | Gets or sets the type of the note. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WatcherGroup | Gets or sets the group that is watching this note watch |
| WatcherPersonAlias | Gets or sets the person alias of the person watching this note watch |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
