# AI Agent Session Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `AI`
- Model title: `AIAgentSession`
- EntityType GUID: `2415941a-8a3f-49fe-8039-db27096b0edf`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 30 |
| Database-marked properties | 13 |
| Lava-marked properties | 20 |
| Lava-marked non-database properties | 7 |
| Related model links | 2 |
| Pre-alpha changes touching this model | 4 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AIAgent |  |  | yes |  |  | The agent that the session is associated with. |
| AIAgentId | yes | yes |  | yes |  | The identifier of the agent that the session is associated with. |
| AIAgentSessionAnchors |  | yes | yes |  |  | A collection containing the AIAgentSessionAnchor entities that represent the anchors that provide context to the session. |
| AIAgentSessionHistories |  | yes | yes |  |  | A collection containing the AIAgentSessionHistory entities that represent the chat history records for this session. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
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
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastMessageDateTime | yes | yes |  |  |  | The date and time the session was last used. This should be updated whenever a new message is added to the session history table. This will be set automatically when the session is first created. |
| Name | yes | yes |  |  |  | An optional name for the session. This can be used to help identify this session later. If no name is specified then the date should be used as a way to identify the session in the UI. |
| PersonAlias |  |  | yes |  |  | The the PersonAlias that owns this session. This is used to ensure that a person cannot view another person's chat history. |
| PersonAliasId | yes | yes |  |  |  | The identifier of the PersonAlias that owns this session. This is used to ensure that a person cannot view another person's chat history. |
| RelatedEntityId | yes | yes |  |  |  | An optional identifier for the specific entity that this session is related to. Multiple sessions can be related to the same entity. |
| RelatedEntityType |  |  | yes |  |  | The type of the entity that this session is related to. |
| RelatedEntityTypeId | yes | yes |  |  |  | An optional identifier for the type of entity that this session is related to. |
| StartDateTime | yes | yes |  |  |  | The date and time the session was started. This will be set automatically when the session is created. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AIAgentSessionAnchors | A collection containing the AIAgentSessionAnchor entities that represent the anchors that provide context to the session. |
| AIAgentSessionHistories | A collection containing the AIAgentSessionHistory entities that represent the chat history records for this session. |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AIAgentSessionAnchors | [AIAgentSessionAnchor](ai-agent-session-anchor.md) |  |
| AIAgentSessionHistories | [AIAgentSessionHistory](ai-agent-session-history.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | SessionType |  |
| property_removed | RelatedEntityId |  |
| property_removed | RelatedEntityType |  |
| property_removed | RelatedEntityTypeId |  |
