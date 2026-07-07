# Step Program Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Engagement`
- Model title: `StepProgram`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `e89f9528-a74e-41b7-8b65-b56b4ce7a122`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 50 |
| Database-marked properties | 19 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 16 |
| Related model links | 5 |
| Method signatures | 36 |
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
| Category |  | yes | yes |  |  | Gets or sets the Category. |
| CategoryId | yes |  |  |  |  | Gets or sets the Id of the Category. |
| CompletionFlow | yes | yes |  | yes |  | Gets or sets how the steps in a program are ordered and how prerequisites are handled. This is a hard coded list of values defined in the code as an enumeration. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefaultListView | yes | yes |  |  |  | Gets or sets the default view mode for the program. This value is required. This is a hard coded list of values defined in the code as an enumeration. |
| Description | yes | yes |  |  |  | Gets or sets a description of the program. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if this item is active or not. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Step Program is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the program. This property is required. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| StepProgramAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| StepStatuses |  | yes | yes |  |  | Gets or sets a collection containing the StepStatuses that this Program utilizes. |
| StepTerm | yes | yes |  |  |  | Gets or sets the term used for steps within this program. This property is required. |
| StepTypes |  | yes | yes |  |  | Gets or sets a collection containing the Step Types that are of this program. |
| StepWorkflowTriggers |  | yes | yes |  |  | Gets or sets a collection containing the StepWorkflowTriggers that are of this step program. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the Category. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| StepStatuses | Gets or sets a collection containing the StepStatuses that this Program utilizes. |
| StepTypes | Gets or sets a collection containing the Step Types that are of this program. |
| StepWorkflowTriggers | Gets or sets a collection containing the StepWorkflowTriggers that are of this step program. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Category | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| CategoryId | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| StepStatuses | StepStatuses | 6c270d6a-f126-445b-93f0-5079a968bf4e |
| StepTypes | Step Types | 5e795620-9f16-49d2-9030-947c0e348a8e |
| StepWorkflowTriggers | StepWorkflowTriggers | 55c1d610-d42f-4e08-9cd9-1ec9801bc4e3 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
