# Connection Request Workflow Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Engagement`
- Model title: `ConnectionRequestWorkflow`
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
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ConnectionRequest |  | yes | yes |  |  | Gets or sets the ConnectionRequest. |
| ConnectionRequestId | yes | yes |  | yes |  | Gets or sets the ConnectionRequest identifier. |
| ConnectionRequestWorkflowAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ConnectionWorkflow |  | yes | yes |  |  | Gets or sets the ConnectionWorkflow. |
| ConnectionWorkflowId | yes | yes |  | yes |  | Gets or sets the ConnectionWorkflow identifier. |
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
| ConnectionRequest | Gets or sets the ConnectionRequest. |
| ConnectionWorkflow | Gets or sets the ConnectionWorkflow. |
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
| ConnectionRequest | [ConnectionRequest](connection-request.md) |  |
| ConnectionRequestId | [ConnectionRequest](connection-request.md) |  |
| ConnectionWorkflow | [ConnectionWorkflow](connection-workflow.md) |  |
| ConnectionWorkflowId | [ConnectionWorkflow](connection-workflow.md) |  |
| Workflow | [Workflow](workflow.md) |  |
| WorkflowId | [Workflow](workflow.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | TriggerType | enum_values |
