# Related Entity Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `RelatedEntity`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `bd29e403-ba47-4688-be29-45a38ce8bd03`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 20 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 14 |
| Related model links | 4 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  | Gets or sets the additional settings json. |
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
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Site was created by and is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Note | yes | yes |  |  |  | Gets or sets the note. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PurposeKey | yes | yes |  |  |  | Gets or sets the purpose key. This indicates the purpose of the relationship. For example: See notes on RelatedEntityPurposeKey for details. |
| QualifierValue | yes | yes |  |  |  | Gets or sets the qualifier value. See more details on RelatedEntityPurposeKey. |
| Quantity | yes | yes |  |  |  | Gets or sets the quantity. |
| RelatedEntityAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| SourceEntityId | yes | yes |  | yes |  | Gets or sets the EntityId of the Entity Type of the source. See notes on RelatedEntityPurposeKey for details. |
| SourceEntityType |  | yes | yes |  |  | Gets or sets the type of the source entity. See notes on RelatedEntityPurposeKey for details. |
| SourceEntityTypeId | yes | yes |  | yes |  | Gets or sets the EntityTypeId for the Entity Type of source entity. See notes on RelatedEntityPurposeKey for details. |
| SupportedActions |  |  | yes |  |  |  |
| TargetEntityId | yes | yes |  | yes |  | Gets or sets the EntityId of the Entity Type of the target. See notes on RelatedEntityPurposeKey for details. |
| TargetEntityType |  | yes | yes |  |  | Gets or sets the type of the target entity. See notes on RelatedEntityPurposeKey for details. |
| TargetEntityTypeId | yes | yes |  | yes |  | Gets or sets the EntityTypeId for the Entity Type of target entity. See notes on RelatedEntityPurposeKey for details. |
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
| SourceEntityType | Gets or sets the type of the source entity. See notes on RelatedEntityPurposeKey for details. |
| TargetEntityType | Gets or sets the type of the target entity. See notes on RelatedEntityPurposeKey for details. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| SourceEntityId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| SourceEntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| TargetEntityId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| TargetEntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
