# Interaction Session Location Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `InteractionSessionLocation`
- EntityType GUID: `790ec7ac-7443-466c-a07e-f702d86b9e1b`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 19 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 15 |
| Related model links | 3 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CountryCode | yes | yes |  |  |  | Gets or sets the country code. |
| CountryValue |  | yes | yes |  |  | Gets or sets the country value. |
| CountryValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the DefinedValue that represents the country. |
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
| GeoPoint | yes | yes |  |  |  | Gets or sets the GeoPoint (GeoLocation) for the session |
| Guid | yes | yes |  |  |  |  |
| ISP | yes | yes |  |  |  | Gets or sets the ISP. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InteractionSessionLocationAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| InteractionSessions |  | yes | yes |  |  | Gets or sets the Interactions for this session. |
| IpAddress | yes | yes |  |  |  | Gets or sets the IP address of the request. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Location | yes | yes |  |  |  | Gets or sets the location. |
| LookupDateTime | yes | yes |  |  |  | Gets or sets the lookup datetime. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PostalCode | yes | yes |  |  |  | Gets or sets the postal code. |
| RegionCode | yes | yes |  |  |  | Gets or sets the region code. |
| RegionValue |  | yes | yes |  |  | Gets or sets the region value. |
| RegionValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the DefinedValue that represents the region. |
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
| CountryValue | Gets or sets the country value. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| InteractionSessions | Gets or sets the Interactions for this session. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RegionValue | Gets or sets the region value. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| CountryValueId | [DefinedValue](defined-value.md) |  |
| InteractionSessions | Interactions |  |
| RegionValueId | [DefinedValue](defined-value.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
