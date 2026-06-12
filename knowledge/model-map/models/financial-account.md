# Financial Account Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Finance`
- Model title: `FinancialAccount`
- EntityType GUID: `798bce48-6aa7-4983-9214-f9bcefb4521d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 59 |
| Database-marked properties | 27 |
| Lava-marked properties | 44 |
| Lava-marked non-database properties | 17 |
| Related model links | 5 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AccountTypeValue |  | yes | yes |  |  | Gets or sets the Account Type DefinedValue for this FinancialAccount. |
| AccountTypeValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the DefinedValue that represents the FinancialAccountType for this FinancialAccount. These are found in the "Account Type" Defined Type. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Campus |  | yes | yes |  |  | Gets or sets the Campus that this FinancialAccount is associated with. |
| CampusId | yes | yes |  |  |  | Gets or sets the CampusId of the Campus that this FinancialAccount is associated with. If this FinancialAccount is not associated with a Campus this property will be null. |
| ChildAccounts |  | yes | yes |  |  | Gets or sets a collection containing the FinancialAccounts that are sub accounts/child accounts of this account. This is not a recursive search. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the user defined description of the FinancialAccount. |
| EncryptedKey |  |  | yes |  |  |  |
| EndDate | yes | yes |  |  |  | Gets or sets the closing/end date for this FinancialAccount. This is the last day that transactions can be posted to this account. If there is not a end date for this account, transactions can be posted for an indefinite period of time. Ongoing FinancialAccounts will not have an end date. |
| EntityStringValue |  | yes | yes |  |  |  |
| FinancialAccountAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GlCode | yes | yes |  |  |  | Gets or sets the General Ledger account code for this FinancialAccount. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| ImageBinaryFile |  | yes | yes |  |  | Gets or sets the Image that can be used when displaying this Financial Account |
| ImageBinaryFileId | yes | yes |  |  |  | Gets or sets the Image Id that can be used when displaying this Financial Account |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating if this FinancialAccount is active. |
| IsPublic | yes | yes |  |  |  | Gets or sets a value indicating if this FinancialAccount is public. |
| IsTaxDeductible | yes | yes |  |  |  | Gets or sets a flag indicating if transactions posted to this FinancialAccount are tax-deductible. |
| IsValid |  |  | yes |  |  | Gets a value indicating whether this instance is valid. |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the (internal) Name of the FinancialAccount. This property is required. |
| Order | yes | yes |  |  |  | Gets or sets the sort and display order of the FinancialAccount. This is an ascending order, so the lower the value the higher the sort priority. |
| ParentAccount |  | yes | yes |  |  | Gets or sets the parent FinancialAccount. |
| ParentAccountId | yes | yes |  |  |  | Gets or sets the FinancialAccountId of the parent FinancialAccount to this FinancialAccount. If this FinancialAccount does not have a parent, this property will be null. |
| ParentAccountIds | yes | yes |  |  |  | Returns an enumerable collection of the FinancialAccount Ids that are ancestors of a specified accountId sorted starting with the most immediate parent |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PublicDescription | yes | yes |  |  |  | Gets or sets the user defined public description of the FinancialAccount. |
| PublicName | yes | yes |  |  |  | Gets or sets the public name of the Financial Account. |
| StartDate | yes | yes |  |  |  | Gets or sets the opening date for this FinancialAccount. This is the first date that transactions can be posted to this account. If there isn't a start date for this account, transactions can be posted as soon as the account is created until the EndDate (if applicable). |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| Url | yes | yes |  |  |  | Gets or sets the URL which could be used to generate a link to a 'More Info' page |
| UrlEncodedKey |  | yes | yes |  |  |  |
| UsesCampusChildAccounts | yes | yes |  |  |  | Determines if this account will use child account matching logic using a campus. When true , a supported block will be able to automatically determine the child account to use based on the campus. When possible, use the method to perform the matching logic. If no campus is specified or available, then this (the parent) account will be used.If an active direct child account has a campus that matches the specified campus, then the first matching child account will be used.If no active direct child account matches the specified campus, then this (the parent) account will be used. If this value is true then it implies that the CampusId on this account is not supported and should be ignored. The UI will ensure that both can't be set at the same time. |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AccountTypeValue | Gets or sets the Account Type DefinedValue for this FinancialAccount. |
| AttributeValues |  |
| Attributes |  |
| Campus | Gets or sets the Campus that this FinancialAccount is associated with. |
| ChildAccounts | Gets or sets a collection containing the FinancialAccounts that are sub accounts/child accounts of this account. This is not a recursive search. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ImageBinaryFile | Gets or sets the Image that can be used when displaying this Financial Account |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ParentAccount | Gets or sets the parent FinancialAccount. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AccountTypeValue | [DefinedValue](defined-value.md) |  |
| AccountTypeValueId | [DefinedValue](defined-value.md) |  |
| Campus | [Campus](campus.md) |  |
| CampusId | [Campus](campus.md) |  |
| ParentAccountIds | [FinancialAccount](financial-account.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | UsesCampusChildAccounts | description |
