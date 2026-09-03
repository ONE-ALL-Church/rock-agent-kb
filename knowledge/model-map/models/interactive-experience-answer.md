# Interactive Experience Answer Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Event`
- Model title: `InteractiveExperienceAnswer`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `d11da9d4-8887-4ec2-b396-78556926de89`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 50 |
| Database-marked properties | 18 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 17 |
| Related model links | 5 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| ApprovalStatus | yes | yes |  |  |  | Gets or sets the approval status. This is a hard coded list of values defined in the code as an enumeration. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the Campus that this answer originated from. |
| CampusId | yes |  |  |  |  | Gets or sets the identifier of the Campus the answer originated from. |
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
| InteractionSession |  | yes | yes |  |  | Gets or sets the InteractionSession that this answer is associated with. |
| InteractionSessionId | yes | yes |  |  |  | Gets or sets the Id of the Interaction Session Session. |
| InteractiveExperienceAction |  | yes | yes |  |  | Gets or sets the Interactive Experience Action that the Interactive Experience Answer belongs to. |
| InteractiveExperienceActionId | yes | yes |  | yes |  | Gets or sets the Id of the Interactive Experience Action that this Interactive Experience Answer is associated with. This property is required. |
| InteractiveExperienceAnswerAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| InteractiveExperienceOccurrence |  | yes | yes |  |  | Gets or sets the Interactive Experience Occurrence that the Interactive Experience Answer belongs to. |
| InteractiveExperienceOccurrenceId | yes | yes |  | yes |  | Gets or sets the Id of the Interactive Experience Occurrence that this Interactive Experience Answer is associated with. This property is required. |
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
| PersonAliasId | yes | yes |  |  |  | Gets or sets the person alias identifier. |
| Response | yes | yes |  |  |  | Gets or sets the response. |
| ResponseDataJson | yes | yes |  |  |  | Gets or sets the custom response data JSON. This will hold additional information that does not need referential integrity. |
| ResponseDateTime | yes | yes |  |  |  | Gets or sets the response date time. |
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
| Campus | Gets or sets the Campus that this answer originated from. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| InteractionSession | Gets or sets the InteractionSession that this answer is associated with. |
| InteractiveExperienceAction | Gets or sets the Interactive Experience Action that the Interactive Experience Answer belongs to. |
| InteractiveExperienceOccurrence | Gets or sets the Interactive Experience Occurrence that the Interactive Experience Answer belongs to. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the person alias. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| InteractionSessionId | [Interaction Session](interaction-session.md) | 338025de-c16f-47bb-ba31-6de0c59e59aa |
| InteractiveExperienceAction | [Interactive Experience Action](interactive-experience-action.md) | 8635e7e7-3576-47ff-92de-30a69eb5d011 |
| InteractiveExperienceActionId | [Interactive Experience Action](interactive-experience-action.md) | 8635e7e7-3576-47ff-92de-30a69eb5d011 |
| InteractiveExperienceOccurrence | [Interactive Experience Occurrence](interactive-experience-occurrence.md) | 2d1263a1-a3e7-4568-aa4b-c1234824188d |
| InteractiveExperienceOccurrenceId | [Interactive Experience Occurrence](interactive-experience-occurrence.md) | 2d1263a1-a3e7-4568-aa4b-c1234824188d |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
