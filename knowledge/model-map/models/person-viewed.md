# Person Viewed Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `CRM`
- Model title: `PersonViewed`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `af13df44-4ee7-4492-aee4-6bd2a62f9c76`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 24 |
| Database-marked properties | 10 |
| Lava-marked properties | 17 |
| Lava-marked non-database properties | 7 |
| Related model links | 4 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
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
| IpAddress | yes | yes |  |  |  | Gets or sets the IP address of the computer/device that requested the page view. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Source | yes | yes |  |  |  | Gets or sets the source of the view (site id or application name) |
| TargetPersonAlias |  | yes | yes |  |  | Gets or sets the Person entity of the individual who was viewed. |
| TargetPersonAliasId | yes | yes |  |  |  | Gets or sets the Id of the Target/Viewed Person. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| ViewDateTime | yes | yes |  |  |  | Gets or sets the Date and Time that the that the person was viewed. |
| ViewerPersonAlias |  | yes | yes |  |  | Gets or sets the Person entity of the viewer. |
| ViewerPersonAliasId | yes | yes |  |  |  | Gets or sets the Id of the Person that was the viewer. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| IdKey |  |
| TargetPersonAlias | Gets or sets the Person entity of the individual who was viewed. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| ViewerPersonAlias | Gets or sets the Person entity of the viewer. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| TargetPersonAlias | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| TargetPersonAliasId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| ViewerPersonAlias | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| ViewerPersonAliasId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
