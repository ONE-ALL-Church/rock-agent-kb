# Person Alias Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `CRM`
- Model title: `PersonAlias`
- EntityType GUID: `90f5e87b-f0d5-4617-8ae9-eb57e673f36f`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 26 |
| Database-marked properties | 12 |
| Lava-marked properties | 16 |
| Lava-marked non-database properties | 6 |
| Related model links | 2 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AliasEncryptedKey |  |  | yes |  |  | Gets the previous encrypted key for the Person. |
| AliasPersonGuid | yes |  |  |  |  | If AliasPersonId equals PersonId, this is the Guid of the Person. Otherwise, the AliasPersonGuid is the previous person's guid that was merged into a new person record. If this is NULL it is special case where the PersonAlias is or was anonymous. |
| AliasPersonId | yes |  |  |  |  | If AliasPersonId equals PersonId, this is the PrimaryAlias. Otherwise, the AliasPersonId is the previous person id that was merged into a new person record. If this is NULL it is special case where the PersonAlias is or was anonymous. |
| AliasedDateTime | yes | yes |  |  |  | Gets or sets the aliased date time. |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InternalMessage | yes | yes |  |  |  | Gets or sets the internal message. This is used by core Rock to track internal state messages of the record. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastVisitDateTime | yes | yes |  |  |  | Gets or sets the last visit time. |
| Name | yes | yes |  |  |  | Gets or sets the name of the alias |
| Person |  | yes | yes |  |  | Gets or sets the person. |
| PersonId | yes | yes |  | yes |  | Gets or sets the person Id of the Person. This property is required. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| IdKey |  |
| Person | Gets or sets the person. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AliasEncryptedKey | [Person](person.md) |  |
| PersonId | [Person](person.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
