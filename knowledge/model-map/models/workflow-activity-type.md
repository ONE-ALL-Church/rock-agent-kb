# Workflow Activity Type Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Workflow`
- Model title: `WorkflowActivityType`
- EntityType GUID: `e5fbdba2-9539-4679-b948-2e06c1bb1e3f`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 44 |
| Database-marked properties | 15 |
| Lava-marked properties | 29 |
| Lava-marked non-database properties | 14 |
| Related model links | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| ActionTypes |  | yes | yes |  |  | Gets or sets a collection containing the WorkflowActionTypes that are performed by this WorkflowActivityType. |
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
| Description | yes | yes |  |  |  | Gets or sets the description or summary about this WorkflowActivityType. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActivatedWithWorkflow | yes | yes |  |  |  | Gets or sets a value indicating if this WorkflowActivityType is activated with the workflow. |
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if this WorkflowActivityType is active. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the friendly Name of this WorkflowActivityType. This property is required. |
| Order | yes | yes |  | yes |  | Gets or sets the order that this WorkflowActivityType will be executed in the WorkflowType's process. |
| ParentAuthority |  |  | yes |  |  | Gets the parent security authority for this WorkflowActivityType. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowActivityTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| WorkflowType |  | yes | yes |  |  | Gets or sets the WorkflowType that runs this WorkflowActivityType. |
| WorkflowTypeId | yes | yes |  |  |  | Gets or sets the WorkflowTypeId of the WorkflowType that this WorkflowActivityType belongs to. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ActionTypes | Gets or sets a collection containing the WorkflowActionTypes that are performed by this WorkflowActivityType. |
| AttributeValues |  |
| Attributes |  |
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
| WorkflowType | Gets or sets the WorkflowType that runs this WorkflowActivityType. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ActionTypes | WorkflowActionTypes |  |
| WorkflowType | [WorkflowType](workflow-type.md) |  |
| WorkflowTypeId | [WorkflowType](workflow-type.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
