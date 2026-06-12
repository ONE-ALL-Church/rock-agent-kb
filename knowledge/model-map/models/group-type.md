# Group Type Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Group`
- Model title: `GroupType`
- EntityType GUID: `0dd30b04-01cf-4b38-8e83-be661e2f7286`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 138 |
| Database-marked properties | 88 |
| Lava-marked properties | 116 |
| Lava-marked non-database properties | 28 |
| Related model links | 36 |
| Pre-alpha changes touching this model | 14 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AdministratorTerm | yes | yes |  |  |  | Gets or sets the administrator term for the group of this GroupType. |
| AllowAnyChildGroupType | yes | yes |  |  |  | Gets or sets a value indicating if group type allows any child group type. |
| AllowGroupSpecificRecordSource | yes | yes |  |  |  | Gets or sets whether Groups of this type can override GroupMemberRecordSourceValueId. |
| AllowGroupSync | yes | yes |  |  |  | Gets or sets a flag indicating if groups of this type are allowed to be sync'ed. |
| AllowMultipleLocations | yes | yes |  |  |  | Gets or sets a flag indicating if Groups of this type are allowed to have multiple locations. |
| AllowSpecificGroupMemberAttributes | yes | yes |  |  |  | Gets or sets a flag indicating if specific groups are allowed to have their own member attributes. |
| AllowSpecificGroupMemberWorkflows | yes | yes |  |  |  | Gets or sets a flag indicating if groups of this type should be allowed to have Group Member Workflows. |
| AllowedScheduleTypes | yes | yes |  |  |  | Gets or sets the allowed schedule types. This is a hard coded list of values defined in the code as an enumeration. |
| AlreadyEnrolledMatchingLogic | yes | yes |  |  |  | When AttendanceRule is set to then this specifies the group matching logic used. simply that the person be a member of the group and no additional filtering is performed. will additionally then filter out any non-preferred groups if the person is a member of any preferred groups. This is a hard coded list of values defined in the code as an enumeration. |
| AreAnyRelationshipMultipliersCustomized |  |  | yes |  |  | Gets whether any relationship multipliers have been customized for this group type (if any of them don't equal 100%). |
| AttendanceCountsAsWeekendService | yes | yes |  |  |  | Gets or sets a value indicating whether [attendance counts as weekend service]. |
| AttendancePrintTo | yes | yes |  |  |  | Gets or sets the PrintTo indicating the type of location of where attendee labels for Groups of this GroupType should print. This is a hard coded list of values defined in the code as an enumeration. |
| AttendanceReminderFollowupDays | yes | yes |  |  |  | Gets or sets the attendance reminder followup days. This is a comma-delimited list of integer values. See AttendanceReminderFollowupDaysList |
| AttendanceReminderFollowupDaysList |  |  | yes |  |  | Gets or sets the attendance reminder followup days list. This is the logical representation of AttendanceReminderFollowupDays. |
| AttendanceReminderSendStartOffsetMinutes | yes | yes |  |  |  | Gets or sets the attendance reminder send start offset minutes. |
| AttendanceReminderSystemCommunication |  | yes | yes |  |  | Gets or sets the attendance reminder system communication. |
| AttendanceReminderSystemCommunicationId | yes | yes |  |  |  | Gets or sets the attendance reminder system communication identifier. |
| AttendanceRule | yes | yes |  |  |  | Gets or sets the AttendanceRule that indicates how attendance is managed a Group of this GroupType This is a hard coded list of values defined in the code as an enumeration. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ChatPushNotificationMode | yes | yes |  |  |  | Gets or sets the ChatNotificationMode to control how push notifications are sent for chat channels of this type. This can be overridden by the value of Group.ChatPushNotificationModeOverride. This is a hard coded list of values defined in the code as an enumeration. |
| ChildGroupTypes |  | yes | yes |  |  | Gets or sets the collection of GroupTypes that inherit from this GroupType. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefaultGroupRole |  | yes | yes |  |  | Gets or sets the default GroupTypeRole for GroupMembers who belong to a Group of this GroupType. |
| DefaultGroupRoleId | yes | yes |  |  |  | Gets or sets the Id of the GroupTypeRole that a GroupMember of a Group belonging to this GroupType is given by default. |
| Description | yes | yes |  |  |  | Gets or sets the Description of the GroupType. |
| EnableGroupHistory | yes | yes |  |  |  | Gets or sets a value indicating whether group history should be enabled for groups of this type |
| EnableGroupTag | yes | yes |  |  |  | Gets or sets a value indicating whether group tag should be enabled for groups of this type |
| EnableInactiveReason | yes | yes |  |  |  | Gets or sets a value indicating whether [enable inactive reason]. |
| EnableLocationSchedules | yes | yes |  |  |  | Gets or sets the enable location schedules. |
| EnableRSVP | yes | yes |  |  |  | Indicates whether RSVP functionality should be enabled for this group. |
| EnableSpecificGroupRequirements | yes | yes |  |  |  | Gets or sets a flag indicating if group requirements section is enabled for group of this type. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GroupAttendanceRequiresLocation | yes | yes |  |  |  | Gets or sets a value indicating whether [group attendance requires location]. |
| GroupAttendanceRequiresSchedule | yes | yes |  |  |  | Gets or sets a value indicating whether [group attendance requires schedule]. |
| GroupCapacityRule | yes | yes |  |  |  | Gets or sets the group capacity rule. This is a hard coded list of values defined in the code as an enumeration. |
| GroupCount |  | yes | yes |  |  | Gets a count of Groups that belong to this GroupType. |
| GroupMemberRecordSourceValue |  | yes | yes |  |  | Gets or sets the default Record Source Type DefinedValue, representing the source of GroupMembers added to Groups of this type. This can be overridden by Group.GroupMemberRecordSourceValue if AllowGroupSpecificRecordSource is . |
| GroupMemberRecordSourceValueId | yes | yes |  |  |  | Gets or sets the default Id of the Record Source Type DefinedValue, representing the source of GroupMembers added to Groups of this type. This can be overridden by Group.GroupMemberRecordSourceValueId. These are found in the "Record Source" Defined Type. |
| GroupMemberTerm | yes | yes |  | yes |  | Gets or sets the term that a GroupMember of a Group that belongs to this GroupType is called. |
| GroupMemberWorkflowTriggers |  |  | yes |  |  | Gets or sets the group member workflow triggers. |
| GroupQuery |  |  | yes |  |  | Gets a queryable collection of Groups that belong to this GroupType. |
| GroupRequirements |  | yes | yes |  |  | Gets or sets the group requirements for groups of this Group Type (NOTE: Groups also can have additional GroupRequirements ) |
| GroupScheduleExclusions |  |  | yes |  |  | Gets or sets the group schedule exclusions. |
| GroupStatusDefinedType |  |  | yes |  |  | Gets or sets the DefinedType that Groups of this type will use for the Group.StatusValue |
| GroupStatusDefinedTypeId | yes | yes |  |  |  | Gets or sets the DefinedType that Groups of this type will use for the Group.StatusValue |
| GroupTerm | yes | yes |  | yes |  | Gets or sets the term that a Group belonging to this GroupType is called. |
| GroupTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupTypeColor | yes | yes |  |  |  | The color used to visually distinguish groups on lists. |
| GroupTypePurposeValue |  | yes | yes |  |  | Gets or sets the DefinedValue that represents the purpose of the GroupType. |
| GroupTypePurposeValueId | yes | yes |  |  |  | Gets or sets Id of the DefinedValue that represents the purpose of the GroupType. These are found in the "Group Type Purpose" Defined Type. |
| GroupViewLavaTemplate | yes | yes |  |  |  | Gets or sets a lava template that can be used for generating view details for Group. |
| Groups |  | yes | yes |  |  | Gets or sets a collection of the Groups that belong to this GroupType. |
| GroupsRequireCampus | yes | yes |  |  |  | Gets or sets a value indicating whether [groups require campus]. |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class name for a font vector based icon. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IgnorePersonInactivated | yes | yes |  |  |  | Gets or sets a value indicating whether to ignore person inactivated. By default group members are inactivated in their group whenever the person is inactivated. If this value is set to true, members in groups of this type will not be marked inactive when the person is inactivated |
| InheritedGroupType |  | yes | yes |  |  | Gets or sets the GroupType that this GroupType is inheriting settings and properties from. This is similar to a parent or a template GroupType. |
| InheritedGroupTypeId | yes | yes |  |  |  | Gets or sets the Id of the GroupType to inherit settings and properties from. This is essentially copying the values, but they can be overridden. |
| IsCapacityRequired | yes | yes |  | yes |  | Gets or sets a value indicating whether this instance is capacity required. |
| IsChatAllowed | yes | yes |  |  |  | Gets or sets whether groups of this type are allowed to participate in the chat system as a chat channel. |
| IsChatChannelAlwaysShown | yes | yes |  |  |  | Gets or sets whether chat channels of this type are always shown in the channel list even if the person has not joined the channel. This also implies that the channel may be joined by any person via the chat application. This can be overridden by the value of Group.IsChatChannelAlwaysShownOverride. |
| IsChatChannelPublic | yes | yes |  |  |  | Gets or sets whether chat channels of this type are public. A public channel is visible to everyone when performing a search. This also implies that the channel may be joined by any person via the chat application. This can be overridden by the value of Group.IsChatChannelPublicOverride. |
| IsChatEnabledForAllGroups | yes | yes |  |  |  | Gets or sets whether all groups of this type have the chat feature enabled by default. This can be overridden by the value of Group.IsChatEnabledOverride. |
| IsConcurrentCheckInPrevented | yes | yes |  |  |  | Gets or sets a value that groups in this area should not be available when a person already has a check-in for the same schedule. |
| IsIndexEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is index enabled. |
| IsLeavingChatChannelAllowed | yes | yes |  |  |  | Gets or sets whether individuals are allowed to leave chat channels of this type. If set to , then they will only be allowed to mute the channel. This can be overridden by the value of Group.IsLeavingChatChannelAllowedOverride. |
| IsPeerNetworkEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether the Group Type has Peer Network enabled. |
| IsSchedulingEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether scheduling is enabled for groups of this type |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this GroupType is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. |
| Item |  |  | yes |  |  |  |
| LeaderToLeaderRelationshipMultiplier | yes | yes |  |  |  | Gets or sets the leader to leader relationship multiplier. |
| LeaderToNonLeaderRelationshipMultiplier | yes | yes |  |  |  | Gets or sets the leader to non leader relationship multiplier. |
| LocationSelectionMode | yes | yes |  |  |  | Gets or sets selection mode that the Location Picker should use when adding locations to groups of this type This is a hard coded list of values defined in the code as an enumeration. |
| LocationTypes |  | yes | yes |  |  | Gets or sets a collection of the GroupTypeLocationTypes that are associated with this GroupType. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the GroupType. This property is required. |
| NonLeaderToLeaderRelationshipMultiplier | yes | yes |  |  |  | Gets or sets the non leader to leader relationship multiplier. |
| NonLeaderToNonLeaderRelationshipMultiplier | yes | yes |  |  |  | Gets or sets the non leader to non leader relationship multiplier. |
| Order | yes | yes |  | yes |  | Gets or sets the order for this GroupType. This is used for display and priority purposes, the lower the number the higher the priority, or the higher the GroupType is displayed. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ParentGroupTypes |  |  | yes |  |  | Gets or sets a collection containing the GroupTypes that this GroupType inherits from. |
| RSVPReminderOffsetDays | yes | yes |  |  |  | Gets or sets the number of days prior to the RSVP date that a reminder should be sent. |
| RSVPReminderSystemCommunicationId | yes | yes |  |  |  | Gets or sets the system communication to use for sending an RSVP reminder. |
| RelationshipGrowthEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether relationship growth is enabled. |
| RelationshipStrength | yes | yes |  |  |  | Gets or sets the relationship strength. |
| RequiresInactiveReason | yes | yes |  |  |  | Gets or sets a value indicating whether [requires inactive reason]. |
| RequiresReasonIfDeclineSchedule | yes | yes |  |  |  | Gets or sets a value indicating whether a person must specify a reason when declining/cancelling. |
| Roles |  | yes | yes |  |  | Gets or sets a collection containing the GroupRoles that this GroupType utilizes. |
| ScheduleCancellationWorkflowType |  | yes | yes |  |  | Gets or sets the WorkflowType to execute when a person indicates they won't be able to attend at their scheduled time |
| ScheduleCancellationWorkflowTypeId | yes | yes |  |  |  | Gets or sets the WorkflowType to execute when a person indicates they won't be able to attend at their scheduled time |
| ScheduleConfirmationEmailOffsetDays | yes | yes |  |  |  | Gets or sets the number of days prior to the schedule to send a confirmation email. |
| ScheduleConfirmationLogic | yes | yes |  |  |  | Gets or sets the schedule confirmation logic. This is a hard coded list of values defined in the code as an enumeration. |
| ScheduleConfirmationSystemCommunication |  | yes | yes |  |  | Gets or sets the system communication to use when a person is scheduled or when the schedule has been updated |
| ScheduleConfirmationSystemCommunicationId | yes | yes |  |  |  | Gets or sets the system communication to use when a person is scheduled or when the schedule has been updated. |
| ScheduleConfirmationSystemEmail |  | yes | yes |  |  | [Obsoleted in v10] Use ScheduleConfirmationSystemCommunication instead. Gets or sets the system email to use when a person is scheduled or when the schedule has been updated |
| ScheduleConfirmationSystemEmailId | yes | yes |  |  |  | [Obsoleted in v10] Use ScheduleConfirmationSystemCommunicationId instead. Gets or sets the system email to use when a person is scheduled or when the schedule has been updated |
| ScheduleCoordinatorNotificationTypes | yes | yes |  |  |  | Gets or sets the types of notifications the coordinator receives about scheduled individuals. This is a hard coded list of values defined in the code as an enumeration. |
| ScheduleReminderEmailOffsetDays | yes | yes |  |  |  | Gets or sets the number of days prior to the schedule to send a reminder email. See also GroupMember.ScheduleReminderEmailOffsetDays. |
| ScheduleReminderSystemCommunication |  | yes | yes |  |  | Gets or sets the system communication to use when sending a Schedule Reminder |
| ScheduleReminderSystemCommunicationId | yes | yes |  |  |  | Gets or sets the system communication to use when sending a schedule reminder. |
| ScheduleReminderSystemEmail |  | yes | yes |  |  | [Obsoleted in v10] Use ScheduleReminderSystemCommunication instead. Gets or sets the system email to use when sending a Schedule Reminder |
| ScheduleReminderSystemEmailId | yes | yes |  |  |  | [Obsoleted in v10] Use ScheduleReminderSystemCommunicationId instead. Gets or sets the system email to use when sending a schedule reminder |
| SendAttendanceReminder | yes | yes |  |  |  | Gets or sets a value indicating if an attendance reminder should be sent to group leaders. |
| ShowAdministrator | yes | yes |  | yes |  | Gets or sets a value indicating whether administrator for the group of this GroupType will be shown. |
| ShowConnectionStatus | yes | yes |  |  |  | Gets or sets a value indicating whether to show the Person's connection status as a column in the Group Member Grid |
| ShowInGroupList | yes | yes |  |  |  | Gets or sets a flag indicating if a Group of this GroupType will be shown in the group list. |
| ShowInNavigation | yes | yes |  |  |  | Gets or sets a flag indicating if this GroupType and its Groups are shown in Navigation. If false, this GroupType will be hidden navigation controls, such as TreeViews and Menus |
| ShowMaritalStatus | yes | yes |  |  |  | Gets or sets a value indicating whether to show the Person's marital status as a column in the Group Member Grid |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TakesAttendance | yes | yes |  |  |  | Gets or sets a flag indicating if a Group of this GroupType supports taking attendance. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttendanceReminderSystemCommunication | Gets or sets the attendance reminder system communication. |
| AttributeValues |  |
| Attributes |  |
| ChildGroupTypes | Gets or sets the collection of GroupTypes that inherit from this GroupType. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DefaultGroupRole | Gets or sets the default GroupTypeRole for GroupMembers who belong to a Group of this GroupType. |
| EntityStringValue |  |
| GroupCount | Gets a count of Groups that belong to this GroupType. |
| GroupMemberRecordSourceValue | Gets or sets the default Record Source Type DefinedValue, representing the source of GroupMembers added to Groups of this type. This can be overridden by Group.GroupMemberRecordSourceValue if AllowGroupSpecificRecordSource is . |
| GroupRequirements | Gets or sets the group requirements for groups of this Group Type (NOTE: Groups also can have additional GroupRequirements ) |
| GroupTypePurposeValue | Gets or sets the DefinedValue that represents the purpose of the GroupType. |
| Groups | Gets or sets a collection of the Groups that belong to this GroupType. |
| IdKey |  |
| InheritedGroupType | Gets or sets the GroupType that this GroupType is inheriting settings and properties from. This is similar to a parent or a template GroupType. |
| LocationTypes | Gets or sets a collection of the GroupTypeLocationTypes that are associated with this GroupType. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Roles | Gets or sets a collection containing the GroupRoles that this GroupType utilizes. |
| ScheduleCancellationWorkflowType | Gets or sets the WorkflowType to execute when a person indicates they won't be able to attend at their scheduled time |
| ScheduleConfirmationSystemCommunication | Gets or sets the system communication to use when a person is scheduled or when the schedule has been updated |
| ScheduleConfirmationSystemEmail | [Obsoleted in v10] Use ScheduleConfirmationSystemCommunication instead. Gets or sets the system email to use when a person is scheduled or when the schedule has been updated |
| ScheduleReminderSystemCommunication | Gets or sets the system communication to use when sending a Schedule Reminder |
| ScheduleReminderSystemEmail | [Obsoleted in v10] Use ScheduleReminderSystemCommunication instead. Gets or sets the system email to use when sending a Schedule Reminder |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AllowGroupSpecificRecordSource | [Group](group.md) |  |
| AllowMultipleLocations | Groups |  |
| AttendancePrintTo | Groups |  |
| AttendancePrintTo | PrintTo |  |
| AttendanceRule | AttendanceRule |  |
| AttendanceRule | [Group](group.md) |  |
| ChatPushNotificationMode | ChatNotificationMode |  |
| ChildGroupTypes | GroupTypes |  |
| DefaultGroupRole | [Group](group.md) |  |
| DefaultGroupRole | GroupMembers |  |
| DefaultGroupRole | [GroupTypeRole](group-type-role.md) |  |
| DefaultGroupRoleId | [Group](group.md) |  |
| DefaultGroupRoleId | [GroupMember](group-member.md) |  |
| DefaultGroupRoleId | [GroupTypeRole](group-type-role.md) |  |
| GroupCount | Groups |  |
| GroupMemberRecordSourceValue | [DefinedValue](defined-value.md) |  |
| GroupMemberRecordSourceValue | [Group](group.md) |  |
| GroupMemberRecordSourceValue | [GroupMember](group-member.md) |  |
| GroupMemberRecordSourceValueId | [DefinedValue](defined-value.md) |  |
| GroupMemberRecordSourceValueId | [Group](group.md) |  |
| GroupMemberRecordSourceValueId | [GroupMember](group-member.md) |  |
| GroupMemberTerm | [Group](group.md) |  |
| GroupMemberTerm | [GroupMember](group-member.md) |  |
| GroupQuery | Groups |  |
| GroupTerm | [Group](group.md) |  |
| GroupTerm | [GroupType](group-type.md) |  |
| GroupTypePurposeValue | [DefinedValue](defined-value.md) |  |
| GroupTypePurposeValueId | [DefinedValue](defined-value.md) |  |
| Groups | Groups |  |
| InheritedGroupType | [GroupType](group-type.md) |  |
| LocationTypes | GroupTypeLocationTypes |  |
| Roles | GroupRoles |  |
| ShowInGroupList | [Group](group.md) |  |
| ShowInNavigation | Groups |  |
| SupportedActions | Dictionary`2 |  |
| TakesAttendance | [Group](group.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | RSVPReminderSystemCommunication |  |
| property_removed | ScheduleConfirmationSystemEmail |  |
| property_removed | ScheduleConfirmationSystemEmailId |  |
| property_removed | ScheduleReminderSystemEmail |  |
| property_removed | ScheduleReminderSystemEmailId |  |
| property_changed | AlreadyEnrolledMatchingLogic | description |
| property_changed | AttendancePrintTo | related_entity_links |
| property_changed | AttendanceRule | related_entity_links |
| property_changed | ChatPushNotificationMode | related_entity_links |
| property_changed | GroupMemberRecordSourceValue | description |
| property_changed | GroupMemberRecordSourceValueId | enum_values |
| property_changed | IsLeavingChatChannelAllowed | description |
| property_changed | LocationTypes | related_entity_links |
| property_changed | SupportedActions | related_entity_links |
