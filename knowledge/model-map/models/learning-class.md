# Learning Class Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `LMS`
- Model title: `LearningClass`
- EntityType GUID: `eb41e4e1-64b1-4aa1-8f66-f0dfd81557d9`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 126 |
| Database-marked properties | 64 |
| Lava-marked properties | 99 |
| Lava-marked non-database properties | 35 |
| Related model links | 38 |
| Pre-alpha changes touching this model | 13 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowGuests | yes | yes |  |  |  | Gets or sets whether group allows members to specify additional "guests" that will be part of the group (i.e. attend event) |
| AllowsInteractiveBulkIndexing |  |  | yes |  |  | Gets a value indicating whether [allows interactive bulk indexing]. |
| Announcements |  |  | yes |  |  | Gets or sets a collection of announcements for the class. |
| ArchivedByPersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias that archived (soft deleted) this group |
| ArchivedByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAliasId that archived (soft deleted) this group |
| ArchivedDateTime | yes | yes |  |  |  | Gets or sets the date time that this group was archived (soft deleted) |
| AreAnyRelationshipMultipliersCustomized |  |  | yes |  |  | Gets whether any relationship multipliers have been customized for this group or its parent group type. |
| AttendanceRecordRequiredForCheckIn | yes | yes |  |  |  | Gets or sets the attendance record required for check in. This is a hard coded list of values defined in the code as an enumeration. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the Campus that this Group is associated with. |
| CampusId | yes | yes |  |  |  | Gets or sets the Id of the Campus that this Group is associated with. |
| ChatChannelAvatarBinaryFile |  | yes | yes |  |  | Gets or sets the chat channel avatar binary file. This is the image that will be shown in the external chat application for this channel. |
| ChatChannelAvatarBinaryFileId | yes | yes |  |  |  | Gets or sets the chat channel avatar binary file identifier. This is the image that will be shown in the external chat application for this channel. |
| ChatChannelKey | yes | yes |  |  |  | Gets or sets the identifier of the chat channel in the external chat service. No assumptions should be made that if this value is set the channel still exists in the external chat service. |
| ChatPushNotificationModeOverride | yes | yes |  |  |  | Gets or sets the ChatNotificationMode to control how push notifications are sent for this chat channel. If set to , then the value of GroupType.ChatPushNotificationMode will be used. This should only be used when editing the group. Call the method instead to determine how push notifications are sent, as that method will also check the GroupType.ChatPushNotificationMode property. This is a hard coded list of values defined in the code as an enumeration. |
| ConfirmationAdditionalDetails | yes | yes |  |  |  | Gets or sets the confirmation additional details. |
| ContentPages |  |  | yes |  |  | Gets or sets a collection of content pages for the class. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the optional description of the group. |
| DisableScheduleToolboxAccess | yes | yes |  |  |  | Gets or sets a flag indicating if the schedule toolbox access is disabled. |
| DisableScheduling | yes | yes |  |  |  | Gets or sets a flag indicating if scheduling is disabled. |
| ElevatedSecurityLevel | yes | yes |  |  |  | Gets or sets the elevated security level. This setting is used to determine the group member's Account Protection Profile. This is a hard coded list of values defined in the code as an enumeration. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GroupAdministratorPersonAlias |  | yes | yes |  |  | Gets or sets the group administrator PersonAlias. |
| GroupAdministratorPersonAliasId |  | yes | yes |  |  | Gets or sets the group administrator PersonAlias identifier. |
| GroupAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupCapacity | yes | yes |  |  |  | Gets or sets the group capacity. |
| GroupLocations |  | yes | yes |  |  | Gets or Sets the GroupLocations that are associated with the Group. |
| GroupMemberRecordSourceValue |  | yes | yes |  |  | Gets or sets the default Record Source Type DefinedValue, representing the source of GroupMembers added to this Group. If set to (or if GroupType.AllowGroupSpecificRecordSource is not ), then the value of GroupType.GroupMemberRecordSourceValue will be used. This should only be used when editing the group. Call the method instead to get the value, as that method will also check the GroupType.GroupMemberRecordSourceValue property. |
| GroupMemberRecordSourceValueId | yes | yes |  |  |  | Gets or sets the default Id of the Record Source Type DefinedValue, representing the source of GroupMembers added to this Group. If set to (or if GroupType.AllowGroupSpecificRecordSource is not ), then the value of GroupType.GroupMemberRecordSourceValueId will be used. This should only be used when editing the group. Call the method instead to get the value, as that method will also check the GroupType.GroupMemberRecordSourceValueId property. These are found in the "Record Source" Defined Type. |
| GroupMemberWorkflowTriggers |  | yes | yes |  |  | Gets or sets the Group Member Workflow Triggers. |
| GroupRequirements |  | yes | yes |  |  | Gets or sets the group requirements (not including GroupRequirements from the GroupType) |
| GroupSalutation | yes | yes |  |  |  | List leaders names, in order by males → females. Examples: Ted & Cindy Decker -or- Ted Decker & Cindy Wright. |
| GroupSalutationFull | yes | yes |  |  |  | List all active group members, or order by leaders males → females - non leaders by age. Examples: Ted, Cindy, Noah and Alex Decker. |
| GroupSyncs |  | yes | yes |  |  | Gets or sets the group syncs. |
| GroupType |  | yes | yes |  |  | Gets or sets the GroupType that this Group is a member of. |
| GroupTypeId | yes | yes |  | yes |  | Gets or sets the Id of the GroupType that this Group is a member belongs to. This property is required. |
| Groups |  | yes | yes |  |  | Gets or sets a collection the Groups that are children of this group. |
| Guid | yes | yes |  |  |  |  |
| HistoryChangeList |  |  | yes |  |  | [Obsoleted in v14] Does nothing. No longer needed. We replaced this with a private property under the SaveHook class for this entity. Gets or sets the history change list. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InactiveDateTime | yes | yes |  |  |  | Gets or sets the date that this group became inactive |
| InactiveReasonNote | yes | yes |  |  |  | Gets or sets the inactive reason note. |
| InactiveReasonValue |  |  | yes |  |  | Gets or sets the inactive group reason. |
| InactiveReasonValueId | yes | yes |  |  |  | Gets or sets the inactive reason value identifier. These are found in the "Inactive Group Reasons" Defined Type. |
| IsActive | yes | yes |  | yes |  | Gets or sets a flag indicating if this is an active group. This value is required. |
| IsArchived | yes | yes |  |  |  | Gets or sets a value indicating whether this group is archived (soft deleted) |
| IsChatChannelAlwaysShownOverride | yes | yes |  |  |  | Gets or sets whether this chat channel is always shown in the channel list even if the person has not joined the channel. This also implies that the channel may be joined by any person via the chat application. If set to , then the value of GroupType.IsChatChannelAlwaysShown will be used. This should only be used when editing the group. Call the method instead to determine if the chat channel is always shown, as that method will also check the GroupType.IsChatChannelAlwaysShown property. |
| IsChatChannelPublicOverride | yes | yes |  |  |  | Gets or sets whether this chat channel is public. A public channel is visible to everyone when performing a search. This also implies that the channel may be joined by any person via the chat application. If set to , then the value of GroupType.IsChatChannelPublic will be used. This should only be used when editing the group. Call the method instead to determine if the chat channel is public, as that method will also check the GroupType.IsChatChannelPublic property. |
| IsChatEnabledOverride | yes | yes |  |  |  | Gets or sets whether chat is enabled for this group. If set to (or if the parent GroupType.IsChatAllowed is set to ), then the group will not have chat enabled. If set to , then it will have chat enabled. If set to , then the value from GroupType.IsChatEnabledForAllGroups will be used. This should only be used when editing the group. Call the method instead to determine if the group is being used for chat, as that method will also check the GroupType.IsChatAllowed and GroupType.IsChatEnabledForAllGroups properties. |
| IsLeavingChatChannelAllowedOverride | yes | yes |  |  |  | Gets or sets whether individuals are allowed to leave this chat channel. If set to , then they will only be allowed to mute the channel. If set to , then they will be allowed to both leave and mute the channel. If set to , then the value of GroupType.IsLeavingChatChannelAllowed will be used. This should only be used when editing the group. Call the method instead to determine if leaving is allowed, as that method will also check the GroupType.IsLeavingChatChannelAllowed property. |
| IsOverridingGroupTypePeerNetworkConfiguration |  |  | yes |  |  | Gets whether this group is overriding its parent group type's peer network configuration in any way. |
| IsPublic | yes | yes |  | yes |  | Gets or sets a value indicating whether the group should be shown in group finders |
| IsSecurityRole | yes | yes |  | yes |  | Indicates this Group is a Security Role even though it isn't a SecurityRole Group Type. Note: Don't use this alone to determine if a Group is a security role group. Use to see if a Group is for a Security Role. |
| IsSpecialNeeds | yes | yes |  |  |  | Gets or sets a value that indicates if this group is a special needs group. For a check-in group, this indicates that the group is intended for people with special needs. It can be used in other contexts to have different meaning for "special needs". |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Group is a part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. |
| Item |  |  | yes |  |  |  |
| LeaderToLeaderRelationshipMultiplierOverride | yes | yes |  |  |  | Gets or sets the leader to leader relationship multiplier. |
| LeaderToNonLeaderRelationshipMultiplierOverride | yes | yes |  |  |  | Gets or sets the leader to non leader relationship multiplier. |
| LearningClassActivities |  |  | yes |  |  | Gets or sets a collection of activities for the class. |
| LearningClassAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| LearningCourse |  | yes | yes |  |  | Gets or sets the related LearningCourse. |
| LearningCourseId | yes | yes |  |  |  | Gets or sets the id of the related LearningCourse for the class. |
| LearningGradingSystem |  | yes | yes |  |  | Gets or sets the related LearningGradingSystem. |
| LearningGradingSystemId | yes | yes |  |  |  | Gets or sets the id of the related LearningGradingSystem for the class. |
| LearningParticipants |  |  | yes |  |  | Gets or sets a collection of participants for the class. |
| LearningSemester |  | yes | yes |  |  | Gets or sets the related LearningSemester. |
| LearningSemesterId | yes | yes |  |  |  | Gets or sets the Id of the related LearningSemester for the class. |
| Linkages |  | yes | yes |  |  | Gets or sets the linkages. |
| Members |  | yes | yes |  |  | Gets or sets a collection containing the GroupMembers who are associated with the Group. Note that this does not include Archived GroupMembers |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the Group. This property is required. |
| NonLeaderToLeaderRelationshipMultiplierOverride | yes | yes |  |  |  | Gets or sets the non leader to leader relationship multiplier. |
| NonLeaderToNonLeaderRelationshipMultiplierOverride | yes | yes |  |  |  | Gets or sets the non leader to non leader relationship multiplier. |
| Order | yes | yes |  | yes |  | Gets or sets the display order of the group in the group list and group hierarchy. The lower the number the higher the display priority this group has. This property is required. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  | An optional additional parent authority. (i.e for Groups, the GroupType is main parent authority, but parent group is an additional parent authority ) |
| ParentGroup |  | yes | yes |  |  | Gets or sets this parent Group of this Group. |
| ParentGroupId | yes | yes |  |  |  | Gets or sets the Id of the Group's Parent Group. |
| RSVPReminderOffsetDays | yes | yes |  |  |  | Gets or sets the number of days prior to the RSVP date that a reminder should be sent. |
| RSVPReminderSystemCommunication |  | yes | yes |  |  | Gets or sets the system communication to use for sending an RSVP reminder. |
| RSVPReminderSystemCommunicationId | yes | yes |  |  |  | Gets or sets the system communication to use for sending an RSVP reminder. |
| RelationshipGrowthEnabledOverride | yes | yes |  |  |  | Gets or sets a value indicating whether relationship growth is enabled. |
| RelationshipStrengthOverride | yes | yes |  |  |  | Gets or sets the relationship strength. |
| ReminderAdditionalDetails | yes | yes |  |  |  | Gets or sets the reminder additional details. |
| ReminderOffsetDays | yes | yes |  |  |  | Gets or sets the number of days prior to an event date that a reminder should be sent. |
| ReminderSystemCommunicationId | yes | yes |  |  |  | Gets or sets the system communication to use for sending a reminder. |
| RequiredSignatureDocumentTemplate |  | yes | yes |  |  | Gets or sets the type of the required signature document. |
| RequiredSignatureDocumentTemplateId | yes | yes |  |  |  | Gets or sets the required signature document type identifier. |
| Schedule |  | yes | yes |  |  | Gets or sets the Schedule. |
| ScheduleCancellationPersonAlias |  |  | yes |  |  | [Obsoleted in v16] Use ScheduleCoordinatorPersonAlias instead. Gets or sets the PersonAlias of the person to notify when a person cancels |
| ScheduleCancellationPersonAliasId |  | yes | yes |  |  | [Obsoleted in v16] Use ScheduleCoordinatorPersonAliasId instead. Gets or sets the PersonAliasId of the person to notify when a person cancels |
| ScheduleConfirmationLogic | yes | yes |  |  |  | Gets or sets the schedule confirmation logic. This is a hard coded list of values defined in the code as an enumeration. |
| ScheduleCoordinatorNotificationTypes | yes | yes |  |  |  | Gets or sets the types of notifications the coordinator receives about scheduled individuals. This is a hard coded list of values defined in the code as an enumeration. |
| ScheduleCoordinatorPersonAlias |  |  | yes |  |  | Gets or sets the PersonAlias of the person who receives notifications about changes to scheduled individuals. |
| ScheduleCoordinatorPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAliasId of the person who receives notifications about changes to scheduled individuals. |
| ScheduleId | yes | yes |  |  |  | Gets or sets the Schedule identifier. |
| SchedulingMustMeetRequirements | yes | yes |  |  |  | Gets or sets a value indicating whether GroupMembers must meet GroupMemberRequirements before they can be scheduled. |
| StatusValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the Group's status. DefinedType depends on this group's GroupType.GroupTypePurposeValue |
| StatusValueId | yes | yes |  |  |  | Gets or sets the Group Status Id. DefinedType depends on this group's GroupType.GroupStatusDefinedType |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ArchivedByPersonAlias | Gets or sets the PersonAlias that archived (soft deleted) this group |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the Campus that this Group is associated with. |
| ChatChannelAvatarBinaryFile | Gets or sets the chat channel avatar binary file. This is the image that will be shown in the external chat application for this channel. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| GroupAdministratorPersonAlias | Gets or sets the group administrator PersonAlias. |
| GroupAdministratorPersonAliasId | Gets or sets the group administrator PersonAlias identifier. |
| GroupLocations | Gets or Sets the GroupLocations that are associated with the Group. |
| GroupMemberRecordSourceValue | Gets or sets the default Record Source Type DefinedValue, representing the source of GroupMembers added to this Group. If set to (or if GroupType.AllowGroupSpecificRecordSource is not ), then the value of GroupType.GroupMemberRecordSourceValue will be used. This should only be used when editing the group. Call the method instead to get the value, as that method will also check the GroupType.GroupMemberRecordSourceValue property. |
| GroupMemberWorkflowTriggers | Gets or sets the Group Member Workflow Triggers. |
| GroupRequirements | Gets or sets the group requirements (not including GroupRequirements from the GroupType) |
| GroupSyncs | Gets or sets the group syncs. |
| GroupType | Gets or sets the GroupType that this Group is a member of. |
| Groups | Gets or sets a collection the Groups that are children of this group. |
| IdKey |  |
| LearningCourse | Gets or sets the related LearningCourse. |
| LearningGradingSystem | Gets or sets the related LearningGradingSystem. |
| LearningSemester | Gets or sets the related LearningSemester. |
| Linkages | Gets or sets the linkages. |
| Members | Gets or sets a collection containing the GroupMembers who are associated with the Group. Note that this does not include Archived GroupMembers |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ParentGroup | Gets or sets this parent Group of this Group. |
| RSVPReminderSystemCommunication | Gets or sets the system communication to use for sending an RSVP reminder. |
| RequiredSignatureDocumentTemplate | Gets or sets the type of the required signature document. |
| Schedule | Gets or sets the Schedule. |
| ScheduleCancellationPersonAliasId | [Obsoleted in v16] Use ScheduleCoordinatorPersonAliasId instead. Gets or sets the PersonAliasId of the person to notify when a person cancels |
| StatusValue | Gets or sets the DefinedValue representing the Group's status. DefinedType depends on this group's GroupType.GroupTypePurposeValue |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Announcements | announcements |  |
| ArchivedByPersonAlias | [PersonAlias](person-alias.md) |  |
| ArchivedByPersonAliasId | [PersonAliasId](person-alias.md) |  |
| Campus | [Campus](campus.md) |  |
| CampusId | [Campus](campus.md) |  |
| ChatPushNotificationModeOverride | ChatNotificationMode |  |
| ContentPages | content pages |  |
| GroupAdministratorPersonAlias | [PersonAlias](person-alias.md) |  |
| GroupAdministratorPersonAliasId | [PersonAlias](person-alias.md) |  |
| GroupLocations | GroupLocations |  |
| GroupMemberRecordSourceValue | [DefinedValue](defined-value.md) |  |
| GroupMemberRecordSourceValue | [Group](group.md) |  |
| GroupMemberRecordSourceValue | [GroupMember](group-member.md) |  |
| GroupMemberRecordSourceValueId | [DefinedValue](defined-value.md) |  |
| GroupMemberRecordSourceValueId | [Group](group.md) |  |
| GroupMemberRecordSourceValueId | [GroupMember](group-member.md) |  |
| GroupMemberWorkflowTriggers | Group Member Workflow Triggers |  |
| GroupSyncs | group syncs |  |
| GroupType | [GroupType](group-type.md) |  |
| GroupTypeId | [GroupType](group-type.md) |  |
| LearningClassActivities | activities |  |
| LearningCourse | [LearningCourse](learning-course.md) |  |
| LearningCourseId | [LearningCourse](learning-course.md) |  |
| LearningGradingSystem | [LearningGradingSystem](learning-grading-system.md) |  |
| LearningGradingSystemId | [LearningGradingSystem](learning-grading-system.md) |  |
| LearningParticipants | participants |  |
| LearningSemester | [LearningSemester](learning-semester.md) |  |
| LearningSemesterId | [LearningSemester](learning-semester.md) |  |
| Linkages | linkages |  |
| Members | GroupMembers |  |
| Schedule | [Schedule](schedule.md) |  |
| ScheduleCancellationPersonAlias | [PersonAlias](person-alias.md) |  |
| ScheduleCancellationPersonAliasId | [PersonAliasId](person-alias.md) |  |
| ScheduleCoordinatorPersonAlias | [PersonAlias](person-alias.md) |  |
| ScheduleCoordinatorPersonAliasId | [PersonAliasId](person-alias.md) |  |
| ScheduleId | [Schedule](schedule.md) |  |
| StatusValue | [DefinedValue](defined-value.md) |  |
| SupportedActions | Dictionary`2 |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_removed | HistoryChangeList |  |
| property_changed | ChatPushNotificationModeOverride | description, related_entity_links |
| property_changed | GroupMemberRecordSourceValue | description |
| property_changed | GroupMemberRecordSourceValueId | description, enum_values |
| property_changed | GroupSalutation | description |
| property_changed | IsChatChannelAlwaysShownOverride | description |
| property_changed | IsChatChannelPublicOverride | description |
| property_changed | IsChatEnabledOverride | description |
| property_changed | IsLeavingChatChannelAllowedOverride | description |
| property_changed | IsSecurityRole | description |
| property_changed | ScheduleCancellationPersonAlias | description, is_obsolete |
| property_changed | ScheduleCancellationPersonAliasId | description, is_obsolete |
| property_changed | SupportedActions | related_entity_links |
