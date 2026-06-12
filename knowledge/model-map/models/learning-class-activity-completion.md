# Learning Class Activity Completion Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `LMS`
- Model title: `LearningClassActivityCompletion`
- EntityType GUID: `14d1295a-ce9e-4fcb-a63c-6df04db5e9b1`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 64 |
| Database-marked properties | 31 |
| Lava-marked properties | 42 |
| Lava-marked non-database properties | 16 |
| Related model links | 23 |
| Pre-alpha changes touching this model | 2 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| ActivityComponentCompletionJson | yes | yes |  |  |  | Gets or sets the completion json for the activity component. This is the JSON configuration for the activity component including the responses and configuration at the time of completion. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableDateTime | yes | yes |  |  |  | Gets or sets the date the LearningClassActivity became available for student to complete. |
| AvailableKeys |  |  | yes |  |  |  |
| BinaryFileId | yes | yes |  |  |  | Gets or sets the binary file id for use by the activity component. |
| CompletedByPersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias of the person who completed this. |
| CompletedByPersonAliasId | yes | yes |  |  |  | Gets or sets the id of the PersonAlias that completed this activity. |
| CompletedDateTime | yes | yes |  |  |  | Gets or sets the date the student completed the related LearningClassActivity. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DueDate | yes | yes |  |  |  | Gets or sets the due date of the LearningClassActivity for the student. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FacilitatorComment | yes | yes |  |  |  | Gets or sets the facilitator's comment. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GradePercent |  |  | yes |  |  | Gets the grade as a percentage for the student Activity. If no points are configured or LearningClassActivity is null then 100 is returned. |
| GradedByPersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias of the faciltator that graded this completion. |
| GradedByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAlias identifier of the facilitator who graded the activity. |
| Guid | yes | yes |  |  |  |  |
| HadExtension | yes |  |  |  |  | Determines if the individual was given an extension on the activity DueDate. |
| HasFacilitatorComment | yes |  |  |  |  | Determine if the activity has a facilitator comment. |
| HasStudentComment | yes |  |  |  |  | Determine if the activity has a student comment. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsFacilitatorCompleted | yes | yes |  |  |  | Indicates whether or not the related activity instance for the student has been completed by the facilitator. |
| IsLate | yes |  |  |  |  | Determines if the activity was completed late or is currently incomplete and late. |
| IsStudentCompleted | yes | yes |  |  |  | Indicates whether or not the related activity instance has been completed by the student. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LearningClassActivity |  | yes | yes |  |  | Gets or sets the LearningClassActivity for the student activity instance. |
| LearningClassActivityCompletionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| LearningClassActivityId | yes | yes |  |  |  | Gets or sets the id of the LearningClassActivity this completion relates to. |
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
| RequiresGrading | yes | yes |  |  |  | Indicates whether or not the LearningClassActivityCompletion needs to be graded by a Facilitator. |
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
| WasCompletedOnTime | yes | yes |  |  |  | Indicates whether or not the related LearningClassActivity was completed by this student before the DueDate. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CompletedByPersonAlias | Gets or sets the PersonAlias of the person who completed this. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| GradedByPersonAlias | Gets or sets the PersonAlias of the faciltator that graded this completion. |
| IdKey |  |
| LearningClassActivity | Gets or sets the LearningClassActivity for the student activity instance. |
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
| AvailableDateTime | [LearningClassActivity](learning-class-activity.md) |  |
| AvailableDateTime | student |  |
| CompletedByPersonAlias | [PersonAlias](person-alias.md) |  |
| CompletedByPersonAliasId | [PersonAlias](person-alias.md) |  |
| CompletedDateTime | [LearningClassActivity](learning-class-activity.md) |  |
| CompletedDateTime | student |  |
| DueDate | [LearningClassActivity](learning-class-activity.md) |  |
| DueDate | student |  |
| FacilitatorComment | facilitator's |  |
| GradePercent | Activity |  |
| GradedByPersonAlias | [PersonAlias](person-alias.md) |  |
| GradedByPersonAliasId | [PersonAlias](person-alias.md) |  |
| IsFacilitatorCompleted | facilitator |  |
| IsStudentCompleted | student |  |
| LearningClassActivity | [LearningClassActivity](learning-class-activity.md) |  |
| LearningClassActivityId | [LearningClassActivity](learning-class-activity.md) |  |
| RequiresGrading | [LearningClassActivityCompletion](learning-class-activity-completion.md) |  |
| SentNotificationCommunication | [Communication](communication.md) |  |
| SentNotificationCommunicationId | [Communication](communication.md) |  |
| Student | student |  |
| StudentComment | student's |  |
| StudentId | student |  |
| WasCompletedOnTime | [LearningClassActivity](learning-class-activity.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | IsCompleted |  |
| property_changed | WasCompletedOnTime | description |
