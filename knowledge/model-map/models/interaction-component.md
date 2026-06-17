# Interaction Component Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `InteractionComponent`
- EntityType GUID: `ace6145b-57d6-4694-972f-ec43af776de7`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 45 |
| Database-marked properties | 17 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 13 |
| Related model links | 5 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ChannelCustom1 | yes | yes |  |  |  | Gets or sets the channel custom 1. |
| ChannelCustom2 | yes | yes |  |  |  | Gets or sets the channel custom 2. |
| ChannelCustomIndexed1 | yes | yes |  |  |  | Gets or sets the channel custom indexed 1. |
| ComponentData | yes | yes |  |  |  | Gets or sets the interaction component data. |
| ComponentSummary | yes | yes |  |  |  | Gets or sets the component summary. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  | Gets or sets the Id of the entity that this interaction component is related to (determined by InteractionChannel.ComponentEntityTypeId ) Page ViewsPage IdCommunication Recipient ActivityCommunication IdContent Channel ActivityContent Channel IdSystem Events, like Workflow Form EntryDepends on Content Channel Type |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InteractionChannel |  | yes | yes |  |  | Gets or sets the channel. |
| InteractionChannelId | yes | yes |  | yes |  | Gets or sets the Id of the Interaction Channel channel that is associated with this Component. |
| InteractionComponentAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the interaction component name. |
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
| EntityStringValue |  |
| IdKey |  |
| InteractionChannel | Gets or sets the channel. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| EntityId | [Communication](communication.md) | c4ccbd91-1264-48bf-bc33-92751c8948b5 |
| EntityId | [Content Channel](content-channel.md) | 44484685-477e-4668-89a6-84f29739eb68 |
| EntityId | [Content Channel Type](content-channel-type.md) | d5992f79-7fb8-49ff-82ab-e8cb2cec1e74 |
| EntityId | [Page](page.md) | e104dcdf-247c-4ced-a119-8cc51632761f |
| InteractionChannelId | [Interaction Channel](interaction-channel.md) | 08606092-5ff5-4a34-a7a6-3dee43f2843a |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
