# Registration Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Event`
- Model title: `Registration`
- EntityType GUID: `d2f294c6-e161-4a56-85c7-cd74d535f61a`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 66 |
| Database-marked properties | 24 |
| Lava-marked properties | 50 |
| Lava-marked non-database properties | 26 |
| Related model links | 9 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BalanceDue |  | yes | yes |  |  | Gets the balance due. |
| Campus |  | yes | yes |  |  | Gets or sets the Campus the registration will be tied to |
| CampusId | yes | yes |  |  |  | Gets or sets the Id of the Campus the registration will be tied to |
| ConfirmationEmail | yes | yes |  |  |  | Gets or sets the confirmation email. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateKey | yes | yes |  |  |  | Gets the created date key. |
| CreatedDateTime | yes | yes |  |  |  |  |
| CreatedSourceDate |  | yes | yes |  |  | Gets or sets the created source date. |
| CustomSortValue |  |  | yes |  |  |  |
| DiscountAmount | yes | yes |  |  |  | Gets or sets the discount amount. |
| DiscountCode | yes | yes |  |  |  | Gets or sets the code. |
| DiscountPercentage | yes | yes |  |  |  | Gets or sets the discount percentage. |
| DiscountedCost |  | yes | yes |  |  | Gets the discounted cost. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FirstName | yes | yes |  |  |  | Gets or sets the first name. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Group. |
| GroupId | yes | yes |  |  |  | Gets or sets the Group identifier. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsPaymentPlanActive |  | yes | yes |  |  | Gets a boolean value indicating whether this registration has an active payment plan. |
| IsTemporary | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is temporary (started from another page). |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastName | yes | yes |  |  |  | Gets or sets the last name. |
| LastPaymentReminderDateTime | yes | yes |  |  |  | Gets or sets the last payment reminder date time. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  | A parent authority. If a user is not specifically allowed or denied access to this object, Rock will check the default authorization on the current type, and then the authorization on the Rock.Security.GlobalDefault entity |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PaymentPlanFinancialScheduledTransaction |  | yes | yes |  |  | Gets or sets the payment plan Financial Scheduled Transaction. |
| PaymentPlanFinancialScheduledTransactionId | yes | yes |  |  |  | Gets or sets the payment plan Financial Scheduled Transaction identifier. |
| Payments |  | yes | yes |  |  | Gets the payments. |
| PersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias. |
| PersonAliasId | yes | yes |  |  |  | Gets or sets the Person Alias identifier. |
| PersonId |  |  | yes |  |  | Gets the person identifier. |
| Registrants |  | yes | yes |  |  | Gets or sets the registrants. |
| RegistrationAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| RegistrationInstance |  | yes | yes |  |  | Gets or sets the registration instance. |
| RegistrationInstanceId | yes | yes |  | yes |  | Gets or sets the registration instance identifier. |
| RegistrationTemplate |  | yes | yes |  |  | Gets or sets the registration template. |
| RegistrationTemplateId | yes | yes |  |  |  | Gets the registration template identifier. NOTE: this is needed so that Registration Attributes can have a RegistrationTemplateId qualifier |
| SupportedActions |  |  | yes |  |  |  |
| TotalCost |  | yes | yes |  |  | Gets the total cost. |
| TotalPaid |  | yes | yes |  |  | Gets the total paid. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| BalanceDue | Gets the balance due. |
| Campus | Gets or sets the Campus the registration will be tied to |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| CreatedSourceDate | Gets or sets the created source date. |
| DiscountedCost | Gets the discounted cost. |
| EntityStringValue |  |
| Group | Gets or sets the Group. |
| IdKey |  |
| IsPaymentPlanActive | Gets a boolean value indicating whether this registration has an active payment plan. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PaymentPlanFinancialScheduledTransaction | Gets or sets the payment plan Financial Scheduled Transaction. |
| Payments | Gets the payments. |
| PersonAlias | Gets or sets the Person Alias. |
| Registrants | Gets or sets the registrants. |
| RegistrationInstance | Gets or sets the registration instance. |
| RegistrationTemplate | Gets or sets the registration template. |
| TotalCost | Gets the total cost. |
| TotalPaid | Gets the total paid. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Campus | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| CampusId | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| PaymentPlanFinancialScheduledTransaction | [Financial Scheduled Transaction](financial-scheduled-transaction.md) | 76824e8a-ccc4-4085-84d9-8af8c0807e20 |
| PaymentPlanFinancialScheduledTransactionId | [Financial Scheduled Transaction](financial-scheduled-transaction.md) | 76824e8a-ccc4-4085-84d9-8af8c0807e20 |
| Payments | payments | ac4ac28b-8e7e-4d7e-85db-dffb4f3adcce |
| PersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| PersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
