# History Login Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Security`
- Model title: `HistoryLogin`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `38`
- Obsolete methods: `4`
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
| Method signatures | 38 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

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
| PersonAlias |  |  | yes |  |  | Gets or sets the Person Alias that is associated with this login history. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the Id of the PersonAlias that is associated with this login history. |
| RelatedDataJson | yes | yes |  |  |  | Gets or sets any related data. DO NOT read from or write to this property directly. Instead, use the GetRelatedDataOrNull() and SetRelatedDataJson(Rock.Security.HistoryLoginRelatedData)() methods to ensure data is properly serialized and deserialized to and from this property. |
| SourceSite |  |  | yes |  |  | Gets or sets the Site that is associated with this login history. |
| SourceSiteId | yes | yes |  |  |  | Gets or sets the Id of the source Site that is associated with this login history. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| UserLogin |  |  | yes |  |  | Gets or sets the User Login that is associated with this login history. |
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
| PersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| SourceSite | [Site](site.md) | 7244c10b-5d87-467b-a7f5-12dc29910ca8 |
| SourceSiteId | [Site](site.md) | 7244c10b-5d87-467b-a7f5-12dc29910ca8 |
| UserLogin | [User Login](user-login.md) | 0fa592f1-728c-4885-be38-60ed6c0d834f |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
