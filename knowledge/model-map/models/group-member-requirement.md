# Group Member Requirement Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Group`
- Model title: `GroupMemberRequirement`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `ff1b2c4b-0f2d-4d9b-9e85-7336ccc24a62`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 58 |
| Database-marked properties | 25 |
| Lava-marked properties | 41 |
| Lava-marked non-database properties | 16 |
| Related model links | 11 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DoesNotMeetWorkflow |  | yes | yes |  |  | Gets or sets the "Does Not Meet" Workflow. |
| DoesNotMeetWorkflowId | yes | yes |  |  |  | Gets or sets the "Does Not Meet" Workflow identifier for the group member's requirement. |
| DueDate | yes | yes |  |  |  | Gets or sets the due date for the group member requirement. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GroupMember |  | yes | yes |  |  | Gets or sets the Group Member. |
| GroupMemberId | yes | yes |  | yes |  | Gets or sets the group member identifier. |
| GroupMemberRequirementAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupMemberRequirementState | yes | yes |  | yes |  | Gets the current calculated state of the group member requirement. Note: Normally, properties of this type are named to match the name of their enum. In this case, GroupMemberRequirementState was chosen for improved clarity and readability when used throughout the codebase. This is a hard coded list of values defined in the code as an enumeration. |
| GroupRequirement |  | yes | yes |  |  | Gets or sets the Group Requirement. |
| GroupRequirementId | yes | yes |  | yes |  | Gets or sets the Group Requirement identifier. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastRequirementCheckDateTime | yes | yes |  |  |  | Gets or sets the last requirement check date time. |
| ManuallyCompletedByPersonAlias |  |  | yes |  |  | Gets or sets the Person Alias of the person who manually completed the member requirement. |
| ManuallyCompletedByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAliasId that manually completed this member requirement. |
| ManuallyCompletedDateTime | yes | yes |  |  |  | Gets or sets the manually completed date for the group member requirement. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| OverriddenByPersonAlias |  |  | yes |  |  | Gets or sets the Person Alias of the person who overrode the member requirement. |
| OverriddenByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAliasId that overrode this member requirement. |
| OverriddenDateTime | yes | yes |  |  |  | Gets or sets the overridden date for the group member requirement. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RequirementFailDateTime | yes | yes |  |  |  | Gets or sets the requirement fail date time. |
| RequirementMetDateTime | yes | yes |  |  |  | Gets or sets the requirement met date time. |
| RequirementWarningDateTime | yes | yes |  |  |  | Gets or sets the requirement warning date time. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WarningWorkflow |  | yes | yes |  |  | Gets or sets the "Warning" Workflow. |
| WarningWorkflowId | yes | yes |  |  |  | Gets or sets the "Warning" Workflow identifier for the group member's requirement. |
| WasManuallyCompleted | yes | yes |  |  |  | Gets or sets whether the member requirement was manually completed. |
| WasOverridden | yes | yes |  |  |  | Gets or sets whether the member requirement was overridden. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DoesNotMeetWorkflow | Gets or sets the "Does Not Meet" Workflow. |
| EntityStringValue |  |
| GroupMember | Gets or sets the Group Member. |
| GroupRequirement | Gets or sets the Group Requirement. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WarningWorkflow | Gets or sets the "Warning" Workflow. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| DoesNotMeetWorkflow | [Workflow](workflow.md) | 3540e9a7-fe30-43a9-8b0a-a372b63dfc93 |
| DoesNotMeetWorkflowId | [Workflow](workflow.md) | 3540e9a7-fe30-43a9-8b0a-a372b63dfc93 |
| GroupMember | [Group Member](group-member.md) | 49668b95-fedc-43dd-8085-d2b0d6343c48 |
| GroupRequirement | [Group Requirement](group-requirement.md) | cfc7de86-222e-4669-83c2-a3f5b04cb5d6 |
| GroupRequirementId | [Group Requirement](group-requirement.md) | cfc7de86-222e-4669-83c2-a3f5b04cb5d6 |
| ManuallyCompletedByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| ManuallyCompletedByPersonAliasId | [PersonAliasId](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| OverriddenByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| OverriddenByPersonAliasId | [PersonAliasId](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| WarningWorkflow | [Workflow](workflow.md) | 3540e9a7-fe30-43a9-8b0a-a372b63dfc93 |
| WarningWorkflowId | [Workflow](workflow.md) | 3540e9a7-fe30-43a9-8b0a-a372b63dfc93 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
