# Financial Transaction Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Finance`
- Model title: `FinancialTransaction`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `35`
- Obsolete methods: `4`
- EntityType GUID: `2c1cb26b-ab22-42d0-8164-aedee0dae667`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 85 |
| Database-marked properties | 38 |
| Lava-marked properties | 66 |
| Lava-marked non-database properties | 30 |
| Related model links | 18 |
| Method signatures | 35 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 5 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AuthorizedPersonAlias |  | yes | yes |  |  | Gets or sets the authorized Person Alias. |
| AuthorizedPersonAliasId | yes | yes |  |  |  | Gets or sets the authorized person identifier. |
| AvailableKeys |  |  | yes |  |  |  |
| Batch |  | yes | yes |  |  | Gets or sets the Financial Batch that contains the transaction. |
| BatchHistoryChangeList |  |  | yes |  | yes | Gets or sets the batch history change list. |
| BatchId | yes | yes |  |  |  | Gets or sets BatchId of the Financial Batch that contains this transaction. |
| CheckMicrEncrypted | yes | yes |  |  |  | Gets or sets an encrypted version of a scanned check's raw track of the MICR data. Note that different scanning hardware might use different special characters for fields such as Transit and On-US. Also, encryption of the same values results in different encrypted data, so this field can't be used for check matching |
| CheckMicrHash | yes | yes |  |  |  | One Way Encryption (SHA1 Hash) of Raw Track of the MICR read. The same raw MICR will result in the same hash. Enables detection of duplicate scanned checks Note: duplicate detection requires that the duplicate check was scanned using the same scanner type (Ranger vs Magtek) |
| CheckMicrParts | yes | yes |  |  |  | Gets or sets an encrypted version of a scanned check's parsed MICR in the format {routingnumber}_{accountnumber}_{checknumber} |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FinancialGateway |  | yes | yes |  |  | Gets or sets the gateway. |
| FinancialGatewayId | yes | yes |  |  |  | Gets or sets the gateway identifier. |
| FinancialPaymentDetail |  | yes | yes |  |  | Gets or sets the Financial Payment Detail. |
| FinancialPaymentDetailId | yes | yes |  |  |  | Gets or sets the financial payment detail identifier. |
| FinancialTransactionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ForeignCurrencyCodeValueId | yes | yes |  |  |  | Gets or sets the foreign currency code value identifier. These are found in the Currency Code Defined Type. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FutureProcessingDateTime | yes | yes |  |  |  | Gets or sets date and time that the transaction should be processed after. This is the local server time. |
| Guid | yes | yes |  |  |  |  |
| HistoryChangeList |  |  | yes |  | yes | Gets or sets the history change list. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| Images |  | yes | yes |  |  | Gets or sets a collection containing any images associated with this transaction. An example of this would be a scanned image of a check. |
| IsReconciled | yes | yes |  |  |  | Gets or sets a flag indicating if the transaction has been reconciled or not. |
| IsSettled | yes | yes |  |  |  | Gets or sets a flag indicating if the transaction has been settled by the processor/gateway. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MICRStatus | yes | yes |  |  |  | Gets or sets the micr status (if this Transaction is from a scanned check) Fail means that the check scanner detected a bad MICR read, but the user choose to Upload it anyway This is a hard coded list of values defined in the code as an enumeration. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| NonCashAssetTypeValue |  | yes | yes |  |  | Gets or sets the non cash asset type Defined Value. |
| NonCashAssetTypeValueId | yes | yes |  |  |  | Gets or sets the non cash asset type Defined Value identifier. These are found in the Non-Cash Asset Types Defined Type. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ProcessedByPersonAlias |  | yes | yes |  |  | Gets or sets the PersonAlias of the Person Alias who processed the transaction. For example, if the transaction is from a scanned check, the ProcessedByPersonAlias is the person who matched (or started to match) the check to the person who wrote the check. |
| ProcessedByPersonAliasId | yes |  |  |  |  | Gets or sets the PersonAliasId of the Person Alias who processed the transaction. For example, if the transaction is from a scanned check, the ProcessedByPersonAlias is the person who matched (or started to match) the check to the person who wrote the check. |
| ProcessedDateTime | yes |  |  |  |  | Gets or sets the processed date time. For example, if the transaction is from a scanned check, the ProcessedDateTime is when the transaction was matched (or started to match) to the person who wrote the check. |
| RefundDetails |  | yes | yes |  |  | Gets or sets the refund transaction that is associated with this transaction. If this transaction is not a refund transaction this value will be null. |
| Refunds |  | yes | yes |  |  | Gets or sets the refunds. |
| ScheduledTransaction |  | yes | yes |  |  | Gets or sets the Scheduled Transaction that initiated this transaction. |
| ScheduledTransactionId | yes | yes |  |  |  | Gets or sets the ScheduledTransactionId of the Financial Scheduled Transaction that triggered this transaction. If this was an ad-hoc/on demand transaction, this property will be null. |
| SettledDate | yes | yes |  |  |  | Gets or sets the date that the transaction was settled by the processor/gateway. |
| SettledDateKey | yes | yes |  |  |  | Gets the settled date key. |
| SettledGroupId | yes | yes |  |  |  | The group/batch identifier used by the processor/gateway when the transaction has been settled. |
| SettledSourceDate |  | yes | yes |  |  | Gets or sets the settled source date. |
| ShowAsAnonymous | yes | yes |  |  |  | Gets or sets a value indicating whether to show the transaction as anonymous when displayed publicly, for example on a list of fundraising contributors |
| SourceTypeValue |  | yes | yes |  |  | Gets or sets the source type Defined Value indicating where the transaction originated from; the source of the transaction. |
| SourceTypeValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the source type Defined Value for this transaction. Representing the source (method) of this transaction. These are found in the Transaction Source Defined Type. |
| Status | yes | yes |  |  |  | Gets the status of the transaction provided by the payment gateway (i.e. Pending, Complete, Failed) |
| StatusMessage | yes | yes |  |  |  | Gets or sets the status message. |
| Summary | yes | yes |  |  |  | Gets or sets a summary of the transaction. This would store any comments made. |
| SundayDate | yes | yes |  |  |  | Gets Sunday date. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TotalAmount |  | yes | yes |  |  | Gets the total amount. |
| TotalFeeAmount |  | yes | yes |  |  | Gets the total fee amount. |
| TotalFeeCoverageAmount |  | yes | yes |  |  | Gets the total fee coverage amount. |
| TransactionCode | yes | yes |  |  |  | For Credit Card transactions, this is the response code that the gateway returns. For Scanned Checks, this is the check number. |
| TransactionDateKey | yes | yes |  |  |  | Gets the transaction date key. |
| TransactionDateTime | yes | yes |  |  |  | Gets or sets date and time that the transaction occurred. This is the local server time. |
| TransactionDetails |  | yes | yes |  |  | Gets or sets the Transaction Detail line items for this transaction. |
| TransactionSourceDate |  | yes | yes |  |  | Gets or sets the transaction source date. |
| TransactionTypeValue |  | yes | yes |  |  | Gets or sets the transaction type Defined Value indicating the type of transaction that occurred. |
| TransactionTypeValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the TransactionType Defined Value indicating the type of the transaction. These are found in the Transaction Type Defined Type. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| AuthorizedPersonAlias | Gets or sets the authorized Person Alias. |
| Batch | Gets or sets the Financial Batch that contains the transaction. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| FinancialGateway | Gets or sets the gateway. |
| FinancialPaymentDetail | Gets or sets the Financial Payment Detail. |
| IdKey |  |
| Images | Gets or sets a collection containing any images associated with this transaction. An example of this would be a scanned image of a check. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| NonCashAssetTypeValue | Gets or sets the non cash asset type Defined Value. |
| ProcessedByPersonAlias | Gets or sets the PersonAlias of the Person Alias who processed the transaction. For example, if the transaction is from a scanned check, the ProcessedByPersonAlias is the person who matched (or started to match) the check to the person who wrote the check. |
| RefundDetails | Gets or sets the refund transaction that is associated with this transaction. If this transaction is not a refund transaction this value will be null. |
| Refunds | Gets or sets the refunds. |
| ScheduledTransaction | Gets or sets the Scheduled Transaction that initiated this transaction. |
| SettledSourceDate | Gets or sets the settled source date. |
| SourceTypeValue | Gets or sets the source type Defined Value indicating where the transaction originated from; the source of the transaction. |
| TotalAmount | Gets the total amount. |
| TotalFeeAmount | Gets the total fee amount. |
| TotalFeeCoverageAmount | Gets the total fee coverage amount. |
| TransactionDetails | Gets or sets the Transaction Detail line items for this transaction. |
| TransactionSourceDate | Gets or sets the transaction source date. |
| TransactionTypeValue | Gets or sets the transaction type Defined Value indicating the type of transaction that occurred. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AuthorizedPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| Batch | [Financial Batch](financial-batch.md) | bdd09c8e-2c52-4d08-9062-be7d52d190c2 |
| BatchId | [Financial Batch](financial-batch.md) | bdd09c8e-2c52-4d08-9062-be7d52d190c2 |
| FinancialGateway | gateway | 122efe60-84a6-4c7a-a852-30e4bd89a662 |
| FinancialPaymentDetail | [Financial Payment Detail](financial-payment-detail.md) | f3659077-43fd-4805-bc42-bc8a3f9c3008 |
| Images | images | 78dca7ee-c5fe-49ae-9995-0e254cc8e2a2 |
| NonCashAssetTypeValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| NonCashAssetTypeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| ProcessedByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| ProcessedByPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| RefundDetails | refund | 7616e2af-cef2-44a5-b27f-3e70ec8b70fa |
| ScheduledTransaction | Scheduled Transaction | 76824e8a-ccc4-4085-84d9-8af8c0807e20 |
| ScheduledTransactionId | [Financial Scheduled Transaction](financial-scheduled-transaction.md) | 76824e8a-ccc4-4085-84d9-8af8c0807e20 |
| SourceTypeValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| SourceTypeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| TransactionDetails | Transaction Detail | ac4ac28b-8e7e-4d7e-85db-dffb4f3adcce |
| TransactionTypeValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| TransactionTypeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_removed | BatchHistoryChangeList |  |
| property_removed | HistoryChangeList |  |
| property_changed | ForeignCurrencyCodeValueId | enum_values |
| property_changed | NonCashAssetTypeValueId | enum_values |
| property_changed | SourceTypeValueId | enum_values |
