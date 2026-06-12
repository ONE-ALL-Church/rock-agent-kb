# Tag Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `Tag`
- EntityType GUID: `d34258d0-d366-4efb-aa76-84b059fb5434`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 53 |
| Database-marked properties | 21 |
| Lava-marked properties | 38 |
| Lava-marked non-database properties | 17 |
| Related model links | 5 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BackgroundColor | yes | yes |  |  |  | Gets or sets the background color of each tag |
| BackgroundColorHex |  | yes | yes |  |  | Returns a hexadecimal value for the BackgroundColor value. |
| Category |  | yes | yes |  |  | Gets or sets the category. |
| CategoryId | yes | yes |  |  |  | Gets or sets the category identifier. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the EntityType of the Entities that this Tag can be applied to. |
| EntityTypeId | yes | yes |  |  |  | Gets or sets the EntityTypeId of the EntityType containing the entities that can use this Tag. This property is required. |
| EntityTypeQualifierColumn | yes | yes |  |  |  | Gets or sets the name of the column/property that contains the value that can narrow the scope of entities that can receive this Tag. Entities where this column contains the EntityTypeQualifierValue will be eligible to have this Tag. This property must be used in conjunction with the EntityTypeQualifierValue property. If all entities of the specified EntityType are eligible to use this Tag, this property will be null. |
| EntityTypeQualifierValue | yes | yes |  |  |  | Gets or sets the value in the EntityTypeQualifierColumn that narrows the scope of entities that can receive this Tag. Entities that contain this value in the EntityTypeQualifierColumn are eligible to use this Tag. This property must be used in conjunction with the EntityTypeQualifierColumn property. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is active. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Tag is part of the Rock core system/framework. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the Tag. This property is required. |
| Order | yes | yes |  | yes |  | Gets or sets the display order of the tag. the lower the number, the higher display priority that the Tag has. For example the Tags with the lower Order could be displayed higher on the Tag list. This property is required. |
| OwnerPersonAlias |  | yes | yes |  |  | Gets or sets the owner person alias. |
| OwnerPersonAliasId | yes | yes |  |  |  | Gets or sets the owner person alias identifier. |
| ParentAuthority |  |  | yes |  |  | Gets the parent security authority of this Tag. Where security is inherited from. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TagAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| TaggedItems |  | yes | yes |  |  | Gets or sets a collection of TaggedItems representing the entities that are tagged with this Tag. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| BackgroundColorHex | Returns a hexadecimal value for the BackgroundColor value. |
| Category | Gets or sets the category. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the EntityType of the Entities that this Tag can be applied to. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| OwnerPersonAlias | Gets or sets the owner person alias. |
| TaggedItems | Gets or sets a collection of TaggedItems representing the entities that are tagged with this Tag. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| EntityType | [EntityType](entity-type.md) |  |
| EntityTypeId | [EntityType](entity-type.md) |  |
| EntityTypeQualifierColumn | [EntityType](entity-type.md) |  |
| SupportedActions | Dictionary`2 |  |
| TaggedItems | TaggedItems |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | SupportedActions | related_entity_links |
