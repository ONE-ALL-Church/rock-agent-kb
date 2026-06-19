# Learning Program Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `LMS`
- Model title: `LearningProgram`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `afd89885-6923-4fa1-b6fe-a1df8d821bbc`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 63 |
| Database-marked properties | 28 |
| Lava-marked properties | 44 |
| Lava-marked non-database properties | 17 |
| Related model links | 11 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

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
| CompletionWorkflowTypeId | yes | yes |  |  |  | Gets or sets the Id of the Workflow Type that is triggered when the program is completed by a student. |
| ConfigurationMode | yes | yes |  | yes |  | Gets or sets the configuration mode of the LearningProgram. This is a hard coded list of values defined in the code as an enumeration. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefaultLearningGradingSystem |  | yes | yes |  |  | Gets or sets the default Learning Grading System for this LearningProgram. |
| DefaultLearningGradingSystemId | yes | yes |  |  |  | Gets or sets the default Learning Grading System identifier. |
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
| ImageBinaryFile |  | yes | yes |  |  | Gets or sets the related Binary File for the program. |
| ImageBinaryFileId | yes | yes |  |  |  | Gets or sets the binary file id of the image for the LearningProgram. |
| IsActive | yes | yes |  |  |  | Gets a value indicating whether this LearningProgram is active. |
| IsCompletionStatusTracked | yes | yes |  |  |  | Gets a value indicating whether this LearningProgram tracks student's completion of the program. Once a LearningProgram begins this value cannot be changed. |
| IsPublic | yes | yes |  |  |  | Indicates whether or not this LearningProgram should be displayed in public contexts (e.g. on a public site). Defaults to true. |
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
| SystemCommunication |  | yes | yes |  |  | Gets or sets the related System Communication for the program. |
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
| DefaultLearningGradingSystem | Gets or sets the default Learning Grading System for this LearningProgram. |
| EntityStringValue |  |
| IdKey |  |
| ImageBinaryFile | Gets or sets the related Binary File for the program. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| SystemCommunication | Gets or sets the related System Communication for the program. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Category | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| CategoryId | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| CompletionWorkflowType | [WorkflowType](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| CompletionWorkflowTypeId | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| DefaultLearningGradingSystem | [Learning Grading System](learning-grading-system.md) | 0b693caf-3718-4913-b7ac-61d31b4df099 |
| DefaultLearningGradingSystemId | [Learning Grading System](learning-grading-system.md) | 0b693caf-3718-4913-b7ac-61d31b4df099 |
| ImageBinaryFile | [Binary File](binary-file.md) | 9bb1a349-5998-47c1-97d5-d6cc00275662 |
| LearningCourses | LearningCourses | 21870376-4a6e-4402-ace3-42aa4441fc2e |
| LearningProgramCompletions | LearningProgramCompletions | b82813a7-e70e-4f04-8568-0d84efb484b2 |
| LearningSemesters | LearningSemesters | f9a40931-0ace-4b50-a507-0d1d75f92bc4 |
| SystemCommunication | [System Communication](system-communication.md) | d0cad7c0-10fe-41ef-b89d-e6f0d22456c4 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
