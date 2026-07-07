# Group Demographic Type Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Group`
- Model title: `GroupDemographicType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `9ae7a87b-e274-4ff5-befd-55ccf603ce13`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 46 |
| Database-marked properties | 17 |
| Lava-marked properties | 31 |
| Lava-marked non-database properties | 14 |
| Related model links | 3 |
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
| ComponentEntityType |  | yes | yes |  |  | Gets or sets the type of the component entity. |
| ComponentEntityTypeId | yes | yes |  | yes |  | Gets or sets the component entity type identifier. This is an FK of EntityType.Id. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | The description of the Group Demographic Type. Previewable. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GroupDemographicTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupType |  | yes | yes |  |  | Gets or sets the type of the group. |
| GroupTypeId | yes | yes |  | yes |  | The Group Type identifier of the group this Group Demographic Type is associated with. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsAutomated | yes | yes |  | yes |  | Specify if this GroupDemographicType is automated. If true the UI will not allow manual entry. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastRunDurationSeconds | yes | yes |  |  |  | How long a component took to get its values in seconds. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | The name of the Group Demographic Type. Previewable. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RoleFilter | yes | yes |  |  |  | A comma delimited list of GroupTypeRoles IDs |
| RunOnPersonUpdate | yes | yes |  | yes |  | Indicates if the component for this Group Demographic Type should be run everytime a person is updated. |
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
| ComponentEntityType | Gets or sets the type of the component entity. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
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
| GroupType | type | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |
| GroupTypeId | [Group Type](group-type.md) | 0dd30b04-01cf-4b38-8e83-be661e2f7286 |
| RoleFilter | GroupTypeRoles | d155c373-9e47-4c6a-badd-792f31af5fba |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
