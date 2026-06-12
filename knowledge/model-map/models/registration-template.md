# Registration Template Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Event`
- Model title: `RegistrationTemplate`
- EntityType GUID: `a01e3e99-a8ad-4c6c-baac-98795738ba70`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 111 |
| Database-marked properties | 70 |
| Lava-marked properties | 95 |
| Lava-marked non-database properties | 25 |
| Related model links | 18 |
| Pre-alpha changes touching this model | 7 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AddPersonNote | yes | yes |  |  |  | Gets or sets a value indicating whether a person note should be added when a person registers for this type of registration. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowExternalRegistrationUpdates | yes | yes |  |  |  | Gets or sets a value indicating whether to allow external registration updates (should a person be able to update their registration on-line after submitting it). |
| AllowGroupPlacement | yes | yes |  |  |  | [Obsoleted in v10] No longer used. Replaced by Group Placement feature (RegistrationTemplatePlacement, etc) Gets or sets a value indicating whether [allow group placement]. |
| AllowMultipleRegistrants | yes | yes |  |  |  | Gets or sets a value indicating whether a registrar can register multiple registrants per registration. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BatchNamePrefix | yes | yes |  |  |  | Gets or sets the batch name prefix. |
| Category |  | yes | yes |  |  | Gets or sets the Category. |
| CategoryId | yes | yes |  |  |  | Gets or sets the category identifier. |
| ConfirmationEmailTemplate | yes | yes |  |  |  | Gets or sets the confirmation email text to send. |
| ConfirmationFromEmail | yes | yes |  |  |  | Gets or sets the confirmation from email. |
| ConfirmationFromName | yes | yes |  |  |  | Gets or sets the name of the confirmation from. |
| ConfirmationSubject | yes | yes |  |  |  | Gets or sets the confirmation subject. |
| ConnectionStatusValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the connection status. |
| ConnectionStatusValueId | yes | yes |  |  |  | Gets or sets the connection status value identifier. |
| ContextKey |  |  | yes |  |  |  |
| Cost | yes | yes |  |  |  | Gets or sets the cost (if SetCostOnInstance == false). |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefaultPayment | yes | yes |  |  |  | Gets or sets the default amount to pay per registrant (if SetCostOnInstance == false). If this is null, the default payment will be the Cost |
| Description | yes | yes |  |  |  | Gets or sets the description of the Attribute. |
| DiscountCodeTerm | yes | yes |  |  |  | Gets or sets the term to use for discount code |
| Discounts |  | yes | yes |  |  | Gets or sets the discounts. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FeeTerm | yes | yes |  |  |  | Gets or sets the term to use for fee |
| Fees |  | yes | yes |  |  | Gets or sets the fees. |
| FinancialGateway |  | yes | yes |  |  | Gets or sets the FinancialGateway. |
| FinancialGatewayId | yes | yes |  |  |  | Gets or sets the financial gateway identifier. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Forms |  | yes | yes |  |  | Gets or sets the forms. |
| GroupMemberRoleId | yes | yes |  |  |  | Gets or sets the group member role that registrants will be added to group as |
| GroupMemberStatus | yes | yes |  |  |  | Gets or sets the group member status that registrants will be added to group with. This is a hard coded list of values defined in the code as an enumeration. |
| GroupType |  | yes | yes |  |  | Gets or sets the type of the group. |
| GroupTypeId | yes | yes |  |  |  | Gets or sets the group type that this registration template applies to |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| Instances |  | yes | yes |  |  | Gets or sets the collection of the current template's child instances. |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is active. |
| IsPaymentPlanAllowed | yes | yes |  |  |  | Gets or sets a value indicating whether registrants should be able to pay their registration costs in multiple, scheduled installments. |
| IsRegistrationMeteringEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is registration metering enabled. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LoginRequired | yes | yes |  |  |  | Gets or sets a value indicating whether [log in required]. |
| MaxRegistrants | yes | yes |  |  |  | Gets or sets the maximum number of registrants that a registrar can register per registration. |
| MinimumInitialPayment | yes | yes |  |  |  | Gets or sets the minimum initial payment (if SetCostOnInstance == false). |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the registration template |
| Notify | yes | yes |  |  |  | Gets or sets the notify. This is a hard coded list of values defined in the code as an enumeration. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PaymentPlanFrequencyValueIds | yes | yes |  |  |  | Gets or sets the payment plan frequency value identifiers (separated by commas) from which a registrant can select. |
| PaymentPlanFrequencyValueIdsCollection |  |  | yes |  |  | Gets or sets the collection of payment plan frequency value IDs from which a registrant can select. This is a convenient property for working with the IDs as a collection instead of the PaymentPlanFrequencyValueIds property directly. Updates made to PaymentPlanFrequencyValueIds will require getting this property again. |
| PaymentReminderEmailTemplate | yes | yes |  |  |  | Gets or sets the payment reminder email template. |
| PaymentReminderFromEmail | yes | yes |  |  |  | Gets or sets the payment reminder from email. |
| PaymentReminderFromName | yes | yes |  |  |  | Gets or sets the name of the payment reminder from. |
| PaymentReminderSubject | yes | yes |  |  |  | Gets or sets the payment reminder subject. |
| PaymentReminderTimeSpan | yes | yes |  |  |  | Gets or sets the payment reminder time span in days. |
| Placements |  | yes | yes |  |  | Gets or sets the placements. |
| RegistrantRecordSourceValue |  | yes | yes |  |  | Gets or sets the default Record Source Type DefinedValue, representing the source of RegistrationRegistrants added to RegistrationInstances that are linked to this template. This can be overridden by RegistrationInstance.RegistrantRecordSourceValue. |
| RegistrantRecordSourceValueId | yes | yes |  |  |  | Gets or sets the default Id of the Record Source Type DefinedValue, representing the source of RegistrationRegistrants added to RegistrationInstances that are linked to this template. This can be overridden by RegistrationInstance.RegistrantRecordSourceValueId. These are found in the "Record Source" Defined Type. |
| RegistrantTerm | yes | yes |  |  |  | Gets or sets the term to use for registrant |
| RegistrantWorkflowType |  | yes | yes |  |  | Gets or sets the WorkflowType to launch for the registrant |
| RegistrantWorkflowTypeId | yes | yes |  |  |  | Optional workflow type to launch for registrant |
| RegistrantsSameFamily | yes | yes |  |  |  | Gets or sets flag indicating if registrants registered for this template are typically in same family. values are ( yes, no, ask ). This is a hard coded list of values defined in the code as an enumeration. |
| RegistrarOption | yes | yes |  |  |  | Gets or sets the registrar option. This is a hard coded list of values defined in the code as an enumeration. |
| RegistrationAttributeTitleEnd | yes | yes |  |  |  | Gets or sets the section title for attributes that are collected at the end of the registration entry process. |
| RegistrationAttributeTitleStart | yes | yes |  |  |  | Gets or sets the section title for attributes that are collected at the start of the registration entry process. |
| RegistrationInstructions | yes | yes |  |  |  | Gets or sets the registration instructions. |
| RegistrationTemplateAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| RegistrationTerm | yes | yes |  |  |  | Gets or sets the term to use for registration |
| RegistrationWorkflowType |  | yes | yes |  |  | Gets or sets the WorkflowType to launch at end of registration. |
| RegistrationWorkflowTypeId | yes | yes |  |  |  | Optional workflow type to launch at end of registration |
| ReminderEmailTemplate | yes | yes |  |  |  | Gets or sets the reminder email template. |
| ReminderFromEmail | yes | yes |  |  |  | Gets or sets the reminder from email. |
| ReminderFromName | yes | yes |  |  |  | Gets or sets the name of the reminder from. |
| ReminderSubject | yes | yes |  |  |  | Gets or sets the reminder subject. |
| RequestEntryName | yes | yes |  |  |  | Gets or sets the name of the request entry. |
| RequiredSignatureDocumentTemplate |  | yes | yes |  |  | Gets or sets the type of the required signature document. |
| RequiredSignatureDocumentTemplateId | yes | yes |  |  |  | Gets or sets the required signature document type identifier. |
| SetCostOnInstance | yes | yes |  |  |  | Gets or sets the set cost on instance. |
| ShowCurrentFamilyMembers | yes | yes |  |  |  | Gets or sets a value indicating whether [show current family members]. |
| ShowSmsOptIn | yes | yes |  |  |  | Gets or sets a value indicating whether [show SMS opt in]. When enabled a checkbox will be shown next to each mobile phone number for registrants allowing the registrar to enable SMS messaging for this number. |
| SignatureDocumentAction | yes | yes |  |  |  | Gets or sets the signature documentation. This is a hard coded list of values defined in the code as an enumeration. |
| SuccessText | yes | yes |  |  |  | Gets or sets the success text. |
| SuccessTitle | yes | yes |  |  |  | Gets or sets the success title. |
| SupportedActions |  |  | yes |  |  | Provides a Dictionary`2 of actions that this model supports, and the description of each. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WaitListEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether a wait list is enabled for this event template |
| WaitListTransitionEmailTemplate | yes | yes |  |  |  | Gets or sets the wait list transition email template. |
| WaitListTransitionFromEmail | yes | yes |  |  |  | Gets or sets the wait list transition from email. |
| WaitListTransitionFromName | yes | yes |  |  |  | Gets or sets the name of the wait list transition from. |
| WaitListTransitionSubject | yes | yes |  |  |  | Gets or sets the wait list transition subject. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the Category. |
| ConnectionStatusValue | Gets or sets the DefinedValue representing the connection status. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| Discounts | Gets or sets the discounts. |
| EntityStringValue |  |
| Fees | Gets or sets the fees. |
| FinancialGateway | Gets or sets the FinancialGateway. |
| Forms | Gets or sets the forms. |
| GroupType | Gets or sets the type of the group. |
| IdKey |  |
| Instances | Gets or sets the collection of the current template's child instances. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Placements | Gets or sets the placements. |
| RegistrantRecordSourceValue | Gets or sets the default Record Source Type DefinedValue, representing the source of RegistrationRegistrants added to RegistrationInstances that are linked to this template. This can be overridden by RegistrationInstance.RegistrantRecordSourceValue. |
| RegistrantWorkflowType | Gets or sets the WorkflowType to launch for the registrant |
| RegistrationWorkflowType | Gets or sets the WorkflowType to launch at end of registration. |
| RequiredSignatureDocumentTemplate | Gets or sets the type of the required signature document. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Category | [Category](category.md) |  |
| ConnectionStatusValue | [DefinedValue](defined-value.md) |  |
| Discounts | discounts |  |
| Fees | fees |  |
| FinancialGateway | [FinancialGateway](financial-gateway.md) |  |
| GroupType | type |  |
| Instances | instances |  |
| Placements | placements |  |
| RegistrantRecordSourceValue | [DefinedValue](defined-value.md) |  |
| RegistrantRecordSourceValue | [RegistrationInstance](registration-instance.md) |  |
| RegistrantRecordSourceValue | [RegistrationRegistrant](registration-registrant.md) |  |
| RegistrantRecordSourceValueId | [DefinedValue](defined-value.md) |  |
| RegistrantRecordSourceValueId | [RegistrationInstance](registration-instance.md) |  |
| RegistrantRecordSourceValueId | [RegistrationRegistrant](registration-registrant.md) |  |
| RegistrantWorkflowType | [WorkflowType](workflow-type.md) |  |
| RegistrationWorkflowType | [WorkflowType](workflow-type.md) |  |
| RequiredSignatureDocumentTemplate | [signature document](signature-document.md) |  |
| SupportedActions | Dictionary`2 |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | AdditionalSettingsJson |  |
| property_added | AreDuplicateRegistrantsPrevented |  |
| property_added | FullPaymentOrPaymentPlanRequiredMessage |  |
| property_added | IsFullPaymentOrPaymentPlanRequired |  |
| property_changed | AllowGroupPlacement | description, is_obsolete |
| property_changed | RegistrantRecordSourceValueId | enum_values |
| property_changed | SupportedActions | related_entity_links |
