# AI Agent Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `AI`
- Model title: `AIAgent`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `ee3fe609-5c7c-492e-b0e9-5461045fc825`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 45 |
| Database-marked properties | 16 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 14 |
| Related model links | 1 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AIAgentAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| AIAgentSkills |  | yes | yes |  |  | A collection containing the AI Agent Skill entities that represent the skills attached to this agent. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AgentType | yes | yes |  |  |  | The type of agent represented by this instance. This is a hard coded list of values defined in the code as an enumeration. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AudienceType | yes | yes |  |  |  | The type of audience that this agent is intended for. This is a hard coded list of values defined in the code as an enumeration. |
| AvailableKeys |  |  | yes |  |  |  |
| AvatarBinaryFile |  | yes | yes |  |  | The binary file that contains the image to use as the avatar to represent the agent. This will be used in the administrative UI and the chat UI to represent the agent visually. |
| AvatarBinaryFileId | yes | yes |  |  |  | The identifier of the binary file that contains the image to use as the avatar to represent the agent. This will be used in the administrative UI and the chat UI to represent the agent visually. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | The description of the agent, which provides additional context or information about its intended purpose and functionality. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| Instructions | yes | yes |  |  |  | When AgentType is Rock.Enums.AI.Agent.AgentType.Chat, this contains the instructions for the agent, which is a string that describes how the agent should behavor or respond. This can include tone, style, and special instructions it should follow when interacting with people. When AgentType is Rock.Enums.AI.Agent.AgentType.Mcp, this contains the instructions that should be sent when a client connects to the MCP server. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | The friendly name of the agent that will be used to identify it in the UI. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AIAgentSkills | A collection containing the AI Agent Skill entities that represent the skills attached to this agent. |
| AttributeValues |  |
| Attributes |  |
| AvatarBinaryFile | The binary file that contains the image to use as the avatar to represent the agent. This will be used in the administrative UI and the chat UI to represent the agent visually. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AIAgentSkills | [AI Agent Skill](ai-agent-skill.md) | 36deda2f-75bd-4bee-ac36-46d20dcd1331 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
