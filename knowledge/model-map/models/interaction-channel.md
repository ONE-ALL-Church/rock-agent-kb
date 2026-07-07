# Interaction Channel Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Core`
- Model title: `InteractionChannel`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `08606092-5ff5-4a34-a7a6-3dee43f2843a`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 65 |
| Database-marked properties | 34 |
| Lava-marked properties | 50 |
| Lava-marked non-database properties | 16 |
| Related model links | 21 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ChannelData | yes | yes |  |  |  | Gets or sets the channel data. |
| ChannelDetailTemplate | yes | yes |  |  |  | Gets or sets the channel detail template. |
| ChannelEntityId | yes | yes |  |  |  | Gets or sets the channel entity identifier. Note, the ChannelEntityType is inferred based on what the ChannelTypeMediumValue is: Page Views (Rock.SystemGuid.DefinedValue.INTERACTIONCHANNELTYPE_WEBSITE)Site IdCommunication Recipient Activity (Rock.SystemGuid.DefinedValue.INTERACTIONCHANNELTYPE_COMMUNICATION)Communication IdContent Channel Activity (Rock.SystemGuid.DefinedValue.INTERACTIONCHANNELTYPE_CONTENTCHANNEL)Content Channel IdSystem Events, like Workflow Form Entry (Rock.SystemGuid.DefinedValue.INTERACTIONCHANNELTYPE_SYSTEM_EVENTS)null, only one ChannelChat Events, like chat message counts (Rock.SystemGuid.DefinedValue.INTERACTIONCHANNELTYPE_CHAT)null, only one Channel |
| ChannelListTemplate | yes | yes |  |  |  | Gets or sets the channel list template. |
| ChannelTypeMediumValue |  | yes | yes |  |  | Gets or sets the Id of the Channel Type Defined Value representing what type of Interaction Channel this is. This helps determine the ChannelEntityId |
| ChannelTypeMediumValueId | yes | yes |  |  |  | Gets or sets the Id of the Channel Type Defined Value representing what type of Interaction Channel this is. This helps determine the ChannelEntityId These are found in the Interaction Medium Defined Type. |
| ComponentCacheDuration | yes | yes |  |  |  | Gets or sets the length of time (in minutes) that components of this channel should be cached |
| ComponentCustom1Label | yes | yes |  |  |  | Gets or sets the component custom 1 label. |
| ComponentCustom2Label | yes | yes |  |  |  | Gets or sets the component custom 2 label. |
| ComponentCustomIndexed1Label | yes | yes |  |  |  | Gets or sets the component custom indexed 1 label. |
| ComponentDetailTemplate | yes | yes |  |  |  | Gets or sets the component detail template. |
| ComponentEntityType |  | yes | yes |  |  | Gets or sets the Entity Type for each of this channel's components. The Id of the ComponentEntityTypeId is stored in down in InteractionComponent.EntityId. For example: PageViewEntityType is Page. Page.Id is stored down in InteractionComponent.EntityIdCommunication Recipient ActivityEntityType is Communication. Communication.Id is stored down in InteractionComponent.EntityIdWorkflow Entry FormEntityType is Workflow Type. WorkflowType.Id is stored down in InteractionComponent.EntityId |
| ComponentEntityTypeId | yes | yes |  |  |  | Gets or sets the Entity Type for each of this channel's components. The Id of the ComponentEntityTypeId is stored in down in InteractionComponent.EntityId. For example: PageViewEntityType is Page. Page.Id is stored down in InteractionComponent.EntityIdCommunication Recipient ActivityEntityType is Communication. Communication.Id is stored down in InteractionComponent.EntityIdWorkflow Entry FormEntityType is Workflow Type. WorkflowType.Id is stored down in InteractionComponent.EntityId |
| ComponentListTemplate | yes | yes |  |  |  | Gets or sets the component list template. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EngagementStrength | yes | yes |  |  |  | Gets or sets the engagement strength. |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InteractionChannelAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| InteractionCustom1Label | yes | yes |  |  |  | Gets or sets the interaction custom 1 label. |
| InteractionCustom2Label | yes | yes |  |  |  | Gets or sets the interaction custom 2 label. |
| InteractionCustomIndexed1Label | yes | yes |  |  |  | Gets or sets the interaction custom indexed 1 label. |
| InteractionDetailTemplate | yes | yes |  |  |  | Gets or sets the interaction detail template. |
| InteractionEntityType |  | yes | yes |  |  | Gets or sets the EntityTypeId for the Entity Type of entity that was modified. For example: PageViewnullCommunication Recipient ActivityCommunication RecipientWorkflow Entry FormWorkflow |
| InteractionEntityTypeId | yes | yes |  |  |  | Gets or sets the EntityTypeId for the Entity Type of entity that was modified. For example: PageViewnullCommunication Recipient ActivityCommunication RecipientWorkflow Entry FormWorkflow |
| InteractionListTemplate | yes | yes |  |  |  | Gets or sets the interaction list template. |
| InteractionSessions |  | yes | yes |  |  | Gets or sets the interaction sessions for this channel. |
| IsActive | yes | yes |  | yes |  | Gets or sets a flag indicating if this is an active group. This value is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  |  |  | Gets or sets the interaction channel name. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RetentionDuration | yes | yes |  |  |  | Gets or sets the retention days. |
| SessionDetailTemplate | yes | yes |  |  |  | Gets or sets the session detail template. |
| SessionListTemplate | yes | yes |  |  |  | Gets or sets the session list template. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| UsesSession | yes | yes |  |  |  | Gets or sets a value indicating whether [uses session]. Set to true if interactions in this channel from a web browser session (for example: PageViews). Set to false if interactions in this channel are not associated with a web browser session (for example: communication clicks and opens from an email client or sms device). |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| ChannelTypeMediumValue | Gets or sets the Id of the Channel Type Defined Value representing what type of Interaction Channel this is. This helps determine the ChannelEntityId |
| ComponentEntityType | Gets or sets the Entity Type for each of this channel's components. The Id of the ComponentEntityTypeId is stored in down in InteractionComponent.EntityId. For example: PageViewEntityType is Page. Page.Id is stored down in InteractionComponent.EntityIdCommunication Recipient ActivityEntityType is Communication. Communication.Id is stored down in InteractionComponent.EntityIdWorkflow Entry FormEntityType is Workflow Type. WorkflowType.Id is stored down in InteractionComponent.EntityId |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| InteractionEntityType | Gets or sets the EntityTypeId for the Entity Type of entity that was modified. For example: PageViewnullCommunication Recipient ActivityCommunication RecipientWorkflow Entry FormWorkflow |
| InteractionSessions | Gets or sets the interaction sessions for this channel. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ChannelEntityId | [Communication](communication.md) | c4ccbd91-1264-48bf-bc33-92751c8948b5 |
| ChannelEntityId | [Content Channel](content-channel.md) | 44484685-477e-4668-89a6-84f29739eb68 |
| ChannelEntityId | [Site](site.md) | 7244c10b-5d87-467b-a7f5-12dc29910ca8 |
| ChannelTypeMediumValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| ChannelTypeMediumValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| ComponentEntityType | [Communication](communication.md) | c4ccbd91-1264-48bf-bc33-92751c8948b5 |
| ComponentEntityType | components | ace6145b-57d6-4694-972f-ec43af776de7 |
| ComponentEntityType | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| ComponentEntityType | [Page](page.md) | e104dcdf-247c-4ced-a119-8cc51632761f |
| ComponentEntityType | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| ComponentEntityTypeId | [Communication](communication.md) | c4ccbd91-1264-48bf-bc33-92751c8948b5 |
| ComponentEntityTypeId | components | ace6145b-57d6-4694-972f-ec43af776de7 |
| ComponentEntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| ComponentEntityTypeId | [Page](page.md) | e104dcdf-247c-4ced-a119-8cc51632761f |
| ComponentEntityTypeId | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| InteractionEntityType | [Communication Recipient](communication-recipient.md) | 3ec89b90-6692-451e-a48f-0d2adeba05bc |
| InteractionEntityType | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| InteractionEntityType | [Workflow](workflow.md) | 3540e9a7-fe30-43a9-8b0a-a372b63dfc93 |
| InteractionEntityTypeId | [Communication Recipient](communication-recipient.md) | 3ec89b90-6692-451e-a48f-0d2adeba05bc |
| InteractionEntityTypeId | [Entity Type](entity-type.md) | a2277fba-d09f-4d07-b0ab-1c650c25a7a7 |
| InteractionEntityTypeId | [Workflow](workflow.md) | 3540e9a7-fe30-43a9-8b0a-a372b63dfc93 |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | ChannelTypeMediumValueId | enum_values |
