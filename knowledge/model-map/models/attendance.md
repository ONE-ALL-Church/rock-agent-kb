# Attendance Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Event`
- Model title: `Attendance`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `39`
- Obsolete methods: `4`
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
| Method signatures | 39 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttendanceAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| AttendanceCheckInSession |  |  | yes |  |  | Gets or sets the Attendance Check In Session. |
| AttendanceCheckInSessionId | yes | yes |  |  |  | Gets or sets the Attendance Check In Session identifier. |
| AttendanceCode |  | yes | yes |  |  | Gets or sets the Attendance Code associated with this Attendance. |
| AttendanceCodeId | yes | yes |  |  |  | Gets or sets the Id of the Attendance Code that is associated with this Attendance entity. |
| AttendanceData |  | yes | yes |  |  | Gets or sets additional data associated with the Attendance, including LabelData |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the Campus where the Person attended. |
| CampusId | yes | yes |  |  |  | Gets or sets the Id of the Campus that the individual attended/checked in to. |
| CheckInStatus | yes | yes |  |  |  | Gets or sets the check in status of this attendance record. This is a hard coded list of values defined in the code as an enumeration. |
| CheckedInByPersonAliasId | yes | yes |  |  |  | Gets or sets the person who was identified as the person doing the check-in. |
| CheckedOutByPersonAlias |  | yes | yes |  |  | Gets or sets the checked-out by Person Alias. |
| CheckedOutByPersonAliasId | yes | yes |  |  |  | Gets or sets the person that checked-out the Person Alias person attended. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DeclineReasonValue |  | yes | yes |  |  | Gets or sets the decline reason value. |
| DeclineReasonValueId | yes | yes |  |  |  | Gets or sets the Reason that the PersonAlias person declined to attend These are found in the Group Schedule Decline Reason Defined Type. |
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
| Occurrence |  | yes | yes |  |  | Gets or sets the Attendance Occurrence for the attendance. |
| OccurrenceId | yes | yes |  |  |  | Gets or sets the Id of the Attendance Occurrence that the attendance is for. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the Id of the Person that attended/checked in to the Group |
| PresentByPersonAlias |  | yes | yes |  |  | Gets or sets the presented by Person Alias. |
| PresentByPersonAliasId | yes | yes |  |  |  | Gets or sets the person that presented the Person Alias person attended. |
| PresentDateTime | yes | yes |  |  |  | Gets or sets the present date and time. |
| Processed | yes | yes |  |  |  | Gets or sets the processed. |
| Qualifier |  | yes | yes |  |  | Gets or sets the qualifier. |
| QualifierValueId | yes | yes |  |  |  | Gets or sets the qualifier value id. Qualifier can be used to "qualify" attendance records. There are not any system values for this particular defined type |
| RSVP | yes | yes |  |  |  | Gets or sets the RSVP. This is a hard coded list of values defined in the code as an enumeration. |
| RSVPDateTime | yes | yes |  |  |  | Gets or sets the RSVP date time. |
| RequestedToAttend | yes | yes |  |  |  | Gets or sets if the PersonAlias person has been requested to attend. |
| ScheduleConfirmationSent | yes | yes |  |  |  | Gets or sets if a schedule confirmation has been sent to the PersonAlias person |
| ScheduleReminderSent | yes | yes |  |  |  | Gets or sets if a schedule reminder has been sent to the PersonAlias person |
| ScheduledByPersonAlias |  | yes | yes |  |  | Gets or sets the scheduled by Person Alias. |
| ScheduledByPersonAliasId | yes | yes |  |  |  | Gets or sets the person that scheduled the PersonAlias person to attend |
| ScheduledToAttend | yes | yes |  |  |  | Gets or sets if the PersonAlias person is scheduled (confirmed) to attend. |
| SearchResultGroup |  | yes | yes |  |  | Gets or sets the Group (family) that was selected after searching during check-in. |
| SearchResultGroupId | yes | yes |  |  |  | Gets or sets the Id of the Group (family) that was selected after searching. |
| SearchTypeValue |  | yes | yes |  |  | Gets or sets the Defined Value representing the type of search used during check-in |
| SearchTypeValueId | yes | yes |  |  |  | Gets or sets the Id of the Check-in Search Type Defined Value that was used to search for the person/family. These are found in the Search Type Defined Type. |
| SearchValue | yes | yes |  |  |  | Gets or sets the value that was entered when searching for family during check-in. |
| SourceValue |  | yes | yes |  |  | Gets or sets the Defined Value representing the source of this attendance record. |
| SourceValueId | yes | yes |  |  |  | Gets or sets the Id of the Attendance Source Defined Value that is considered the source of this attendance record. These are found in the Attendance Source Defined Type. |
| StartDateTime | yes | yes |  |  |  | Gets or sets the date and time that person checked in |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttendanceCode | Gets or sets the Attendance Code associated with this Attendance. |
| AttendanceData | Gets or sets additional data associated with the Attendance, including LabelData |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the Campus where the Person attended. |
| CheckedOutByPersonAlias | Gets or sets the checked-out by Person Alias. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DeclineReasonValue | Gets or sets the decline reason value. |
| Device | Gets or sets the Device that was used to check in |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Occurrence | Gets or sets the Attendance Occurrence for the attendance. |
| PersonAlias | Gets or sets the Person Alias. |
| PresentByPersonAlias | Gets or sets the presented by Person Alias. |
| Qualifier | Gets or sets the qualifier. |
| ScheduledByPersonAlias | Gets or sets the scheduled by Person Alias. |
| SearchResultGroup | Gets or sets the Group (family) that was selected after searching during check-in. |
| SearchTypeValue | Gets or sets the Defined Value representing the type of search used during check-in |
| SourceValue | Gets or sets the Defined Value representing the source of this attendance record. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AttendanceCheckInSession | [Attendance Check In Session](attendance-check-in-session.md) | d60a20a7-98a2-45b5-bf7e-a327e4090940 |
| AttendanceCheckInSessionId | [Attendance Check In Session](attendance-check-in-session.md) | d60a20a7-98a2-45b5-bf7e-a327e4090940 |
| AttendanceCode | [Attendance Code](attendance-code.md) | d5adc6d3-9aa0-4ac6-9762-a703ee684934 |
| AttendanceCodeId | [Attendance](attendance.md) | 4ccb856f-51e0-4e48-b94a-1705efba6c9e |
| AttendanceCodeId | [Attendance Code](attendance-code.md) | d5adc6d3-9aa0-4ac6-9762-a703ee684934 |
| Campus | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| Campus | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| CampusId | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| CheckedOutByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| CheckedOutByPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| Device | [Device](device.md) | c06ee1fe-af12-410a-a364-7a366cd72414 |
| DeviceId | [Device](device.md) | c06ee1fe-af12-410a-a364-7a366cd72414 |
| Occurrence | [Attendance Occurrence](attendance-occurrence.md) | 0f6fd7f1-7af5-4135-843f-e34948d4ea28 |
| OccurrenceId | [Attendance Occurrence](attendance-occurrence.md) | 0f6fd7f1-7af5-4135-843f-e34948d4ea28 |
| PersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| PersonAliasId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| PersonAliasId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| PresentByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| PresentByPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| ScheduledByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| SearchResultGroup | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| SearchResultGroupId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| SearchTypeValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| SearchTypeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| SourceValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| SourceValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
