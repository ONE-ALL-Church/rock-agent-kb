# Connection Opportunity Group Config Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Engagement`
- Model title: `ConnectionOpportunityGroupConfig`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `59756122-b779-4a4e-9ce7-6a4468aa9524`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 44 |
| Database-marked properties | 14 |
| Lava-marked properties | 29 |
| Lava-marked non-database properties | 15 |
| Related model links | 6 |
| Method signatures | 34 |
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
| ConnectionOpportunity |  | yes | yes |  |  | Gets or sets the Connection Opportunity. |
| ConnectionOpportunityGroupConfigAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ConnectionOpportunityId | yes | yes |  | yes |  | Gets or sets the Connection Opportunity identifier. |
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
| GroupMemberRole |  | yes | yes |  |  | Gets or sets the group member role. |
| GroupMemberRoleId | yes | yes |  |  |  | Gets or sets the group member role identifier. |
| GroupMemberStatus | yes | yes |  |  |  | Gets or sets the GroupMemberStatus. This is a hard coded list of values defined in the code as an enumeration. |
| GroupType |  | yes | yes |  |  | Gets or sets the type of the group. |
| GroupTypeId | yes | yes |  | yes |  | Gets or sets the Group Type identifier. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
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
| UseAllGroupsOfType | yes | yes |  | yes |  | Gets or sets a value indicating whether [use all groups of type]. |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| ConnectionOpportunity | Gets or sets the Connection Opportunity. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| GroupMemberRole | Gets or sets the group member role. |
| GroupType | Gets or sets the type of the group. |
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
| ConnectionOpportunity | [Connection Opportunity](connection-opportunity.md) | 79f64363-bc90-4109-9d31-a5eeb397cb2f |
| ConnectionOpportunityId | [Connection Opportunity](connection-opportunity.md) | 79f64363-bc90-4109-9d31-a5eeb397cb2f |
| GroupMemberRole | group member role | d155c373-9e47-4c6a-badd-792f31af5fba |
| GroupMemberRoleId | group member role | d155c373-9e47-4c6a-badd-792f31af5fba |
| GroupType | type | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |
| GroupTypeId | [Group Type](group-type.md) | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
