# Step Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Engagement`
- Model title: `Step`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `8eadb0dc-17f4-4541-a46e-53f89e21a622`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 62 |
| Database-marked properties | 24 |
| Lava-marked properties | 46 |
| Lava-marked non-database properties | 22 |
| Related model links | 11 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the Campus. |
| CampusId | yes | yes |  |  |  | Gets or sets the Id of the Campus associated with this step. |
| Caption |  |  | yes |  |  | Gets or sets the caption. |
| CompletedDateKey | yes | yes |  |  |  | Gets the completed date key. |
| CompletedDateTime | yes | yes |  |  |  | Gets or sets the DateTime associated with the completion of this step. |
| CompletedSourceDate |  | yes | yes |  |  | Gets or sets the completed source date. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EndDateKey | yes | yes |  |  |  | Gets the end date key. |
| EndDateTime | yes | yes |  |  |  | Gets or sets the DateTime associated with the end of this step. |
| EndSourceDate |  | yes | yes |  |  | Gets or sets the end source date. |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsComplete |  | yes | yes |  |  | Indicates if this step has been completed |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Note | yes | yes |  |  |  | Gets or sets the note. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  | A parent authority. If a user is not specifically allowed or denied access to this object, Rock will check the default authorization on the current type, and then the authorization on the Rock.Security.GlobalDefault entity |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias. |
| PersonAliasId | yes | yes |  | yes |  | Gets or sets the Id of the Person Alias that identifies the Person associated with taking this step. This property is required. |
| RelatedEntityId | yes | yes |  |  |  | Gets or sets the related entity identifier. |
| RelatedEntityTypeId | yes | yes |  |  |  | Gets or sets the related entity type identifier. |
| StartDateKey | yes | yes |  |  |  | Gets the start date key. |
| StartDateTime | yes | yes |  |  |  | Gets or sets the DateTime associated with the start of this step. |
| StartSourceDate |  | yes | yes |  |  | Gets or sets the start source date. |
| StepAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| StepProgramCompletion |  | yes | yes |  |  | Gets or sets the Step Program Completion. |
| StepProgramCompletionId | yes | yes |  |  |  | Gets or sets the Id of the Step Program Completion to which this step belongs. |
| StepStatus |  | yes | yes |  |  | Gets or sets the Step Status. |
| StepStatusId | yes | yes |  |  |  | Gets or sets the Id of the Step Status to which this step belongs. |
| StepType |  | yes | yes |  |  | Gets or sets the Step Type. |
| StepTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Step Type to which this step belongs. This property is required. |
| StepWorkflows |  | yes | yes |  |  | Gets or sets a collection containing the StepWorkflows that are of this step. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the Campus. |
| CompletedSourceDate | Gets or sets the completed source date. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EndSourceDate | Gets or sets the end source date. |
| EntityStringValue |  |
| IdKey |  |
| IsComplete | Indicates if this step has been completed |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the Person Alias. |
| StartSourceDate | Gets or sets the start source date. |
| StepProgramCompletion | Gets or sets the Step Program Completion. |
| StepStatus | Gets or sets the Step Status. |
| StepType | Gets or sets the Step Type. |
| StepWorkflows | Gets or sets a collection containing the StepWorkflows that are of this step. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Campus | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| CampusId | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| PersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| PersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| StepProgramCompletion | [Step Program Completion](step-program-completion.md) | b7a9c37d-2b04-4fd3-91bd-dfca50b3cc8c |
| StepProgramCompletionId | [Step Program Completion](step-program-completion.md) | b7a9c37d-2b04-4fd3-91bd-dfca50b3cc8c |
| StepStatus | [Step Status](step-status.md) | 6c270d6a-f126-445b-93f0-5079a968bf4e |
| StepStatusId | [Step Status](step-status.md) | 6c270d6a-f126-445b-93f0-5079a968bf4e |
| StepType | [Step Type](step-type.md) | 5e795620-9f16-49d2-9030-947c0e348a8e |
| StepTypeId | [Step Type](step-type.md) | 5e795620-9f16-49d2-9030-947c0e348a8e |
| StepWorkflows | StepWorkflows | 9e164dcb-2b3c-49db-a3da-e25e24bb23b9 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
