# Event Item Occurrence Channel Item Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Event`
- Model title: `EventItemOccurrenceChannelItem`
- EntityType GUID: `378a9559-bd86-45a8-b218-2c5d4cf3d770`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 40 |
| Database-marked properties | 11 |
| Lava-marked properties | 25 |
| Lava-marked non-database properties | 14 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContentChannelItem |  | yes | yes |  |  | Gets or sets the Content Channel Item. |
| ContentChannelItemId | yes | yes |  |  |  | Gets or sets the Content Channel Item. |
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
| EventItemOccurrenceChannelItemAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| EventItemOccurrenceId | yes | yes |  |  |  | Gets or sets the Event Item Occurrence identifier. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
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
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| ContentChannelItem | Gets or sets the Content Channel Item. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EventItemOccurrence | Gets or sets the Event Item Occurrence. |
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
| ContentChannelItem | [Content Channel Item](content-channel-item.md) | bf12ae64-21fb-433b-a8a4-e40e8c426dda |
| ContentChannelItemId | [Content Channel Item](content-channel-item.md) | bf12ae64-21fb-433b-a8a4-e40e8c426dda |
| EventItemOccurrence | [Event Item Occurrence](event-item-occurrence.md) | 71632e1a-1e7f-42b9-a630-ec99f375303a |
| EventItemOccurrenceId | [Event Item Occurrence](event-item-occurrence.md) | 71632e1a-1e7f-42b9-a630-ec99f375303a |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
