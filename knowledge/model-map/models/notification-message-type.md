# Notification Message Type Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `NotificationMessageType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `36fb1038-8836-429f-bad4-04d32892d6d0`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 51 |
| Database-marked properties | 19 |
| Lava-marked properties | 36 |
| Lava-marked non-database properties | 17 |
| Related model links | 4 |
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
| ComponentDataJson | yes | yes |  |  |  | Gets or sets the component data json. This data is only understood by the component itself and should not be modified elsewhere. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the Entity Type of the component that handles logic for this instance. |
| EntityTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Entity Type component that handles logic for this instance. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsDeletedOnRead | yes | yes |  |  |  | Gets or sets a value indicating whether messages are deleted instead of being marked as read. |
| IsMobileApplicationSupported | yes | yes |  |  |  | Gets or sets a value indicating whether messages are supported on mobile applications. |
| IsTvApplicationSupported | yes | yes |  |  |  | Gets or sets a value indicating whether messages are supported on TV applications. |
| IsValid |  |  | yes |  |  |  |
| IsWebSupported | yes | yes |  |  |  | Gets or sets a value indicating whether messages are supported on web sites. |
| Item |  |  | yes |  |  |  |
| Key | yes | yes |  | yes |  | Gets or sets the key that identifies this instance to the component. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| NotificationMessageTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| NotificationMessages |  | yes | yes |  |  | Gets or sets a collection containing the Notification Message objects that belong to this Notification Message Type. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RelatedMobileApplicationSite |  | yes | yes |  |  | Gets or sets the related mobile site. If specified then messages will only show up on this mobile application. Otherwise messages will show up on all mobile applications. This does not affect other site types. |
| RelatedMobileApplicationSiteId | yes | yes |  |  |  | Gets or sets the related mobile site identifier. If specified then messages will only show up on this mobile application. Otherwise messages will show up on all mobile applications. This does not affect other site types. |
| RelatedTvApplicationSite |  | yes | yes |  |  | Gets or sets the related TV site. If specified then messages will only show up on this TV application. Otherwise messages will show up on all TV applications. This does not affect other site types. |
| RelatedTvApplicationSiteId | yes | yes |  |  |  | Gets or sets the related TV site identifier. If specified then messages will only show up on this TV application. Otherwise messages will show up on all TV applications. This does not affect other site types. |
| RelatedWebSite |  | yes | yes |  |  | Gets or sets the related web site. If specified then messages will only show up on this website. Otherwise messages will show up on all websites. This does not affect other site types. |
| RelatedWebSiteId | yes | yes |  |  |  | Gets or sets the related web site identifier. If specified then messages will only show up on this website. Otherwise messages will show up on all websites. This does not affect other site types. |
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
| EntityType | Gets or sets the Entity Type of the component that handles logic for this instance. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| NotificationMessages | Gets or sets a collection containing the Notification Message objects that belong to this Notification Message Type. |
| RelatedMobileApplicationSite | Gets or sets the related mobile site. If specified then messages will only show up on this mobile application. Otherwise messages will show up on all mobile applications. This does not affect other site types. |
| RelatedTvApplicationSite | Gets or sets the related TV site. If specified then messages will only show up on this TV application. Otherwise messages will show up on all TV applications. This does not affect other site types. |
| RelatedWebSite | Gets or sets the related web site. If specified then messages will only show up on this website. Otherwise messages will show up on all websites. This does not affect other site types. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| EntityType | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| EntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| NotificationMessages | [Notification Message](notification-message.md) | 239add2e-2dbf-46a7-bd28-4a2a201d4e7b |
| NotificationMessages | [Notification Message Type](notification-message-type.md) | 36fb1038-8836-429f-bad4-04d32892d6d0 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
