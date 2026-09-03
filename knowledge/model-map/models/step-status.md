# Step Status Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Engagement`
- Model title: `StepStatus`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `6c270d6a-f126-445b-93f0-5079a968bf4e`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 46 |
| Database-marked properties | 16 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 14 |
| Related model links | 3 |
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
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if this item is active or not. |
| IsCompleteStatus | yes | yes |  |  |  | Gets or sets a flag indicating if this status means that the step is complete. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Step Status is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the status. This property is required. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| StatusColor | yes | yes |  |  |  | Gets or sets the color of the status. |
| StatusColorOrDefault |  |  | yes |  |  | Gets the status color or default color depending on IsCompleteStatus. |
| StepProgram |  | yes | yes |  |  | Gets or sets the Step Program. |
| StepProgramId | yes | yes |  | yes |  | Gets or sets the Id of the Step Program to which this status belongs. This property is required. |
| StepStatusAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Steps |  | yes | yes |  |  | Gets or sets a collection containing the Steps that are of this step status. |
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
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| StepProgram | Gets or sets the Step Program. |
| Steps | Gets or sets a collection containing the Steps that are of this step status. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| StepProgram | [Step Program](step-program.md) | e89f9528-a74e-41b7-8b65-b56b4ce7a122 |
| StepProgramId | [Step Program](step-program.md) | e89f9528-a74e-41b7-8b65-b56b4ce7a122 |
| Steps | Steps | 8eadb0dc-17f4-4541-a46e-53f89e21a622 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
