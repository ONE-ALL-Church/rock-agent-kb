# Streak Type Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Engagement`
- Model title: `StreakType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `66203975-2a7a-4000-870e-76457df3c920`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 51 |
| Database-marked properties | 21 |
| Lava-marked properties | 35 |
| Lava-marked non-database properties | 14 |
| Related model links | 2 |
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
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a description of the Streak Type. |
| EnableAttendance | yes | yes |  |  |  | This determines whether the streak type will write attendance records when marking someone as present or if it will just update the enrolled individual’s map. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FirstDayOfWeek | yes | yes |  |  |  | Gets or sets the first day of the week for StreakOccurrenceFrequency.Weekly streak type calculations. Leave this null to assume the system setting, which is accessed via Rock.RockDateTime.FirstDayOfWeek. This is a hard coded list of values defined in the code as an enumeration. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if this item is active or not. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the Streak Type. This property is required. |
| OccurrenceFrequency | yes | yes |  | yes |  | Gets or sets the timespan that each map bit represents (StreakOccurrenceFrequency). This is a hard coded list of values defined in the code as an enumeration. |
| OccurrenceMap | yes | yes |  |  |  | The sequence of bits that represent occurrences where engagement was possible. The least significant bit (right side) is representative of the StartDate. More significant bits (going left) are more recent dates. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RequiresEnrollment | yes | yes |  |  |  | Gets or sets a flag indicating if this streak type requires explicit enrollment. If not set, a person can be implicitly enrolled through attendance. |
| StartDate | yes | yes |  | yes |  | Gets or sets the DateTime associated with the least significant bit of all maps in this streak type. |
| StreakTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| StreakTypeExclusions |  | yes | yes |  |  | Gets or sets a collection containing the StreakTypeExclusions that are of this streak type. |
| Streaks |  | yes | yes |  |  | Gets or sets a collection containing the Streaks that are of this streak type. |
| StructureEntityId | yes | yes |  |  |  | Gets or sets the Id of the Entity associated with attendance for this streak type. If not set, this streak type will account for any attendance record. |
| StructureSettings |  |  | yes |  |  | Gets or sets the structure settings. |
| StructureSettingsJSON | yes | yes |  |  |  | Gets or sets the structure settings JSON. |
| StructureType | yes | yes |  |  |  | Gets or sets the attendance association (StreakStructureType). If not set, this streak type will not be associated with attendance. This is a hard coded list of values defined in the code as an enumeration. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| StreakTypeExclusions | Gets or sets a collection containing the StreakTypeExclusions that are of this streak type. |
| Streaks | Gets or sets a collection containing the Streaks that are of this streak type. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| StreakTypeExclusions | StreakTypeExclusions | 1f00c782-f8a2-4cfa-b7df-e5b3b6d36069 |
| Streaks | Streaks | d953b0a5-0065-4624-8844-10010de01e5c |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
