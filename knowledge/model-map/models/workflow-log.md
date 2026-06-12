# Workflow Log Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Workflow`
- Model title: `WorkflowLog`
- EntityType GUID: `332cff36-d637-414d-b732-370b330b8d73`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 5 |
| Database-marked properties | 4 |
| Lava-marked properties | 5 |
| Lava-marked non-database properties | 1 |
| Related model links | 2 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| Id | yes | yes |  |  |  | Gets or sets the value of the identifier. This value is the primary field/key for the entity object. This value is system and database dependent, and is not guaranteed to be unique. This id should only be used to identify an object internally to a single implementation of Rock since this value has a very high probability of not being consistent in an external implementation of Rock. |
| LogDateTime | yes | yes |  | yes |  | Gets or sets the date and time that the WorkflowLog entry was created. This property is required. |
| LogText | yes | yes |  | yes |  | Gets or sets the body/text of the WorkflowLog entry. This property is required. |
| Workflow |  | yes | yes |  |  | Gets or sets the Workflow instance that is being logged. |
| WorkflowId | yes | yes |  |  |  | Gets or sets the WorkflowId of the Workflow instance that is being logged. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Workflow | Gets or sets the Workflow instance that is being logged. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Workflow | [Workflow](workflow.md) |  |
| WorkflowId | [Workflow](workflow.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
