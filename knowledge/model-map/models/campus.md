# Campus Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Core`
- Model title: `Campus`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `00096bed-9587-415e-8ad4-4e076ae8fbf0`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 65 |
| Database-marked properties | 29 |
| Lava-marked properties | 48 |
| Lava-marked non-database properties | 19 |
| Related model links | 9 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| AverageWeekendAttendance | yes | yes |  |  |  | Gets or sets the average weekend attendance. |
| BeaconId | yes | yes |  |  |  | The identifier of the beacon that is associated with this campus. This is typically used with Bluetooth proximity beacons and allows the Campus to be determined from a beacon. |
| CampusAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| CampusSchedules |  | yes | yes |  |  | Gets or sets a collection containing the Schedules that are associated with this Campus. |
| CampusStatusValue |  | yes | yes |  |  | Gets or sets the Defined Value representing the campus status. |
| CampusStatusValueId | yes | yes |  |  |  | Gets or sets the campus status value identifier. These are found in the Campus Status Defined Type. |
| CampusTopics |  | yes | yes |  |  | Gets or sets a collection containing the Topics that are associated with this Campus. |
| CampusTypeValue |  | yes | yes |  |  | Gets or sets the Defined Value representing the campus type. |
| CampusTypeValueId | yes | yes |  |  |  | Gets or sets the campus type value identifier. These are found in the Campus Type Defined Type. |
| ClosedDate | yes | yes |  |  |  | Gets or sets the closed date. |
| CondensedName |  |  | yes |  |  | Gets the condensed name of the campus. This will be the short code if set, otherwise the name of the campus by stripping off any trailing " Campus" text. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CurrentDateTime |  |  | yes |  |  | Gets the current date time basd on the TimeZoneId. |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets the is active. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if the Campus is a part of the Rock system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LeaderPersonAlias |  | yes | yes |  |  | Gets or sets the Person entity that is associated with the leader of the campus. |
| LeaderPersonAliasId | yes | yes |  |  |  | Gets or sets the Id of the Person that is the leader of the campus. |
| Location |  | yes | yes |  |  | Gets or sets the Location entity that is associated with this campus. |
| LocationId | yes | yes |  |  |  | Gets or sets the Id of the Location that is associated with this campus. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the Campus. This property is required. |
| OpenedDate | yes | yes |  |  |  | Gets or sets the opened date. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PhoneNumber | yes | yes |  |  |  | Gets or sets the phone number of the campus. |
| ServiceTimes | yes | yes |  |  | yes | Gets or sets the service times (Stored as a delimited list) |
| ShortCode | yes | yes |  |  |  | Gets or sets an optional short code identifier for the campus. |
| SupportedActions |  |  | yes |  |  |  |
| TeamGroup |  | yes | yes |  |  | Gets or sets the team group. |
| TeamGroupId | yes | yes |  |  |  | Gets or sets the team group identifier. |
| TimeZoneId | yes | yes |  |  |  | Gets or sets the time zone identifier (System.TimeZoneInfo.Id) If this is not set, the Campus time zone will be the default Rock time zone (Rock.RockDateTime.OrgTimeZoneInfo ) |
| TitheMetric | yes | yes |  |  |  | Gets or sets the tithe metric. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| Url | yes | yes |  |  |  | Gets or sets the URL. |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CampusSchedules | Gets or sets a collection containing the Schedules that are associated with this Campus. |
| CampusStatusValue | Gets or sets the Defined Value representing the campus status. |
| CampusTopics | Gets or sets a collection containing the Topics that are associated with this Campus. |
| CampusTypeValue | Gets or sets the Defined Value representing the campus type. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| LeaderPersonAlias | Gets or sets the Person entity that is associated with the leader of the campus. |
| Location | Gets or sets the Location entity that is associated with this campus. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TeamGroup | Gets or sets the team group. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| BeaconId | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| CampusSchedules | Schedules | 134b8879-cd7c-4872-8065-882aa3721c2d |
| CampusStatusValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| CampusTopics | Topics | 0ffdcb0b-b435-4e66-9085-2750534e706a |
| CampusTypeValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| LeaderPersonAlias | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| LeaderPersonAliasId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| Location | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| LocationId | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
