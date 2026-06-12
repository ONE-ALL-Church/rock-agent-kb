# Group Member Assignment Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Group`
- Model title: `GroupMemberAssignment`
- EntityType GUID: `22bf14ed-e882-4bb0-9328-d12545bf5f61`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 46 |
| Database-marked properties | 15 |
| Lava-marked properties | 28 |
| Lava-marked non-database properties | 14 |
| Related model links | 8 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ConfirmationSentDateTime | yes | yes |  |  |  | The date and time when the confirmation is sent. |
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
| GroupId | yes | yes |  | yes |  | Gets or sets the Group identifier. |
| GroupMember |  |  | yes |  |  | Gets or sets the GroupMember. |
| GroupMemberAssignmentAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupMemberId | yes | yes |  |  |  | Gets or sets the GroupMember identifier. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastReminderSentDateTime | yes |  |  |  |  | The date and time when the last reminder was sent. |
| Location |  | yes | yes |  |  | Gets or sets the Location. |
| LocationId | yes | yes |  |  |  | Gets or sets the Location identifier. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonId |  |  | yes |  |  | Gets the Person identifier. |
| Schedule |  | yes | yes |  |  | Gets or sets the Schedule. |
| ScheduleId | yes | yes |  |  |  | Gets or sets the Schedule identifier. |
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
| Location | Gets or sets the Location. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Schedule | Gets or sets the Schedule. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| GroupId | [Group](group.md) |  |
| GroupMember | [GroupMember](group-member.md) |  |
| GroupMemberId | [GroupMember](group-member.md) |  |
| Location | [Location](location.md) |  |
| LocationId | [Location](location.md) |  |
| PersonId | [Person](person.md) |  |
| Schedule | [Schedule](schedule.md) |  |
| ScheduleId | [Schedule](schedule.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
