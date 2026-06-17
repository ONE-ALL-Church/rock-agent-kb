# Workflow Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Workflow`
- Model title: `Workflow`
- EntityType GUID: `3540e9a7-fe30-43a9-8b0a-a372b63dfc93`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 60 |
| Database-marked properties | 22 |
| Lava-marked properties | 42 |
| Lava-marked non-database properties | 20 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| ActivatedDateTime | yes | yes |  |  |  | Gets or sets the date and time that this Workflow instance was activated. |
| ActiveActivities |  |  | yes |  |  | Gets an enumerable collection of the Active WorkflowActivities for this Workflow instance, ordered by their order value. |
| ActiveActivityNames |  |  | yes |  |  | Gets the active activity names. |
| Activities |  | yes | yes |  |  | Gets or sets a collection containing all the WorkflowActivities that are a part of this Workflow instance. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the campus tied to the CampusId. |
| CampusId | yes | yes |  |  |  | Gets or sets the Campus Id of the workflow campus |
| CompletedDateTime | yes | yes |  |  |  | Gets or sets the date and time that the Workflow completed. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a description or summary about this Workflow instance. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  | Gets or sets the Entity Id. |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityTypeId | yes | yes |  |  |  | Gets or sets the Entity Type Id. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HasActiveActivities |  |  | yes |  |  | Gets a flag indicating whether this instance has active activities. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InitiatorPersonAlias |  | yes | yes |  |  | Gets or sets the initiator person alias. |
| InitiatorPersonAliasId | yes | yes |  |  |  | Gets or sets the initiator person alias identifier. |
| IsActive |  | yes | yes |  |  | Gets a flag indicating whether this Workflow instance is active. |
| IsPersisted |  | yes | yes |  |  | Gets or sets a value indicating whether this instance is persisted. |
| IsProcessing | yes | yes |  |  |  | Gets or sets a flag indicating whether this instance is processing. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastProcessedDateTime | yes | yes |  |  |  | Gets or sets the date and time that the Workflow was last processed. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets a friendly name for this Workflow instance. This property is required. |
| ParentAuthority |  |  | yes |  |  | A parent authority. If a user is not specifically allowed or denied access to this object, Rock will check the default authorization on the current type, and then the authorization on the Rock.Security.GlobalDefault entity |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Status | yes | yes |  | yes |  | Gets or sets the status of this Workflow instance. This property is required. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| WorkflowId |  | yes | yes |  |  | This value is a string of the WorkflowType's WorkflowIdPrefix combined with the WorkflowIdNumber. |
| WorkflowIdNumber | yes | yes |  |  |  | A type specific number to uniquely identify a workflow. |
| WorkflowType |  | yes | yes |  |  | Gets or sets the Workflow Type that is being executed in this persisted Workflow instance. |
| WorkflowTypeCache |  | yes | yes |  |  | Gets the workflow type cache. |
| WorkflowTypeId | yes | yes |  |  |  | Gets or sets the WorkflowTypeId of the Workflow Type that this Workflow instance is executing. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Activities | Gets or sets a collection containing all the WorkflowActivities that are a part of this Workflow instance. |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the campus tied to the CampusId. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| InitiatorPersonAlias | Gets or sets the initiator person alias. |
| IsActive | Gets a flag indicating whether this Workflow instance is active. |
| IsPersisted | Gets or sets a value indicating whether this instance is persisted. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WorkflowId | This value is a string of the WorkflowType's WorkflowIdPrefix combined with the WorkflowIdNumber. |
| WorkflowType | Gets or sets the Workflow Type that is being executed in this persisted Workflow instance. |
| WorkflowTypeCache | Gets the workflow type cache. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ActiveActivities | WorkflowActivities | 2cb52ed0-cb06-4d62-9e2c-73b60afa4c9f |
| Activities | WorkflowActivities | 2cb52ed0-cb06-4d62-9e2c-73b60afa4c9f |
| WorkflowType | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| WorkflowTypeId | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
