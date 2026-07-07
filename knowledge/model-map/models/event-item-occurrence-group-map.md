# Event Item Occurrence Group Map Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Event`
- Model title: `EventItemOccurrenceGroupMap`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `35`
- Obsolete methods: `4`
- EntityType GUID: `1479d2b7-65c0-4e98-9e70-0848422fa00c`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 46 |
| Database-marked properties | 15 |
| Lava-marked properties | 31 |
| Lava-marked non-database properties | 16 |
| Related model links | 8 |
| Method signatures | 35 |
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
| Campus |  | yes | yes |  |  | Gets or sets the Campus the event will be tied to. |
| CampusId | yes | yes |  |  |  | Gets or sets the Id of the Campus the event will be tied to. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EventItemOccurrence |  | yes | yes |  |  | Gets or sets the Event Item Occurrence. |
| EventItemOccurrenceGroupMapAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| EventItemOccurrenceId | yes | yes |  |  |  | Gets or sets the Event Item Occurrence identifier. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Group. |
| GroupId | yes | yes |  |  |  | Gets or sets the Group identifier. |
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
| PublicName | yes | yes |  |  |  | Gets or sets the name of the public. |
| RegistrationInstance |  | yes | yes |  |  | Gets or sets the Registration Instance. |
| RegistrationInstanceId | yes | yes |  |  |  | Gets or sets the Registration Instance identifier. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| UrlSlug | yes | yes |  |  |  | Gets or sets the URL slug. |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the Campus the event will be tied to. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EventItemOccurrence | Gets or sets the Event Item Occurrence. |
| Group | Gets or sets the Group. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RegistrationInstance | Gets or sets the Registration Instance. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Campus | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| CampusId | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| EventItemOccurrence | [Event Item Occurrence](event-item-occurrence.md) | 71632e1a-1e7f-42b9-a630-ec99f375303a |
| EventItemOccurrenceId | [Event Item Occurrence](event-item-occurrence.md) | 71632e1a-1e7f-42b9-a630-ec99f375303a |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| RegistrationInstance | [Registration Instance](registration-instance.md) | 5cd9c0c8-c047-61a0-4e36-0fdb8496f066 |
| RegistrationInstanceId | [Registration Instance](registration-instance.md) | 5cd9c0c8-c047-61a0-4e36-0fdb8496f066 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
