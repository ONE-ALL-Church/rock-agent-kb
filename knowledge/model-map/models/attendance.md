# Attendance Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Event`
- Model title: `Attendance`
- EntityType GUID: `4ccb856f-51e0-4e48-b94a-1705efba6c9e`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 82 |
| Database-marked properties | 39 |
| Lava-marked properties | 65 |
| Lava-marked non-database properties | 26 |
| Related model links | 26 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttendanceAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| AttendanceCheckInSession |  |  | yes |  |  | Gets or sets the AttendanceCheckInSession. |
| AttendanceCheckInSessionId | yes | yes |  |  |  | Gets or sets the AttendanceCheckInSession identifier. |
| AttendanceCode |  | yes | yes |  |  | Gets or sets the AttendanceCode associated with this Attendance. |
| AttendanceCodeId | yes | yes |  |  |  | Gets or sets the Id of the AttendanceCode that is associated with this Attendance entity. |
| AttendanceData |  | yes | yes |  |  | Gets or sets additional data associated with the Attendance, including LabelData |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the Campus where the Person attended. |
| CampusId | yes | yes |  |  |  | Gets or sets the Id of the Campus that the individual attended/checked in to. |
| CheckInStatus | yes | yes |  |  |  | Gets or sets the check in status of this attendance record. This is a hard coded list of values defined in the code as an enumeration. |
| CheckedInByPersonAliasId | yes | yes |  |  |  | Gets or sets the person who was identified as the person doing the check-in. |
| CheckedOutByPersonAlias |  | yes | yes |  |  | Gets or sets the checked-out by PersonAlias. |
| CheckedOutByPersonAliasId | yes | yes |  |  |  | Gets or sets the person that checked-out the PersonAlias person attended. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DeclineReasonValue |  | yes | yes |  |  | Gets or sets the decline reason value. |
| DeclineReasonValueId | yes | yes |  |  |  | Gets or sets the Reason that the PersonAlias person declined to attend These are found in the "Group Schedule Decline Reason" Defined Type. |
| Device |  | yes | yes |  |  | Gets or sets the Device that was used to check in |
| DeviceId | yes | yes |  |  |  | Gets or sets the Id of the Device that was used (the device where the person checked in from). |
| DidAttend | yes | yes |  |  |  | Gets or sets a flag indicating if the person attended. |
| EncryptedKey |  |  | yes |  |  |  |
| EndDateTime | yes | yes |  |  |  | Gets or sets the date and time that person checked out. |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsCurrentlyCheckedIn |  |  | yes |  |  | Gets a value indicating whether this attendance is currently checked in. |
| IsFirstTime | yes | yes |  |  |  | Gets or sets if this first time that this person has ever checked into anything |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Note | yes | yes |  |  |  | Gets or sets the note. |
| Occurrence |  | yes | yes |  |  | Gets or sets the AttendanceOccurrence for the attendance. |
| OccurrenceId | yes | yes |  |  |  | Gets or sets the Id of the AttendanceOccurrence that the attendance is for. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the Id of the Person that attended/checked in to the Group |
| PresentByPersonAlias |  | yes | yes |  |  | Gets or sets the presented by PersonAlias. |
| PresentByPersonAliasId | yes | yes |  |  |  | Gets or sets the person that presented the PersonAlias person attended. |
| PresentDateTime | yes | yes |  |  |  | Gets or sets the present date and time. |
| Processed | yes | yes |  |  |  | Gets or sets the processed. |
| Qualifier |  | yes | yes |  |  | Gets or sets the qualifier. |
| QualifierValueId | yes | yes |  |  |  | Gets or sets the qualifier value id. Qualifier can be used to "qualify" attendance records. There are not any system values for this particular defined type |
| RSVP | yes | yes |  |  |  | Gets or sets the RSVP. This is a hard coded list of values defined in the code as an enumeration. |
| RSVPDateTime | yes | yes |  |  |  | Gets or sets the RSVP date time. |
| RequestedToAttend | yes | yes |  |  |  | Gets or sets if the PersonAlias person has been requested to attend. |
| ScheduleConfirmationSent | yes | yes |  |  |  | Gets or sets if a schedule confirmation has been sent to the PersonAlias person |
| ScheduleReminderSent | yes | yes |  |  |  | Gets or sets if a schedule reminder has been sent to the PersonAlias person |
| ScheduledByPersonAlias |  | yes | yes |  |  | Gets or sets the scheduled by PersonAlias. |
| ScheduledByPersonAliasId | yes | yes |  |  |  | Gets or sets the person that scheduled the PersonAlias person to attend |
| ScheduledToAttend | yes | yes |  |  |  | Gets or sets if the PersonAlias person is scheduled (confirmed) to attend. |
| SearchResultGroup |  | yes | yes |  |  | Gets or sets the Group (family) that was selected after searching during check-in. |
| SearchResultGroupId | yes | yes |  |  |  | Gets or sets the Id of the Group (family) that was selected after searching. |
| SearchTypeValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the type of search used during check-in |
| SearchTypeValueId | yes | yes |  |  |  | Gets or sets the Id of the Check-in Search Type DefinedValue that was used to search for the person/family. These are found in the "Search Type" Defined Type. |
| SearchValue | yes | yes |  |  |  | Gets or sets the value that was entered when searching for family during check-in. |
| SourceValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the source of this attendance record. |
| SourceValueId | yes | yes |  |  |  | Gets or sets the Id of the Attendance Source DefinedValue that is considered the source of this attendance record. These are found in the "Attendance Source" Defined Type. |
| StartDateTime | yes | yes |  |  |  | Gets or sets the date and time that person checked in |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttendanceCode | Gets or sets the AttendanceCode associated with this Attendance. |
| AttendanceData | Gets or sets additional data associated with the Attendance, including LabelData |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the Campus where the Person attended. |
| CheckedOutByPersonAlias | Gets or sets the checked-out by PersonAlias. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DeclineReasonValue | Gets or sets the decline reason value. |
| Device | Gets or sets the Device that was used to check in |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Occurrence | Gets or sets the AttendanceOccurrence for the attendance. |
| PersonAlias | Gets or sets the PersonAlias. |
| PresentByPersonAlias | Gets or sets the presented by PersonAlias. |
| Qualifier | Gets or sets the qualifier. |
| ScheduledByPersonAlias | Gets or sets the scheduled by PersonAlias. |
| SearchResultGroup | Gets or sets the Group (family) that was selected after searching during check-in. |
| SearchTypeValue | Gets or sets the DefinedValue representing the type of search used during check-in |
| SourceValue | Gets or sets the DefinedValue representing the source of this attendance record. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AttendanceCheckInSession | [AttendanceCheckInSession](attendance-check-in-session.md) |  |
| AttendanceCheckInSessionId | [AttendanceCheckInSession](attendance-check-in-session.md) |  |
| AttendanceCode | [AttendanceCode](attendance-code.md) |  |
| AttendanceCodeId | [Attendance](attendance.md) |  |
| AttendanceCodeId | [AttendanceCode](attendance-code.md) |  |
| Campus | [Campus](campus.md) |  |
| Campus | [Person](person.md) |  |
| CampusId | [Campus](campus.md) |  |
| CheckedOutByPersonAlias | [PersonAlias](person-alias.md) |  |
| CheckedOutByPersonAliasId | [PersonAlias](person-alias.md) |  |
| Device | [Device](device.md) |  |
| DeviceId | [Device](device.md) |  |
| Occurrence | [AttendanceOccurrence](attendance-occurrence.md) |  |
| OccurrenceId | [AttendanceOccurrence](attendance-occurrence.md) |  |
| PersonAlias | [PersonAlias](person-alias.md) |  |
| PersonAliasId | [Group](group.md) |  |
| PersonAliasId | [Person](person.md) |  |
| PresentByPersonAlias | [PersonAlias](person-alias.md) |  |
| PresentByPersonAliasId | [PersonAlias](person-alias.md) |  |
| ScheduledByPersonAlias | [PersonAlias](person-alias.md) |  |
| SearchResultGroup | [Group](group.md) |  |
| SearchResultGroupId | [Group](group.md) |  |
| SearchTypeValue | [DefinedValue](defined-value.md) |  |
| SearchTypeValueId | [DefinedValue](defined-value.md) |  |
| SourceValue | [DefinedValue](defined-value.md) |  |
| SourceValueId | [DefinedValue](defined-value.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | SourceValueId | enum_values |
