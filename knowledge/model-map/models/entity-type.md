# Entity Type Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Core`
- Model title: `EntityType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `16`
- Obsolete methods: `3`
- EntityType GUID: `a2277fba-d09f-4d07-b0ab-1c650c25a7a7`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 39 |
| Database-marked properties | 24 |
| Lava-marked properties | 25 |
| Lava-marked non-database properties | 6 |
| Related model links | 0 |
| Method signatures | 16 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AssemblyName | yes | yes |  |  |  | Gets or sets the assembly name of the EntityType. |
| AttributesSupportPrePostHtml | yes | yes |  |  |  | Gets or sets a value indicating whether attributes of this entity type support a Pre-HTML and Post-HTML option. |
| AttributesSupportShowOnBulk | yes | yes |  |  |  | Gets or sets a value indicating whether attributes of this entity type support displaying on bulk entry forms. |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FriendlyName | yes | yes |  |  |  | Gets or sets the friendly name of the EntityType (the class name). |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IndexDocumentUrl | yes |  |  |  |  | Gets or sets the index document URL. |
| IndexModelType | yes |  |  |  |  | Gets the name of the get index model. |
| IndexResultTemplate | yes |  |  |  |  | Gets or sets the index result template. |
| IsAchievementsEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this instance has achievements enabled. |
| IsCommon | yes | yes |  |  |  | Gets or sets a flag indicating whether this entity type is a commonly used entity. If so, it will grouped at the top by the entity type picker control |
| IsEntity | yes | yes |  |  |  | Gets or sets a flag indicating whether this entity type implements the IEntity interface. |
| IsIndexingEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is indexing enabled. |
| IsIndexingSupported | yes |  |  |  |  | Gets a value indicating whether this entity supports indexing. |
| IsMessageBusEventPublishEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is message bus event publish enabled. |
| IsRelatedToInteractionTrackedOnCreate | yes | yes |  |  |  | Gets or sets a value indicating if this entity type will automatically have InteractionEntity records created to associate the creation of new entities with the interaction that was active at the time. |
| IsSecured | yes | yes |  |  |  | Gets or sets a flag indicating whether this entity type implements the ISecured interface. |
| IsSystem |  | yes | yes |  |  | Gets a flag indicating whether this instance is part of the Rock core system/framework. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LinkUrlLavaTemplate | yes |  |  |  |  | Gets or sets a lava template that can be used for generating a link to view details for this entity (i.e. "~/person/{{ Entity.Id }}"). |
| MultiValueFieldType |  |  | yes |  |  | Gets or sets the type of the multi value field. This helps determine what type of control can be used to select this type of Entity (multiple values) |
| MultiValueFieldTypeId | yes | yes |  |  |  | Gets or sets the multi value field type identifier. |
| Name | yes | yes |  |  |  | Gets or sets the full name of the EntityType (including the namespace). This value is required and is an alternate key. |
| SingleValueFieldType |  |  | yes |  |  | Gets or sets the type of the single value field. This helps determine what type of control can be used to select this type of Entity (single values) |
| SingleValueFieldTypeId | yes | yes |  |  |  | Gets or sets the single value field type identifier. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| IdKey |  |
| IsSystem | Gets a flag indicating whether this instance is part of the Rock core system/framework. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
