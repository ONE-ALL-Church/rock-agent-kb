# Group Member Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Group`
- Model title: `GroupMember`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `42`
- Obsolete methods: `4`
- EntityType GUID: `49668b95-fedc-43dd-8085-d2b0d6343c48`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 64 |
| Database-marked properties | 30 |
| Lava-marked properties | 49 |
| Lava-marked non-database properties | 19 |
| Related model links | 15 |
| Method signatures | 42 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| ArchivedByPersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias that archived (soft deleted) this group member |
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
| GroupRole |  | yes | yes |  |  | Gets or sets the GroupMember's role (Group Type Role) in the Group. |
| GroupRoleId | yes | yes |  | yes |  | Gets or sets the Id of the GroupMember's GroupRole in the Group. This property is required. |
| GroupTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Group Type that this Group member belongs to. This property is required. |
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
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Note | yes | yes |  |  |  | Gets or sets the note. |
| ParentAuthority |  |  | yes |  |  | A parent authority. If a user is not specifically allowed or denied access to this object, Rock will check the default authorization on the current type, and then the authorization on the Rock.Security.GlobalDefault entity |
| ParentAuthorityPre |  |  | yes |  |  | An optional additional parent authority. (i.e for Groups, the GroupType is main parent authority, but parent group is an additional parent authority ) |
| Person |  | yes | yes |  |  | Gets or sets the Person representing the GroupMember. |
| PersonId | yes | yes |  | yes |  | Gets or sets the Id of the Person that is represented by the GroupMember. This property is required. |
| ScheduleReminderEmailOffsetDays | yes | yes |  |  |  | Gets or sets the number of days prior to the schedule to send a reminder email. See also GroupType.ScheduleReminderEmailOffsetDays. |
| ScheduleStartDate | yes | yes |  |  |  | Gets or sets the schedule start date to base the schedule off of. See Group Member Schedule Template. |
| ScheduleTemplate |  | yes | yes |  |  | Gets or sets the Group Member Schedule Template. |
| ScheduleTemplateId | yes | yes |  |  |  | Gets or sets the Id of the Group Member Schedule Template |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ArchivedByPersonAlias | Gets or sets the Person Alias that archived (soft deleted) this group member |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| Group | Gets or sets the Group that the GroupMember belongs to. |
| GroupMemberAssignments | Gets or sets the group member assignments. |
| GroupMemberRequirements | Gets or sets the group member requirements. |
| GroupRole | Gets or sets the GroupMember's role (Group Type Role) in the Group. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Person | Gets or sets the Person representing the GroupMember. |
| ScheduleTemplate | Gets or sets the Group Member Schedule Template. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ArchivedByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| ArchivedByPersonAliasId | [PersonAliasId](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupMemberAssignments | group member assignments | 22bf14ed-e882-4bb0-9328-d12545bf5f61 |
| GroupMemberRequirements | group member requirements | ff1b2c4b-0f2d-4d9b-9e85-7336ccc24a62 |
| GroupRole | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupRole | [Group Type Role](group-type-role.md) | d155c373-9e47-4c6a-badd-792f31af5fba |
| GroupRoleId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupTypeId | [Group Type](group-type.md) | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |
| Person | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| PersonId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| ScheduleStartDate | [Group Member Schedule Template](group-member-schedule-template.md) | d84ed719-b659-433c-bfa0-e798e52c6b24 |
| ScheduleTemplate | [Group Member Schedule Template](group-member-schedule-template.md) | d84ed719-b659-433c-bfa0-e798e52c6b24 |
| ScheduleTemplateId | [Group Member Schedule Template](group-member-schedule-template.md) | d84ed719-b659-433c-bfa0-e798e52c6b24 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
