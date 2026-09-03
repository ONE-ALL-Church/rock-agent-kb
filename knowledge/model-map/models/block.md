# Block Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `CMS`
- Model title: `Block`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `d89555ca-9ae4-4d62-8af1-e5e463c1ef65`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 55 |
| Database-marked properties | 23 |
| Lava-marked properties | 40 |
| Lava-marked non-database properties | 17 |
| Related model links | 16 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettings | yes | yes |  |  |  | Gets or sets the additional settings. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BlockAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| BlockLocation |  | yes | yes |  |  | Gets the location where this Block is being implemented on (Page, Layout, or Site) This is a hard coded list of values defined in the code as an enumeration. |
| BlockType |  | yes | yes |  |  | Gets or sets the Block Type entity that this Block is implementing. |
| BlockTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Block Type that this Block is implementing. This property is required. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CssClass | yes | yes |  |  |  | Gets or sets an optional CSS class to include when the block's parent container is rendered |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Block was created by and is a part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Layout |  | yes | yes |  |  | Gets or sets the Layout entity that this Block is implemented on. This property will be null if this Block is being implemented on as part of a Page or Site. |
| LayoutId | yes | yes |  |  |  | Gets or sets the Id of the Layout that this Block is implemented on. This property will only be populated if the Block is implemented on a Layout. Blocks that have a specific LayoutId will be shown on all pages on a site that have the specified LayoutId |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets a user defined name of the block implementation. This property is required. |
| Order | yes | yes |  | yes |  | Gets or sets the order that this Block appears in the Page/Layout zone that the Block is implemented in. Blocks are displayed/rendered in Ascending (1,2,3,...) order. The lower the number the higher in the Zone the Block will appear. Page Blocks have priority over layout Blocks, so they will appear higher in the Zone than Site/Layout Blocks. This property is required |
| OutputCacheDuration | yes | yes |  | yes |  | Gets or sets the length of time (in minutes) that the Block's data is cached. This property is required. |
| Page |  | yes | yes |  |  | Gets or sets the Page entity that this Block is implemented on. This property will be null if this Block is being implemented on as part of a Layout or Site. |
| PageId | yes | yes |  |  |  | Gets or sets the Id of the Page that this Block is implemented on. This property will only be populated if the Block is implemented on a Page. Blocks that have a specific PageId will only be shown in the specified Page |
| ParentAuthority |  |  | yes |  |  | Gets the securable object that security permissions should be inherited from based on BlockLocation (Page, Layout, or Site) |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PostHtml | yes | yes |  |  |  | Gets or sets any HTML to be rendered after the block |
| PreHtml | yes | yes |  |  |  | Gets or sets any HTML to be rendered before the block |
| Role | yes | yes |  |  |  | The role that has been assigned to this Block. This will override the BlockType's default role. This is a hard coded list of values defined in the code as an enumeration. |
| Site |  | yes | yes |  |  | Gets or sets the Site entity that this Block is implemented on. This property will be null if this Block is being implemented on as part of a Page or Layout. |
| SiteId | yes | yes |  |  |  | Gets or sets the Id of the Site that this Block is implemented on. This property will only be populated if the Block is implemented on a Site. Blocks that have a specific SiteId will be shown on all pages on a site |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| Zone | yes | yes |  | yes |  | Gets or sets the name of the layout zone/section that this Block is being implemented on. This property is required. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| BlockLocation | Gets the location where this Block is being implemented on (Page, Layout, or Site) This is a hard coded list of values defined in the code as an enumeration. |
| BlockType | Gets or sets the Block Type entity that this Block is implementing. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| Layout | Gets or sets the Layout entity that this Block is implemented on. This property will be null if this Block is being implemented on as part of a Page or Site. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Page | Gets or sets the Page entity that this Block is implemented on. This property will be null if this Block is being implemented on as part of a Layout or Site. |
| Site | Gets or sets the Site entity that this Block is implemented on. This property will be null if this Block is being implemented on as part of a Page or Layout. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| BlockType | [Block Type](block-type.md) | 04768edf-c0cd-4950-b629-4d2370b57c99 |
| BlockTypeId | [Block Type](block-type.md) | 04768edf-c0cd-4950-b629-4d2370b57c99 |
| Layout | [Layout](layout.md) | 9dacc861-fed4-47fc-946d-d6a120ff6d56 |
| Layout | [Page](page.md) | e104dcdf-247c-4ced-a119-8cc51632761f |
| Layout | [Site](site.md) | 7244c10b-5d87-467b-a7f5-12dc29910ca8 |
| LayoutId | [Layout](layout.md) | 9dacc861-fed4-47fc-946d-d6a120ff6d56 |
| Order | [Page](page.md) | e104dcdf-247c-4ced-a119-8cc51632761f |
| Order | [Site](site.md) | 7244c10b-5d87-467b-a7f5-12dc29910ca8 |
| Page | [Layout](layout.md) | 9dacc861-fed4-47fc-946d-d6a120ff6d56 |
| Page | [Page](page.md) | e104dcdf-247c-4ced-a119-8cc51632761f |
| Page | [Site](site.md) | 7244c10b-5d87-467b-a7f5-12dc29910ca8 |
| PageId | [Page](page.md) | e104dcdf-247c-4ced-a119-8cc51632761f |
| Site | [Layout](layout.md) | 9dacc861-fed4-47fc-946d-d6a120ff6d56 |
| Site | [Page](page.md) | e104dcdf-247c-4ced-a119-8cc51632761f |
| Site | [Site](site.md) | 7244c10b-5d87-467b-a7f5-12dc29910ca8 |
| SiteId | [Site](site.md) | 7244c10b-5d87-467b-a7f5-12dc29910ca8 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
