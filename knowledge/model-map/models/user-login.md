# User Login Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `CRM`
- Model title: `UserLogin`
- EntityType GUID: `0fa592f1-728c-4885-be38-60ed6c0d834f`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 59 |
| Database-marked properties | 25 |
| Lava-marked properties | 42 |
| Lava-marked non-database properties | 18 |
| Related model links | 4 |
| Pre-alpha changes touching this model | 2 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| ApiKey | yes | yes |  |  |  | Gets or sets the API key associated with the UserLogin |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ConfirmationCode |  | yes | yes |  |  | Gets an encrypted confirmation code for the UserLogin. |
| ConfirmationCodeEncoded |  | yes | yes |  |  | Gets a URL encoded and encrypted confirmation code. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the EntityType for the authentication service that this UserLogin user. |
| EntityTypeId | yes | yes |  | yes |  | Gets or sets the EntityTypeId of the EntityType for the authentication service that this UserLogin user will use. |
| FailedPasswordAttemptCount | yes | yes |  |  |  | Gets or sets the number of failed password attempts within the failed password attempt window. |
| FailedPasswordAttemptWindowStartDateTime | yes | yes |  |  |  | Gets or sets the failed password attempt window start date time. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsAuthenticated |  | yes | yes |  |  | Gets a flag indicating if the User authenticated with their last interaction with Rock (versus using an impersonation link). |
| IsConfirmed | yes | yes |  |  |  | Gets or sets a flag indicating if the UserLogin has been confirmed. |
| IsLockedOut | yes | yes |  |  |  | Gets or sets a flag indicating if the UserLogin is currently locked out. |
| IsOnLine | yes | yes |  |  |  | Gets or sets a flag indicating if the user is currently online and logged in to the system. |
| IsPasswordChangeRequired | yes | yes |  |  |  | Gets or sets the is password change required. |
| IsPasswordless |  | yes | yes |  |  | Returns a boolean indicating if this is a passwordless user. |
| IsTwoFactorAuthenticated |  |  | yes |  |  | Gets a flag indicating if the User is two-factor authenticated. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastActivityDateTime | yes | yes |  |  |  | Gets or sets the date and time of the last activity (login, password change, etc.) performed with this UserLogin. |
| LastLockedOutDateTime | yes | yes |  |  |  | Gets or sets date and time that the UserLogin was last locked out. |
| LastLoginDateTime | yes | yes |  |  |  | Gets or sets the most recent date and time that a user successfully logged in using this UserLogin. |
| LastPasswordChangedDateTime | yes | yes |  |  |  | Gets or sets the date and time that the password was successfully changed. |
| LastPasswordExpirationWarningDateTime | yes | yes |  |  |  | Gets or sets the last time that user was notified about their password expiring. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Password | yes |  |  |  |  | Gets or sets the Password. Stored as a BCrypt hash for Rock Database Auth, but possibly a different hashtype for other ServiceTypes |
| Person |  | yes | yes |  |  | Gets or sets the Person that this UserLogin is associated with. |
| PersonId | yes | yes |  |  |  | Gets or sets the Id of the Person who this UserLogin belongs to. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| UserLoginAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| UserName | yes | yes |  | yes |  | Gets or sets the UserName that is associated with this UserLogin. This property is required. |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| ConfirmationCode | Gets an encrypted confirmation code for the UserLogin. |
| ConfirmationCodeEncoded | Gets a URL encoded and encrypted confirmation code. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the EntityType for the authentication service that this UserLogin user. |
| IdKey |  |
| IsAuthenticated | Gets a flag indicating if the User authenticated with their last interaction with Rock (versus using an impersonation link). |
| IsPasswordless | Returns a boolean indicating if this is a passwordless user. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Person | Gets or sets the Person that this UserLogin is associated with. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| EntityType | [EntityType](entity-type.md) |  |
| EntityTypeId | [EntityType](entity-type.md) |  |
| Person | [Person](person.md) |  |
| PersonId | [Person](person.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | ApiKeyPurpose |  |
| property_added | Description |  |
