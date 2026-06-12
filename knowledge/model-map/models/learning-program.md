# Learning Program Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `LMS`
- Model title: `LearningProgram`
- EntityType GUID: `afd89885-6923-4fa1-b6fe-a1df8d821bbc`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 63 |
| Database-marked properties | 28 |
| Lava-marked properties | 44 |
| Lava-marked non-database properties | 17 |
| Related model links | 12 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AbsencesCriticalCount | yes | yes |  |  |  | Gets or sets the number of absences at which a critical alert should be triggered. |
| AbsencesWarningCount | yes | yes |  |  |  | Gets or sets the number of absences at which a warning should be triggered. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  | Gets or sets the additional settings json. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Category |  | yes | yes |  |  | Gets or sets the related Category for the program. |
| CategoryId | yes | yes |  |  |  | Gets or sets the Category identifier. |
| CompletionWorkflowType |  | yes | yes |  |  | Gets or sets the related completion WorkflowType for the program. |
| CompletionWorkflowTypeId | yes | yes |  |  |  | Gets or sets the Id of the WorkflowType that is triggered when the program is completed by a student. |
| ConfigurationMode | yes | yes |  | yes |  | Gets or sets the configuration mode of the LearningProgram. This is a hard coded list of values defined in the code as an enumeration. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefaultLearningGradingSystem |  | yes | yes |  |  | Gets or sets the default LearningGradingSystem for this LearningProgram. |
| DefaultLearningGradingSystemId | yes | yes |  |  |  | Gets or sets the default LearningGradingSystem identifier. |
| Description | yes | yes |  |  |  | Gets or sets the Description of the LearningProgram. |
| EncryptedKey |  |  | yes |  |  |  |
| EnforcePublicSecurity | yes | yes |  |  |  | Gets or sets a value indicating whether public security should be enforced for this program. |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HighlightColor | yes | yes |  |  |  | Gets or sets the color of the highlight. |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| ImageBinaryFile |  | yes | yes |  |  | Gets or sets the related BinaryFile for the program. |
| ImageBinaryFileId | yes | yes |  |  |  | Gets or sets the binary file id of the image for the LearningProgram. |
| IsActive | yes | yes |  |  |  | Gets a value indicating whether this LearningProgram is active. |
| IsCompletionStatusTracked | yes | yes |  |  |  | Gets a value indicating whether this LearningProgram tracks student's completion of the program. Once a LearningProgram begins this value cannot be changed. |
| IsPublic | yes | yes |  |  |  | Indicates whether or not this LearningProgram should be displayed in public contexts (e.g. on a public site). Defaults to true . |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LearningCourses |  |  | yes |  |  | Gets or sets a collection of LearningCourses for this LearningProgram. |
| LearningProgramAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| LearningProgramCompletions |  |  | yes |  |  | Gets or sets a collection of LearningProgramCompletions for this LearningProgram. |
| LearningSemesters |  |  | yes |  |  | Gets or sets a collection of LearningSemesters for this LearningProgram. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the LearningProgram. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PublicName | yes | yes |  | yes |  | Gets or sets the public name of the LearningProgram. |
| Summary | yes | yes |  |  |  | Gets or sets the summary text of the LearningProgram. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| SystemCommunication |  | yes | yes |  |  | Gets or sets the related SystemCommunication for the program. |
| SystemCommunicationId | yes |  |  |  |  | Gets or sets the id of the system communication. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the related Category for the program. |
| CompletionWorkflowType | Gets or sets the related completion WorkflowType for the program. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DefaultLearningGradingSystem | Gets or sets the default LearningGradingSystem for this LearningProgram. |
| EntityStringValue |  |
| IdKey |  |
| ImageBinaryFile | Gets or sets the related BinaryFile for the program. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| SystemCommunication | Gets or sets the related SystemCommunication for the program. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Category | [Category](category.md) |  |
| CategoryId | [Category](category.md) |  |
| CompletionWorkflowType | [WorkflowType](workflow-type.md) |  |
| CompletionWorkflowTypeId | [WorkflowType](workflow-type.md) |  |
| DefaultLearningGradingSystem | [LearningGradingSystem](learning-grading-system.md) |  |
| DefaultLearningGradingSystemId | [LearningGradingSystem](learning-grading-system.md) |  |
| ImageBinaryFile | [BinaryFile](binary-file.md) |  |
| LearningCourses | LearningCourses |  |
| LearningProgramCompletions | LearningProgramCompletions |  |
| LearningSemesters | LearningSemesters |  |
| SupportedActions | Dictionary`2 |  |
| SystemCommunication | [SystemCommunication](system-communication.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | SupportedActions | related_entity_links |
