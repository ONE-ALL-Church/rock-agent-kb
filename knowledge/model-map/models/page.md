# Page Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `CMS`
- Model title: `Page`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `37`
- Obsolete methods: `4`
- EntityType GUID: `e104dcdf-247c-4ced-a119-8cc51632761f`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 83 |
| Database-marked properties | 45 |
| Lava-marked properties | 66 |
| Lava-marked non-database properties | 21 |
| Related model links | 8 |
| Method signatures | 37 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettings | yes | yes |  |  | yes | Gets or sets the additional settings. |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AllowIndexing | yes | yes |  |  |  | Gets or sets a value indicating whether [allow indexing]. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Blocks |  | yes | yes |  |  | Gets or sets the collection of Blocks that are used on the page. |
| BodyCssClass | yes | yes |  |  |  | Gets or sets the body CSS class. |
| BotGuardianLevel | yes | yes |  |  |  | Gets or sets the Bot Guardian Level for the Page. This is a hard coded list of values defined in the code as an enumeration. |
| BreadCrumbDisplayIcon | yes | yes |  |  |  | Gets or sets a value indicating whether icon is displayed in breadcrumb. |
| BreadCrumbDisplayName | yes | yes |  |  |  | Gets or sets a value indicating whether the Page Name is displayed in the breadcrumb. |
| BrowserTitle | yes | yes |  |  |  | Gets or sets the browser title to use for the page. |
| CacheControlHeader |  |  | yes |  |  | Gets the cache control header. This shouldn't be used to set the properties directly but the json version should be used to set the CacheControlHeaderSettings property. |
| CacheControlHeaderSettings | yes | yes |  |  |  | Gets or sets the cache control header settings. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets a user defined description of the page. This will be added as a meta tag for the page |
| DisplayInNavWhen | yes | yes |  | yes |  | Gets or sets a value indicating when the Page should be displayed in the navigation. This is a hard coded list of values defined in the code as an enumeration. |
| EnableViewState | yes | yes |  |  |  | Gets or sets a flag indicating if view state should be enabled on the page. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HeaderContent | yes | yes |  |  |  | Gets or sets HTML content to add to the page header area of the page when rendered. |
| IconBinaryFile |  | yes | yes |  |  | Gets or sets the icon Binary File. |
| IconBinaryFileId | yes | yes |  |  |  | Gets or sets the icon binary file identifier. |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class name for a font vector based icon. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IncludeAdminFooter | yes | yes |  | yes |  | Gets or sets a flag indicating if the admin footer should be displayed when a Site Administrator is logged in. |
| InternalName | yes | yes |  | yes |  | Gets or sets the internal name to use when administering this page |
| IsRateLimited |  | yes | yes |  |  | Gets a value indicating whether this instance is rate limited. |
| IsSystem | yes | yes |  |  |  | Gets or sets a flag indicating if the Page is part of the Rock core system/framework. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| KeyWords | yes | yes |  |  |  | Gets or sets the key words. |
| Layout |  | yes | yes |  |  | Gets or sets the Layout that the pages uses. |
| LayoutId | yes | yes |  |  |  | Gets or sets the Id of the Layout that this Page uses. |
| MedianPageLoadTimeDurationSeconds | yes | yes |  |  |  | Gets or sets the median page load time in seconds. Typically calculated from a set of Interaction.InteractionTimeToServe values. |
| MenuDisplayChildPages | yes | yes |  | yes |  | Gets or sets a flag indicating if the Page's children Pages should be displayed in the menu. |
| MenuDisplayDescription | yes | yes |  | yes |  | Gets or sets a flag indicating if the Page description should be displayed in the menu. |
| MenuDisplayIcon | yes | yes |  | yes |  | Gets or sets a flag indicating if the Page icon should be displayed in the menu. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Order | yes | yes |  | yes |  | Gets or sets a number indicating the order of the page in the menu and in the site map. This will also affect the page order in the menu. This property is required. |
| OutputCacheDuration | yes | yes |  |  | yes | Gets or sets a value indicating the length of time (in seconds) in that rendered output is cached. This property is required. |
| PageAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| PageContexts |  | yes | yes |  |  | Gets or sets a collection of Page Context entities that are used on this page. |
| PageDisplayBreadCrumb | yes | yes |  |  |  | Gets or sets a flag indicating whether breadcrumbs are displayed on Page |
| PageDisplayDescription | yes | yes |  |  |  | Gets or sets a value indicating whether the Page description should be displayed on the page. |
| PageDisplayIcon | yes | yes |  |  |  | Gets or sets a value indicating whether the Page icon should be displayed on the Page. |
| PageDisplayTitle | yes | yes |  |  |  | Gets or sets a value indicating whether the Page Title should be displayed on the page (if the Layout supports it). |
| PageRoutes |  | yes | yes |  |  | Gets or sets the PageRoutes that reference this page. |
| PageTitle | yes | yes |  |  |  | Gets or sets the title of the of the Page to use as the page caption, in menu's, breadcrumb display etc. |
| Pages |  | yes | yes |  |  | Gets or sets the collection of the current page's child pages. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority for the page. Page security is automatically inherited from the parent page, unless explicitly overridden. If there is no parent page, it is inherited from the site (through the layout) |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ParentPage |  | yes | yes |  |  | Gets or sets the Page entity for the parent page. |
| ParentPageId | yes | yes |  |  |  | Gets or sets the Id of the parent Page. |
| RateLimitPeriod |  |  | yes |  | yes | Gets or sets the rate limit period (in seconds). |
| RateLimitPeriodDurationSeconds | yes | yes |  |  |  | Gets or sets the rate limit period (in seconds). |
| RateLimitRequestPerPeriod | yes | yes |  |  |  | Gets or sets the rate limit request per period. |
| RequiresEncryption | yes | yes |  |  |  | Gets or sets a flag that indicates if the Page requires SSL encryption. |
| Site |  | yes | yes |  |  | Gets or sets the Site that the pages uses. |
| SiteId | yes | yes |  |  |  | Gets the site identifier of the Page's Layout. NOTE: This is needed so that Page Attributes qualified by SiteId work. |
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
| Blocks | Gets or sets the collection of Blocks that are used on the page. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IconBinaryFile | Gets or sets the icon Binary File. |
| IdKey |  |
| IsRateLimited | Gets a value indicating whether this instance is rate limited. |
| Layout | Gets or sets the Layout that the pages uses. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PageContexts | Gets or sets a collection of Page Context entities that are used on this page. |
| PageRoutes | Gets or sets the PageRoutes that reference this page. |
| Pages | Gets or sets the collection of the current page's child pages. |
| ParentPage | Gets or sets the Page entity for the parent page. |
| Site | Gets or sets the Site that the pages uses. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Blocks | Blocks | d89555ca-9ae4-4d62-8af1-e5e463c1ef65 |
| IconBinaryFile | [Binary File](binary-file.md) | 9bb1a349-5998-47c1-97d5-d6cc00275662 |
| Layout | [Layout](layout.md) | 9dacc861-fed4-47fc-946d-d6a120ff6d56 |
| LayoutId | [Layout](layout.md) | 9dacc861-fed4-47fc-946d-d6a120ff6d56 |
| PageContexts | [Page Context](page-context.md) | 5c56b915-8a8b-4747-9d84-ebaf0bacc9a1 |
| PageDisplayTitle | [Layout](layout.md) | 9dacc861-fed4-47fc-946d-d6a120ff6d56 |
| PageRoutes | PageRoutes | 42c14361-67b2-472c-95be-ea8a9c511837 |
| Site | [Site](site.md) | 7244c10b-5d87-467b-a7f5-12dc29910ca8 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
