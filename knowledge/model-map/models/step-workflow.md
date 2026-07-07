# Step Workflow Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Engagement`
- Model title: `StepWorkflow`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `9e164dcb-2b3c-49db-a3da-e25e24bb23b9`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 42 |
| Database-marked properties | 12 |
| Lava-marked properties | 27 |
| Lava-marked non-database properties | 15 |
| Related model links | 6 |
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
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Step |  | yes | yes |  |  | Gets or sets the Step. |
| StepId | yes | yes |  | yes |  | Gets or sets the Id of the Step that triggered the workflow. This property is required. |
| StepWorkflowAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| StepWorkflowTrigger |  | yes | yes |  |  | Gets or sets the Step Workflow Trigger. |
| StepWorkflowTriggerId | yes | yes |  | yes |  | Gets or sets the Id of the Step Workflow Trigger by which this Workflow was triggered. This property is required. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| Workflow |  | yes | yes |  |  | Gets or sets the Workflow. |
| WorkflowId | yes | yes |  | yes |  | Gets or sets the Id of the Workflow that was triggered. This property is required. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Step | Gets or sets the Step. |
| StepWorkflowTrigger | Gets or sets the Step Workflow Trigger. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| Workflow | Gets or sets the Workflow. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Step | [Step](step.md) | 8eadb0dc-17f4-4541-a46e-53f89e21a622 |
| StepId | [Step](step.md) | 8eadb0dc-17f4-4541-a46e-53f89e21a622 |
| StepWorkflowTrigger | [Step Workflow Trigger](step-workflow-trigger.md) | 55c1d610-d42f-4e08-9cd9-1ec9801bc4e3 |
| StepWorkflowTriggerId | [Step Workflow Trigger](step-workflow-trigger.md) | 55c1d610-d42f-4e08-9cd9-1ec9801bc4e3 |
| Workflow | [Workflow](workflow.md) | 3540e9a7-fe30-43a9-8b0a-a372b63dfc93 |
| WorkflowId | [Workflow](workflow.md) | 3540e9a7-fe30-43a9-8b0a-a372b63dfc93 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
