# Interaction Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `Interaction`
- EntityType GUID: `3bb4b095-2de4-4009-8fa2-705bf284f7b7`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 68 |
| Database-marked properties | 35 |
| Lava-marked properties | 53 |
| Lava-marked non-database properties | 18 |
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
| Campaign | yes | yes |  |  |  | Gets or sets the campaign name |
| CampaignValueId | yes | yes |  |  |  | Gets or sets the UTM Campaign identifier. These values are associated with the Defined Type "UTM Campaign". |
| ChannelCustom1 | yes | yes |  |  |  | Gets or sets the channel custom 1. |
| ChannelCustom2 | yes | yes |  |  |  | Gets or sets the channel custom 2. |
| ChannelCustomIndexed1 | yes | yes |  |  |  | Gets or sets the channel custom indexed 1. |
| Content | yes | yes |  |  |  | Gets or sets the campaign content. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  | Gets or sets the Id of the entity that this interaction component is tracking activity for. Page ViewsEntityId is left null, Page is the Component, Site is the ChannelCommunication Recipient ActivityEntityId is the CommunicationRecipient Id. Communication is the Component, single ChannelContent Channel ActivityEntityId is left null, ContentChannel is the Component, single ChannelWorkflow Form EntryEntityId is the Workflow Id, WorkflowType is the Component, single Channel |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InteractionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| InteractionComponent |  | yes | yes |  |  | Gets or sets the interaction component. |
| InteractionComponentId | yes | yes |  | yes |  | Gets or sets the Id of the InteractionComponent Component that is associated with this Interaction. |
| InteractionData | yes | yes |  |  |  | Gets or sets the interaction data. |
| InteractionDateKey | yes | yes |  |  |  | Gets the interaction date key. |
| InteractionDateTime | yes | yes |  |  |  | Gets or sets the interaction datetime. |
| InteractionEndDateTime | yes | yes |  |  |  | Gets or sets the interaction end date time. |
| InteractionLength | yes | yes |  |  |  | Gets or sets the length of time (or percent of time) of the interaction. The units on this depend on the InteractionChannel, which might have this be a Percent, Days, Seconds, Minutes, etc For example, if this interaction type is watching a video, this might be what percent of the video they watched |
| InteractionSession |  | yes | yes |  |  | Gets or sets the interaction component. |
| InteractionSessionId | yes | yes |  |  |  | Gets or sets the Id of the InteractionSession Session that that is associated with this Interaction. |
| InteractionSourceDate |  | yes | yes |  |  | Gets or sets the interaction source date. |
| InteractionSummary | yes | yes |  |  |  | Gets or sets the interaction summary. |
| InteractionTimeToServe | yes | yes |  |  |  | Gets or sets the interaction time to serve. The units on this depend on the InteractionChannel, which might have this be a Percent, Days, Seconds, Minutes, etc. For example, if this is a page view, this would be how long (in seconds) it took for Rock to generate a response. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Medium | yes | yes |  |  |  | Gets or sets the campaign medium. |
| MediumValueId | yes | yes |  |  |  | Gets or sets the UTM Medium identifier. These values are associated with the Defined Type "UTM Medium". |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Operation | yes | yes |  |  |  | Gets or sets the operation. For example: 'View', 'Opened', 'Click', 'Prayed', 'Form Viewed', 'Form Completed', 'Complete', 'Incomplete', 'Watch', 'Present'. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the person alias. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the person alias identifier. |
| PersonalDevice |  | yes | yes |  |  | Gets or sets the personal device. |
| PersonalDeviceId | yes | yes |  |  |  | Gets or sets the personal device identifier. |
| RelatedEntityId | yes | yes |  |  |  | Gets or sets the related entity identifier. |
| RelatedEntityType |  | yes | yes |  |  | Gets or sets the type of the related entity. |
| RelatedEntityTypeId | yes | yes |  |  |  | Gets or sets the related entity type identifier. |
| Source | yes | yes |  |  |  | Gets or sets the campaign source. |
| SourceValueId | yes | yes |  |  |  | Gets or sets the UTM Source identifier. These values are associated with the Defined Type "UTM Source". |
| SupportedActions |  |  | yes |  |  |  |
| Term | yes | yes |  |  |  | Gets or sets the term(s). |
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
| InteractionComponent | Gets or sets the interaction component. |
| InteractionSession | Gets or sets the interaction component. |
| InteractionSourceDate | Gets or sets the interaction source date. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the person alias. |
| PersonalDevice | Gets or sets the personal device. |
| RelatedEntityType | Gets or sets the type of the related entity. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| EntityId | [CommunicationRecipient](communication-recipient.md) |  |
| EntityId | [Workflow](workflow.md) |  |
| InteractionComponentId | [InteractionComponent](interaction-component.md) |  |
| InteractionSessionId | [InteractionSession](interaction-session.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
