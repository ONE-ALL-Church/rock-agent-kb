# Group Type Role Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Group`
- Model title: `GroupTypeRole`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `d155c373-9e47-4c6a-badd-792f31af5fba`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 54 |
| Database-marked properties | 26 |
| Lava-marked properties | 39 |
| Lava-marked non-database properties | 13 |
| Related model links | 6 |
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
| CanEdit | yes | yes |  |  |  | Gets or sets a value indicating whether this instance can edit. |
| CanManageMembers | yes | yes |  |  |  | Gets or sets a value indicating whether this instance can manage members. |
| CanTakeAttendance | yes | yes |  |  |  | Gets or sets a value indicating whether this instance can take attendance. |
| CanView | yes | yes |  |  |  | Gets or sets a value indicating whether this instance can view. |
| ChatRole | yes | yes |  |  |  | Gets or sets the role of the chat individual, to be synchronized with the external chat system. This is a hard coded list of values defined in the code as an enumeration. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the user defined description of the GroupRole. This property is required. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GroupType |  | yes | yes |  |  | Gets or sets the Group Type that this GroupRole belongs to. |
| GroupTypeId | yes | yes |  |  |  | Gets or sets the Id of the Group Type that this GroupRole belongs to. This property is required. |
| GroupTypeRoleAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsCheckInAllowed | yes | yes |  |  |  | Gets or sets a value indicating if this role can check into the group. This only applies during the "already member" check during check-in. |
| IsExcludedFromPeerNetwork | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is excluded from peer network. |
| IsLeader | yes | yes |  |  |  | Gets or sets a flag indicating if this is a group leader role. |
| IsPublic | yes | yes |  |  |  | Determines if this role is intended to be used and displayed on public facing sites and features. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this GroupRole is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MaxCount | yes | yes |  |  |  | Gets or sets the maximum count of GroupMembers that a Group can have who belong to this GroupRole. |
| MinCount | yes | yes |  |  |  | Gets or sets the minimum count of GroupMembers that a Group can have who belong to this GroupRole. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the GroupRole. This property is required. |
| Order | yes | yes |  |  |  | Gets or sets the sort order position of the GroupRole. The lower the SortOrder the higher the GroupRole shows in lists/controls. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ReceiveRequirementsNotifications | yes | yes |  |  |  | Gets or sets a value indicating whether this role should receive requirements notifications]. |
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
| GroupType | Gets or sets the Group Type that this GroupRole belongs to. |
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
| GroupType | [Group Type](group-type.md) | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |
| GroupTypeId | [Group Type](group-type.md) | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |
| MaxCount | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| MaxCount | GroupMembers | 49668b95-fedc-43dd-8085-d2b0d6343c48 |
| MinCount | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| MinCount | GroupMembers | 49668b95-fedc-43dd-8085-d2b0d6343c48 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
