# Financial Person Saved Account Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Finance`
- Model title: `FinancialPersonSavedAccount`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `35`
- Obsolete methods: `4`
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
| Method signatures | 35 |
| Obsolete methods | 4 |
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
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FinancialGateway |  | yes | yes |  |  | Gets or sets the Financial Gateway. |
| FinancialGatewayId | yes | yes |  |  |  | Gets or sets the Financial Gateway identifier. |
| FinancialPaymentDetail |  | yes | yes |  |  | Gets or sets the Financial Payment Detail. |
| FinancialPaymentDetailId | yes | yes |  |  |  | Gets or sets the Financial Payment Detail identifier. |
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
| PersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the Person Alias identifier. |
| PreferredForeignCurrencyCodeValueId | yes | yes |  |  |  | Gets or sets the foreign currency code value identifier. These are found in the Currency Code Defined Type. |
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
| FinancialGateway | Gets or sets the Financial Gateway. |
| FinancialPaymentDetail | Gets or sets the Financial Payment Detail. |
| Group | Gets or sets the Group. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the Person Alias. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| FinancialGateway | [Financial Gateway](financial-gateway.md) | 122efe60-84a6-4c7a-a852-30e4bd89a662 |
| FinancialGatewayId | [Financial Gateway](financial-gateway.md) | 122efe60-84a6-4c7a-a852-30e4bd89a662 |
| FinancialPaymentDetail | [Financial Payment Detail](financial-payment-detail.md) | f3659077-43fd-4805-bc42-bc8a3f9c3008 |
| FinancialPaymentDetailId | [Financial Payment Detail](financial-payment-detail.md) | f3659077-43fd-4805-bc42-bc8a3f9c3008 |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| PersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| PersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
