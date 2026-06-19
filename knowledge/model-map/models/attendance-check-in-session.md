# Attendance Check In Session Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Event`
- Model title: `AttendanceCheckInSession`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `13`
- Obsolete methods: `3`
- EntityType GUID: `d60a20a7-98a2-45b5-bf7e-a327e4090940`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 21 |
| Database-marked properties | 7 |
| Lava-marked properties | 14 |
| Lava-marked non-database properties | 7 |
| Related model links | 3 |
| Method signatures | 13 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Attendances |  | yes | yes |  |  | Gets or sets the Attendances associated with this session |
| AvailableKeys |  |  | yes |  |  |  |
| ClientIpAddress | yes | yes |  |  |  | Gets or sets the client ip address. |
| ContextKey |  |  | yes |  |  |  |
| Device |  | yes | yes |  |  | Gets or sets the Device that was used to check in |
| DeviceId | yes | yes |  |  |  | Gets or sets the Id of the Device that was used (the device where the person checked in from). |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Attendances | Gets or sets the Attendances associated with this session |
| Device | Gets or sets the Device that was used to check in |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Attendances | Attendances | 4ccb856f-51e0-4e48-b94a-1705efba6c9e |
| Device | [Device](device.md) | c06ee1fe-af12-410a-a364-7a366cd72414 |
| DeviceId | [Device](device.md) | c06ee1fe-af12-410a-a364-7a366cd72414 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
