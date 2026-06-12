# Analytics Dim Financial Account Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Reporting`
- Model title: `AnalyticsDimFinancialAccount`
- EntityType GUID: `893f38f8-fbf8-4157-b718-6009298abc91`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 37 |
| Database-marked properties | 25 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 5 |
| Related model links | 0 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AccountId | yes | yes |  |  |  | Gets or sets the account identifier. |
| AccountType | yes | yes |  |  |  | The name of the account type based on the value of FinancialAccount.AccountTypeValueId |
| ActiveStatus | yes | yes |  |  |  | A string representing the IsActive flag of FinancialAccount: "Active" or "Inactive" |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CampusName | yes | yes |  |  |  | Gets or sets the campus. |
| CampusShortCode | yes | yes |  |  |  | Gets or sets the campus short code. |
| ContextKey |  |  | yes |  |  |  |
| Count | yes | yes |  |  |  | Gets or sets the count. NOTE: This always has a (hard-coded) value of 1. It is stored in the table to assist with analytics calculations. |
| Description | yes | yes |  |  |  | Gets or sets the user defined description of the FinancialAccount. |
| EncryptedKey |  |  | yes |  |  |  |
| EndDate | yes | yes |  |  |  | Gets or sets the closing/end date for this FinancialAccount. This is the last day that transactions can be posted to this account. If there is not a end date for this account, transactions can be posted for an indefinite period of time. Ongoing FinancialAccounts will not have an end date. |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GlCode | yes | yes |  |  |  | Gets or sets the General Ledger account code for this FinancialAccount. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| ImageBinaryFileId | yes | yes |  |  |  | Gets or sets the Image Id that can be used when displaying this Financial Account |
| ImageUrl | yes | yes |  |  |  | Gets or sets the image URL |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the (internal) Name of the FinancialAccount. This property is required. |
| Order | yes | yes |  |  |  | Gets or sets the sort and display order of the FinancialAccount. This is an ascending order, so the lower the value the higher the sort priority. |
| ParentAccountId | yes | yes |  |  |  | Gets or sets the parent account identifier. |
| PublicDescription | yes | yes |  |  |  | Gets or sets the user defined public description of the FinancialAccount. |
| PublicName | yes | yes |  |  |  | Gets or sets the public name of the Financial Account. |
| PublicStatus | yes | yes |  |  |  | A string representing the IsPublic flag of FinancialAccount: "Public" or "Non Public" |
| StartDate | yes | yes |  |  |  | Gets or sets the opening date for this FinancialAccount. This is the first date that transactions can be posted to this account. If there isn't a start date for this account, transactions can be posted as soon as the account is created until the EndDate (if applicable). |
| TaxStatus | yes | yes |  |  |  | A string representing the IsTaxable flag of the FinancialAccount. For example, "Taxable" or "Not Taxable" |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| Url | yes | yes |  |  |  | Gets or sets the URL which could be used to generate a link to a 'More Info' page |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| EntityStringValue |  |
| IdKey |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
