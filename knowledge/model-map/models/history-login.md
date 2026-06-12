# History Login Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Security`
- Model title: `HistoryLogin`
- EntityType GUID: `b0c039e1-d2b0-460a-a787-83565bcb665c`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 52 |
| Database-marked properties | 22 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 12 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AuthClientClientId | yes | yes |  |  |  | Gets or sets the client identifier for the authorization client that is associated with this login history. |
| AvailableKeys |  |  | yes |  |  |  |
| ClientIpAddress | yes | yes |  |  |  | Gets or sets the client IP address from which this login history originated. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DestinationUrl | yes | yes |  |  |  | Gets or sets the destination URL. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExternalSource | yes | yes |  |  |  | Gets or sets the name of the external source that is associated with this login history. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HistoryLoginAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LoginAttemptDateTime | yes | yes |  |  |  | Gets or sets the login attempt date time. |
| LoginFailureMessage | yes | yes |  |  |  | Gets or sets the login failure message, if login was unsuccessful. |
| LoginFailureReason | yes | yes |  |  |  | Gets or sets the login failure reason, if login was unsuccessful. This is a hard coded list of values defined in the code as an enumeration. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  |  | yes |  |  | Gets or sets the PersonAlias that is associated with this login history. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the Id of the PersonAlias that is associated with this login history. |
| RelatedDataJson | yes | yes |  |  |  | Gets or sets any related data. DO NOT read from or write to this property directly. Instead, use the and methods to ensure data is properly serialized and deserialized to and from this property. |
| SourceSite |  |  | yes |  |  | Gets or sets the Site that is associated with this login history. |
| SourceSiteId | yes | yes |  |  |  | Gets or sets the Id of the source Site that is associated with this login history. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| UserLogin |  |  | yes |  |  | Gets or sets the UserLogin that is associated with this login history. |
| UserLoginId | yes | yes |  |  |  | Gets or sets the Id of the UserLogin that is associated with this login history. |
| UserName | yes | yes |  |  |  | Gets or sets the UserName. |
| ValidationResults |  |  | yes |  |  |  |
| WasLoginSuccessful | yes | yes |  |  |  | Gets or sets a flag indicating if the login was successful. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
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
| PersonAlias | [PersonAlias](person-alias.md) |  |
| SourceSite | [Site](site.md) |  |
| SourceSiteId | [Site](site.md) |  |
| UserLogin | [UserLogin](user-login.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | RelatedDataJson | description |
