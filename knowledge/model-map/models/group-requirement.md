# Group Requirement Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Group`
- Model title: `GroupRequirement`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `39`
- Obsolete methods: `5`
- EntityType GUID: `cfc7de86-222e-4669-83c2-a3f5b04cb5d6`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 52 |
| Database-marked properties | 19 |
| Lava-marked properties | 37 |
| Lava-marked non-database properties | 18 |
| Related model links | 9 |
| Method signatures | 39 |
| Obsolete methods | 5 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowLeadersToOverride | yes | yes |  |  |  | Gets or sets whether leaders are allowed to mark requirements as met manually. |
| AppliesToAgeClassification | yes | yes |  |  |  | Gets or sets the "Applies To" Age Classification. This is a hard coded list of values defined in the code as an enumeration. |
| AppliesToDataView |  | yes | yes |  |  | Gets or sets the "Applies To" Data View. |
| AppliesToDataViewId | yes | yes |  |  |  | Gets or sets the "Applies To" Data View identifier. |
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
| DueDateAttribute |  | yes | yes |  |  | Gets or sets the Attribute for DueDateType.GroupAttribute. |
| DueDateAttributeId | yes | yes |  |  |  | Gets or sets the "Due Date" attribute identifier for when the GroupRequirementType.DueDateType is DueDateType.GroupAttribute. |
| DueDateStaticDate | yes | yes |  |  |  | Gets or sets the configured date for when the GroupRequirementType.DueDateType is DueDateType.ConfiguredDate. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Group. |
| GroupId | yes | yes |  |  |  | Gets or sets the Group identifier. |
| GroupRequirementAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupRequirementType |  | yes | yes |  |  | Gets or sets the type of the group requirement. |
| GroupRequirementTypeId | yes | yes |  | yes |  | Gets or sets the group requirement type identifier. |
| GroupRole |  | yes | yes |  |  | The specific Group Role that this requirement is for. NULL means this requirement applies to all roles. |
| GroupRoleId | yes | yes |  |  |  | The specific GroupRoleId that this requirement is for. NULL means this requirement applies to all roles. |
| GroupType |  | yes | yes |  |  | Gets or sets the type of the group. |
| GroupTypeId | yes | yes |  |  |  | Gets or sets the Group Type identifier. |
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
| MustMeetRequirementToAddMember | yes | yes |  |  |  | Gets or sets a value indicating whether a member must meet this requirement before adding (only applies to DataView and SQL RequirementCheckType) |
| ParentAuthority |  |  | yes |  |  | Gets the parent security authority for this GroupRequirement. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AppliesToDataView | Gets or sets the "Applies To" Data View. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DueDateAttribute | Gets or sets the Attribute for DueDateType.GroupAttribute. |
| EntityStringValue |  |
| Group | Gets or sets the Group. |
| GroupRequirementType | Gets or sets the type of the group requirement. |
| GroupRole | The specific Group Role that this requirement is for. NULL means this requirement applies to all roles. |
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
| AppliesToDataView | [Data View](data-view.md) | 57f8fa29-dcf1-4f74-8553-87e90f234139 |
| AppliesToDataViewId | [Data View](data-view.md) | 57f8fa29-dcf1-4f74-8553-87e90f234139 |
| DueDateAttribute | [Attribute](attribute.md) | 5997c8d3-8840-4591-99a5-552919f90cbd |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupRequirementType | type | 8e67e852-d1bf-485c-9898-09f19998cc40 |
| GroupRole | Group Role | d155c373-9e47-4c6a-badd-792f31af5fba |
| GroupType | type | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |
| GroupTypeId | [Group Type](group-type.md) | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
