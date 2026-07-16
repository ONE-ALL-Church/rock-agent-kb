# Step Workflow Trigger Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Engagement`
- Model title: `StepWorkflowTrigger`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `55c1d610-d42f-4e08-9cd9-1ec9801bc4e3`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 47 |
| Database-marked properties | 16 |
| Lava-marked properties | 32 |
| Lava-marked non-database properties | 16 |
| Related model links | 7 |
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
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if this item is active or not. |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| StepProgram |  | yes | yes |  |  | Gets or sets the Step Program. |
| StepProgramId | yes | yes |  |  |  | Gets or sets the Id of the Step Program by which this Workflow is triggered. |
| StepType |  | yes | yes |  |  | Gets or sets the Step Type. |
| StepTypeId | yes | yes |  |  |  | Gets or sets the Id of the Step Type by which this Workflow is triggered. |
| StepWorkflowTriggerAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| StepWorkflows |  | yes | yes |  |  | Gets or sets a collection containing the StepWorkflows that are of this trigger. |
| SupportedActions |  |  | yes |  |  |  |
| TriggerType | yes | yes |  | yes |  | Gets or sets the type of the trigger. This is a hard coded list of values defined in the code as an enumeration. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| TypeQualifier | yes | yes |  |  |  | Gets or sets the type qualifier. |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowName | yes | yes |  |  |  | Gets or sets the name of the workflow trigger. |
| WorkflowType |  | yes | yes |  |  | Gets or sets the Workflow Type. |
| WorkflowTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Workflow Type that is triggered. This property is required. |

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
| StepProgram | Gets or sets the Step Program. |
| StepType | Gets or sets the Step Type. |
| StepWorkflows | Gets or sets a collection containing the StepWorkflows that are of this trigger. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WorkflowType | Gets or sets the Workflow Type. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| StepProgram | [Step Program](step-program.md) | e89f9528-a74e-41b7-8b65-b56b4ce7a122 |
| StepProgramId | [Step Program](step-program.md) | e89f9528-a74e-41b7-8b65-b56b4ce7a122 |
| StepType | [Step Type](step-type.md) | 5e795620-9f16-49d2-9030-947c0e348a8e |
| StepTypeId | [Step Type](step-type.md) | 5e795620-9f16-49d2-9030-947c0e348a8e |
| StepWorkflows | StepWorkflows | 9e164dcb-2b3c-49db-a3da-e25e24bb23b9 |
| WorkflowType | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| WorkflowTypeId | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
