# Campus Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `Campus`
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
| Pre-alpha changes touching this model | 3 |

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
| CampusStatusValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the campus status. |
| CampusStatusValueId | yes | yes |  |  |  | Gets or sets the campus status value identifier. These are found in the "Campus Status" Defined Type. |
| CampusTopics |  | yes | yes |  |  | Gets or sets a collection containing the Topics that are associated with this Campus. |
| CampusTypeValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the campus type. |
| CampusTypeValueId | yes | yes |  |  |  | Gets or sets the campus type value identifier. These are found in the "Campus Type" Defined Type. |
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
| ServiceTimes | yes | yes |  |  |  | Gets or sets the service times (Stored as a delimited list) |
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
| CampusStatusValue | Gets or sets the DefinedValue representing the campus status. |
| CampusTopics | Gets or sets a collection containing the Topics that are associated with this Campus. |
| CampusTypeValue | Gets or sets the DefinedValue representing the campus type. |
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
| BeaconId | [Campus](campus.md) |  |
| CampusSchedules | Schedules |  |
| CampusStatusValue | [DefinedValue](defined-value.md) |  |
| CampusTopics | Topics |  |
| CampusTypeValue | [DefinedValue](defined-value.md) |  |
| LeaderPersonAlias | [Person](person.md) |  |
| LeaderPersonAliasId | [Person](person.md) |  |
| Location | [Location](location.md) |  |
| LocationId | [Location](location.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | CampusStatusValueId | enum_values |
| property_changed | CampusTypeValueId | enum_values |
| property_changed | ServiceTimes | is_obsolete |
