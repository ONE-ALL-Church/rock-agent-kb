# Lava Endpoint Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `CMS`
- Model title: `LavaEndpoint`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `38`
- Obsolete methods: `4`
- EntityType GUID: `f1bbf7d4-cafd-450d-a89a-b3312c9738a2`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 52 |
| Database-marked properties | 23 |
| Lava-marked properties | 36 |
| Lava-marked non-database properties | 13 |
| Related model links | 2 |
| Method signatures | 38 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  | Gets or sets the additional settings json. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CacheControlHeader |  |  | yes |  |  | Gets the cache control header. |
| CacheControlHeaderSettings | yes | yes |  |  |  | Gets or sets a cache control settings. |
| CodeTemplate | yes | yes |  |  |  | Gets or sets the code template. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description. |
| EnabledLavaCommands | yes | yes |  |  |  | Gets or sets a comma-delimited list of enabled LavaCommands |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HttpMethod | yes | yes |  |  |  | Gets or sets the http method. This is a hard coded list of values defined in the code as an enumeration. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is active. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this endpoint is a part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LavaApplication |  | yes | yes |  |  | Gets or sets the Lava Application. |
| LavaApplicationId | yes | yes |  | yes |  | Gets or sets the Id of the Lava Application lava application that is associated with this end point. |
| LavaEndpointAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority where security authorizations are being inherited from. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RateLimitPeriodDurationSeconds | yes | yes |  |  |  | Gets or sets the rate limit period in seconds. |
| RateLimitRequestPerPeriod | yes | yes |  |  |  | Gets or sets the rate limit requests per period. |
| SecurityMode | yes | yes |  |  |  | Gets or sets the security mode. This is a hard coded list of values defined in the code as an enumeration. |
| Slug | yes | yes |  |  |  | Gets or sets the slug. |
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
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| LavaApplication | Gets or sets the Lava Application. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| LavaApplication | [Lava Application](lava-application.md) | fffe0de1-b410-435e-9aa8-3a0b18aaf0f7 |
| LavaApplicationId | [Lava Application](lava-application.md) | fffe0de1-b410-435e-9aa8-3a0b18aaf0f7 |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | LavaApplicationId | is_qualifier |
