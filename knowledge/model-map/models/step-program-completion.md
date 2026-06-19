# Step Program Completion Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Engagement`
- Model title: `StepProgramCompletion`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `b7a9c37d-2b04-4fd3-91bd-dfca50b3cc8c`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 47 |
| Database-marked properties | 16 |
| Lava-marked properties | 32 |
| Lava-marked non-database properties | 16 |
| Related model links | 6 |
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
| Campus |  | yes | yes |  |  | Gets or sets the Campus. This will be the campus from whichever step was completed last (most recently). |
| CampusId | yes | yes |  |  |  | Gets or sets the Campus identifier. This will be the campus from whichever step was completed last (most recently). |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EndDateKey | yes | yes |  |  |  | Gets the end date key. |
| EndDateTime | yes | yes |  |  |  | Gets or sets the DateTime associated with the end of the step program. |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
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
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the person alias. |
| PersonAliasId | yes | yes |  | yes |  | Gets or sets the Id of the Person Alias that identifies the Person associated with the step. This property is required. |
| StartDateKey | yes | yes |  |  |  | Gets the start date key. |
| StartDateTime | yes | yes |  |  |  | Gets or sets the DateTime associated with the start of the step program. |
| StepProgram |  | yes | yes |  |  | Gets or sets the Step Program. |
| StepProgramCompletionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| StepProgramId | yes | yes |  | yes |  | Gets or sets the Id of the Step Program to which this step program completion belongs. This property is required. |
| Steps |  | yes | yes |  |  | Gets or sets a collection containing the Steps that are related to step program completion. |
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
| Campus | Gets or sets the Campus. This will be the campus from whichever step was completed last (most recently). |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the person alias. |
| StepProgram | Gets or sets the Step Program. |
| Steps | Gets or sets a collection containing the Steps that are related to step program completion. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Campus | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| CampusId | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| PersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| StepProgram | [Step Program](step-program.md) | e89f9528-a74e-41b7-8b65-b56b4ce7a122 |
| StepProgramId | [Step Program](step-program.md) | e89f9528-a74e-41b7-8b65-b56b4ce7a122 |
| Steps | Steps | 8eadb0dc-17f4-4541-a46e-53f89e21a622 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
