# Group Requirement Type Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Group`
- Model title: `GroupRequirementType`
- EntityType GUID: `8e67e852-d1bf-485c-9898-09f19998cc40`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 65 |
| Database-marked properties | 33 |
| Lava-marked properties | 50 |
| Lava-marked non-database properties | 17 |
| Related model links | 7 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CanExpire | yes | yes |  | yes |  | Gets or sets a value indicating whether this requirement can expire. |
| Category |  | yes | yes |  |  | Gets or sets the category. |
| CategoryId | yes | yes |  |  |  | Gets or sets the category identifier. |
| CheckboxLabel | yes | yes |  |  |  | Gets or sets the checkbox label. This is the text that is used for the checkbox if this is a manually set requirement |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DataView |  | yes | yes |  |  | Gets or sets the DataView. |
| DataViewId | yes | yes |  |  |  | Gets or sets the DataView identifier. |
| Description | yes | yes |  |  |  | Gets or sets the description. |
| DoesNotMeetWorkflowLinkText | yes | yes |  |  |  | Gets or sets the text for the "Does Not Meet" workflow link. |
| DoesNotMeetWorkflowType |  | yes | yes |  |  | Gets or sets "Does Not Meet" workflow type. |
| DoesNotMeetWorkflowTypeId | yes | yes |  |  |  | Gets or sets the WorkflowType identifier for the group requirement type it does not meet. |
| DueDateOffsetInDays | yes | yes |  |  |  | Gets or sets the number of days before the requirement is due. |
| DueDateType | yes | yes |  |  |  | Gets or sets the type of due date. This is a hard coded list of values defined in the code as an enumeration. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExpireInDays | yes | yes |  |  |  | Gets or sets the number of days after the requirement is met before it expires (If CanExpire is true). NULL means never expires |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GroupRequirementTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class. |
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
| Name | yes | yes |  | yes |  | Gets or sets the name. |
| NegativeLabel | yes | yes |  |  |  | Gets or sets the negative label. This is the text that is displayed when the requirement is not met. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PositiveLabel | yes | yes |  |  |  | Gets or sets the positive label. This is the text that is displayed when the requirement is met. |
| RequirementCheckType | yes | yes |  |  |  | Gets or sets the type of the requirement check. This is a hard coded list of values defined in the code as an enumeration. |
| ShouldAutoInitiateDoesNotMeetWorkflow | yes | yes |  |  |  | Gets or sets a value indicating whether this requirement type's "Does Not Meet" workflow should auto-initiate. |
| ShouldAutoInitiateWarningWorkflow | yes | yes |  |  |  | Gets or sets a value indicating whether this requirement type's "Warning" workflow should auto-initiate. |
| SqlExpression | yes | yes |  |  |  | Gets or sets the SQL expression. |
| Summary | yes | yes |  |  |  | Gets or sets the summary. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WarningDataView |  | yes | yes |  |  | Gets or sets the warning DataView. |
| WarningDataViewId | yes | yes |  |  |  | Gets or sets the warning DataView identifier. |
| WarningLabel | yes | yes |  |  |  | Gets or sets the warning label. |
| WarningSqlExpression | yes | yes |  |  |  | Gets or sets the warning SQL expression. |
| WarningWorkflowLinkText | yes | yes |  |  |  | Gets or sets the text for the "Warning" workflow link. |
| WarningWorkflowType |  | yes | yes |  |  | Gets or sets "Warning" workflow type. |
| WarningWorkflowTypeId | yes | yes |  |  |  | Gets or sets the WorkflowType identifier for the group requirement type's warning. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the category. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DataView | Gets or sets the DataView. |
| DoesNotMeetWorkflowType | Gets or sets "Does Not Meet" workflow type. |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WarningDataView | Gets or sets the warning DataView. |
| WarningWorkflowType | Gets or sets "Warning" workflow type. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| DataView | [DataView](data-view.md) |  |
| DataViewId | [DataView](data-view.md) |  |
| DoesNotMeetWorkflowTypeId | [WorkflowType](workflow-type.md) |  |
| SupportedActions | Dictionary`2 |  |
| WarningDataView | [DataView](data-view.md) |  |
| WarningDataViewId | [DataView](data-view.md) |  |
| WarningWorkflowTypeId | [WorkflowType](workflow-type.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | SupportedActions | related_entity_links |
