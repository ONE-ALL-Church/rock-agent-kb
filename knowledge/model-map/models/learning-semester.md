# Learning Semester Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `LMS`
- Model title: `LearningSemester`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `f9a40931-0ace-4b50-a507-0d1d75f92bc4`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 43 |
| Database-marked properties | 14 |
| Lava-marked properties | 27 |
| Lava-marked non-database properties | 13 |
| Related model links | 2 |
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
| EndDate | yes | yes |  |  |  | Gets or sets the date the semester ends. |
| EnrollmentCloseDate | yes | yes |  |  |  | Gets or sets the date that students must enroll by. |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LearningClasses |  |  | yes |  |  | Gets or sets a collection of LearningClasses for this semester. |
| LearningProgram |  | yes | yes |  |  | Gets or sets the LearningProgram of the semester. |
| LearningProgramId | yes | yes |  |  |  | Gets or sets the Id of the related Learning Program. |
| LearningSemesterAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the LearningSemester. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| StartDate | yes | yes |  |  |  | Gets or sets the date the semester starts |
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
| LearningProgram | Gets or sets the LearningProgram of the semester. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| LearningClasses | LearningClasses | eb41e4e1-64b1-4aa1-8f66-f0dfd81557d9 |
| LearningProgramId | [Learning Program](learning-program.md) | afd89885-6923-4fa1-b6fe-a1df8d821bbc |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
