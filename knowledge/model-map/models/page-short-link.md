# Page Short Link Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `CMS`
- Model title: `PageShortLink`
- EntityType GUID: `83d8c6df-1d53-438b-93b2-75a2038bbee6`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 47 |
| Database-marked properties | 16 |
| Lava-marked properties | 31 |
| Lava-marked non-database properties | 15 |
| Related model links | 2 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Category |  | yes | yes |  |  | Gets or sets the category this short link is for. Categories are used for reporting purposes only. They do not affect the ability to use a short link. |
| CategoryId | yes | yes |  |  |  | Gets or sets the identifier of the category this short link is for. Categories are used for reporting purposes only. They do not affect the ability to use a short link. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsPinned | yes | yes |  |  |  | Gets or sets a value indicating whether the short link is pinned. |
| IsScheduled | yes | yes |  |  |  | Gets a flag that determines if this short link has schedules enabled. When true , the schedule details will be contained in the additional settings. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| PageShortLinkAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ShortLinkUrl |  | yes | yes |  |  | Gets the short link URL. |
| Site |  | yes | yes |  |  | Gets or sets the Site that is associated with this PageShortLink. |
| SiteId | yes | yes |  | yes |  | Gets or sets the Id of the Site that this PageShortLink references. This property is required. |
| SupportedActions |  |  | yes |  |  |  |
| Token | yes | yes |  | yes |  | Gets or sets the token. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| Url | yes | yes |  | yes |  | Gets or sets the URL. |
| UrlEncodedKey |  | yes | yes |  |  |  |
| UrlWithUtm |  |  | yes |  |  | Gets the URL, including query parameters for UTM values. |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the category this short link is for. Categories are used for reporting purposes only. They do not affect the ability to use a short link. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ShortLinkUrl | Gets the short link URL. |
| Site | Gets or sets the Site that is associated with this PageShortLink. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Site | [Site](site.md) |  |
| SiteId | [Site](site.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | ExpireDate |  |
