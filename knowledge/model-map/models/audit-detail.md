# Audit Detail Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `AuditDetail`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `00a4323f-4a05-4e6a-8480-35d8b7bb6615`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 22 |
| Database-marked properties | 9 |
| Lava-marked properties | 15 |
| Lava-marked non-database properties | 6 |
| Related model links | 2 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Audit |  | yes | yes |  |  | Gets or sets the Audit parent entity. |
| AuditId | yes | yes |  | yes |  | Gets or sets the EntityTypeId for the Entity Type of entity that was modified. This property is required. |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CurrentValue | yes | yes |  |  |  | Gets or sets the Current Value. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| OriginalValue | yes | yes |  |  |  | Gets or sets the Original Value. |
| Property | yes | yes |  | yes |  | Gets or sets the Property. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Audit | Gets or sets the Audit parent entity. |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Audit | [Audit](audit.md) | 5de389e2-4e25-4bb0-8292-67a94ecb379b |
| AuditId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
