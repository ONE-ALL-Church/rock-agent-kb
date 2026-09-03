# Content Channel Type Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `CMS`
- Model title: `ContentChannelType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `d5992f79-7fb8-49ff-82ab-e8cb2cec1e74`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 45 |
| Database-marked properties | 17 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 13 |
| Related model links | 2 |
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
| Channels |  | yes | yes |  |  | Gets or sets the channels. |
| ContentChannelTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DateRangeType | yes | yes |  |  |  | Gets or sets an ContentChannelDateType enumeration that represents the type of date range that this DateRangeTypeEnum supports. This is a hard coded list of values defined in the code as an enumeration. |
| DisableContentField | yes | yes |  |  |  | Gets or sets a value indicating whether [disable content field]. |
| DisablePriority | yes | yes |  |  |  | Gets or sets a value indicating whether [disable priority]. |
| DisableStatus | yes | yes |  |  |  | Gets or sets a value indicating whether [disable status]. If this is set to True, all of the ContentChannelItems are "Approved" |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IncludeTime | yes | yes |  |  |  | Gets or sets a value indicating whether time should be included with the single or date range values |
| IsSystem | yes | yes |  |  |  | Gets or sets a flag indicating if this ContentType is part of the Rock core system/framework. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the ContentType. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ShowInChannelList | yes | yes |  |  |  | A flag indicating if a Content Channel of this ContentChannelType will be shown in the content channel list. When false, it means any 'Channel Types Include' settings MUST specifically include in order to show it. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Channels | Gets or sets the channels. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
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
| Channels | channels | 44484685-477e-4668-89a6-84f29739eb68 |
| ShowInChannelList | [Content Channel](content-channel.md) | 44484685-477e-4668-89a6-84f29739eb68 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
