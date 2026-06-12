# Financial Scheduled Transaction Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Finance`
- Model title: `FinancialScheduledTransaction`
- EntityType GUID: `76824e8a-ccc4-4085-84d9-8af8c0807e20`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 71 |
| Database-marked properties | 32 |
| Lava-marked properties | 53 |
| Lava-marked non-database properties | 21 |
| Related model links | 12 |
| Pre-alpha changes touching this model | 3 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AuthorizedPersonAlias |  | yes | yes |  |  | Gets or sets the authorized PersonAlias. |
| AuthorizedPersonAliasId | yes | yes |  |  |  | Gets or sets the authorized person alias identifier. |
| AvailableKeys |  |  | yes |  |  |  |
| CardReminderDate | yes | yes |  |  |  | Gets or sets the date to remind user to update scheduled transaction. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EndDate | yes | yes |  |  |  | Gets or sets the end date for this transaction schedule. Transactions will cease to occur on or before this date. This property is nullable for ongoing schedules or for schedules that will end after a specified number of payments/transaction occur (in the NumberOfPayments property). |
| EntityStringValue |  | yes | yes |  |  |  |
| FinancialGateway |  | yes | yes |  |  | Gets or sets the gateway. |
| FinancialGatewayId | yes | yes |  |  |  | Gets or sets the gateway identifier. |
| FinancialPaymentDetail |  | yes | yes |  |  | Gets or sets the FinancialPaymentDetail. |
| FinancialPaymentDetailId | yes | yes |  |  |  | Gets or sets the financial payment detail identifier. |
| FinancialScheduledTransactionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ForeignCurrencyCodeValue |  | yes | yes |  |  | Gets or sets the foreign currency code type DefinedValue indicating where the transaction originated from; the source of the transaction. |
| ForeignCurrencyCodeValueId | yes | yes |  |  |  | Gets or sets the foreign currency code value identifier. These are found in the "Currency Code" Defined Type. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| GatewayScheduleId | yes | yes |  |  |  | Gets or sets the payment gateway's payment schedule key/identifier. This is the value that uniquely identifies the payment schedule on with the payment gateway. |
| Guid | yes | yes |  |  |  |  |
| HistoryChangeList |  |  | yes |  |  | [Obsoleted in v14] Does nothing. No longer needed. We replaced this with a private property under the SaveHook class for this entity. Gets or sets the history change list. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InactivateDateTime | yes | yes |  |  |  | Gets or sets the inactivate date time. |
| IsActive | yes | yes |  |  |  | Gets or sets a flag indicating if this scheduled transaction is active. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastRemindedDate | yes | yes |  |  |  | Gets or sets the date that user was last reminded to update scheduled transaction. |
| LastStatusUpdateDateTime | yes | yes |  |  |  | Gets or sets the date and time of the last status update. In other words, the date and time the gateway was last queried for the status of the scheduled profile/transaction. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| NextPaymentDate | yes | yes |  |  |  | Gets or sets the date of the next payment in this schedule. |
| NumberOfPayments | yes | yes |  |  |  | Gets or sets the maximum number of times that this payment should repeat in this schedule. If there is not a set number of payments, this value will be null. This property is overridden by the schedule's EndDate. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PaymentPlan |  |  | yes |  |  |  |
| PreviousGatewayScheduleIds |  |  | yes |  |  | This will be any previous GatewayScheduleId that this FinancialScheduledTransaction has had. This might be used in a case where a GatewayComponent may have changed what schedule id it used. |
| PreviousGatewayScheduleIdsJson | yes | yes |  |  |  | The JSON for PreviousGatewayScheduleIds. If this is null, there are no PreviousGatewayScheduleIds. |
| ScheduledTransactionDetails |  | yes | yes |  |  | Gets or sets the transaction details for this scheduled transaction. |
| SourceTypeValue |  | yes | yes |  |  | Gets or sets the source type DefinedValue indicating where the transaction originated from; the source of the transaction. |
| SourceTypeValueId | yes | yes |  |  |  | Gets or sets the source type value identifier. These are found in the "Transaction Source" Defined Type. |
| StartDate | yes | yes |  |  |  | Gets or sets the start date for this schedule. The first transaction will occur on or after this date. |
| Status | yes | yes |  |  |  | The status of the scheduled transactions provided by the payment gateway (i.e. Active, Cancelled, etc). If the gateway doesn't have a status field, this will be null; The payment gateway component maps this based on the StatusMessage. This is a hard coded list of values defined in the code as an enumeration. |
| StatusMessage | yes | yes |  |  |  | Gets or sets the raw scheduled transaction status message returned from the Gateway If the gateway doesn't have a status field, this will be null; |
| Summary | yes | yes |  |  |  | Gets or sets a summary of the scheduled transaction. This would store any comments made. |
| SupportedActions |  |  | yes |  |  |  |
| TotalAmount | yes | yes |  |  |  | Gets the total amount. |
| TransactionCode | yes | yes |  |  |  | Gets or sets the transaction code used for this scheduled transaction. |
| TransactionFrequencyValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the payment frequency associated with this scheduled transaction. |
| TransactionFrequencyValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the transaction frequency DefinedValue that represents the frequency that this transaction will occur. These are found in the "Recurring Transaction Frequency" Defined Type. |
| TransactionTypeValue |  | yes | yes |  |  | Gets or sets the transaction type DefinedValue indicating the type of transaction that occurred. |
| TransactionTypeValueId | yes | yes |  |  |  | Gets or sets the transaction type value identifier. These are found in the "Transaction Type" Defined Type. |
| Transactions |  | yes | yes |  |  | Gets or sets FinancialTransactions that have been processed and have cleared for this scheduled transaction profile. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| AuthorizedPersonAlias | Gets or sets the authorized PersonAlias. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| FinancialGateway | Gets or sets the gateway. |
| FinancialPaymentDetail | Gets or sets the FinancialPaymentDetail. |
| ForeignCurrencyCodeValue | Gets or sets the foreign currency code type DefinedValue indicating where the transaction originated from; the source of the transaction. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ScheduledTransactionDetails | Gets or sets the transaction details for this scheduled transaction. |
| SourceTypeValue | Gets or sets the source type DefinedValue indicating where the transaction originated from; the source of the transaction. |
| TransactionFrequencyValue | Gets or sets the DefinedValue representing the payment frequency associated with this scheduled transaction. |
| TransactionTypeValue | Gets or sets the transaction type DefinedValue indicating the type of transaction that occurred. |
| Transactions | Gets or sets FinancialTransactions that have been processed and have cleared for this scheduled transaction profile. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AuthorizedPersonAlias | [PersonAlias](person-alias.md) |  |
| FinancialGateway | gateway |  |
| FinancialPaymentDetail | [FinancialPaymentDetail](financial-payment-detail.md) |  |
| ForeignCurrencyCodeValue | [DefinedValue](defined-value.md) |  |
| PreviousGatewayScheduleIds | [FinancialScheduledTransaction](financial-scheduled-transaction.md) |  |
| PreviousGatewayScheduleIds | GatewayComponent |  |
| ScheduledTransactionDetails | transaction details |  |
| SourceTypeValue | [DefinedValue](defined-value.md) |  |
| TransactionFrequencyValue | [DefinedValue](defined-value.md) |  |
| TransactionFrequencyValueId | [DefinedValue](defined-value.md) |  |
| TransactionTypeValue | [DefinedValue](defined-value.md) |  |
| Transactions | FinancialTransactions |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_removed | HistoryChangeList |  |
| property_changed | ForeignCurrencyCodeValueId | enum_values |
| property_changed | PreviousGatewayScheduleIds | related_entity_links |
