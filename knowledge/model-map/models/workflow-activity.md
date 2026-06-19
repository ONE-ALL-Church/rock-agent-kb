# Workflow Activity Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Workflow`
- Model title: `WorkflowActivity`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `38`
- Obsolete methods: `4`
- EntityType GUID: `2cb52ed0-cb06-4d62-9e2c-73b60afa4c9f`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 53 |
| Database-marked properties | 17 |
| Lava-marked properties | 38 |
| Lava-marked non-database properties | 21 |
| Related model links | 6 |
| Method signatures | 38 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| Actions |  | yes | yes |  |  | Gets or sets a collection containing the WorkflowActions that are run by this WorkflowActivity. |
| ActivatedByActivity |  | yes | yes |  |  | Gets or sets the activated by activity. |
| ActivatedByActivityId | yes | yes |  |  |  | Gets or sets the activated by activity identifier. |
| ActivatedDateTime | yes | yes |  |  |  | Gets or sets the date and time that this WorkflowActivity was activated. |
| ActiveActions |  | yes | yes |  |  | Gets an enumerable collection containing the active WorkflowActions for this WorkflowActivity, ordered by their order property. |
| ActivityType |  | yes | yes |  |  | Gets or sets the Workflow Activity Type that is being performed by this WorkflowActivity instance. |
| ActivityTypeCache |  | yes | yes |  |  | Gets the activity type cache. |
| ActivityTypeId | yes | yes |  |  |  | Gets or sets the ActivityTypeId of the Workflow Activity Type that is being executed. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AssignedGroup |  | yes | yes |  |  | Gets or sets the assigned group. |
| AssignedGroupId | yes | yes |  |  |  | Gets or sets the assigned group identifier. |
| AssignedPersonAlias |  | yes | yes |  |  | Gets or sets the assigned person alias. |
| AssignedPersonAliasId | yes | yes |  |  |  | Gets or sets the assigned person alias identifier. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CompletedDateTime | yes | yes |  |  |  | Gets or sets the date and time that this WorkflowActivity completed. |
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
| IsActive |  | yes | yes |  |  | Gets a value indicating whether this WorkflowActivity instance is active. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastProcessedDateTime | yes | yes |  |  |  | Gets or sets the date and time that this WorkflowActivity was last processed. |
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
| Workflow |  | yes | yes |  |  | Gets or sets the Workflow instance that is performing this WorkflowActivity. |
| WorkflowActivityAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| WorkflowId | yes | yes |  |  |  | Gets or sets the WorkflowId of the Workflow instance that is performing this WorkflowActivity. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Actions | Gets or sets a collection containing the WorkflowActions that are run by this WorkflowActivity. |
| ActivatedByActivity | Gets or sets the activated by activity. |
| ActiveActions | Gets an enumerable collection containing the active WorkflowActions for this WorkflowActivity, ordered by their order property. |
| ActivityType | Gets or sets the Workflow Activity Type that is being performed by this WorkflowActivity instance. |
| ActivityTypeCache | Gets the activity type cache. |
| AssignedGroup | Gets or sets the assigned group. |
| AssignedPersonAlias | Gets or sets the assigned person alias. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| IsActive | Gets a value indicating whether this WorkflowActivity instance is active. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| Workflow | Gets or sets the Workflow instance that is performing this WorkflowActivity. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Actions | WorkflowActions | 9cbf4bec-5653-47f9-8e87-0d31c6ca5947 |
| ActiveActions | WorkflowActions | 9cbf4bec-5653-47f9-8e87-0d31c6ca5947 |
| ActivityType | [Workflow Activity Type](workflow-activity-type.md) | e5fbdba2-9539-4679-b948-2e06c1bb1e3f |
| ActivityTypeId | [Workflow Activity Type](workflow-activity-type.md) | e5fbdba2-9539-4679-b948-2e06c1bb1e3f |
| Workflow | [Workflow](workflow.md) | 3540e9a7-fe30-43a9-8b0a-a372b63dfc93 |
| WorkflowId | [Workflow](workflow.md) | 3540e9a7-fe30-43a9-8b0a-a372b63dfc93 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
