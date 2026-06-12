# Html Content Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `CMS`
- Model title: `HtmlContent`
- EntityType GUID: `fb30ec4c-7dcc-41a4-94ab-e728a8ce537b`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 47 |
| Database-marked properties | 18 |
| Lava-marked properties | 32 |
| Lava-marked non-database properties | 14 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| ApprovedByPersonAlias |  | yes | yes |  |  | Gets or sets the approved by PersonAlias. |
| ApprovedByPersonAliasId | yes | yes |  |  |  | Gets or sets the Id of the Person who approved the HTMLContent. |
| ApprovedDateTime | yes | yes |  |  |  | Gets or sets the date and time that the HTMLContent was approved. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Block |  | yes | yes |  |  | Gets or sets the Block that this HTMLContent appears on. |
| BlockId | yes | yes |  | yes |  | Gets or sets the Id of the Block that the HTML content should appear on. This property is required. |
| Content | yes | yes |  |  |  | Gets or sets the HTML content that will display on the block when conditions (if any) are met. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityValue | yes | yes |  |  |  | Gets or sets the Entity Value that must be present on the page for this HTML Content to be displayed. If this value will null there will not be an entity restriction on the HTMLContent object. |
| ExpireDateTime | yes | yes |  |  |  | Gets or sets the date and time that the HTMLContent expires and is no longer available. If this value is null the HTMLContent remains available until it is overwritten or replaced with a new version. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HtmlContentAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsApproved | yes | yes |  | yes |  | Gets or sets a flag indicating if the content has been approved. If approval is required, the content will not be displayed until it has been approved. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| StartDateTime | yes | yes |  |  |  | Gets or sets the date and time that the HTMLContent becomes active and available to be displayed on the web. If a date and time is provided, the HTMLContent will not be available until then; if null the HTMLContent will be available immediately. Please note that the start date is overridden by the approval status, if the HTMLContent is subject to approval, it will not be displayed until it is approved. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| Version | yes | yes |  | yes |  | Gets or sets the version number for the HTMLContent |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ApprovedByPersonAlias | Gets or sets the approved by PersonAlias. |
| AttributeValues |  |
| Attributes |  |
| Block | Gets or sets the Block that this HTMLContent appears on. |
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
| ApprovedByPersonAlias | [PersonAlias](person-alias.md) |  |
| ApprovedByPersonAliasId | [Person](person.md) |  |
| Block | [Block](block.md) |  |
| BlockId | [Block](block.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | BlockId | description, is_required |
