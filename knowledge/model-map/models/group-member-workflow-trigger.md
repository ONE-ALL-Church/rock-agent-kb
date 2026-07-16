# Group Member Workflow Trigger Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Group`
- Model title: `GroupMemberWorkflowTrigger`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `3ce3406a-1ffe-4cca-a8d5-916eef800d76`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 29 |
| Database-marked properties | 14 |
| Lava-marked properties | 22 |
| Lava-marked non-database properties | 8 |
| Related model links | 6 |
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
| Group |  | yes | yes |  |  | Gets or sets the Group. |
| GroupId | yes | yes |  |  |  | Gets or sets the Group identifier. |
| GroupType |  | yes | yes |  |  | Gets or sets the type of the group. |
| GroupTypeId | yes | yes |  |  |  | Gets or sets the Group Type identifier. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if the WorkflowTrigger is active. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the name. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| TriggerType | yes | yes |  | yes |  | Gets or sets the type of the trigger. This is a hard coded list of values defined in the code as an enumeration. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| TypeQualifier | yes | yes |  |  |  | Gets or sets the type qualifier. |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowName | yes | yes |  |  |  | Gets or sets the name of the workflow trigger. |
| WorkflowType |  | yes | yes |  |  | Gets or sets the Workflow Type that is executed by this WorkflowTrigger. |
| WorkflowTypeId | yes | yes |  | yes |  | Gets or sets the WorkflowTypeId of the Workflow Type that is executed by this WorkflowTrigger. This property is required. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| Group | Gets or sets the Group. |
| GroupType | Gets or sets the type of the group. |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WorkflowType | Gets or sets the Workflow Type that is executed by this WorkflowTrigger. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupType | type | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |
| GroupTypeId | [Group Type](group-type.md) | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |
| WorkflowType | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| WorkflowTypeId | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
