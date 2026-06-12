# Group Member Requirement Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Group`
- Model title: `GroupMemberRequirement`
- EntityType GUID: `ff1b2c4b-0f2d-4d9b-9e85-7336ccc24a62`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 57 |
| Database-marked properties | 24 |
| Lava-marked properties | 40 |
| Lava-marked non-database properties | 16 |
| Related model links | 11 |
| Pre-alpha changes touching this model | 1 |

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
| GroupMember |  | yes | yes |  |  | Gets or sets the GroupMember. |
| GroupMemberId | yes | yes |  | yes |  | Gets or sets the group member identifier. |
| GroupMemberRequirementAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupRequirement |  | yes | yes |  |  | Gets or sets the GroupRequirement. |
| GroupRequirementId | yes | yes |  | yes |  | Gets or sets the GroupRequirement identifier. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastRequirementCheckDateTime | yes | yes |  |  |  | Gets or sets the last requirement check date time. |
| ManuallyCompletedByPersonAlias |  |  | yes |  |  | Gets or sets the PersonAlias of the person who manually completed the member requirement. |
| ManuallyCompletedByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAliasId that manually completed this member requirement. |
| ManuallyCompletedDateTime | yes | yes |  |  |  | Gets or sets the manually completed date for the group member requirement. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| OverriddenByPersonAlias |  |  | yes |  |  | Gets or sets the PersonAlias of the person who overrode the member requirement. |
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
| GroupMember | Gets or sets the GroupMember. |
| GroupRequirement | Gets or sets the GroupRequirement. |
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
| DoesNotMeetWorkflow | [Workflow](workflow.md) |  |
| DoesNotMeetWorkflowId | [Workflow](workflow.md) |  |
| GroupMember | [GroupMember](group-member.md) |  |
| GroupRequirement | [GroupRequirement](group-requirement.md) |  |
| GroupRequirementId | [GroupRequirement](group-requirement.md) |  |
| ManuallyCompletedByPersonAlias | [PersonAlias](person-alias.md) |  |
| ManuallyCompletedByPersonAliasId | [PersonAliasId](person-alias.md) |  |
| OverriddenByPersonAlias | [PersonAlias](person-alias.md) |  |
| OverriddenByPersonAliasId | [PersonAliasId](person-alias.md) |  |
| WarningWorkflow | [Workflow](workflow.md) |  |
| WarningWorkflowId | [Workflow](workflow.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | GroupMemberRequirementState |  |
