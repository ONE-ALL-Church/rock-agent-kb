# Layout Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `CMS`
- Model title: `Layout`
- EntityType GUID: `9dacc861-fed4-47fc-946d-d6a120ff6d56`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 46 |
| Database-marked properties | 16 |
| Lava-marked properties | 31 |
| Lava-marked non-database properties | 15 |
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
| Blocks |  | yes | yes |  |  | Gets or sets the collection of Blocks that are used on the layout. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the user defined description of the Layout. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FileName | yes | yes |  | yes |  | Gets or sets the file name portion of the associated .Net ASCX UserControl that provides the HTML Markup and code for this Layout. Value should not include the extension. And the path is relative to the theme folder. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Layout was created by and is a part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LayoutAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| LayoutMobilePhone | yes | yes |  |  |  | Gets or sets the layout mobile phone. |
| LayoutMobileTablet | yes | yes |  |  |  | Gets or sets the layout mobile tablet. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the logical name of the Layout. |
| Pages |  | yes | yes |  |  | Gets or sets a collection of Pages that are using this Layout. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority for the layout. Layout security is automatically inherited from the site. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Site |  | yes | yes |  |  | Gets or sets the Site that this Layout Block is associated with. |
| SiteId | yes | yes |  |  |  | Gets or sets the Id of the Site that this layout is associated with. |
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
| Blocks | Gets or sets the collection of Blocks that are used on the layout. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Pages | Gets or sets a collection of Pages that are using this Layout. |
| Site | Gets or sets the Site that this Layout Block is associated with. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Blocks | Blocks | d89555ca-9ae4-4d62-8af1-e5e463c1ef65 |
| Pages | Pages | e104dcdf-247c-4ced-a119-8cc51632761f |
| Site | [Site](site.md) | 7244c10b-5d87-467b-a7f5-12dc29910ca8 |
| SiteId | [Site](site.md) | 7244c10b-5d87-467b-a7f5-12dc29910ca8 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
