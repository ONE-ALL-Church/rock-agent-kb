# Group Requirement Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Group`
- Model title: `GroupRequirement`
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
| Pre-alpha changes touching this model | 3 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowLeadersToOverride | yes | yes |  |  |  | Gets or sets whether leaders are allowed to mark requirements as met manually. |
| AppliesToAgeClassification | yes | yes |  |  |  | Gets or sets the "Applies To" Age Classification. This is a hard coded list of values defined in the code as an enumeration. |
| AppliesToDataView |  | yes | yes |  |  | Gets or sets the "Applies To" DataView. |
| AppliesToDataViewId | yes | yes |  |  |  | Gets or sets the "Applies To" DataView identifier. |
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
| DueDateAttribute |  | yes | yes |  |  | Gets or sets the Attribute for . |
| DueDateAttributeId | yes | yes |  |  |  | Gets or sets the "Due Date" attribute identifier for when the GroupRequirementType.DueDateType is . |
| DueDateStaticDate | yes | yes |  |  |  | Gets or sets the configured date for when the GroupRequirementType.DueDateType is . |
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
| GroupTypeId | yes | yes |  |  |  | Gets or sets the GroupType identifier. |
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
| AppliesToDataView | Gets or sets the "Applies To" DataView. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DueDateAttribute | Gets or sets the Attribute for . |
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
| AppliesToDataView | [DataView](data-view.md) |  |
| AppliesToDataViewId | [DataView](data-view.md) |  |
| DueDateAttribute | [Attribute](attribute.md) |  |
| Group | [Group](group.md) |  |
| GroupId | [Group](group.md) |  |
| GroupRequirementType | type |  |
| GroupRole | Group Role |  |
| GroupType | type |  |
| GroupTypeId | [GroupType](group-type.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | DueDateAttribute | description |
| property_changed | DueDateAttributeId | description |
| property_changed | DueDateStaticDate | description |
