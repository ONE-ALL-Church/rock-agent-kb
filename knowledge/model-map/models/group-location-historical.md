# Group Location Historical Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Group`
- Model title: `GroupLocationHistorical`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `35`
- Obsolete methods: `4`
- EntityType GUID: `03128778-5e7d-4fe4-9c7a-929936e06f90`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 19 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 15 |
| Related model links | 6 |
| Method signatures | 35 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 1 |

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
| CurrentRowIndicator | yes | yes |  |  |  | Gets or sets a value indicating whether [current row indicator]. This will be True if this represents the same values as the current tracked record for this |
| CustomSortValue |  |  | yes |  |  |  |
| EffectiveDateTime | yes | yes |  |  |  | Gets or sets the effective date. This is the starting date that the tracked record had the values reflected in this record |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExpireDateTime | yes | yes |  |  |  | Gets or sets the expire date time This is the last date that the tracked record had the values reflected in this record For example, if a tracked record's Name property changed on '2016-07-14', the ExpireDate of the previously current record will be '2016-07-13', and the EffectiveDate of the current record will be '2016-07-14' If this is most current record, the ExpireDate will be '9999-01-01' |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Group for this group's location at this point in history |
| GroupId | yes | yes |  |  |  | Gets or sets the Group id for this group's location at this point in history |
| GroupLocation |  | yes | yes |  |  | Gets or sets the Group Location that this is a historical snapshot for |
| GroupLocationHistoricalAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupLocationId | yes | yes |  |  |  | Gets or sets the group location identifier that this is a Historical snapshot for |
| GroupLocationTypeName | yes | yes |  |  |  | Gets or sets the group's location type name at this point in history (Group.GroupLocation.GroupLocationTypeValue.Value) |
| GroupLocationTypeValueId | yes | yes |  |  |  | Gets or sets the group location type value identifier for this group location at this point in history These are found in the Location Type Defined Type. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Location |  | yes | yes |  |  | Gets or sets the Location of this group's location at this point in history |
| LocationId | yes | yes |  |  |  | Gets or sets the Location id of this group's location at this point in history |
| LocationModifiedDateTime | yes | yes |  |  |  | Gets or sets the Location's ModifiedDateTime. This is used internally to detect if the group's location has changed |
| LocationName | yes | yes |  |  |  | Gets or sets the Location name of this group's location at this point in history (Group.GroupLocation.Location.ToString()) |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
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
| Group | Gets or sets the Group for this group's location at this point in history |
| GroupLocation | Gets or sets the Group Location that this is a historical snapshot for |
| IdKey |  |
| Location | Gets or sets the Location of this group's location at this point in history |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupLocation | [Group Location](group-location.md) | 26248ee7-09f3-4578-a1d6-47e01d91d6ef |
| Location | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| LocationId | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| LocationName | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | GroupLocationTypeValueId | enum_values |
