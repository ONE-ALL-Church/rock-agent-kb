# Step Type Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Engagement`
- Model title: `StepType`
- EntityType GUID: `5e795620-9f16-49d2-9030-947c0e348a8e`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 70 |
| Database-marked properties | 33 |
| Lava-marked properties | 55 |
| Lava-marked non-database properties | 22 |
| Related model links | 15 |
| Pre-alpha changes touching this model | 2 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AchievementTypes |  | yes | yes |  |  | Gets or sets the achievement types. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowManualEditing | yes | yes |  |  |  | Gets or sets a flag indicating if this item can be edited by a person. |
| AllowMultiple | yes | yes |  |  |  | Gets or sets a flag indicating if this step type allows multiple step records per person. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AudienceDataView |  | yes | yes |  |  | Gets or sets the DataView. The data view reveals the people that are allowed to be considered for this step type. |
| AudienceDataViewId | yes | yes |  |  |  | Gets or sets the Id of the DataView associated with this step type. The data view reveals the people that are allowed to be considered for this step type. |
| AutoCompleteDataView |  | yes | yes |  |  | Gets or sets the DataView. The data view reveals the people that should be considered as having completed this step. |
| AutoCompleteDataViewId | yes | yes |  |  |  | Gets or sets the Id of the DataView associated with this step type. The data view reveals the people that should be considered as having completed this step. |
| AvailableKeys |  |  | yes |  |  |  |
| CallToActionDescription | yes | yes |  |  |  | Gets or sets the description displayed with the call to action button. |
| CallToActionLabel | yes | yes |  |  |  | Gets or sets the label for the call to action button. |
| CallToActionLink | yes | yes |  |  |  | Gets or sets the URL link for the call to action button. |
| CardLavaTemplate | yes | yes |  |  |  | Gets or sets the lava template used to render custom card details. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a description of the step type. |
| EncryptedKey |  |  | yes |  |  |  |
| EngagementType | yes | yes |  |  |  | Gets or sets the engagement type for this step type. This is a hard coded list of values defined in the code as an enumeration. |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HasEndDate | yes | yes |  |  |  | Gets or sets a flag indicating if this step type happens over time (like being in a group) or is it achievement based (like attended a class). |
| HighlightColor | yes | yes |  |  |  | Gets or sets the highlight color for badges and cards. |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| ImpactWeight | yes | yes |  |  |  | Gets or sets the impact weight for this step type (1-5). |
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if this item is active or not. |
| IsDateRequired | yes | yes |  |  |  | Gets or sets a value indicating whether this step requires a date. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Step Type is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MergeTemplate |  | yes | yes |  |  | Gets or sets the MergeTemplate. This template can represent things like certificates or letters. |
| MergeTemplateDescriptor | yes | yes |  |  |  | Gets or sets the name used to describe the merge template (e.g. Certificate). |
| MergeTemplateId | yes | yes |  |  |  | Gets or sets the Id of the MergeTemplate associated with this step type. This template can represent things like certificates or letters. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the step type. This property is required. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| OrganizationalObjectiveValue |  | yes | yes |  |  | Gets or sets the DefinedValue for the organizational objective. |
| OrganizationalObjectiveValueId | yes | yes |  |  |  | Gets or sets the organizational objective for this step type. These are found in the "Organizational Objective" Defined Type. |
| ParentAuthority |  |  | yes |  |  | A parent authority. If a user is not specifically allowed or denied access to this object, Rock will check the default authorization on the current type, and then the authorization on the Rock.Security.GlobalDefault entity |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ShowCountOnBadge | yes | yes |  |  |  | Gets or sets a flag indicating if the number of occurrences should be shown on the badge. |
| StepProgram |  | yes | yes |  |  | Gets or sets the StepProgram. |
| StepProgramId | yes | yes |  | yes |  | Gets or sets the Id of the StepProgram to which this step type belongs. This property is required. |
| StepTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| StepTypeDependencies |  | yes | yes |  |  | Gets or sets a collection containing the Dependencies for this step type. These are StepTypes where this StepType is a prerequisite. These are step types that require this step type to be completed before that step type can be completed. |
| StepTypePrerequisites |  | yes | yes |  |  | Gets or sets a collection containing the Prerequisites for this step type. These are StepTypes that must be completed prior to this step type. |
| StepWorkflowTriggers |  | yes | yes |  |  | Gets or sets a collection containing the StepWorkflowTriggers that are of this step type. |
| Steps |  | yes | yes |  |  | Gets or sets a collection containing the Steps that are of this step type. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AchievementTypes | Gets or sets the achievement types. |
| AttributeValues |  |
| Attributes |  |
| AudienceDataView | Gets or sets the DataView. The data view reveals the people that are allowed to be considered for this step type. |
| AutoCompleteDataView | Gets or sets the DataView. The data view reveals the people that should be considered as having completed this step. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| MergeTemplate | Gets or sets the MergeTemplate. This template can represent things like certificates or letters. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| OrganizationalObjectiveValue | Gets or sets the DefinedValue for the organizational objective. |
| StepProgram | Gets or sets the StepProgram. |
| StepTypeDependencies | Gets or sets a collection containing the Dependencies for this step type. These are StepTypes where this StepType is a prerequisite. These are step types that require this step type to be completed before that step type can be completed. |
| StepTypePrerequisites | Gets or sets a collection containing the Prerequisites for this step type. These are StepTypes that must be completed prior to this step type. |
| StepWorkflowTriggers | Gets or sets a collection containing the StepWorkflowTriggers that are of this step type. |
| Steps | Gets or sets a collection containing the Steps that are of this step type. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AchievementTypes | achievement types |  |
| AudienceDataView | [DataView](data-view.md) |  |
| AudienceDataViewId | [DataView](data-view.md) |  |
| AutoCompleteDataView | [DataView](data-view.md) |  |
| AutoCompleteDataViewId | [DataView](data-view.md) |  |
| MergeTemplate | [MergeTemplate](merge-template.md) |  |
| MergeTemplateId | [MergeTemplate](merge-template.md) |  |
| OrganizationalObjectiveValue | [DefinedValue](defined-value.md) |  |
| StepProgram | [StepProgram](step-program.md) |  |
| StepProgramId | [StepProgram](step-program.md) |  |
| StepTypeDependencies | Dependencies |  |
| StepTypePrerequisites | Prerequisites |  |
| StepWorkflowTriggers | StepWorkflowTriggers |  |
| Steps | Steps |  |
| SupportedActions | Dictionary`2 |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | OrganizationalObjectiveValueId | enum_values |
| property_changed | SupportedActions | related_entity_links |
