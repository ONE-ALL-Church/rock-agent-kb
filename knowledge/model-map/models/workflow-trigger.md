# Workflow Trigger Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Workflow`
- Model title: `WorkflowTrigger`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `3781c82a-7f40-4d88-b3db-1b9589d73d3d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 29 |
| Database-marked properties | 14 |
| Lava-marked properties | 21 |
| Lava-marked non-database properties | 7 |
| Related model links | 4 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the Entity Type that contains the entities that are affected by this WorkflowTrigger. |
| EntityTypeId | yes | yes |  | yes |  | Gets or sets the EntityTypeId of the Entity Type of the entities that this trigger applies to |
| EntityTypeQualifierColumn | yes | yes |  |  |  | Gets or sets the name of the Entity Qualifier Column that contains the value that filters the scope of the WorkflowTrigger. This property must be used in conjunction with the EntityTypeQualifierValue property. |
| EntityTypeQualifierValue | yes | yes |  |  |  | Gets or sets the EntityTypeQualifierValue in the EntityTypeQualifierColumn that is used to filter the scope of the WorkflowTrigger. |
| EntityTypeQualifierValuePrevious | yes | yes |  |  |  | Gets or sets the EntityTypeQualifierValuePrevious in the EntityTypeQualifierColumn that is used to filter the scope of the WorkflowTrigger. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if the WorkflowTrigger is active. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this WorkflowTrigger is part of Rock core system/framework. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowName | yes | yes |  |  |  | Gets or sets the name of the workflow trigger. |
| WorkflowTriggerType | yes | yes |  | yes |  | Gets or sets the type of the workflow trigger. Indicates the type of change and the timing the trigger. This is a hard coded list of values defined in the code as an enumeration. |
| WorkflowTriggerValueChangeType |  |  | yes |  |  | Indicates if this WorkflowTrigger is looking for a Value that is Changed From one value To another, or just if the Value Equals something This is determined by the values for EntityTypeQualifierValue and EntityTypeQualifierValuePrevious. If EntityTypeQualifierValue and EntityTypeQualifierValuePrevious are the same value, this is a trigger that only fires if the ValueEquals on save. Otherwise, it'll only fire if the previous value was Changed From EntityTypeQualifierValuePrevious To EntityTypeQualifierValue This is a hard coded list of values defined in the code as an enumeration. |
| WorkflowType |  | yes | yes |  |  | Gets or sets the Workflow Type that is executed by this WorkflowTrigger. |
| WorkflowTypeId | yes | yes |  | yes |  | Gets or sets the WorkflowTypeId of the Workflow Type that is executed by this WorkflowTrigger. This property is required. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| EntityType | Gets or sets the Entity Type that contains the entities that are affected by this WorkflowTrigger. |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WorkflowType | Gets or sets the Workflow Type that is executed by this WorkflowTrigger. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| EntityType | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| EntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| WorkflowType | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| WorkflowTypeId | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
