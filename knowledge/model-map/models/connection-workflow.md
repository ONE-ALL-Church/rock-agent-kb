# Connection Workflow Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Engagement`
- Model title: `ConnectionWorkflow`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `4eb8711f-7301-4699-a223-0505a7ceb20a`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 52 |
| Database-marked properties | 18 |
| Lava-marked properties | 37 |
| Lava-marked non-database properties | 19 |
| Related model links | 7 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AppliesToAgeClassification | yes | yes |  |  |  | Gets or sets the Age Classification this workflow applies to. This is a hard coded list of values defined in the code as an enumeration. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ConnectionOpportunity |  | yes | yes |  |  | Gets or sets the Connection Opportunity. |
| ConnectionOpportunityId | yes | yes |  |  |  | Gets or sets the Connection Opportunity identifier. |
| ConnectionType |  | yes | yes |  |  | Gets or sets the type of the connection. |
| ConnectionTypeId | yes | yes |  |  |  | Gets or sets the Connection Type identifier. |
| ConnectionWorkflowAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExcludeDataView |  | yes | yes |  |  | Gets or sets the DataView for exclusion filtering. |
| ExcludeDataViewId | yes | yes |  |  |  | Gets or sets the DataViewId for exclusion filtering. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IncludeDataView |  | yes | yes |  |  | Gets or sets the DataView for inclusion filtering. |
| IncludeDataViewId | yes | yes |  |  |  | Gets or sets the DataViewId for inclusion filtering. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ManualTriggerFilterConnectionStatus |  | yes | yes |  |  | Gets or sets the Connection Status. |
| ManualTriggerFilterConnectionStatusId | yes | yes |  |  |  | Gets or sets Connection Status Id used to filter workflows with manual trigger. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| QualifierValue | yes | yes |  |  |  | Gets or sets the qualifier value. |
| SupportedActions |  |  | yes |  |  |  |
| TriggerType | yes | yes |  |  |  | Gets or sets the type of the trigger. This is a hard coded list of values defined in the code as an enumeration. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowType |  | yes | yes |  |  | Gets or sets the type of the workflow. |
| WorkflowTypeCache |  | yes | yes |  |  | Gets the type of the cache workflow. |
| WorkflowTypeId | yes | yes |  | yes |  | Gets or sets the Workflow Type identifier. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| ConnectionOpportunity | Gets or sets the Connection Opportunity. |
| ConnectionType | Gets or sets the type of the connection. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| ExcludeDataView | Gets or sets the DataView for exclusion filtering. |
| IdKey |  |
| IncludeDataView | Gets or sets the DataView for inclusion filtering. |
| ManualTriggerFilterConnectionStatus | Gets or sets the Connection Status. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WorkflowType | Gets or sets the type of the workflow. |
| WorkflowTypeCache | Gets the type of the cache workflow. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ConnectionOpportunity | [Connection Opportunity](connection-opportunity.md) | 79f64363-bc90-4109-9d31-a5eeb397cb2f |
| ConnectionOpportunityId | [Connection Opportunity](connection-opportunity.md) | 79f64363-bc90-4109-9d31-a5eeb397cb2f |
| ConnectionType | type | b1e52ead-65bd-4c4d-bccd-73368067621d |
| ConnectionTypeId | [Connection Type](connection-type.md) | b1e52ead-65bd-4c4d-bccd-73368067621d |
| ManualTriggerFilterConnectionStatus | [Connection Status](connection-status.md) | f3840c8b-63bf-4f98-ac4a-9336896e589b |
| WorkflowType | type | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| WorkflowTypeId | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
