# History Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `History`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `58`
- Obsolete methods: `4`
- EntityType GUID: `546d5f43-1184-47c9-8265-2d7bf4e1bca5`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 57 |
| Database-marked properties | 26 |
| Lava-marked properties | 42 |
| Lava-marked non-database properties | 16 |
| Related model links | 2 |
| Method signatures | 58 |
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
| Caption | yes | yes |  |  |  | Gets or sets the caption |
| Category |  | yes | yes |  |  | Gets or sets the category. |
| CategoryId | yes | yes |  | yes |  | Gets or sets the Id of the Category. This property is required. |
| ChangeType | yes | yes |  |  |  | Gets or sets the ChangeType which is a structured (for querying) field to describe what type of data was changed (Record, Property, Attribute, Location, Schedule, etc) HistoryChangeType constants for common change types |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  | yes |  | Gets or sets the Id of the entity that this history is related to. |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the entity type this history is associated with |
| EntityTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Entity Type. This property is required. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HistoryAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsSensitive | yes | yes |  |  |  | Gets or sets whether the NewValue and/or OldValue is null because the value is sensitive data that shouldn't be logged If "IsSensitive" doesn't apply to this, it can be left null |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this history is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| NewRawValue | yes | yes |  |  |  | Creates new rawvalue. |
| NewValue | yes | yes |  |  |  | Gets or sets the new value. |
| OldRawValue | yes | yes |  |  |  | Gets or sets the old raw value. |
| OldValue | yes | yes |  |  |  | Gets or sets the old value. |
| ParentAuthority |  |  | yes |  |  | Gets the parent security authority of this History. Where security is inherited from. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RelatedData | yes | yes |  |  |  | Gets or sets the related data. |
| RelatedEntityId | yes | yes |  |  |  | Gets or sets the related entity identifier. |
| RelatedEntityType |  | yes | yes |  |  | Gets or sets the type of the related entity. |
| RelatedEntityTypeId | yes | yes |  |  |  | Gets or sets the related entity type identifier. |
| SourceOfChange | yes | yes |  |  |  | Optional: Gets or sets name of the tool or process that changed the value |
| SummaryHtml |  | yes | yes |  |  | Calculates and returns a formatted summary |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| ValueName | yes | yes |  |  |  | Gets or sets the name of the value depending on ChangeType: ChangeTypeName.Property =&gt; Property Friendly Name, ChangeType.Attribute =&gt; Attribute Name, ChangeType.Record =&gt; the ToString of the record |
| Verb | yes | yes |  |  |  | Gets or sets the verb which is a structured (for querying) field to describe what the action is (ADD, DELETE, UPDATE, VIEW, WATCHED, etc). HistoryVerb constants for common verbs |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the category. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the entity type this history is associated with |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RelatedEntityType | Gets or sets the type of the related entity. |
| SummaryHtml | Calculates and returns a formatted summary |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| CategoryId | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| EntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
