# Group Location Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Group`
- Model title: `GroupLocation`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `26248ee7-09f3-4578-a1d6-47e01d91d6ef`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 50 |
| Database-marked properties | 17 |
| Lava-marked properties | 35 |
| Lava-marked non-database properties | 18 |
| Related model links | 13 |
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
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Group that is associated with this GroupLocation |
| GroupId | yes | yes |  |  |  | Gets or sets the Id of the Group that is associated with this GroupLocation. This property is required. |
| GroupLocationAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupLocationScheduleConfigs |  | yes | yes |  |  | Gets or sets properties that are specific to Group+Location+Schedule |
| GroupLocationTypeValue |  | yes | yes |  |  | Gets or sets the Location Type Defined Value of this GroupLocation. |
| GroupLocationTypeValueId | yes | yes |  |  |  | The Id of the GroupLocationType Defined Value that is used to identify the type of Group Location that this is. Examples: Home Address, Work Address, Primary Address. These are found in the Location Type Defined Type. |
| GroupMemberPersonAlias |  | yes | yes |  |  | Gets or sets the group member Person Alias. A GroupLocation can optionally be created by selecting one of the group member's locations. If the GroupLocation is created this way, the member is saved with the group location |
| GroupMemberPersonAliasId | yes | yes |  |  |  | Gets or sets the group member Person Alias identifier. A GroupLocation can optionally be created by selecting one of the group member's locations. If the GroupLocation is created this way, the member's person alias id is saved with the group location |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsMailingLocation | yes | yes |  |  |  | Gets or sets a flag indicating if the Location referenced by this GroupLocation is the mailing address/location for the Group. This field is only supported in the UI for family groups |
| IsMappedLocation | yes | yes |  |  |  | Gets or sets a flag indicating if this is the mappable location for this This field is only supported in the UI for family groups |
| IsOverflowLocation | yes | yes |  |  |  | Gets or sets a flag indicating if the Location if used as an overflow location for the group. This is primarily used by check-in. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Location |  | yes | yes |  |  | Gets or sets the Location that is associated with this GroupLocation. |
| LocationId | yes | yes |  |  |  | Gets or sets the Id of the Location that is associated with this GroupLocation. This property is required. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Order | yes | yes |  | yes |  | Gets or sets the display order of the GroupLocation in the group location list. The lower the number the higher the display priority this GroupLocation has. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Schedules |  | yes | yes |  |  | Gets or sets a collection containing the Schedules that are associated with this GroupLocation. |
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
| Group | Gets or sets the Group that is associated with this GroupLocation |
| GroupLocationScheduleConfigs | Gets or sets properties that are specific to Group+Location+Schedule |
| GroupLocationTypeValue | Gets or sets the Location Type Defined Value of this GroupLocation. |
| GroupMemberPersonAlias | Gets or sets the group member Person Alias. A GroupLocation can optionally be created by selecting one of the group member's locations. If the GroupLocation is created this way, the member is saved with the group location |
| IdKey |  |
| Location | Gets or sets the Location that is associated with this GroupLocation. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Schedules | Gets or sets a collection containing the Schedules that are associated with this GroupLocation. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupLocationTypeValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| GroupLocationTypeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| GroupLocationTypeValueId | [Group Location](group-location.md) | 26248ee7-09f3-4578-a1d6-47e01d91d6ef |
| GroupMemberPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| GroupMemberPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| IsMailingLocation | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| IsMailingLocation | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| IsOverflowLocation | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| Location | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| LocationId | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| Schedules | Schedules | 0b2c38a7-d79c-4f85-9757-f1b045d32c8a |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
