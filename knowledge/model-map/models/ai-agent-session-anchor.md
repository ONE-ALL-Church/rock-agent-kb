# AI Agent Session Anchor Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `AI`
- Model title: `AIAgentSessionAnchor`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `3ed1476a-b7fc-40e2-bbab-af084c82d7f1`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 29 |
| Database-marked properties | 15 |
| Lava-marked properties | 20 |
| Lava-marked non-database properties | 5 |
| Related model links | 0 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AIAgentSession |  |  | yes |  |  | The session that the history is associated with. |
| AIAgentSessionId | yes | yes |  | yes |  | The identifier of the session that the anchor is associated with. |
| AddedDateTime | yes | yes |  |  |  | The date and time the anchor was added to the session. This will be set automatically when the anchor is created. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  | The identifier of the entity that this anchor is associated with. |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  |  | yes |  |  | The entity type that EntityId is referring to. |
| EntityTypeId | yes | yes |  |  |  | The identifier of the entity type that EntityId is referring to. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Indicates whether the anchor is currently active. An anchor that is not active will not be sent to the language model. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastRefreshedDateTime | yes | yes |  |  |  | The date and time the payload was last refreshed. This is used to automatically refresh the payload after a period of time. This is required since the referenced entity might have changed. |
| Name | yes | yes |  |  |  | The name of the entity that this anchor is associated with. This is used to help identify the anchor in the UI. It may not always be in sync with the actual entity. |
| PayloadJson | yes | yes |  |  |  | The JSON payload that contains the context for the anchor. This exact contents will vary based on the entity type. |
| RemovedDateTime | yes | yes |  |  |  | The date and time the anchor was removed from the session. This will be set automatically when the anchor is made inactive. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
