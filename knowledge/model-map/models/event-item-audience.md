# Event Item Audience Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Event`
- Model title: `EventItemAudience`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `22394315-e21b-40af-afda-75d9f5dad721`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 40 |
| Database-marked properties | 11 |
| Lava-marked properties | 25 |
| Lava-marked non-database properties | 14 |
| Related model links | 4 |
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
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefinedValue |  | yes | yes |  |  | Gets or sets the Defined Value that this EventItemAudience is associated with. |
| DefinedValueId | yes | yes |  | yes |  | Gets or sets the Id of the Defined Value that this EventItemAudience is associated with. This property is required. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EventItem |  | yes | yes |  |  | Gets or sets the Event Item that this EventItemAudience is associated with. |
| EventItemAudienceAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| EventItemId | yes | yes |  | yes |  | Gets or sets the Id of the Event Item that this EventItemAudience is associated with. This property is required. |
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
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DefinedValue | Gets or sets the Defined Value that this EventItemAudience is associated with. |
| EntityStringValue |  |
| EventItem | Gets or sets the Event Item that this EventItemAudience is associated with. |
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
| DefinedValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| DefinedValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| EventItem | [Event Item](event-item.md) | 6a58ad11-3491-84ae-4896-8f39906ea65e |
| EventItemId | [Event Item](event-item.md) | 6a58ad11-3491-84ae-4896-8f39906ea65e |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
