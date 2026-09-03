# Financial Payment Detail Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Finance`
- Model title: `FinancialPaymentDetail`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `f3659077-43fd-4805-bc42-bc8a3f9c3008`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 56 |
| Database-marked properties | 22 |
| Lava-marked properties | 39 |
| Lava-marked non-database properties | 17 |
| Related model links | 7 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AccountNumberMasked | yes | yes |  |  |  | Gets or sets the Masked Account Number (Last 4 of Account Number prefixed with 12 *'s) |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BillingLocation |  | yes | yes |  |  | Gets or sets the billing Location. |
| BillingLocationId | yes | yes |  |  |  | Gets or sets the billing location identifier. |
| CardExpirationDate | yes | yes |  |  |  | Gets the card expiration date. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CreditCardTypeValue |  | yes | yes |  |  | Gets or sets the credit card type Defined Value indicating the type of credit card that was used for this transaction. If this was not a credit card based transaction, this value will be null. |
| CreditCardTypeValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the credit card type Defined Value indicating the credit card brand/type that was used to make this transaction. This value will be null for transactions that were not made by credit card. These are found in the Credit Card Type Defined Type. |
| CurrencyAndCreditCardType |  |  | yes |  |  | Gets the type of the currency and credit card. |
| CurrencyTypeValue |  | yes | yes |  |  | Gets or sets the currency type Defined Value indicating the type of currency that was used for this transaction. |
| CurrencyTypeValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the currency type Defined Value indicating the currency that the transaction was made in. These are found in the Currency Type Defined Type. |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExpirationDate |  | yes | yes |  |  | Gets the expiration date formatted as mm/yy, as per ISO7813 https://en.wikipedia.org/wiki/ISO/IEC_7813 |
| ExpirationMonth | yes | yes |  |  |  | Gets the expiration month |
| ExpirationMonthEncrypted | yes | yes |  |  | yes | Gets or sets the expiration month encrypted. Use ExpirationMonth to get the unencrypted version of Month. |
| ExpirationYear | yes | yes |  |  |  | Gets the 4 digit year |
| ExpirationYearEncrypted | yes | yes |  |  | yes | Important Note: that this could be a 2 digit or 4 digit year, so use ExpirationYear to get the unencrypted version of this which will always return a 4 digit year. |
| FinancialPaymentDetailAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| FinancialPersonSavedAccount |  | yes | yes |  |  | Gets or sets the Financial Person Saved Account that was used for this transaction (if there was one) |
| FinancialPersonSavedAccountId | yes | yes |  |  |  | Gets or sets the Financial Person Saved Account id that was used for this transaction (if there was one) |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GatewayPersonIdentifier | yes | yes |  |  |  | Gets or sets the Gateway Person Identifier. This would indicate id the customer vault information on the gateway. |
| Guid | yes | yes |  |  |  |  |
| HistoryChangeList |  |  | yes |  | yes | Gets or sets the history changes. |
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
| NameOnCard | yes | yes |  |  |  | Gets the name on card. |
| NameOnCardEncrypted | yes | yes |  |  | yes | Gets or sets the name on card encrypted. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
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
| BillingLocation | Gets or sets the billing Location. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| CreditCardTypeValue | Gets or sets the credit card type Defined Value indicating the type of credit card that was used for this transaction. If this was not a credit card based transaction, this value will be null. |
| CurrencyTypeValue | Gets or sets the currency type Defined Value indicating the type of currency that was used for this transaction. |
| EntityStringValue |  |
| ExpirationDate | Gets the expiration date formatted as mm/yy, as per ISO7813 https://en.wikipedia.org/wiki/ISO/IEC_7813 |
| FinancialPersonSavedAccount | Gets or sets the Financial Person Saved Account that was used for this transaction (if there was one) |
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
| BillingLocation | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| CreditCardTypeValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| CreditCardTypeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| CurrencyTypeValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| CurrencyTypeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| FinancialPersonSavedAccount | [Financial Person Saved Account](financial-person-saved-account.md) | f5244e64-53db-4707-a398-d248616a776d |
| FinancialPersonSavedAccountId | [Financial Person Saved Account](financial-person-saved-account.md) | f5244e64-53db-4707-a398-d248616a776d |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_removed | HistoryChangeList |  |
