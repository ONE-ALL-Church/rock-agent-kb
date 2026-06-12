# Attendance Occurrence Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Event`
- Model title: `AttendanceOccurrence`
- EntityType GUID: `0f6fd7f1-7af5-4135-843f-e34948d4ea28`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 64 |
| Database-marked properties | 27 |
| Lava-marked properties | 47 |
| Lava-marked non-database properties | 20 |
| Related model links | 14 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AcceptConfirmationMessage | yes | yes |  |  |  | Gets or sets the Accept Confirmation Message (for RSVP). |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AnonymousAttendanceCount | yes | yes |  |  |  | Gets or sets the number anonymous attendance. |
| AttendanceEntered |  | yes | yes |  |  | Gets a value indicating whether attendance was entered (based on presence of any attendee records). |
| AttendanceOccurrenceAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| AttendanceRate |  |  | yes |  |  | Gets the attendance rate. |
| AttendanceReminderLastSentDateTime | yes | yes |  |  |  | Gets or sets the attendance reminder last sent date time. |
| AttendanceTypeValueId | yes | yes |  |  |  | Gets or sets the attendance type value identifier. These are found in the "Attendance Types" Defined Type. |
| Attendees |  | yes | yes |  |  | Gets or sets the attendees. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DeclineConfirmationMessage | yes | yes |  |  |  | Gets or sets the Decline Confirmation Message (for RSVP). |
| DeclineReasonValueIds | yes | yes |  |  |  | A comma-separated list of integer ID values representing the Decline Reasons selected by the attendee. |
| DidAttendCount |  |  | yes |  |  | Gets the number of attendees who attended. |
| DidNotOccur | yes | yes |  |  |  | Gets or sets the did not occur. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Group that was attended. |
| GroupId | yes | yes |  |  |  | Gets or sets the Id of the Group that the Person checked in to. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. |
| Item |  |  | yes |  |  |  |
| Location |  | yes | yes |  |  | Gets or sets the Location where the Person attended. |
| LocationId | yes | yes |  |  |  | Gets or sets the Id of the Location that the individual attended/checked in to. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the name. |
| Notes | yes | yes |  |  |  | Gets or sets the notes. |
| OccurrenceDate | yes | yes |  |  |  | Gets or sets the date of the Attendance. Only the date is used. |
| OccurrenceDateKey | yes | yes |  |  |  | Gets the occurrence date key. |
| OccurrenceSourceDate |  | yes | yes |  |  | Gets or sets the occurrence source date. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RootGroupType |  | yes | yes |  |  | The root GroupType that the Person was checked in to. This is set automatically on save to help with reporting for check-in related attendance. |
| RootGroupTypeId | yes | yes |  |  |  | The identifier of the root GroupType that the Person was checked in to. This is set automatically on save to help with reporting for check-in related attendance. |
| Schedule |  | yes | yes |  |  | Gets or sets the Schedule. |
| ScheduleId | yes | yes |  |  |  | Gets or sets the Id of the Schedule that the Person checked in to. |
| ShowDeclineReasons | yes | yes |  |  |  | Indicates whether or not to show the Decline Confirmation Message. |
| StepType |  | yes | yes |  |  | Gets or sets the StepType. |
| StepTypeId | yes | yes |  |  |  | Gets or sets the Id of the StepType to which this occurrence is associated. |
| SundayDate | yes | yes |  |  |  | Gets Sunday date. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttendanceEntered | Gets a value indicating whether attendance was entered (based on presence of any attendee records). |
| Attendees | Gets or sets the attendees. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| Group | Gets or sets the Group that was attended. |
| IdKey |  |
| Location | Gets or sets the Location where the Person attended. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| OccurrenceSourceDate | Gets or sets the occurrence source date. |
| RootGroupType | The root GroupType that the Person was checked in to. This is set automatically on save to help with reporting for check-in related attendance. |
| Schedule | Gets or sets the Schedule. |
| StepType | Gets or sets the StepType. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Group | [Group](group.md) |  |
| GroupId | [Group](group.md) |  |
| GroupId | [Person](person.md) |  |
| Location | [Location](location.md) |  |
| LocationId | [Location](location.md) |  |
| RootGroupType | [GroupType](group-type.md) |  |
| RootGroupType | [Person](person.md) |  |
| RootGroupTypeId | [GroupType](group-type.md) |  |
| RootGroupTypeId | [Person](person.md) |  |
| Schedule | [Schedule](schedule.md) |  |
| ScheduleId | [Person](person.md) |  |
| ScheduleId | [Schedule](schedule.md) |  |
| StepType | [StepType](step-type.md) |  |
| StepTypeId | [StepType](step-type.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
