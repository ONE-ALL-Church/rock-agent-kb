# Group Historical Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Group`
- Model title: `GroupHistorical`
- EntityType GUID: `422a2ef2-9d74-4308-8cdb-d5fa4b6a01ff`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 61 |
| Database-marked properties | 28 |
| Lava-marked properties | 46 |
| Lava-marked non-database properties | 18 |
| Related model links | 8 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| ArchivedByPersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias that archived (soft deleted) this group at this point in history |
| ArchivedByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAliasId that archived (soft deleted) this group at this point in history |
| ArchivedDateTime | yes | yes |  |  |  | Gets or sets the archived date time value of this group at this point in history |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the Campus of this group at this point in history |
| CampusId | yes | yes |  |  |  | Gets or sets the Campus identifier for this group at this point in history |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CurrentRowIndicator | yes | yes |  |  |  | Gets or sets a value indicating whether [current row indicator]. This will be True if this represents the same values as the current tracked record for this |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description for this group at this point in history |
| EffectiveDateTime | yes | yes |  |  |  | Gets or sets the effective date. This is the starting date that the tracked record had the values reflected in this record |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExpireDateTime | yes | yes |  |  |  | Gets or sets the expire date time This is the last date that the tracked record had the values reflected in this record For example, if a tracked record's Name property changed on '2016-07-14', the ExpireDate of the previously current record will be '2016-07-13', and the EffectiveDate of the current record will be '2016-07-14' If this is most current record, the ExpireDate will be '9999-01-01' |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Group for this group historical record |
| GroupHistoricalAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupId | yes | yes |  |  |  | Gets or sets the group id of the group for this group historical record |
| GroupName | yes | yes |  |  |  | Gets or sets the name of the group at this point in history |
| GroupType |  | yes | yes |  |  | Gets or sets the GroupType of this group at this point in history |
| GroupTypeId | yes | yes |  |  |  | Gets or sets the group type identifier. Normally, a GroupTypeId can't be changed, but just in case, this will be the group type at this point in history |
| GroupTypeName | yes | yes |  |  |  | Gets or sets the name of the GroupType at this point in history |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InactiveDateTime | yes | yes |  |  |  | Gets or sets the InactiveDateTime value of the group at this point in history |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this group had IsActive==True at this point in history |
| IsArchived | yes | yes |  |  |  | Gets or sets a value indicating whether this group was archived at this point in history |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ParentGroup |  | yes | yes |  |  | Gets or sets the parent Group of this group at this point in history |
| ParentGroupId | yes | yes |  |  |  | Gets or sets the parent Group identifier at this point in history |
| Schedule |  | yes | yes |  |  | If this group's group type supports a schedule for a group, this is the schedule for that group at this point in history. |
| ScheduleId | yes | yes |  |  |  | If this group's group type supports a schedule for a group, this is the schedule id for that group at this point in history. |
| ScheduleModifiedDateTime | yes | yes |  |  |  | Gets or sets the Schedule's ModifiedDateTime. This is used internally to detect if the group's schedule has changed |
| ScheduleName | yes | yes |  |  |  | If this group's group type supports a schedule for a group, this is the schedule text (Schedule.ToString()) for that group at this point in history. |
| StatusValueId | yes | yes |  |  |  | Gets or sets the Group Status Id. DefinedType depends on this group's GroupType.GroupStatusDefinedType |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ArchivedByPersonAlias | Gets or sets the PersonAlias that archived (soft deleted) this group at this point in history |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the Campus of this group at this point in history |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| Group | Gets or sets the Group for this group historical record |
| GroupType | Gets or sets the GroupType of this group at this point in history |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ParentGroup | Gets or sets the parent Group of this group at this point in history |
| Schedule | If this group's group type supports a schedule for a group, this is the schedule for that group at this point in history. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ArchivedByPersonAlias | [PersonAlias](person-alias.md) |  |
| Campus | [Campus](campus.md) |  |
| CampusId | [Campus](campus.md) |  |
| Group | [Group](group.md) |  |
| GroupType | [GroupType](group-type.md) |  |
| GroupTypeName | [GroupType](group-type.md) |  |
| ParentGroup | [Group](group.md) |  |
| ParentGroupId | [Group](group.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
