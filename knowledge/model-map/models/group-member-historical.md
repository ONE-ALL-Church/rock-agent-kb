# Group Member Historical Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Group`
- Model title: `GroupMemberHistorical`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `35`
- Obsolete methods: `4`
- EntityType GUID: `233ea15d-8fee-40fe-9772-d369d34e3a8d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 53 |
| Database-marked properties | 22 |
| Lava-marked properties | 38 |
| Lava-marked non-database properties | 16 |
| Related model links | 5 |
| Method signatures | 35 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| ArchivedByPersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias that archived (soft deleted) this group member at this point in history |
| ArchivedByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAliasId that archived (soft deleted) this group member at this point in history |
| ArchivedDateTime | yes | yes |  |  |  | Gets or sets the archived date time value of this group member at this point in history |
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
| Group |  | yes | yes |  |  | Gets or sets the Group for this group member record at this point in history |
| GroupId | yes | yes |  |  |  | Gets or sets GroupId for this group member record at this point in history |
| GroupMember |  | yes | yes |  |  | Gets or sets the Group Member for this group member historical record |
| GroupMemberHistoricalAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupMemberId | yes | yes |  |  |  | Gets or sets the group member id of the group member for this group member historical record |
| GroupMemberStatus | yes | yes |  |  |  | Gets or sets the group member status of this group member at this point in history This is a hard coded list of values defined in the code as an enumeration. |
| GroupRole |  | yes | yes |  |  | Gets or sets the Group Type Role for this group member at this point in history |
| GroupRoleId | yes | yes |  |  |  | Gets or sets the group role id for this group member at this point in history |
| GroupRoleName | yes | yes |  |  |  | Gets or sets the group role name at this point in history |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InactiveDateTime | yes | yes |  |  |  | Gets or sets the InActiveDateTime value of the group member at this point in history (the time when the group member status was changed to GroupMemberStatus.Inactive) |
| IsArchived | yes | yes |  |  |  | Gets or sets a value indicating whether this group member was archived at this point in history |
| IsLeader | yes | yes |  |  |  | Gets or sets a value indicating whether the group member was IsLeader (which is determined by GroupRole.IsLeader) at this point in history |
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
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ArchivedByPersonAlias | Gets or sets the Person Alias that archived (soft deleted) this group member at this point in history |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| Group | Gets or sets the Group for this group member record at this point in history |
| GroupMember | Gets or sets the Group Member for this group member historical record |
| GroupRole | Gets or sets the Group Type Role for this group member at this point in history |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ArchivedByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupId | [GroupId](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupMember | [Group Member](group-member.md) | 49668b95-fedc-43dd-8085-d2b0d6343c48 |
| GroupRole | [Group Type Role](group-type-role.md) | d155c373-9e47-4c6a-badd-792f31af5fba |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
