# Workflow Action Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Workflow`
- Model title: `WorkflowAction`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `40`
- Obsolete methods: `4`
- EntityType GUID: `9cbf4bec-5653-47f9-8e87-0d31c6ca5947`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 47 |
| Database-marked properties | 14 |
| Lava-marked properties | 31 |
| Lava-marked non-database properties | 17 |
| Related model links | 4 |
| Method signatures | 40 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| ActionType |  | yes | yes |  |  | Gets or sets the Workflow Action Type that is being executed by this WorkflowAction. |
| ActionTypeCache |  | yes | yes |  |  | Gets the action type cache. |
| ActionTypeId | yes | yes |  |  |  | Gets or sets the ActionTypeId of the Workflow Action that is being executed by this instance. |
| Activity |  | yes | yes |  |  | Gets or sets the Workflow Activity that contains the WorkflowAction. |
| ActivityId | yes | yes |  |  |  | Gets or sets the WorkflowActivityId of the Workflow Activity that this WorkflowAction is a part of. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CompletedDateTime | yes | yes |  |  |  | Gets or sets the date and time that the WorkflowAction completed. |
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
| FormAction | yes | yes |  |  |  | If ActionType is a UserEntryForm Gets or sets the form action. |
| FormAttributes |  | yes | yes |  |  | Gets the form attributes. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive |  | yes | yes |  |  | Gets a value indicating whether this WorkflowAction is active. |
| IsCriteriaValid |  |  | yes |  |  | Gets a value indicating whether this instance is criteria valid. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastProcessedDateTime | yes | yes |  |  |  | Gets or sets the date and time that this WorkflowAction was last processed. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  | Gets the parent security authority for this WorkflowAction. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowActionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ActionType | Gets or sets the Workflow Action Type that is being executed by this WorkflowAction. |
| ActionTypeCache | Gets the action type cache. |
| Activity | Gets or sets the Workflow Activity that contains the WorkflowAction. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| FormAttributes | Gets the form attributes. |
| IdKey |  |
| IsActive | Gets a value indicating whether this WorkflowAction is active. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ActionType | [Workflow Action Type](workflow-action-type.md) | 23e3273a-b137-48a3-9aff-c8dc832ddca6 |
| ActionTypeId | [Workflow Action](workflow-action.md) | 9cbf4bec-5653-47f9-8e87-0d31c6ca5947 |
| Activity | [Workflow Activity](workflow-activity.md) | 2cb52ed0-cb06-4d62-9e2c-73b60afa4c9f |
| ActivityId | [Workflow Activity](workflow-activity.md) | 2cb52ed0-cb06-4d62-9e2c-73b60afa4c9f |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
