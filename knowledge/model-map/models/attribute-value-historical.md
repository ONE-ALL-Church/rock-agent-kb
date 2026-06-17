# Attribute Value Historical Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Core`
- Model title: `AttributeValueHistorical`
- EntityType GUID: `d940aa57-d977-4b75-b4be-7c2eb40b26a4`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 47 |
| Database-marked properties | 19 |
| Lava-marked properties | 32 |
| Lava-marked non-database properties | 13 |
| Related model links | 2 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValue |  | yes | yes |  |  | Gets or sets the AttributeValue Attribute Value that this AttributeValueHistorical provides a historical value for. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValueHistoricalAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| AttributeValueId | yes | yes |  | yes |  | Gets or sets the AttributeValueId of the Attribute Value that this AttributeValueHistorical provides a historical value for. |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CurrentRowIndicator | yes | yes |  |  |  | Gets or sets a value indicating whether [current row indicator]. This will be True if this represents the same values as the current tracked record for this |
| CustomSortValue |  |  | yes |  |  |  |
| EffectiveDateTime | yes | yes |  |  |  | Gets or sets the effective date. This is the starting date that the tracked record had the values reflected in this record |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExpireDateTime | yes | yes |  |  |  | Gets or sets the expire date time This is the last date that the tracked record had the values reflected in this record For example, if a tracked record's Name property changed on '2016-07-14', the ExpireDate of the previously current record will be '2016-07-13', and the EffectiveDate of the current record will be '2016-07-14' If this is most current record, the ExpireDate will be '9999-01-01' |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
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
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| Value | yes | yes |  |  |  | Gets or sets the value of the AttributeValue at this point in history |
| ValueAsBoolean | yes | yes |  |  |  | Gets or sets the value as boolean at this point in history |
| ValueAsDateTime | yes | yes |  |  |  | Gets or sets the value as date time at this point in history |
| ValueAsNumeric | yes | yes |  |  |  | Gets or sets the value as numeric at this point in history |
| ValueAsPersonId | yes | yes |  |  |  | Gets or sets the value as person identifier. |
| ValueFormatted | yes | yes |  |  |  | Gets or sets the formatted value of the AttributeValue at this point in history |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValue | Gets or sets the AttributeValue Attribute Value that this AttributeValueHistorical provides a historical value for. |
| AttributeValues |  |
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

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AttributeValue | [Attribute Value](attribute-value.md) | d2bdccf0-d3f4-4f29-b286-da5b7bfa41c6 |
| AttributeValueId | [Attribute Value](attribute-value.md) | d2bdccf0-d3f4-4f29-b286-da5b7bfa41c6 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
