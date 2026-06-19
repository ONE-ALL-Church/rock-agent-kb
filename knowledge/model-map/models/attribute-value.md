# Attribute Value Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `AttributeValue`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `d2bdccf0-d3f4-4f29-b286-da5b7bfa41c6`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 55 |
| Database-marked properties | 23 |
| Lava-marked properties | 41 |
| Lava-marked non-database properties | 18 |
| Related model links | 5 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Attribute |  | yes | yes |  |  | Gets or sets the Attribute that uses this AttributeValue. |
| AttributeId | yes | yes |  | yes |  | Gets or sets the AttributeId of the Attribute that this AttributeValue provides a value for. |
| AttributeIsGridColumn |  | yes | yes |  |  | Gets a value indicating whether attribute is grid column. |
| AttributeKey |  | yes | yes |  |  | Gets the attribute key. |
| AttributeName |  | yes | yes |  |  | Gets the name of the attribute |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| AttributeValuesHistorical |  | yes | yes |  |  | Gets or sets the a list of previous values that this attribute value had (If Attribute.EnableHistory is enabled) |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityId | yes | yes |  |  |  | Gets or sets the Id of the entity instance that uses this AttributeValue. An Attribute is a configuration setting, so each instance of the Entity that uses the same Attribute can have a different value. For instance a Block Type has a declared attribute, and that attribute can be configured with a different value on each Block that implements the Block Type. This value will either be 0 or null for global attributes or attributes that have a constant across all instances of an EntityType. |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsPersistedValueDirty | yes | yes |  |  |  | Gets or sets a value indicating whether the persisted values are considered dirty. If the values are dirty then it should be assumed that they are not in sync with the Value property. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this AttributeValue is part of the Rock core system/framework. |
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
| PersistedCondensedHtmlValue | yes | yes |  |  |  | Gets or sets the persisted condensed HTML value. |
| PersistedCondensedTextValue | yes | yes |  |  |  | Gets or sets the persisted condensed text value. |
| PersistedHtmlValue | yes | yes |  |  |  | Gets or sets the persisted HTML value. |
| PersistedTextValue | yes | yes |  |  |  | Gets or sets the persisted text value. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| Value | yes | yes |  |  |  | Gets or sets the raw value |
| ValueAsBoolean | yes | yes |  |  |  | Gets the value as a boolean. This value is only updated on save. |
| ValueAsDateTime | yes | yes |  |  |  | Gets the Value as a DateTime. This value is only updated on save. |
| ValueAsNumeric | yes | yes |  |  |  | Gets the Value as a decimal. This value is only updated on save. |
| ValueAsPersonId | yes | yes |  |  |  | Gets the Value as a PersonId. This value is only updated on save. |
| ValueChecksum | yes | yes |  |  |  | Gets the value checksum. This is a hash of Value that is automatically calculated by the database. |
| ValueFormatted |  | yes | yes |  |  | Gets the value formatted. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Attribute | Gets or sets the Attribute that uses this AttributeValue. |
| AttributeIsGridColumn | Gets a value indicating whether attribute is grid column. |
| AttributeKey | Gets the attribute key. |
| AttributeName | Gets the name of the attribute |
| AttributeValues |  |
| AttributeValuesHistorical | Gets or sets the a list of previous values that this attribute value had (If Attribute.EnableHistory is enabled) |
| Attributes |  |
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
| ValueFormatted | Gets the value formatted. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Attribute | [Attribute](attribute.md) | 5997c8d3-8840-4591-99a5-552919f90cbd |
| AttributeId | [Attribute](attribute.md) | 5997c8d3-8840-4591-99a5-552919f90cbd |
| EntityId | [Attribute](attribute.md) | 5997c8d3-8840-4591-99a5-552919f90cbd |
| EntityId | [Block](block.md) | d89555ca-9ae4-4d62-8af1-e5e463c1ef65 |
| EntityId | [Block Type](block-type.md) | 04768edf-c0cd-4950-b629-4d2370b57c99 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
