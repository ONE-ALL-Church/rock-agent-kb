# Step Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Engagement`
- Model title: `Step`
- EntityType GUID: `8eadb0dc-17f4-4541-a46e-53f89e21a622`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 62 |
| Database-marked properties | 24 |
| Lava-marked properties | 46 |
| Lava-marked non-database properties | 22 |
| Related model links | 14 |
| Pre-alpha changes touching this model | 3 |

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
| PersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias. |
| PersonAliasId | yes | yes |  | yes |  | Gets or sets the Id of the PersonAlias that identifies the Person associated with taking this step. This property is required. |
| RelatedEntityId | yes | yes |  |  |  | Gets or sets the related entity identifier. |
| RelatedEntityTypeId | yes | yes |  |  |  | Gets or sets the related entity type identifier. |
| StartDateKey | yes | yes |  |  |  | Gets the start date key. |
| StartDateTime | yes | yes |  |  |  | Gets or sets the DateTime associated with the start of this step. |
| StartSourceDate |  | yes | yes |  |  | Gets or sets the start source date. |
| StepAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| StepProgramCompletion |  | yes | yes |  |  | Gets or sets the StepProgramCompletion. |
| StepProgramCompletionId | yes | yes |  |  |  | Gets or sets the Id of the StepProgramCompletion to which this step belongs. |
| StepStatus |  | yes | yes |  |  | Gets or sets the StepStatus. |
| StepStatusId | yes | yes |  |  |  | Gets or sets the Id of the StepStatus to which this step belongs. |
| StepType |  | yes | yes |  |  | Gets or sets the StepType. |
| StepTypeId | yes | yes |  | yes |  | Gets or sets the Id of the StepType to which this step belongs. This property is required. |
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
| PersonAlias | Gets or sets the PersonAlias. |
| StartSourceDate | Gets or sets the start source date. |
| StepProgramCompletion | Gets or sets the StepProgramCompletion. |
| StepStatus | Gets or sets the StepStatus. |
| StepType | Gets or sets the StepType. |
| StepWorkflows | Gets or sets a collection containing the StepWorkflows that are of this step. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Campus | [Campus](campus.md) |  |
| CampusId | [Campus](campus.md) |  |
| CompletedDateTime | DateTime |  |
| EndDateTime | DateTime |  |
| PersonAlias | [PersonAlias](person-alias.md) |  |
| PersonAliasId | [PersonAlias](person-alias.md) |  |
| StartDateTime | DateTime |  |
| StepProgramCompletion | [StepProgramCompletion](step-program-completion.md) |  |
| StepProgramCompletionId | [StepProgramCompletion](step-program-completion.md) |  |
| StepStatus | [StepStatus](step-status.md) |  |
| StepStatusId | [StepStatus](step-status.md) |  |
| StepType | [StepType](step-type.md) |  |
| StepTypeId | [StepType](step-type.md) |  |
| StepWorkflows | StepWorkflows |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | CompletedDateTime | related_entity_links |
| property_changed | EndDateTime | related_entity_links |
| property_changed | StartDateTime | related_entity_links |
