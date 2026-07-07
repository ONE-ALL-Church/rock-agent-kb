# Learning Course Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `LMS`
- Model title: `LearningCourse`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `21870376-4a6e-4402-ace3-42aa4441fc2e`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 58 |
| Database-marked properties | 25 |
| Lava-marked properties | 40 |
| Lava-marked non-database properties | 16 |
| Related model links | 7 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowHistoricalAccess | yes | yes |  |  |  | Indicates whether or not this course allows students to access after completion. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Category |  | yes | yes |  |  | Gets or sets the Category for the LearningCourse. |
| CategoryId | yes | yes |  |  |  | Gets or sets the Category id. |
| CompletionWorkflowType |  | yes | yes |  |  | Gets or sets the Workflow Type of the LearningCourse. |
| CompletionWorkflowTypeId | yes | yes |  |  |  | Gets or sets the Id of the Workflow Type that's triggered when the course is completed by a student. |
| ContextKey |  |  | yes |  |  |  |
| CourseCode | yes | yes |  |  |  | Gets or sets the code for the course. |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| Credits | yes | yes |  |  |  | Gets or sets the number of credits awarded for successful completion of the course. |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description of the course. |
| EnableAnnouncements | yes | yes |  |  |  | Indicates whether or not this course allows announcements. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| ImageBinaryFile |  | yes | yes |  |  | Gets or sets the ImageBinaryFile for the LearningCourse. |
| ImageBinaryFileId | yes | yes |  |  |  | Gets or sets the binary file id of the image for the course. |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this course is active. |
| IsPublic | yes | yes |  |  |  | Indicates whether or not this course should be displayed in public contexts (e.g. on a public site). Defaults to true |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LearningClasses |  |  | yes |  |  | Gets or sets a collection of LearningClasses for the LearningCourse. |
| LearningCourseAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| LearningCourseRequirements |  |  | yes |  |  | Gets or sets a collection of LearningCourseRequirements for the course. |
| LearningProgram |  | yes | yes |  |  | Gets or sets the LearningProgram of the course. |
| LearningProgramId | yes | yes |  |  |  | Gets or sets the id of the Learning Program for the course. |
| MaxStudents | yes | yes |  |  |  | Gets or sets the number of students at which to stop accepting enrollments. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the course. |
| Order | yes |  |  |  |  | Gets or sets the order in which the course should be displayed. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PublicName | yes | yes |  | yes |  | Gets or sets the public name of the course. |
| Summary | yes | yes |  |  |  | Gets or sets the summary text of the course. |
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
| Category | Gets or sets the Category for the LearningCourse. |
| CompletionWorkflowType | Gets or sets the Workflow Type of the LearningCourse. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ImageBinaryFile | Gets or sets the ImageBinaryFile for the LearningCourse. |
| LearningProgram | Gets or sets the LearningProgram of the course. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| CategoryId | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| CompletionWorkflowType | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| CompletionWorkflowTypeId | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| ImageBinaryFile | ImageBinaryFile | 9bb1a349-5998-47c1-97d5-d6cc00275662 |
| LearningClasses | LearningClasses | eb41e4e1-64b1-4aa1-8f66-f0dfd81557d9 |
| LearningCourseRequirements | LearningCourseRequirements | 576f54e1-ce70-43ed-a7d8-5169529c70e9 |
| LearningProgramId | [Learning Program](learning-program.md) | afd89885-6923-4fa1-b6fe-a1df8d821bbc |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
