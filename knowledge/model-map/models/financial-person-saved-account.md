# Financial Person Saved Account Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Finance`
- Model title: `FinancialPersonSavedAccount`
- EntityType GUID: `f5244e64-53db-4707-a398-d248616a776d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 53 |
| Database-marked properties | 22 |
| Lava-marked properties | 38 |
| Lava-marked non-database properties | 16 |
| Related model links | 7 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FinancialGateway |  | yes | yes |  |  | Gets or sets the FinancialGateway. |
| FinancialGatewayId | yes | yes |  |  |  | Gets or sets the FinancialGateway identifier. |
| FinancialPaymentDetail |  | yes | yes |  |  | Gets or sets the FinancialPaymentDetail. |
| FinancialPaymentDetailId | yes | yes |  |  |  | Gets or sets the FinancialPaymentDetail identifier. |
| FinancialPersonSavedAccountAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GatewayPersonIdentifier | yes | yes |  |  |  | Gets or sets the Gateway Person Identifier. This would indicate id the customer vault information on the gateway (for gateways that have customer vaults (NMI and MyWell) ) |
| Group |  | yes | yes |  |  | Gets or sets the Group. |
| GroupId | yes | yes |  |  |  | Gets or sets the group identifier. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsDefault | yes | yes |  |  |  | Gets or sets a flag indicating if this saved account is the default payment option for the given person. |
| IsSystem | yes | yes |  |  |  | Gets or sets a flag indicating if this saved account was created by and is a part of the Rock core system/framework. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastErrorCode | yes | yes |  |  |  | Gets or sets the last error code received from the gateway when attempting to charge this account. |
| LastErrorCodeDateTime | yes | yes |  |  |  | Gets or sets the date/time the last error code was received. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the saved account. This property is required. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAlias identifier. |
| PreferredForeignCurrencyCodeValueId | yes | yes |  |  |  | Gets or sets the foreign currency code value identifier. These are found in the "Currency Code" Defined Type. |
| ReferenceNumber | yes | yes |  |  |  | Gets or sets a reference identifier needed by the payment provider to use as a payment token. For gateways that have a concept of a customer vault (NMI and MyWell), this would be the customer vault id GatewayPersonIdentifier For gateways that use a source transaction for payment info (PayFlowPro), this would be the TransactionCode |
| SupportedActions |  |  | yes |  |  |  |
| TransactionCode | yes | yes |  |  |  | Gets or sets the transaction code that was used as the "source transaction", and is used by some gateways (PayFlowPro) to lookup the payment info. For gateways that have the concept of a Customer Vault (NMI and MyWell), GatewayPersonIdentifier is what would be used. |
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
| FinancialGateway | Gets or sets the FinancialGateway. |
| FinancialPaymentDetail | Gets or sets the FinancialPaymentDetail. |
| Group | Gets or sets the Group. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the PersonAlias. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| FinancialGateway | [FinancialGateway](financial-gateway.md) |  |
| FinancialGatewayId | [FinancialGateway](financial-gateway.md) |  |
| FinancialPaymentDetail | [FinancialPaymentDetail](financial-payment-detail.md) |  |
| FinancialPaymentDetailId | [FinancialPaymentDetail](financial-payment-detail.md) |  |
| Group | [Group](group.md) |  |
| PersonAlias | [PersonAlias](person-alias.md) |  |
| PersonAliasId | [PersonAlias](person-alias.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | PreferredForeignCurrencyCodeValueId | enum_values |
