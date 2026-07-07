# Audit Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Core`
- Model title: `Audit`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `5de389e2-4e25-4bb0-8292-67a94ecb379b`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 26 |
| Database-marked properties | 11 |
| Lava-marked properties | 19 |
| Lava-marked non-database properties | 8 |
| Related model links | 2 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AuditType | yes | yes |  | yes |  | Gets or sets the type of change that was made to the entity. This property is required. This is a hard coded list of values defined in the code as an enumeration. |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| DateTime | yes | yes |  |  |  | Gets or sets the date and time that the entity was modified and the audit entry was created. |
| Details |  | yes | yes |  |  | Gets or sets the details. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  | yes |  | Gets or sets the Id of the specific entity that was modified. This property is required. |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the Entity Type of the entity that was modified. |
| EntityTypeId | yes | yes |  | yes |  | Gets or sets the EntityTypeId for the Entity Type of entity that was modified. This property is required. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the person alias. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the person alias identifier. |
| Title | yes | yes |  | yes |  | Gets or sets the Name/Title of the specific entity that was updated. This is usually the value that is return when the entity's ToString() function is called. This property is required. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Details | Gets or sets the details. |
| EntityStringValue |  |
| EntityType | Gets or sets the Entity Type of the entity that was modified. |
| IdKey |  |
| PersonAlias | Gets or sets the person alias. |
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
