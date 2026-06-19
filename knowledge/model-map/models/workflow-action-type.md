# Workflow Action Type Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Workflow`
- Model title: `WorkflowActionType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `37`
- Obsolete methods: `4`
- EntityType GUID: `23e3273a-b137-48a3-9aff-c8dc832ddca6`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 51 |
| Database-marked properties | 20 |
| Lava-marked properties | 35 |
| Lava-marked non-database properties | 15 |
| Related model links | 5 |
| Method signatures | 37 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| ActivityType |  | yes | yes |  |  | Gets or sets the Workflow Activity Type that performs this ActionType. |
| ActivityTypeId | yes | yes |  |  |  | Gets or sets the ActivityTypeId of the Workflow Activity Type that performs this Action Type. |
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
| CriteriaAttributeGuid | yes | yes |  |  |  | Gets or sets the criteria attribute unique identifier. |
| CriteriaComparisonType | yes | yes |  |  |  | Gets or sets the type of the criteria comparison. This is a hard coded list of values defined in the code as an enumeration. |
| CriteriaValue | yes | yes |  |  |  | Gets or sets the criteria value. |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the Entity Type of that this ActionType is running against. |
| EntityTypeId | yes | yes |  |  |  | Gets or sets the EntityTypeId of the Entity Type that the action is operating against. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActionCompletedIfCriteriaUnmet | yes | yes |  |  |  | Gets or sets the boolean value that determines if an action should be completed if criteria is unmet. |
| IsActionCompletedOnSuccess | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is action completed on success. |
| IsActivityCompletedOnSuccess | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is activity completed on success. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the friendly name of the ActionType |
| Order | yes | yes |  | yes |  | Gets or sets the order of the ActionType in the Workflow Activity Type |
| ParentAuthority |  |  | yes |  |  | Gets the parent security authority for this ActionType. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowAction |  |  | yes |  |  | Gets the ActionComponent |
| WorkflowActionTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| WorkflowForm |  | yes | yes |  |  | Gets or sets the workflow form. |
| WorkflowFormId | yes | yes |  |  |  | Gets or sets the workflow form identifier. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ActivityType | Gets or sets the Workflow Activity Type that performs this ActionType. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the Entity Type of that this ActionType is running against. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WorkflowForm | Gets or sets the workflow form. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ActivityType | [Workflow Activity Type](workflow-activity-type.md) | e5fbdba2-9539-4679-b948-2e06c1bb1e3f |
| ActivityTypeId | [Workflow Activity Type](workflow-activity-type.md) | e5fbdba2-9539-4679-b948-2e06c1bb1e3f |
| EntityType | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| EntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| Order | [Workflow Activity Type](workflow-activity-type.md) | e5fbdba2-9539-4679-b948-2e06c1bb1e3f |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
