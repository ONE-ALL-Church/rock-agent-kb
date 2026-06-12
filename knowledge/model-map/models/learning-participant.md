# Learning Participant Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `LMS`
- Model title: `LearningParticipant`
- EntityType GUID: `03195758-1770-4794-9487-7a4aa02930a7`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 75 |
| Database-marked properties | 36 |
| Lava-marked properties | 58 |
| Lava-marked non-database properties | 22 |
| Related model links | 24 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| ArchivedByPersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias that archived (soft deleted) this group member |
| ArchivedByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAliasId that archived (soft deleted) this group member |
| ArchivedDateTime | yes | yes |  |  |  | Gets or sets the date time that this group member was archived (soft deleted) |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CommunicationPreference | yes | yes |  |  |  | Gets or sets the communication preference. This is a hard coded list of values defined in the code as an enumeration. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DateTimeAdded | yes | yes |  |  |  | Gets or sets the date/time that the person was added to the group. Rock will automatically set this value when a group member is added if it isn't set manually |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Group that the GroupMember belongs to. |
| GroupId | yes | yes |  | yes |  | Gets or sets the Id of the Group that this GroupMember is associated with. This property is required. |
| GroupMemberAssignments |  | yes | yes |  |  | Gets or sets the group member assignments. |
| GroupMemberAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupMemberRequirements |  | yes | yes |  |  | Gets or sets the group member requirements. |
| GroupMemberStatus | yes | yes |  | yes |  | Gets or sets the GroupMember's status (GroupMemberStatus) in the Group. This value is required. This is a hard coded list of values defined in the code as an enumeration. |
| GroupOrder | yes | yes |  |  |  | Gets or sets the order of Groups of the Group's GroupType for the Person. For example, if this is a FamilyGroupType, GroupOrder can be used to specify which family should be listed as 1st (primary), 2nd, 3rd, etc for the Person. If GroupOrder is null, the group will be listed in no particular order after the ones that do have a GroupOrder. NOTE: Use int.MaxValue in OrderBy statements for null GroupOrder values |
| GroupRole |  | yes | yes |  |  | Gets or sets the GroupMember's role (GroupTypeRole) in the Group. |
| GroupRoleId | yes | yes |  | yes |  | Gets or sets the Id of the GroupMember's GroupRole in the Group. This property is required. |
| GroupTypeId | yes | yes |  | yes |  | Gets or sets the Id of the GroupType that this Group member belongs to. This property is required. |
| GuestCount | yes | yes |  |  |  | Gets or sets the number of additional guests that member will be bring to group. Only applies when group has the 'AllowGuests' flag set to true. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InactiveDateTime | yes | yes |  |  |  | Gets or sets the date that this group member became inactive |
| IsArchived | yes | yes |  |  |  | Gets or sets a value indicating whether this group member is archived (soft deleted) |
| IsChatBanned | yes | yes |  |  |  | Gets or sets whether this person is banned from the chat channel. It should be assumed that external chat providers do not remove the member from the channel when they are banned; they just set a banned field to true. |
| IsChatMuted | yes | yes |  |  |  | Gets or sets whether notifications for the chat channel are muted for this person. |
| IsNotified | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is notified. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this GroupMember is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. NOTE: Try using IsValidGroupMember instead |
| Item |  |  | yes |  |  |  |
| LearningClass |  | yes | yes |  |  | Gets or sets the related LearningClass. |
| LearningClassActivityCompletions |  |  | yes |  |  | Gets or sets a collection of activities for this participant. |
| LearningClassId | yes | yes |  |  |  | Gets or sets the id of the related LearningClass for this class particpant. |
| LearningCompletionDateTime | yes | yes |  |  |  | Gets or sets the date the student completed the LearningClass. |
| LearningCompletionStatus | yes | yes |  |  |  | Gets or sets the completion status for the participant's LearningClass. This is a hard coded list of values defined in the code as an enumeration. |
| LearningGradePercent | yes | yes |  |  |  | Gets or sets the grade percent achieved for this participant. |
| LearningGradingSystemScale |  | yes | yes |  |  | Gets or sets the related LearningGradingSystemScale. |
| LearningGradingSystemScaleId | yes | yes |  |  |  | Gets or sets the id of the LearningGradingSystemScale for this class participant. |
| LearningParticipantAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| LearningProgramCompletion |  | yes | yes |  |  | Gets or sets the related LearningProgramCompletion. |
| LearningProgramCompletionId | yes | yes |  |  |  | Gets or sets the id of the related LearningProgramCompletion for this particpant. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Note | yes | yes |  |  |  | Gets or sets the note. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  | An optional additional parent authority. (i.e for Groups, the GroupType is main parent authority, but parent group is an additional parent authority ) |
| Person |  | yes | yes |  |  | Gets or sets the Person representing the GroupMember. |
| PersonId | yes | yes |  | yes |  | Gets or sets the Id of the Person that is represented by the GroupMember. This property is required. |
| ScheduleReminderEmailOffsetDays | yes | yes |  |  |  | Gets or sets the number of days prior to the schedule to send a reminder email. See also GroupType.ScheduleReminderEmailOffsetDays. |
| ScheduleStartDate | yes | yes |  |  |  | Gets or sets the schedule start date to base the schedule off of. See GroupMemberScheduleTemplate. |
| ScheduleTemplate |  | yes | yes |  |  | Gets or sets the GroupMemberScheduleTemplate. |
| ScheduleTemplateId | yes | yes |  |  |  | Gets or sets the Id of the GroupMemberScheduleTemplate |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ArchivedByPersonAlias | Gets or sets the PersonAlias that archived (soft deleted) this group member |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| Group | Gets or sets the Group that the GroupMember belongs to. |
| GroupMemberAssignments | Gets or sets the group member assignments. |
| GroupMemberRequirements | Gets or sets the group member requirements. |
| GroupRole | Gets or sets the GroupMember's role (GroupTypeRole) in the Group. |
| IdKey |  |
| LearningClass | Gets or sets the related LearningClass. |
| LearningGradingSystemScale | Gets or sets the related LearningGradingSystemScale. |
| LearningProgramCompletion | Gets or sets the related LearningProgramCompletion. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Person | Gets or sets the Person representing the GroupMember. |
| ScheduleTemplate | Gets or sets the GroupMemberScheduleTemplate. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ArchivedByPersonAlias | [PersonAlias](person-alias.md) |  |
| ArchivedByPersonAliasId | [PersonAliasId](person-alias.md) |  |
| Group | [Group](group.md) |  |
| GroupId | [Group](group.md) |  |
| GroupMemberAssignments | group member assignments |  |
| GroupMemberRequirements | group member requirements |  |
| GroupMemberStatus | GroupMemberStatus |  |
| GroupRole | [Group](group.md) |  |
| GroupRole | [GroupTypeRole](group-type-role.md) |  |
| GroupRoleId | [Group](group.md) |  |
| GroupTypeId | [GroupType](group-type.md) |  |
| LearningClass | [LearningClass](learning-class.md) |  |
| LearningClassActivityCompletions | activities |  |
| LearningClassId | [LearningClass](learning-class.md) |  |
| LearningCompletionDateTime | [LearningClass](learning-class.md) |  |
| LearningGradingSystemScale | [LearningGradingSystemScale](learning-grading-system-scale.md) |  |
| LearningGradingSystemScaleId | [LearningGradingSystemScale](learning-grading-system-scale.md) |  |
| LearningProgramCompletion | [LearningProgramCompletion](learning-program-completion.md) |  |
| LearningProgramCompletionId | [LearningProgramCompletion](learning-program-completion.md) |  |
| Person | [Person](person.md) |  |
| PersonId | [Person](person.md) |  |
| ScheduleStartDate | [GroupMemberScheduleTemplate](group-member-schedule-template.md) |  |
| ScheduleTemplate | [GroupMemberScheduleTemplate](group-member-schedule-template.md) |  |
| ScheduleTemplateId | [GroupMemberScheduleTemplate](group-member-schedule-template.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | GroupMemberStatus | related_entity_links |
