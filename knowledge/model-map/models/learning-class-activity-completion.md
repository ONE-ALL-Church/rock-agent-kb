# Learning Class Activity Completion Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `LMS`
- Model title: `LearningClassActivityCompletion`
- EntityType GUID: `14d1295a-ce9e-4fcb-a63c-6df04db5e9b1`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 65 |
| Database-marked properties | 32 |
| Lava-marked properties | 42 |
| Lava-marked non-database properties | 16 |
| Related model links | 23 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| ActivityComponentCompletionJson | yes | yes |  |  |  | Gets or sets the completion json for the activity component. This is the JSON configuration for the activity component including the responses and configuration at the time of completion. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableDateTime | yes | yes |  |  |  | Gets or sets the date the Learning Class Activity became available for student to complete. |
| AvailableKeys |  |  | yes |  |  |  |
| BinaryFileId | yes | yes |  |  |  | Gets or sets the binary file id for use by the activity component. |
| CompletedByPersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias of the person who completed this. |
| CompletedByPersonAliasId | yes | yes |  |  |  | Gets or sets the id of the Person Alias that completed this activity. |
| CompletedDateTime | yes | yes |  |  |  | Gets or sets the date the student completed the related Learning Class Activity. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DueDate | yes | yes |  |  |  | Gets or sets the due date of the Learning Class Activity for the student. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FacilitatorComment | yes | yes |  |  |  | Gets or sets the facilitator's comment. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GradePercent |  |  | yes |  |  | Gets the grade as a percentage for the student Activity. If no points are configured or LearningClassActivity is null then 100 is returned. |
| GradedByPersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias of the faciltator that graded this completion. |
| GradedByPersonAliasId | yes | yes |  |  |  | Gets or sets the Person Alias identifier of the facilitator who graded the activity. |
| Guid | yes | yes |  |  |  |  |
| HadExtension | yes |  |  |  |  | Determines if the individual was given an extension on the activity DueDate. |
| HasFacilitatorComment | yes |  |  |  |  | Determine if the activity has a facilitator comment. |
| HasStudentComment | yes |  |  |  |  | Determine if the activity has a student comment. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsCompleted | yes |  |  |  |  | Gets whether the assigned party (student or facilitator) has completed the activity. |
| IsFacilitatorCompleted | yes | yes |  |  |  | Indicates whether or not the related activity instance for the student has been completed by the facilitator. |
| IsLate | yes |  |  |  |  | Determines if the activity was completed late or is currently incomplete and late. |
| IsStudentCompleted | yes | yes |  |  |  | Indicates whether or not the related activity instance has been completed by the student. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LearningClassActivity |  | yes | yes |  |  | Gets or sets the Learning Class Activity for the student activity instance. |
| LearningClassActivityCompletionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| LearningClassActivityId | yes | yes |  |  |  | Gets or sets the id of the Learning Class Activity this completion relates to. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PointsEarned | yes | yes |  |  |  | Gets or sets the number of points the student earned by completing the activity. This will be null if no score has been set yet. |
| RequiresFacilitatorCompletion | yes |  |  |  |  | The activity has points, is assigned to the facilitator and hasn't been completed. |
| RequiresGrading | yes | yes |  |  |  | Indicates whether or not the Learning Class Activity Completion needs to be graded by a Facilitator. |
| SentNotificationCommunication |  | yes | yes |  |  | Gets or sets the Communication used for notifications by the student activity instance. |
| SentNotificationCommunicationId | yes | yes |  |  |  | Gets or sets the id of the Communication that was sent as a notification that this activity is available. |
| Student |  |  | yes |  |  | Gets or sets the student the activity instance is for. |
| StudentComment | yes | yes |  |  |  | Gets or sets the student's comment. |
| StudentId | yes | yes |  |  |  | Gets or sets the id of the student this completion belongs to. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WasCompletedOnTime | yes | yes |  |  |  | Indicates whether or not the related Learning Class Activity was completed by this student on or before the DueDate. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CompletedByPersonAlias | Gets or sets the Person Alias of the person who completed this. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| GradedByPersonAlias | Gets or sets the Person Alias of the faciltator that graded this completion. |
| IdKey |  |
| LearningClassActivity | Gets or sets the Learning Class Activity for the student activity instance. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| SentNotificationCommunication | Gets or sets the Communication used for notifications by the student activity instance. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AvailableDateTime | [Learning Class Activity](learning-class-activity.md) | e82f540c-f483-4d4a-898a-3ae7ff76f75a |
| AvailableDateTime | student | 03195758-1770-4794-9487-7a4aa02930a7 |
| CompletedByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| CompletedByPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| CompletedDateTime | [Learning Class Activity](learning-class-activity.md) | e82f540c-f483-4d4a-898a-3ae7ff76f75a |
| CompletedDateTime | student | 03195758-1770-4794-9487-7a4aa02930a7 |
| DueDate | [Learning Class Activity](learning-class-activity.md) | e82f540c-f483-4d4a-898a-3ae7ff76f75a |
| DueDate | student | 03195758-1770-4794-9487-7a4aa02930a7 |
| FacilitatorComment | facilitator's | 03195758-1770-4794-9487-7a4aa02930a7 |
| GradePercent | Activity | 14d1295a-ce9e-4fcb-a63c-6df04db5e9b1 |
| GradedByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| GradedByPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| IsFacilitatorCompleted | facilitator | 03195758-1770-4794-9487-7a4aa02930a7 |
| IsStudentCompleted | student | 03195758-1770-4794-9487-7a4aa02930a7 |
| LearningClassActivity | [Learning Class Activity](learning-class-activity.md) | e82f540c-f483-4d4a-898a-3ae7ff76f75a |
| LearningClassActivityId | [Learning Class Activity](learning-class-activity.md) | e82f540c-f483-4d4a-898a-3ae7ff76f75a |
| RequiresGrading | [Learning Class Activity Completion](learning-class-activity-completion.md) | 14d1295a-ce9e-4fcb-a63c-6df04db5e9b1 |
| SentNotificationCommunication | [Communication](communication.md) | c4ccbd91-1264-48bf-bc33-92751c8948b5 |
| SentNotificationCommunicationId | [Communication](communication.md) | c4ccbd91-1264-48bf-bc33-92751c8948b5 |
| Student | student | 03195758-1770-4794-9487-7a4aa02930a7 |
| StudentComment | student's | 03195758-1770-4794-9487-7a4aa02930a7 |
| StudentId | student | 03195758-1770-4794-9487-7a4aa02930a7 |
| WasCompletedOnTime | [Learning Class Activity](learning-class-activity.md) | e82f540c-f483-4d4a-898a-3ae7ff76f75a |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
