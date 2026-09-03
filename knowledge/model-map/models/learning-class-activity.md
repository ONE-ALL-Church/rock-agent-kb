# Learning Class Activity Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `LMS`
- Model title: `LearningClassActivity`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `e82f540c-f483-4d4a-898a-3ae7ff76f75a`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 62 |
| Database-marked properties | 31 |
| Lava-marked properties | 40 |
| Lava-marked non-database properties | 15 |
| Related model links | 9 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AssignTo | yes | yes |  |  |  | The participant type assigned to complete this activity. This is a hard coded list of values defined in the code as an enumeration. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailabilityCriteria | yes | yes |  |  |  | The method used for determining the AvailableDate of the activity. This is a hard coded list of values defined in the code as an enumeration. |
| AvailableDateCalculated | yes |  |  |  |  | The result of the calculated available date. |
| AvailableDateDefault | yes | yes |  |  |  | Gets or sets the default date the activity is available for the Learning Participant to complete. |
| AvailableDateDescription | yes |  |  |  |  | Attempts to calculate the available date or provides a textual description if unable to calculate. |
| AvailableDateOffset | yes | yes |  |  |  | The optional offset to use for calculating the AvailableDate. |
| AvailableKeys |  |  | yes |  |  |  |
| CompletionWorkflowType |  | yes | yes |  |  | Gets or sets the Workflow Type for the activity. |
| CompletionWorkflowTypeId | yes | yes |  |  |  | Gets or sets the id of the Workflow Type that's triggered when the activity is completed. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DatesDescription | yes |  |  |  |  | A textual description of the available and due dates for the activity. |
| DueDateCalculated | yes |  |  |  |  | The result of the calculated due date. |
| DueDateCriteria | yes | yes |  |  |  | The method used for determining the DueDate of the activity. This is a hard coded list of values defined in the code as an enumeration. |
| DueDateDefault | yes | yes |  |  |  | Gets or sets the default date the activity is due. |
| DueDateDescription | yes |  |  |  |  | A description of the Due Date. |
| DueDateOffset | yes | yes |  |  |  | The optional offset to use for calculating the DueDate. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsPastDue | yes |  |  |  |  | true if the calculated due date is in the past; otherwise false. |
| IsStudentCommentingEnabled | yes | yes |  |  |  | Indicates whether or not this activity allows students to comment. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LearningActivity |  | yes | yes |  |  | Gets or sets the LearningActivity for the class activity. |
| LearningActivityId | yes | yes |  |  |  | Gets or sets the id of the Learning Activity this activity gets its configuration from. |
| LearningClass |  | yes | yes |  |  | Gets or sets the LearningClass for the activity. |
| LearningClassActivityAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| LearningClassActivityCompletions |  |  | yes |  |  | Gets or sets a collection of Learning Class Activity Completion records for this activity. |
| LearningClassId | yes | yes |  |  |  | Gets or sets the id of the Learning Class this activity belongs to. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the name of the activity. |
| Order | yes | yes |  |  |  | Gets or sets the order in which the activity should be displayed. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Points | yes | yes |  |  |  | Gets or sets the maximum number of points the activity is worth. |
| SendNotificationCommunication | yes | yes |  |  |  | Indicates whether or not this activity sends a notification. |
| SupportedActions |  |  | yes |  |  |  |
| TaskBinaryFileId | yes | yes |  |  |  | Gets or sets the id of the TaskBinaryFile for the activity. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CompletionWorkflowType | Gets or sets the Workflow Type for the activity. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| LearningActivity | Gets or sets the LearningActivity for the class activity. |
| LearningClass | Gets or sets the LearningClass for the activity. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AvailableDateDefault | activity | e82f540c-f483-4d4a-898a-3ae7ff76f75a |
| AvailableDateDefault | [Learning Participant](learning-participant.md) | 03195758-1770-4794-9487-7a4aa02930a7 |
| CompletionWorkflowType | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| CompletionWorkflowTypeId | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| DueDateDefault | activity | e82f540c-f483-4d4a-898a-3ae7ff76f75a |
| LearningActivityId | [Learning Activity](learning-activity.md) | 98b98fa8-a92d-4e10-aa3e-b3082e61976f |
| LearningClassActivityCompletions | [Learning Class Activity Completion](learning-class-activity-completion.md) | 14d1295a-ce9e-4fcb-a63c-6df04db5e9b1 |
| LearningClassId | [Learning Class](learning-class.md) | eb41e4e1-64b1-4aa1-8f66-f0dfd81557d9 |
| TaskBinaryFileId | TaskBinaryFile | 9bb1a349-5998-47c1-97d5-d6cc00275662 |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | RetakeThreshold |  |
