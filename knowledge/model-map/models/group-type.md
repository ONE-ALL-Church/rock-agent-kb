# Group Type Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Group`
- Model title: `GroupType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `42`
- Obsolete methods: `5`
- EntityType GUID: `0dd30b04-01cf-4b38-8e83-be661e2f7286`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 135 |
| Database-marked properties | 86 |
| Lava-marked properties | 113 |
| Lava-marked non-database properties | 27 |
| Related model links | 31 |
| Method signatures | 42 |
| Obsolete methods | 5 |
| Pre-alpha changes touching this model | 3 |

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
| AlreadyEnrolledMatchingLogic | yes | yes |  |  |  | When AttendanceRule is set to AttendanceRule.AlreadyEnrolledInGroup then this specifies the group matching logic used. Rock.Enums.CheckIn.AlreadyEnrolledMatchingLogic.MustBeEnrolled simply that the person be a member of the group and no additional filtering is performed. Rock.Enums.CheckIn.AlreadyEnrolledMatchingLogic.PreferEnrolledGroups will additionally then filter out any non-preferred groups if the person is a member of any preferred groups. This is a hard coded list of values defined in the code as an enumeration. |
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
| DefaultGroupRole |  | yes | yes |  |  | Gets or sets the default Group Type Role for GroupMembers who belong to a Group of this GroupType. |
| DefaultGroupRoleId | yes | yes |  |  |  | Gets or sets the Id of the Group Type Role that a Group Member of a Group belonging to this GroupType is given by default. |
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
| GroupMemberRecordSourceValue |  | yes | yes |  |  | Gets or sets the default Record Source Type Defined Value, representing the source of Group Members added to Groups of this type. This can be overridden by Group.GroupMemberRecordSourceValue if AllowGroupSpecificRecordSource is true. |
| GroupMemberRecordSourceValueId | yes | yes |  |  |  | Gets or sets the default Id of the Record Source Type Defined Value, representing the source of Group Members added to Groups of this type. This can be overridden by Group.GroupMemberRecordSourceValueId. These are found in the Record Source Defined Type. |
| GroupMemberTerm | yes | yes |  | yes |  | Gets or sets the term that a Group Member of a Group that belongs to this GroupType is called. |
| GroupMemberWorkflowTriggers |  |  | yes |  |  | Gets or sets the group member workflow triggers. |
| GroupQuery |  |  | yes |  |  | Gets a queryable collection of Groups that belong to this GroupType. |
| GroupRequirements |  | yes | yes |  |  | Gets or sets the group requirements for groups of this Group Type (NOTE: Groups also can have additional GroupRequirements ) |
| GroupScheduleExclusions |  |  | yes |  |  | Gets or sets the group schedule exclusions. |
| GroupStatusDefinedType |  |  | yes |  |  | Gets or sets the DefinedType that Groups of this type will use for the Group.StatusValue |
| GroupStatusDefinedTypeId | yes | yes |  |  |  | Gets or sets the DefinedType that Groups of this type will use for the Group.StatusValue |
| GroupTerm | yes | yes |  | yes |  | Gets or sets the term that a Group belonging to this Group Type is called. |
| GroupTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupTypeColor | yes | yes |  |  |  | The color used to visually distinguish groups on lists. |
| GroupTypePurposeValue |  | yes | yes |  |  | Gets or sets the Defined Value that represents the purpose of the GroupType. |
| GroupTypePurposeValueId | yes | yes |  |  |  | Gets or sets Id of the Defined Value that represents the purpose of the GroupType. These are found in the Group Type Purpose Defined Type. |
| GroupViewLavaTemplate | yes | yes |  |  |  | Gets or sets a lava template that can be used for generating view details for Group. |
| Groups |  | yes | yes |  |  | Gets or sets a collection of the Groups that belong to this GroupType. |
| GroupsRequireCampus | yes | yes |  |  |  | Gets or sets a value indicating whether [groups require campus]. |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class name for a font vector based icon. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IgnorePersonInactivated | yes | yes |  |  |  | Gets or sets a value indicating whether to ignore person inactivated. By default group members are inactivated in their group whenever the person is inactivated. If this value is set to true, members in groups of this type will not be marked inactive when the person is inactivated |
| InheritedGroupType |  | yes | yes |  |  | Gets or sets the Group Type that this GroupType is inheriting settings and properties from. This is similar to a parent or a template GroupType. |
| InheritedGroupTypeId | yes | yes |  |  |  | Gets or sets the Id of the GroupType to inherit settings and properties from. This is essentially copying the values, but they can be overridden. |
| IsCapacityRequired | yes | yes |  | yes |  | Gets or sets a value indicating whether this instance is capacity required. |
| IsChatAllowed | yes | yes |  |  |  | Gets or sets whether groups of this type are allowed to participate in the chat system as a chat channel. |
| IsChatChannelAlwaysShown | yes | yes |  |  |  | Gets or sets whether chat channels of this type are always shown in the channel list even if the person has not joined the channel. This also implies that the channel may be joined by any person via the chat application. This can be overridden by the value of Group.IsChatChannelAlwaysShownOverride. |
| IsChatChannelPublic | yes | yes |  |  |  | Gets or sets whether chat channels of this type are public. A public channel is visible to everyone when performing a search. This also implies that the channel may be joined by any person via the chat application. This can be overridden by the value of Group.IsChatChannelPublicOverride. |
| IsChatEnabledForAllGroups | yes | yes |  |  |  | Gets or sets whether all groups of this type have the chat feature enabled by default. This can be overridden by the value of Group.IsChatEnabledOverride. |
| IsConcurrentCheckInPrevented | yes | yes |  |  |  | Gets or sets a value that groups in this area should not be available when a person already has a check-in for the same schedule. |
| IsIndexEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is index enabled. |
| IsLeavingChatChannelAllowed | yes | yes |  |  |  | Gets or sets whether individuals are allowed to leave chat channels of this type. If set to false, then they will only be allowed to mute the channel. This can be overridden by the value of Group.IsLeavingChatChannelAllowedOverride. |
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
| RSVPReminderSystemCommunication |  | yes | yes |  |  | Gets or sets the system communication to use for sending an RSVP reminder. |
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
| ScheduleCoordinatorNotificationTypes | yes | yes |  |  |  | Gets or sets the types of notifications the coordinator receives about scheduled individuals. This is a hard coded list of values defined in the code as an enumeration. |
| ScheduleReminderEmailOffsetDays | yes | yes |  |  |  | Gets or sets the number of days prior to the schedule to send a reminder email. See also GroupMember.ScheduleReminderEmailOffsetDays. |
| ScheduleReminderSystemCommunication |  | yes | yes |  |  | Gets or sets the system communication to use when sending a Schedule Reminder |
| ScheduleReminderSystemCommunicationId | yes | yes |  |  |  | Gets or sets the system communication to use when sending a schedule reminder. |
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
| DefaultGroupRole | Gets or sets the default Group Type Role for GroupMembers who belong to a Group of this GroupType. |
| EntityStringValue |  |
| GroupCount | Gets a count of Groups that belong to this GroupType. |
| GroupMemberRecordSourceValue | Gets or sets the default Record Source Type Defined Value, representing the source of Group Members added to Groups of this type. This can be overridden by Group.GroupMemberRecordSourceValue if AllowGroupSpecificRecordSource is true. |
| GroupRequirements | Gets or sets the group requirements for groups of this Group Type (NOTE: Groups also can have additional GroupRequirements ) |
| GroupTypePurposeValue | Gets or sets the Defined Value that represents the purpose of the GroupType. |
| Groups | Gets or sets a collection of the Groups that belong to this GroupType. |
| IdKey |  |
| InheritedGroupType | Gets or sets the Group Type that this GroupType is inheriting settings and properties from. This is similar to a parent or a template GroupType. |
| LocationTypes | Gets or sets a collection of the GroupTypeLocationTypes that are associated with this GroupType. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RSVPReminderSystemCommunication | Gets or sets the system communication to use for sending an RSVP reminder. |
| Roles | Gets or sets a collection containing the GroupRoles that this GroupType utilizes. |
| ScheduleCancellationWorkflowType | Gets or sets the WorkflowType to execute when a person indicates they won't be able to attend at their scheduled time |
| ScheduleConfirmationSystemCommunication | Gets or sets the system communication to use when a person is scheduled or when the schedule has been updated |
| ScheduleReminderSystemCommunication | Gets or sets the system communication to use when sending a Schedule Reminder |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AllowGroupSpecificRecordSource | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| AllowMultipleLocations | Groups | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| AttendancePrintTo | Groups | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| AttendanceRule | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| ChildGroupTypes | GroupTypes | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |
| DefaultGroupRole | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| DefaultGroupRole | GroupMembers | 49668b95-fedc-43dd-8085-d2b0d6343c48 |
| DefaultGroupRole | [Group Type Role](group-type-role.md) | d155c373-9e47-4c6a-badd-792f31af5fba |
| DefaultGroupRoleId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| DefaultGroupRoleId | [Group Member](group-member.md) | 49668b95-fedc-43dd-8085-d2b0d6343c48 |
| DefaultGroupRoleId | [Group Type Role](group-type-role.md) | d155c373-9e47-4c6a-badd-792f31af5fba |
| GroupCount | Groups | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupMemberRecordSourceValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| GroupMemberRecordSourceValue | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupMemberRecordSourceValue | [Group Member](group-member.md) | 49668b95-fedc-43dd-8085-d2b0d6343c48 |
| GroupMemberRecordSourceValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| GroupMemberRecordSourceValueId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupMemberRecordSourceValueId | [Group Member](group-member.md) | 49668b95-fedc-43dd-8085-d2b0d6343c48 |
| GroupMemberTerm | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupMemberTerm | [Group Member](group-member.md) | 49668b95-fedc-43dd-8085-d2b0d6343c48 |
| GroupQuery | Groups | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupTerm | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupTerm | [Group Type](group-type.md) | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |
| GroupTypePurposeValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| GroupTypePurposeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| Groups | Groups | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| InheritedGroupType | [Group Type](group-type.md) | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |
| Roles | GroupRoles | d155c373-9e47-4c6a-badd-792f31af5fba |
| ShowInGroupList | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| ShowInNavigation | Groups | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| TakesAttendance | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | IsMeetingStyleEnabled |  |
| property_changed | GroupMemberRecordSourceValueId | enum_values |
| property_changed | GroupTypePurposeValueId | enum_values |
