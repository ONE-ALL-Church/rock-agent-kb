# Content Channel Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `CMS`
- Model title: `ContentChannel`
- EntityType GUID: `44484685-477e-4668-89a6-84f29739eb68`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 65 |
| Database-marked properties | 29 |
| Lava-marked properties | 47 |
| Lava-marked non-database properties | 18 |
| Related model links | 6 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Categories |  | yes | yes |  |  | Gets or sets the collection of Categories that this Content Channel is associated with. NOTE: Since changes to Categories isn't tracked by ChangeTracker, set the ModifiedDateTime if Categories are modified. |
| ChannelUrl | yes | yes |  |  |  | Gets or sets the channel URL. |
| ChildContentChannels |  | yes | yes |  |  | Gets or sets the collection of ContentChannels that this ContentChannel allows as children. |
| ChildItemsManuallyOrdered | yes | yes |  |  |  | Gets or sets a value indicating whether child items are manually ordered or not |
| ContentChannelAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ContentChannelType |  | yes | yes |  |  | Gets or sets the type of the content channel. |
| ContentChannelTypeId | yes | yes |  |  |  | Gets or sets the Content Channel Type identifier. |
| ContentControlType | yes | yes |  |  |  | Gets or sets the type of the control to render when editing content for items of this type. This is a hard coded list of values defined in the code as an enumeration. |
| ContentLibraryConfiguration |  |  | yes |  |  | Gets or sets the content library configuration. |
| ContentLibraryConfigurationJson | yes | yes |  |  |  | Gets or sets the Content Library configuration JSON. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description. |
| EnablePersonalization | yes | yes |  |  |  | Gets or sets a value indicating whether [enable personalization]. |
| EnableRss | yes | yes |  |  |  | Gets or sets a value indicating whether [enable RSS]. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsContentLibraryEnabled |  |  | yes |  |  | Gets a value indicating whether the content library is enabled for this content channel. |
| IsIndexEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is index enabled. |
| IsStructuredContent | yes | yes |  |  |  | Gets or sets a value indicating whether this content is structured. |
| IsTaggingEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is tagging enabled. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ItemTagCategory |  | yes | yes |  |  | Gets or sets the item tag Category. |
| ItemTagCategoryId | yes | yes |  |  |  | Gets or sets the item tag category identifier. |
| ItemUrl | yes | yes |  |  |  | Gets or sets the item URL. |
| Items |  | yes | yes |  |  | Gets or sets the items. |
| ItemsManuallyOrdered | yes | yes |  |  |  | Gets or sets a value indicating whether items are manually ordered or not |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ParentContentChannels |  |  | yes |  |  | Gets or sets a collection containing the ContentChannels that allow this ContentChannel as a child. |
| RequiresApproval | yes | yes |  |  |  | Gets or sets a value indicating whether [requires approval]. |
| RootImageDirectory | yes | yes |  |  |  | Gets or sets the root image directory to use when the HTML control type is used |
| StructuredContentToolValue |  | yes | yes |  |  | Gets or sets the Defined Value representing the content channel's structure content tool. |
| StructuredContentToolValueId | yes | yes |  |  |  | Gets or sets the Structure Content Tool Id. These are found in the Structured Content Editor Tools Defined Type. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TimeToLive | yes | yes |  |  |  | Gets or sets the number of minutes a feed can stay cached before refreshing it from the source. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Categories | Gets or sets the collection of Categories that this Content Channel is associated with. NOTE: Since changes to Categories isn't tracked by ChangeTracker, set the ModifiedDateTime if Categories are modified. |
| ChildContentChannels | Gets or sets the collection of ContentChannels that this ContentChannel allows as children. |
| ContentChannelType | Gets or sets the type of the content channel. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ItemTagCategory | Gets or sets the item tag Category. |
| Items | Gets or sets the items. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| StructuredContentToolValue | Gets or sets the Defined Value representing the content channel's structure content tool. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Categories | Categories | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| ContentChannelType | type | d5992f79-7fb8-49ff-82ab-e8cb2cec1e74 |
| ContentChannelTypeId | [Content Channel Type](content-channel-type.md) | d5992f79-7fb8-49ff-82ab-e8cb2cec1e74 |
| ItemTagCategory | [Category](category.md) | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| Items | items | bf12ae64-21fb-433b-a8a4-e40e8c426dda |
| StructuredContentToolValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | StructuredContentToolValueId | enum_values |
