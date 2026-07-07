# Lava Shortcode Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `CMS`
- Model title: `LavaShortcode`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `7574a473-3326-4973-8df6-c7bf5f64eb36`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 48 |
| Database-marked properties | 20 |
| Lava-marked properties | 31 |
| Lava-marked non-database properties | 13 |
| Related model links | 2 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Categories |  | yes | yes |  |  | Gets or sets the collection of Categories that this Lava Shortcode is associated with. NOTE: Since changes to Categories isn't tracked by ChangeTracker, set the ModifiedDateTime if Categories are modified. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the Description of the Lava Shortcode. |
| Documentation | yes | yes |  |  |  | Gets or sets the documentation. This serves as the technical description of the internals of the shortcode. |
| EnabledLavaCommands | yes |  |  |  |  | Gets or sets a comma-delimited list of enabled LavaCommands |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  | yes |  | Gets or sets a value indicating whether this instance is active. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a value indicating whether this instance is system. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LavaShortcodeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Markup | yes | yes |  | yes |  | Gets or sets the token. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the public name of the shortcode. |
| Parameters | yes |  |  |  |  | Gets or sets the parameters. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ShortcodeScopeBehavior | yes | yes |  | yes |  | Gets or sets how variables defined within this shortcode are scoped. This is a hard coded list of values defined in the code as an enumeration. |
| SupportedActions |  |  | yes |  |  |  |
| TagName | yes | yes |  | yes |  | Gets or sets the name of the tag. |
| TagType | yes | yes |  | yes |  | Gets or sets the type of the tag (inline or block). A tag type of block requires an end tag. This is a hard coded list of values defined in the code as an enumeration. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Categories | Gets or sets the collection of Categories that this Lava Shortcode is associated with. NOTE: Since changes to Categories isn't tracked by ChangeTracker, set the ModifiedDateTime if Categories are modified. |
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
| Categories | Categories | 1d68154e-ec76-44c8-9813-7736b27aecf9 |
| Categories | [Lava Shortcode](lava-shortcode.md) | 7574a473-3326-4973-8df6-c7bf5f64eb36 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
