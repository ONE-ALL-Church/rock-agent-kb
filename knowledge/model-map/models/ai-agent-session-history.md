# AI Agent Session History Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `AI`
- Model title: `AIAgentSessionHistory`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `6ad212be-f8d0-4c58-ab0e-d723ed5e2155`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 27 |
| Database-marked properties | 14 |
| Lava-marked properties | 19 |
| Lava-marked non-database properties | 5 |
| Related model links | 0 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AIAgentSession |  |  | yes |  |  | The session that the history is associated with. |
| AIAgentSessionId | yes | yes |  | yes |  | The identifier of the session that the history is associated with. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ConsumedTokenCount | yes | yes |  |  |  | The number of tokens that were consumed by the entire request sent to the language model. This is only relevant for messages that were returned by the language model, not user messages. This may be 0 if the token count could not be determined. |
| ContextKey |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsCurrentlyInContext | yes | yes |  |  |  | Indicates whether the message is currently in context for the session. A message that is in context is included in the chat history and can be used to generate new responses. |
| IsSummary | yes | yes |  |  |  | Indicates whether the message is a summary of the session. This is used when the chat history grows too large and must be summarized to stay relevant. Only one summary message should be marked as IsCurrentlyInContext. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Message | yes | yes |  |  |  | The text content of the message. |
| MessageDateTime | yes | yes |  |  |  | The date and time the message was posted. |
| MessageRole | yes | yes |  |  |  | The role of the message in the session chat history. This is used to determine if this was a message from the individual, a response from the agent, or some other message type. This is a hard coded list of values defined in the code as an enumeration. |
| TokenCount | yes | yes |  |  |  | The number of tokens used for the message. This may be an estimate depending on the type of message. This may be 0 if the token count could not be determined. |
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
