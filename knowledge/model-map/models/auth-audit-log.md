# Auth Audit Log Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Core`
- Model title: `AuthAuditLog`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `6ac9997f-b238-4a67-933e-d80e1551704d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 34 |
| Database-marked properties | 18 |
| Lava-marked properties | 27 |
| Lava-marked non-database properties | 9 |
| Related model links | 7 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| Action | yes | yes |  | yes |  | Gets or sets the name of action that this Auth entity covers (i.e. view, edit, administrate, etc.). |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ChangeByPersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias that changed the auth. |
| ChangeByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAliasId that changed the auth. |
| ChangeDateTime | yes | yes |  |  |  | Gets or sets the change datetime. |
| ChangeType | yes | yes |  | yes |  | Gets or sets the change type. This is a hard coded list of values defined in the code as an enumeration. |
| ContextKey |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  | Gets or sets the EntityId of the entity that this Auth entity applies to. |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the the Entity Type of the entity that is being secured. |
| EntityTypeId | yes | yes |  | yes |  | Gets or sets the EntityTypeId of the Entity Type for the entity that the Auth object applies to. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Security Role Group that the Auth entity allowed or denied access to. |
| GroupId | yes | yes |  |  |  | Gets or sets the GroupId of the Security Role Group that the Auth entity allowed or denied access to. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias that this Auth entity allows or denies access to. This is used for Person based authorization. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the Id of the Person Alias that this Auth entity allows or denies access to. This is used for user based authorization |
| PostAllowOrDeny | yes | yes |  |  |  | Gets or sets a flag indicating if the Auth entity was post allowed or denied this action for the role. |
| PostOrder | yes | yes |  |  |  | Gets or sets the post order or priority of the Auth entity. |
| PreAllowOrDeny | yes | yes |  |  |  | Gets or sets a flag indicating if the Auth entity was pre allowed or denied this action for the role. |
| PreOrder | yes | yes |  |  |  | Gets or sets the pre order or priority of the Auth entity. |
| SpecialRole | yes | yes |  |  |  | Gets or sets the special role that the Auth entity applies to. This is a hard coded list of values defined in the code as an enumeration. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ChangeByPersonAlias | Gets or sets the Person Alias that changed the auth. |
| EntityStringValue |  |
| EntityType | Gets or sets the the Entity Type of the entity that is being secured. |
| Group | Gets or sets the Security Role Group that the Auth entity allowed or denied access to. |
| IdKey |  |
| PersonAlias | Gets or sets the Person Alias that this Auth entity allows or denies access to. This is used for Person based authorization. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ChangeByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| EntityType | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| EntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| PersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| PersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
