# Analytics Fact Attendance Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Reporting`
- Model title: `AnalyticsFactAttendance`
- EntityType GUID: `3fcc0df5-4299-4971-860c-8cb591da75d8`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 51 |
| Database-marked properties | 37 |
| Lava-marked properties | 44 |
| Lava-marked non-database properties | 7 |
| Related model links | 0 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AreaName | yes | yes |  |  |  | Gets or sets the name of Area (which is GroupType.Name) |
| AttendanceDate |  | yes | yes |  |  |  |
| AttendanceDateKey | yes | yes |  |  |  |  |
| AttendanceId | yes | yes |  |  |  |  |
| AttendanceTypeId | yes | yes |  |  |  |  |
| AttendanceTypeName | yes | yes |  |  |  | Gets or sets the attendance type name (which is a GroupType) The intention of this is to do the same thing that Attendance Analytics has in "Attendance Type" drop down list which comes from SELECT Name FROM GroupType WHERE GroupTypePurposeValueId IN ( SELECT Id FROM DefinedValue WHERE[Guid] = '4A406CB0-495B-4795-B788-52BDFDE00B01'-- GroupTypePurpose Checkin ) |
| AvailableKeys |  |  | yes |  |  |  |
| CampusId | yes | yes |  |  |  |  |
| CampusName | yes | yes |  |  |  | Gets or sets the name of the campus. |
| CampusShortCode | yes | yes |  |  |  | Gets or sets the campus short code. |
| ContextKey |  |  | yes |  |  |  |
| Count | yes | yes |  |  |  |  |
| CurrentFamilyKey | yes | yes |  |  |  | This is the FamilyKey (AnalyticsDimFamilyCurrent.Id) of the family of the Person that attended Note that this is the family that the person is in now |
| CurrentPersonKey | yes | yes |  |  |  |  |
| DaysSinceLastAttendanceOfType | yes | yes |  |  |  |  |
| DeviceId | yes | yes |  |  |  |  |
| DeviceName | yes | yes |  |  |  | Gets or sets the name of the device. |
| DidAttend | yes | yes |  |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EndDateTime | yes | yes |  |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FamilyKey | yes | yes |  |  |  | This is the FamilyKey (AnalyticsDimFamilyCurrent.Id) of the family of the Person that attended Note that this is the family that the person was in at the time of the attendance |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GroupId | yes | yes |  |  |  |  |
| GroupName | yes | yes |  |  |  | Gets or sets the name of the group. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsFirstAttendanceOfType | yes | yes |  |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Location |  | yes | yes |  |  |  |
| LocationId | yes | yes |  |  |  |  |
| LocationName | yes | yes |  |  |  | Gets or sets the name of the location. |
| Note | yes | yes |  |  |  |  |
| PersonAliasId | yes | yes |  |  |  |  |
| PersonKey | yes | yes |  |  |  |  |
| RSVP | yes | yes |  |  |  | This is a hard coded list of values defined in the code as an enumeration. |
| RSVPStatus | yes | yes |  |  |  | Gets or sets the RSVP status. |
| ScheduleId | yes | yes |  |  |  |  |
| ScheduleName | yes | yes |  |  |  | Gets or sets the name of the schedule. |
| SearchTypeName | yes | yes |  |  |  |  |
| StartDateTime | yes | yes |  |  |  |  |
| SundayDate | yes | yes |  |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttendanceDate |  |
| EntityStringValue |  |
| IdKey |  |
| Location |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
