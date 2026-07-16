# AI Agent Session Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `AI`
- Model title: `AIAgentSession`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `2415941a-8a3f-49fe-8039-db27096b0edf`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 28 |
| Database-marked properties | 12 |
| Lava-marked properties | 19 |
| Lava-marked non-database properties | 7 |
| Related model links | 2 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AIAgent |  |  | yes |  |  | The agent that the session is associated with. |
| AIAgentId | yes | yes |  | yes |  | The identifier of the agent that the session is associated with. |
| AIAgentSessionAnchors |  | yes | yes |  |  | A collection containing the AI Agent Session Anchor entities that represent the anchors that provide context to the session. |
| AIAgentSessionHistories |  | yes | yes |  |  | A collection containing the AI Agent Session History entities that represent the chat history records for this session. |
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
| SessionType | yes | yes |  |  |  | The type of session represented by this instance. This is a hard coded list of values defined in the code as an enumeration. |
| StartDateTime | yes | yes |  |  |  | The date and time the session was started. This will be set automatically when the session is created. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AIAgentSessionAnchors | A collection containing the AI Agent Session Anchor entities that represent the anchors that provide context to the session. |
| AIAgentSessionHistories | A collection containing the AI Agent Session History entities that represent the chat history records for this session. |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AIAgentSessionAnchors | [AI Agent Session Anchor](ai-agent-session-anchor.md) | 3ed1476a-b7fc-40e2-bbab-af084c82d7f1 |
| AIAgentSessionHistories | [AI Agent Session History](ai-agent-session-history.md) | 6ad212be-f8d0-4c58-ab0e-d723ed5e2155 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
