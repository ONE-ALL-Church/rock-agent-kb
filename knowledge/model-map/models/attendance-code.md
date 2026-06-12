# Attendance Code Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Event`
- Model title: `AttendanceCode`
- EntityType GUID: `d5adc6d3-9aa0-4ac6-9762-a703ee684934`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 20 |
| Database-marked properties | 7 |
| Lava-marked properties | 12 |
| Lava-marked non-database properties | 5 |
| Related model links | 1 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Attendances |  |  | yes |  |  | Gets or sets a collection of Attendance entities that are associated with this AttendanceCode. |
| AvailableKeys |  |  | yes |  |  |  |
| Code | yes | yes |  |  |  | Gets or sets the attendance/security code. |
| ContextKey |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| IssueDateTime | yes | yes |  |  |  | Gets or sets the date and time that the Attendance Code was issued. |
| Item |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Attendances | [Attendance](attendance.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
