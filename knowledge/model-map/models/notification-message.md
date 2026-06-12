# Notification Message Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `NotificationMessage`
- EntityType GUID: `239add2e-2dbf-46a7-bd28-4a2a201d4e7b`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 29 |
| Database-marked properties | 15 |
| Lava-marked properties | 22 |
| Lava-marked non-database properties | 7 |
| Related model links | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ComponentDataJson | yes | yes |  |  |  | Gets or sets the component data json. This data is only understood by the component itself and should not be modified elsewhere. |
| ContextKey |  |  | yes |  |  |  |
| Count | yes | yes |  |  |  | Gets or sets the count of the message. This value will be summed for all visible messages and used as the total number of messages. It will also usually be displayed as a badge on the message itself. |
| Description | yes | yes |  | yes |  | Gets or sets the description of the message. This should be a somewhat short string, such as a couple of sentences. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExpireDateTime | yes | yes |  |  |  | Gets or sets the date and time the message will automatically expire and be removed. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsRead | yes | yes |  |  |  | Gets or sets a value indicating whether this message has been read. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Key | yes | yes |  |  |  | Gets or sets the key that identifies this instance to the component. The key allows components to look up existing messages so they can be updated. null values are allowed. |
| MessageDateTime | yes | yes |  |  |  | Gets or sets the date and time at which point the message will be shown to the individual. By default the current date and time will be used, but setting to a future date is allowed. |
| NotificationMessageType |  | yes | yes |  |  | Gets or sets the NotificationMessageType that this instance belongs to. |
| NotificationMessageTypeId | yes | yes |  | yes |  | Gets or sets the identifier of the NotificationMessageType that handles logic for this instance. |
| PersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias of the individual this message should be displayed to. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the person alias identifier of the individual this message should be displayed to. |
| Title | yes | yes |  | yes |  | Gets or sets the title of the message. This should be a very short string, such as only a few words. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| IdKey |  |
| NotificationMessageType | Gets or sets the NotificationMessageType that this instance belongs to. |
| PersonAlias | Gets or sets the PersonAlias of the individual this message should be displayed to. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| NotificationMessageType | [NotificationMessageType](notification-message-type.md) |  |
| NotificationMessageTypeId | [NotificationMessageType](notification-message-type.md) |  |
| PersonAlias | [PersonAlias](person-alias.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
