# Category Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Core`
- Model title: `Category`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `1d68154e-ec76-44c8-9813-7736b27aecf9`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 19 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 15 |
| Related model links | 2 |
| Method signatures | 36 |
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
| CategoryAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ChildCategories |  | yes | yes |  |  | Gets or sets a collection of Categories that are children of the current Category. |
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
| EntityType |  | yes | yes |  |  | Gets or sets the Entity Type that can use this Category. |
| EntityTypeId | yes | yes |  | yes |  | Gets or sets the EntityTypeId of the Entity Type that this Category belongs to. |
| EntityTypeQualifierColumn | yes | yes |  |  |  | Gets or sets the entity type qualifier column that contains the value (see EntityTypeQualifierValue) that is used to narrow the scope of the Category. |
| EntityTypeQualifierValue | yes | yes |  |  |  | Gets or sets the entity type qualifier value that is used to narrow the scope of the Category to a subset or specific instance of an EntityType. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HighlightColor | yes | yes |  |  |  | Gets or sets the color of the highlight. |
| IconCssClass | yes | yes |  |  |  | Gets or sets the name of the icon CSS class. This property is only used for CSS based icons. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Category is part of the Rock core system/framework. |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the Category |
| Order | yes | yes |  | yes |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority where security authorizations are being inherited from. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ParentCategory |  | yes | yes |  |  | Gets or sets the parent category. |
| ParentCategoryId | yes | yes |  |  |  | Gets or sets the CategoryId of the parent Category. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| ChildCategories | Gets or sets a collection of Categories that are children of the current Category. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the Entity Type that can use this Category. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ParentCategory | Gets or sets the parent category. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| EntityType | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| EntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
