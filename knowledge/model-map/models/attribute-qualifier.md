# Attribute Qualifier Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Core`
- Model title: `AttributeQualifier`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `15`
- Obsolete methods: `3`
- EntityType GUID: `ec7eb9ac-8b52-4a3d-8587-4a08050780cc`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 22 |
| Database-marked properties | 9 |
| Lava-marked properties | 15 |
| Lava-marked non-database properties | 6 |
| Related model links | 2 |
| Method signatures | 15 |
| Obsolete methods | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Attribute |  | yes | yes |  |  | Gets or sets the Attribute that uses this AttributeQualifier. |
| AttributeId | yes | yes |  | yes |  | Gets or sets the AttributeId of the Attribute that this AttributeQualifier limits the values of. |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if the AttributeQualifer is part of the Rock core system/framework. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Key | yes | yes |  | yes |  | Gets or sets the Key value that represents the type of qualifier that is being used. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| Value | yes | yes |  |  |  | Gets or sets the value of the AttributeQualifier |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Attribute | Gets or sets the Attribute that uses this AttributeQualifier. |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Attribute | [Attribute](attribute.md) | 5997c8d3-8840-4591-99a5-552919f90cbd |
| AttributeId | [Attribute](attribute.md) | 5997c8d3-8840-4591-99a5-552919f90cbd |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
