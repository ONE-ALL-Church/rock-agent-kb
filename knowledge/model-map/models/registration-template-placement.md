# Registration Template Placement Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Event`
- Model title: `RegistrationTemplatePlacement`
- EntityType GUID: `cce05820-5854-47a4-ace3-05df48479939`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 46 |
| Database-marked properties | 17 |
| Lava-marked properties | 31 |
| Lava-marked non-database properties | 14 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowMultiplePlacements | yes | yes |  |  |  | Gets or sets a value indicating whether [allow multiple placements]. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| Cost | yes | yes |  |  |  | Gets or sets the cost. |
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
| GroupType |  | yes | yes |  |  | Gets or sets the GroupType that this registration template placement is associated with. |
| GroupTypeId | yes | yes |  | yes |  | Gets or sets the Id of the GroupType that this registration template placement is associated with. This property is required. |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class that is defined for the RegistrationTemplatePlacement. Use to get the IconCssClass to use since that GroupType.IconCssClass should be used if this isn't defined |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsInternal | yes | yes |  |  |  | Gets or sets a value indicating whether is limited to administration purposes. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the registration template placement. |
| Order | yes | yes |  |  |  | Gets or sets the sort and display order of the registration template placement. This is an ascending order, so the lower the value the higher the sort priority. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RegistrationTemplate |  | yes | yes |  |  | Gets or sets the RegistrationTemplate. |
| RegistrationTemplateId | yes | yes |  | yes |  | Gets or sets the RegistrationTemplate identifier. |
| RegistrationTemplatePlacementAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
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
| GroupType | Gets or sets the GroupType that this registration template placement is associated with. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RegistrationTemplate | Gets or sets the RegistrationTemplate. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| GroupType | [GroupType](group-type.md) |  |
| GroupTypeId | [GroupType](group-type.md) |  |
| RegistrationTemplate | [RegistrationTemplate](registration-template.md) |  |
| RegistrationTemplateId | [RegistrationTemplate](registration-template.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | IconCssClass | description |
