# Event Item Occurrence Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Event`
- Model title: `EventItemOccurrence`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `71632e1a-1e7f-42b9-a630-ec99f375303a`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 51 |
| Database-marked properties | 18 |
| Lava-marked properties | 36 |
| Lava-marked non-database properties | 18 |
| Related model links | 10 |
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
| Campus |  | yes | yes |  |  | Gets or sets the Campus that this EventItemOccurrence is a member of. |
| CampusId | yes | yes |  |  |  | Gets or sets the Campus identifier. |
| ContactEmail | yes | yes |  |  |  | Gets or sets the Contact Person's email address. |
| ContactPersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias representing the personalias who is the contact person. |
| ContactPersonAliasId | yes | yes |  |  |  | Gets or sets the Id of the Person Alias for the EventItemOccurrence's contact person. This property is required. |
| ContactPhone | yes | yes |  |  |  | Gets or sets the Contact Person's phone number. |
| ContentChannelItems |  | yes | yes |  |  | Gets or sets the content channel items. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EventItem |  | yes | yes |  |  | Gets or sets the Event Item that this EventItemOccurrence is a member of. |
| EventItemId | yes | yes |  | yes |  | Gets or sets the Event Item identifier. |
| EventItemOccurrenceAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Linkages |  | yes | yes |  |  | Gets or sets the linkages. |
| Location | yes | yes |  |  |  | Gets or sets the Description of the Location. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| NextStartDateTime | yes | yes |  |  |  | Gets or sets the datetime for the next scheduled occurrence of this event. |
| Note | yes | yes |  |  |  | Gets or sets the campus note. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
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
| Campus | Gets or sets the Campus that this EventItemOccurrence is a member of. |
| ContactPersonAlias | Gets or sets the Person Alias representing the personalias who is the contact person. |
| ContentChannelItems | Gets or sets the content channel items. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EventItem | Gets or sets the Event Item that this EventItemOccurrence is a member of. |
| IdKey |  |
| Linkages | Gets or sets the linkages. |
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
| Campus | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| CampusId | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| ContactPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| ContactPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| ContentChannelItems | content channel items | 378a9559-bd86-45a8-b218-2c5d4cf3d770 |
| EventItem | [Event Item](event-item.md) | 6a58ad11-3491-84ae-4896-8f39906ea65e |
| EventItemId | [Event Item](event-item.md) | 6a58ad11-3491-84ae-4896-8f39906ea65e |
| Linkages | linkages | 1479d2b7-65c0-4e98-9e70-0848422fa00c |
| Schedule | [Schedule](schedule.md) | 0b2c38a7-d79c-4f85-9757-f1b045d32c8a |
| ScheduleId | [Schedule](schedule.md) | 0b2c38a7-d79c-4f85-9757-f1b045d32c8a |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
