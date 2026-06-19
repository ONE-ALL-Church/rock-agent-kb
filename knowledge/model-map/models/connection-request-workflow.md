# Connection Request Workflow Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Engagement`
- Model title: `ConnectionRequestWorkflow`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `c69d1c9f-5521-4c83-8fe9-5044ecc2ce65`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 44 |
| Database-marked properties | 14 |
| Lava-marked properties | 29 |
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
| ConnectionRequest |  | yes | yes |  |  | Gets or sets the Connection Request. |
| ConnectionRequestId | yes | yes |  | yes |  | Gets or sets the Connection Request identifier. |
| ConnectionRequestWorkflowAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ConnectionWorkflow |  | yes | yes |  |  | Gets or sets the Connection Workflow. |
| ConnectionWorkflowId | yes | yes |  | yes |  | Gets or sets the Connection Workflow identifier. |
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
| SupportedActions |  |  | yes |  |  |  |
| TriggerQualifier | yes | yes |  |  |  | Gets or sets the trigger qualifier. |
| TriggerType | yes | yes |  |  |  | Gets or sets the type of the trigger. This is a hard coded list of values defined in the code as an enumeration. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| Workflow |  | yes | yes |  |  | Gets or sets the Workflow. |
| WorkflowId | yes | yes |  | yes |  | Gets or sets the Workflow identifier. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| ConnectionRequest | Gets or sets the Connection Request. |
| ConnectionWorkflow | Gets or sets the Connection Workflow. |
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
| Workflow | Gets or sets the Workflow. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ConnectionRequest | [Connection Request](connection-request.md) | 36b0d0c7-8125-48fa-9da2-729aaa65f718 |
| ConnectionRequestId | [Connection Request](connection-request.md) | 36b0d0c7-8125-48fa-9da2-729aaa65f718 |
| ConnectionWorkflow | [Connection Workflow](connection-workflow.md) | 4eb8711f-7301-4699-a223-0505a7ceb20a |
| ConnectionWorkflowId | [Connection Workflow](connection-workflow.md) | 4eb8711f-7301-4699-a223-0505a7ceb20a |
| Workflow | [Workflow](workflow.md) | 3540e9a7-fe30-43a9-8b0a-a372b63dfc93 |
| WorkflowId | [Workflow](workflow.md) | 3540e9a7-fe30-43a9-8b0a-a372b63dfc93 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
