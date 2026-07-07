# AI Skill Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `AI`
- Model title: `AISkill`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `d953ab34-4ab6-47c6-857b-53044a99ed75`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 43 |
| Database-marked properties | 13 |
| Lava-marked properties | 28 |
| Lava-marked non-database properties | 15 |
| Related model links | 2 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AIAgentSkills |  | yes | yes |  |  | A collection containing the AI Agent Skill entities that represent the agents this skill is attached to. |
| AISkillAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| AISkillTools |  | yes | yes |  |  | A collection containing the AI Skill Tool entities that represent the tools this skill has. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CodeEntityType |  | yes | yes |  |  | The entity type that represents the C# class that implements the tools for this skill. If this is not null then the skill and related tools should not allow editing beyond enabling or disabling them. |
| CodeEntityTypeId | yes | yes |  |  |  | The entity type identifier that represents the C# class that implements the tools for this skill. If this is not null then the skill and related tools should not allow editing beyond enabling or disabling them. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | The description of the skill, which provides additional context or information about its intended purpose and functionality. |
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
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | The friendly name of the skill that will be used to identify it in the UI. |
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
| AIAgentSkills | A collection containing the AI Agent Skill entities that represent the agents this skill is attached to. |
| AISkillTools | A collection containing the AI Skill Tool entities that represent the tools this skill has. |
| AttributeValues |  |
| Attributes |  |
| CodeEntityType | The entity type that represents the C# class that implements the tools for this skill. If this is not null then the skill and related tools should not allow editing beyond enabling or disabling them. |
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
| AISkillTools | [AI Skill Tool](ai-skill-tool.md) | 357d2625-fdca-41f8-ab8d-1cf2ce0abeed |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
