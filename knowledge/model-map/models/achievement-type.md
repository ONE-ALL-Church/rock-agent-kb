# Achievement Type Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Engagement`
- Model title: `AchievementType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `0e99356c-0dea-4f24-944e-21cd5fa83b9e`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 72 |
| Database-marked properties | 33 |
| Lava-marked properties | 56 |
| Lava-marked non-database properties | 24 |
| Related model links | 19 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AchievementEntityType |  | yes | yes |  |  | Gets or sets the Entity Type of the achievement. |
| AchievementFailureWorkflowType |  | yes | yes |  |  | Gets or sets the Workflow Type to be launched when the achievement is failed (closed and not successful). |
| AchievementFailureWorkflowTypeId | yes | yes |  |  |  | Gets or sets the Id of the Workflow Type to be triggered when an achievement is failed (closed and not successful) |
| AchievementIconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class. |
| AchievementStartWorkflowType |  | yes | yes |  |  | Gets or sets the Workflow Type to be launched when the achievement starts. |
| AchievementStartWorkflowTypeId | yes | yes |  |  |  | Gets or sets the Id of the Workflow Type to be triggered when an achievement is started |
| AchievementStepStatus |  | yes | yes |  |  | Gets or sets the Step Status to be used for the Step Type created when the achievement is completed. |
| AchievementStepStatusId | yes | yes |  |  |  | Gets or sets the Id of the Step Status of which a Step will be created when an achievement is completed |
| AchievementStepType |  | yes | yes |  |  | Gets or sets the Step Type to be created when the achievement is completed. |
| AchievementStepTypeId | yes | yes |  |  |  | Gets or sets the Id of the Step Type of which a Step will be created when an achievement is completed |
| AchievementSuccessWorkflowType |  | yes | yes |  |  | Gets or sets the Workflow Type to be launched when the achievement is successful. |
| AchievementSuccessWorkflowTypeId | yes | yes |  |  |  | Gets or sets the Id of the Workflow Type to be triggered when an achievement is successful |
| AchievementTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| AchieverEntityTypeId | yes | yes |  | yes |  | Gets or sets the achiever entity type. The achiever is the object that earns the achievement. The original achiever was a Person Alias via Streak.PersonAliasId. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowOverAchievement | yes | yes |  |  |  | Gets or sets whether over achievement is allowed. This cannot be true if MaxAccomplishmentsAllowed is greater than 1. |
| AlternateImageBinaryFile |  | yes | yes |  |  | Gets or sets the alternate image binary file. |
| AlternateImageBinaryFileId | yes | yes |  |  |  | An alternate image that can be used for custom purposes. |
| Attempts |  | yes | yes |  |  | Gets or sets the attempts. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BadgeLavaTemplate | yes | yes |  |  |  | Gets or sets the lava template used to render a badge. |
| Category |  | yes | yes |  |  | Gets or sets the Category. |
| CategoryId | yes | yes |  |  |  | Gets or sets the Category identifier. |
| ComponentConfigJson | yes | yes |  |  |  | Gets or sets the configuration from the ComponentEntityTypeId. |
| ComponentEntityTypeId | yes | yes |  | yes |  | Gets or sets the Id of the achievement component Entity Type |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| CustomSummaryLavaTemplate | yes | yes |  |  |  | Gets or sets the lava template used to render the status summary of the achievement. |
| Dependencies |  | yes | yes |  |  | Gets or sets the dependencies. |
| Description | yes | yes |  |  |  | Gets or sets a description of the achievement type. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HighlightColor | yes | yes |  |  |  | Gets or sets the color of the highlight. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| ImageBinaryFile |  | yes | yes |  |  | Gets or sets the image binary file. |
| ImageBinaryFileId | yes | yes |  |  |  | Gets or sets the image binary file identifier. This would be the image that would be shown in the achievement summary (for example, a trophy). |
| IsActive | yes | yes |  |  |  | Gets a value indicating whether this instance is active. |
| IsPublic | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is public. |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. |
| Item |  |  | yes |  |  |  |
| MaxAccomplishmentsAllowed | yes | yes |  |  |  | Gets or sets the maximum accomplishments allowed. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the achievement type. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Prerequisites |  | yes | yes |  |  | Gets or sets the prerequisites. |
| ResultsLavaTemplate | yes | yes |  |  |  | Gets or sets the lava template used to render results. |
| SourceEntityTypeId | yes | yes |  |  |  | Gets or sets the source entity type. The source supplies the data framework from which achievements are computed. The original achievement sources were Streaks. |
| SupportedActions |  |  | yes |  |  |  |
| TargetCount | yes |  |  |  |  | Gets or sets the target count of things that must be done for this achievement to be considered accomplished. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AchievementEntityType | Gets or sets the Entity Type of the achievement. |
| AchievementFailureWorkflowType | Gets or sets the Workflow Type to be launched when the achievement is failed (closed and not successful). |
| AchievementStartWorkflowType | Gets or sets the Workflow Type to be launched when the achievement starts. |
| AchievementStepStatus | Gets or sets the Step Status to be used for the Step Type created when the achievement is completed. |
| AchievementStepType | Gets or sets the Step Type to be created when the achievement is completed. |
| AchievementSuccessWorkflowType | Gets or sets the Workflow Type to be launched when the achievement is successful. |
| AlternateImageBinaryFile | Gets or sets the alternate image binary file. |
| Attempts | Gets or sets the attempts. |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the Category. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| Dependencies | Gets or sets the dependencies. |
| EntityStringValue |  |
| IdKey |  |
| ImageBinaryFile | Gets or sets the image binary file. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Prerequisites | Gets or sets the prerequisites. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AchievementEntityType | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| AchievementFailureWorkflowType | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| AchievementFailureWorkflowTypeId | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| AchievementStartWorkflowType | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| AchievementStartWorkflowTypeId | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| AchievementStepStatus | [Step Status](step-status.md) | 6c270d6a-f126-445b-93f0-5079a968bf4e |
| AchievementStepStatus | [Step Type](step-type.md) | 5e795620-9f16-49d2-9030-947c0e348a8e |
| AchievementStepStatusId | [Step](step.md) | 8eadb0dc-17f4-4541-a46e-53f89e21a622 |
| AchievementStepStatusId | [Step Status](step-status.md) | 6c270d6a-f126-445b-93f0-5079a968bf4e |
| AchievementStepType | [Step Type](step-type.md) | 5e795620-9f16-49d2-9030-947c0e348a8e |
| AchievementStepTypeId | [Step](step.md) | 8eadb0dc-17f4-4541-a46e-53f89e21a622 |
| AchievementStepTypeId | [Step Type](step-type.md) | 5e795620-9f16-49d2-9030-947c0e348a8e |
| AchievementSuccessWorkflowType | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| AchievementSuccessWorkflowTypeId | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| AchieverEntityTypeId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| Category | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| CategoryId | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| ComponentEntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| SourceEntityTypeId | Streaks | d953b0a5-0065-4624-8844-10010de01e5c |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
