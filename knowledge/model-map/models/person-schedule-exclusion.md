# Person Schedule Exclusion Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Group`
- Model title: `PersonScheduleExclusion`
- EntityType GUID: `07204f06-c09c-4b37-921a-c31c042938b9`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 46 |
| Database-marked properties | 15 |
| Lava-marked properties | 31 |
| Lava-marked non-database properties | 16 |
| Related model links | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ChildPersonScheduleExclusions |  | yes | yes |  |  | Gets or sets the child person schedule exclusions. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EndDate | yes | yes |  |  |  | Gets or sets the end date. |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | The Group if there is a specific group for this exclusion. |
| GroupId | yes | yes |  |  |  | The GroupId if there is a specific group for this exclusion. |
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
| ParentPersonScheduleExclusion |  | yes | yes |  |  | Gets or sets the parent Person Schedule Exclusion. |
| ParentPersonScheduleExclusionId | yes | yes |  |  |  | Gets or sets the parent person schedule exclusion identifier. Use this to associate this exclusion with another PersonScheduleExclusion. This can be used support family based blackout dates (A person can indicate a blackout date and also include other members of their family). |
| PersonAlias |  | yes | yes |  |  | Gets or sets the person alias of the Person that this exclusion is for |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the person alias identifier of the Person that this exclusion is for |
| PersonScheduleExclusionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| StartDate | yes | yes |  |  |  | Gets or sets the start date. |
| SupportedActions |  |  | yes |  |  |  |
| Title | yes | yes |  |  |  | Gets or sets the title (optional) |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| ChildPersonScheduleExclusions | Gets or sets the child person schedule exclusions. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| Group | The Group if there is a specific group for this exclusion. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ParentPersonScheduleExclusion | Gets or sets the parent Person Schedule Exclusion. |
| PersonAlias | Gets or sets the person alias of the Person that this exclusion is for |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupId | [GroupId](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| ParentPersonScheduleExclusion | [Person Schedule Exclusion](person-schedule-exclusion.md) | 07204f06-c09c-4b37-921a-c31c042938b9 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
