# Following Event Type Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `FollowingEventType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `35`
- Obsolete methods: `4`
- EntityType GUID: `8a0d208b-762d-403a-a972-3a0f079866d4`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 20 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 14 |
| Related model links | 0 |
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
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the user defined description of the FollowingEvent. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityNotificationFormatLava | yes | yes |  |  |  | Gets or sets how an entity should be formatted when included in the event notification to follower. |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the type of the event entity. |
| EntityTypeId | yes | yes |  |  |  | Gets or sets the event MEF component identifier. |
| FollowedEntityType |  | yes | yes |  |  | Gets or sets the type of the followed entity. |
| FollowedEntityTypeId | yes | yes |  |  |  | Gets or sets the followed entity type identifier. |
| FollowingEventTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IncludeNonPublicRequests | yes | yes |  |  |  | Gets or sets a value indicating whether [include non public requests]. |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is active. |
| IsNoticeRequired | yes | yes |  |  |  | Gets or sets a value indicating whether this event is required. If not, followers will be able to optionally select if they want to be notified of this event |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastCheckDateTime | yes | yes |  |  |  | Gets or sets the last check. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the (internal) Name of the FollowingEvent. This property is required. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SendOnWeekends | yes | yes |  |  |  | Gets or sets a value indicating whether [send on weekends]. |
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
| EntityType | Gets or sets the type of the event entity. |
| FollowedEntityType | Gets or sets the type of the followed entity. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
