# Interaction Channel Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `InteractionChannel`
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
| Pre-alpha changes touching this model | 2 |

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
| ChannelEntityId | yes | yes |  |  |  | Gets or sets the channel entity identifier. Note, the ChannelEntityType is inferred based on what the ChannelTypeMediumValue is: Page Views ()Site IdCommunication Recipient Activity ()Communication IdContent Channel Activity ()ContentChannel IdSystem Events, like Workflow Form Entry ()null, only one ChannelChat Events, like chat message counts ()null, only one Channel |
| ChannelListTemplate | yes | yes |  |  |  | Gets or sets the channel list template. |
| ChannelTypeMediumValue |  | yes | yes |  |  | Gets or sets the Id of the Channel Type DefinedValue representing what type of Interaction Channel this is. This helps determine the ChannelEntityId |
| ChannelTypeMediumValueId | yes | yes |  |  |  | Gets or sets the Id of the Channel Type DefinedValue representing what type of Interaction Channel this is. This helps determine the ChannelEntityId These are found in the "Interaction Medium" Defined Type. |
| ComponentCacheDuration | yes | yes |  |  |  | Gets or sets the length of time (in minutes) that components of this channel should be cached |
| ComponentCustom1Label | yes | yes |  |  |  | Gets or sets the component custom 1 label. |
| ComponentCustom2Label | yes | yes |  |  |  | Gets or sets the component custom 2 label. |
| ComponentCustomIndexed1Label | yes | yes |  |  |  | Gets or sets the component custom indexed 1 label. |
| ComponentDetailTemplate | yes | yes |  |  |  | Gets or sets the component detail template. |
| ComponentEntityType |  | yes | yes |  |  | Gets or sets the EntityType for each of this channel's components. The Id of the ComponentEntityTypeId is stored in down in InteractionComponent.EntityId. For example: PageViewEntityType is Page. Page.Id is stored down in InteractionComponent.EntityIdCommunication Recipient ActivityEntityType is Communication. Communication.Id is stored down in InteractionComponent.EntityIdWorkflow Entry FormEntityType is WorkflowType. WorkflowType.Id is stored down in InteractionComponent.EntityId |
| ComponentEntityTypeId | yes | yes |  |  |  | Gets or sets the EntityType for each of this channel's components. The Id of the ComponentEntityTypeId is stored in down in InteractionComponent.EntityId. For example: PageViewEntityType is Page. Page.Id is stored down in InteractionComponent.EntityIdCommunication Recipient ActivityEntityType is Communication. Communication.Id is stored down in InteractionComponent.EntityIdWorkflow Entry FormEntityType is WorkflowType. WorkflowType.Id is stored down in InteractionComponent.EntityId |
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
| InteractionEntityType |  | yes | yes |  |  | Gets or sets the EntityTypeId for the EntityType of entity that was modified. For example: PageViewnullCommunication Recipient ActivityCommunicationRecipientWorkflow Entry FormWorkflow |
| InteractionEntityTypeId | yes | yes |  |  |  | Gets or sets the EntityTypeId for the EntityType of entity that was modified. For example: PageViewnullCommunication Recipient ActivityCommunicationRecipientWorkflow Entry FormWorkflow |
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
| ChannelTypeMediumValue | Gets or sets the Id of the Channel Type DefinedValue representing what type of Interaction Channel this is. This helps determine the ChannelEntityId |
| ComponentEntityType | Gets or sets the EntityType for each of this channel's components. The Id of the ComponentEntityTypeId is stored in down in InteractionComponent.EntityId. For example: PageViewEntityType is Page. Page.Id is stored down in InteractionComponent.EntityIdCommunication Recipient ActivityEntityType is Communication. Communication.Id is stored down in InteractionComponent.EntityIdWorkflow Entry FormEntityType is WorkflowType. WorkflowType.Id is stored down in InteractionComponent.EntityId |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| InteractionEntityType | Gets or sets the EntityTypeId for the EntityType of entity that was modified. For example: PageViewnullCommunication Recipient ActivityCommunicationRecipientWorkflow Entry FormWorkflow |
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
| ChannelEntityId | [Communication](communication.md) |  |
| ChannelEntityId | [ContentChannel](content-channel.md) |  |
| ChannelEntityId | [Site](site.md) |  |
| ChannelTypeMediumValue | [DefinedValue](defined-value.md) |  |
| ChannelTypeMediumValueId | [DefinedValue](defined-value.md) |  |
| ComponentEntityType | [Communication](communication.md) |  |
| ComponentEntityType | components |  |
| ComponentEntityType | [EntityType](entity-type.md) |  |
| ComponentEntityType | [Page](page.md) |  |
| ComponentEntityType | [WorkflowType](workflow-type.md) |  |
| ComponentEntityTypeId | [Communication](communication.md) |  |
| ComponentEntityTypeId | components |  |
| ComponentEntityTypeId | [EntityType](entity-type.md) |  |
| ComponentEntityTypeId | [Page](page.md) |  |
| ComponentEntityTypeId | [WorkflowType](workflow-type.md) |  |
| InteractionEntityType | [CommunicationRecipient](communication-recipient.md) |  |
| InteractionEntityType | [EntityType](entity-type.md) |  |
| InteractionEntityType | [Workflow](workflow.md) |  |
| InteractionEntityTypeId | [CommunicationRecipient](communication-recipient.md) |  |
| InteractionEntityTypeId | [EntityType](entity-type.md) |  |
| InteractionEntityTypeId | [Workflow](workflow.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | ChannelEntityId | description |
| property_changed | ChannelTypeMediumValueId | enum_values |
