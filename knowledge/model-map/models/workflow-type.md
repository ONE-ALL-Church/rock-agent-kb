# Workflow Type Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Workflow`
- Model title: `WorkflowType`
- EntityType GUID: `c9f3c4a5-1526-474d-803f-d6c7a45cbbae`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 65 |
| Database-marked properties | 35 |
| Lava-marked properties | 49 |
| Lava-marked non-database properties | 15 |
| Related model links | 7 |
| Pre-alpha changes touching this model | 3 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| ActivityTypes |  | yes | yes |  |  | Gets or sets a collection containing the ActivityTypes that will be executed/performed as part of this WorkflowType. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Category |  | yes | yes |  |  | Gets or sets the Category that this WorkflowType belongs to. |
| CategoryId | yes | yes |  |  |  | Gets or sets the CategoryId of the Category that this WorkflowType belongs to. |
| CompletedWorkflowRetentionPeriod | yes | yes |  |  |  | Gets or sets the completed workflow retention period in days. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a user defined description or summary about the WorkflowType. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FormBuilderSettingsJson | yes | yes |  |  |  | Gets or sets the form builder settings json. |
| FormBuilderTemplate |  | yes | yes |  |  | Gets or sets the form builder template. |
| FormBuilderTemplateId | yes | yes |  |  |  | Gets or sets the form builder template identifier. |
| FormEndDateTime | yes | yes |  |  |  | Gets or sets the form end date and time. |
| FormStartDateTime | yes | yes |  |  |  | Gets or sets the form start date and time. |
| Guid | yes | yes |  |  |  |  |
| HasActiveForms | yes |  |  |  |  | Gets a value indicating whether this instance has active forms. |
| IconCssClass | yes | yes |  |  |  | Gets or sets the name of the icon CSS class. This property is only used for CSS based icons. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if this WorkflowType is active. |
| IsFormBuilder | yes | yes |  |  |  | Gets or sets a value indicating whether [is form builder]. |
| IsLoginRequired | yes | yes |  |  |  | Gets or sets a value indicating whether [is login required]. |
| IsPersisted | yes | yes |  |  |  | Gets or sets a value indicating whether Workflow instances of this WorkflowType are persisted. |
| IsSystem | yes | yes |  |  |  | Gets or sets a flag indicating if this WorkflowType is part of the Rock core system/framework. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LogRetentionPeriod | yes | yes |  |  |  | Gets or sets the log retention period in days. |
| LoggingLevel | yes | yes |  |  |  | Gets or sets the logging level. Gets or sets the WorkflowLoggingLevel indicating the level of detail that should be logged when instances of this WorkflowType are executed. This is a hard coded list of values defined in the code as an enumeration. |
| MaxWorkflowAgeDays | yes | yes |  |  |  | Gets or sets the number of days since the creation date after which a workflow would be automatically marked completed. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the friendly Name of the WorkflowType. This property is required. |
| NoActionMessage | yes | yes |  |  |  | Gets or sets the text to be displayed when a workflow of this type workflow is active, but does not have an active form. This field supports Lava. |
| Order | yes | yes |  | yes |  | Gets or sets the display order of the WorkFlowType, the lower the number the higher up that the WorkflowType will display in the workflow list. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ProcessingIntervalSeconds | yes | yes |  |  |  | Gets or sets the minimum length of time, in seconds, before a persisted Workflow instance that implements this WorkflowType can be re-executed. |
| Slug | yes | yes |  |  |  | Gets or sets the slug. |
| SummaryViewText | yes | yes |  |  |  | Gets or sets the summary view text to be displayed when a workflow of this type has no form or has been completed. This field supports Lava. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkTerm | yes | yes |  | yes |  | Gets or sets the work term for the WorkflowType. This is the action that is being performed by this WorkflowType. This property is required. |
| WorkflowExpireDateTime | yes | yes |  |  |  | Gets or sets the date time when the workflow of this type will no longer be processed. |
| WorkflowIdPrefix | yes | yes |  |  |  | Gets or sets the workflow identifier prefix. |
| WorkflowTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ActivityTypes | Gets or sets a collection containing the ActivityTypes that will be executed/performed as part of this WorkflowType. |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the Category that this WorkflowType belongs to. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| FormBuilderTemplate | Gets or sets the form builder template. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ActivityTypes | ActivityTypes |  |
| Category | [Category](category.md) |  |
| CategoryId | [Category](category.md) |  |
| IsPersisted | [Workflow](workflow.md) |  |
| LoggingLevel | WorkflowLoggingLevel |  |
| ProcessingIntervalSeconds | [Workflow](workflow.md) |  |
| SupportedActions | Dictionary`2 |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | LoggingLevel | related_entity_links |
| property_changed | ParentAuthority | description |
| property_changed | SupportedActions | related_entity_links |
