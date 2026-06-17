# Schedule Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `Schedule`
- EntityType GUID: `0b2c38a7-d79c-4f85-9757-f1b045d32c8a`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 64 |
| Database-marked properties | 25 |
| Lava-marked properties | 47 |
| Lava-marked non-database properties | 22 |
| Related model links | 2 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AbbreviatedName | yes | yes |  |  |  | Gets or sets the shortened name of the attribute. If null or whitespace then the full name is returned. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AutoInactivateWhenComplete | yes | yes |  |  |  | Gets or sets a value indicating whether [auto inactivate when complete]. |
| AvailableKeys |  |  | yes |  |  |  |
| Category |  | yes | yes |  |  | Gets or sets the Category that this Schedule belongs to. |
| CategoryId | yes | yes |  |  |  | Gets or sets the CategoryId of the Category that this Schedule belongs to. |
| CheckInEndOffsetMinutes | yes | yes |  |  |  | Gets or sets the number of minutes following schedule start that Check-in should be active. 0 represents that Check-in will only be available until the Schedule's start time. |
| CheckInStartOffsetMinutes | yes | yes |  |  |  | Gets or sets the number of minutes prior to the Schedule's start time that Check-in should be active. 0 represents that Check-in will not be available to the beginning of the event. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a user defined Description of the Schedule. |
| DurationInMinutes |  | yes | yes |  |  | Gets the duration in minutes. |
| EffectiveEndDate | yes | yes |  |  |  | Gets or sets that date that this Schedule expires and becomes inactive. This value is inclusive and the schedule will be inactive after this date. |
| EffectiveStartDate | yes | yes |  |  |  | Gets or sets the Date that the Schedule becomes effective/active. This property is inclusive, and the schedule will be inactive before this date. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FirstStartDateTime |  | yes | yes |  |  | Gets the first start date time. |
| FirstStartDateTimeThisWeek |  | yes | yes |  |  | Gets the first start date time this week. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FriendlyScheduleText |  | yes | yes |  |  | Gets the friendly schedule text. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  | yes |  | Gets or sets a flag indicating if this is an active schedule. This value is required. |
| IsCheckInActive |  | yes | yes |  |  | Gets a value indicating whether check-in is currently active for this schedule. This is based on Rock.RockDateTime.Now. Use Campus.CurrentDateTime and WasCheckInActive(System.DateTime)() to get this based on the Campus's current datetime. |
| IsCheckInEnabled |  |  | yes |  |  | Gets a value indicating whether Check-in is enabled for this Schedule. |
| IsPublic | yes | yes |  |  |  | Gets or sets a value indicating if this Schedule is public. |
| IsScheduleActive |  | yes | yes |  |  | Gets a value indicating whether this schedule is currently active. This is based on Rock.RockDateTime.Now. Use Campus.CurrentDateTime and WasScheduleActive(System.DateTime)() to get this based on the Campus's current datetime. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the Name of the Schedule. This property is required. |
| NextStartDateTime |  | yes | yes |  |  | Gets the next start time based on Rock.RockDateTime.Now. Use Campus.CurrentDateTime and GetNextStartDateTime(System.DateTime)() to get this based on the Campus's current datetime. |
| Order | yes | yes |  |  |  | Gets or sets the order. Use Rock.ExtensionMethods.OrderByOrderAndNextScheduledDateTime(System.Collections.Generic.List{Schedule})() to get the schedules in the desired order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ScheduleAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ScheduleDates |  | yes | yes |  |  | The set of specific dates that this schedule has. This list only includes a few years in the past and in the future. |
| ScheduleType |  |  | yes |  |  | Gets the type of the schedule. This is a hard coded list of values defined in the code as an enumeration. |
| StartTimeOfDay |  | yes | yes |  |  | Gets the start time of day. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WeeklyDayOfWeek | yes | yes |  |  |  | Gets or sets the weekly day of week. This is a hard coded list of values defined in the code as an enumeration. |
| WeeklyTimeOfDay | yes | yes |  |  |  | Gets or sets the weekly time of day. |
| WeeklyTimeOfDayText | yes | yes |  |  |  | Gets the weekly time of day in friendly text, such as "7:00 PM". |
| iCalendarContent | yes | yes |  |  |  | Gets or sets the content lines of the iCalendar |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the Category that this Schedule belongs to. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DurationInMinutes | Gets the duration in minutes. |
| EntityStringValue |  |
| FirstStartDateTime | Gets the first start date time. |
| FirstStartDateTimeThisWeek | Gets the first start date time this week. |
| FriendlyScheduleText | Gets the friendly schedule text. |
| IdKey |  |
| IsCheckInActive | Gets a value indicating whether check-in is currently active for this schedule. This is based on Rock.RockDateTime.Now. Use Campus.CurrentDateTime and WasCheckInActive(System.DateTime)() to get this based on the Campus's current datetime. |
| IsScheduleActive | Gets a value indicating whether this schedule is currently active. This is based on Rock.RockDateTime.Now. Use Campus.CurrentDateTime and WasScheduleActive(System.DateTime)() to get this based on the Campus's current datetime. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| NextStartDateTime | Gets the next start time based on Rock.RockDateTime.Now. Use Campus.CurrentDateTime and GetNextStartDateTime(System.DateTime)() to get this based on the Campus's current datetime. |
| ScheduleDates | The set of specific dates that this schedule has. This list only includes a few years in the past and in the future. |
| StartTimeOfDay | Gets the start time of day. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Category | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| CategoryId | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
