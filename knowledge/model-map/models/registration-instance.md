# Registration Instance Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Event`
- Model title: `RegistrationInstance`
- EntityType GUID: `5cd9c0c8-c047-61a0-4e36-0fdb8496f066`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 71 |
| Database-marked properties | 37 |
| Lava-marked properties | 54 |
| Lava-marked non-database properties | 17 |
| Related model links | 13 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| Account |  | yes | yes |  |  | Gets or sets the account. |
| AccountId | yes | yes |  |  |  | Gets or sets the account identifier. |
| AdditionalConfirmationDetails | yes | yes |  |  |  | Gets or sets the additional confirmation details. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalReminderDetails | yes | yes |  |  |  | Gets or sets the additional reminder details. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContactEmail | yes | yes |  |  |  | Gets or sets the contact email. |
| ContactPersonAlias |  | yes | yes |  |  | Gets or sets the Person Alias representing the PersonAlias who is the contact person. |
| ContactPersonAliasId | yes | yes |  |  |  | Gets or sets the name of the contact. |
| ContactPhone | yes | yes |  |  |  | Gets or sets the contact phone. |
| ContextKey |  |  | yes |  |  |  |
| Cost | yes | yes |  |  |  | Gets or sets the cost (if RegistrationTemplate.SetCostOnInstance == true). |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefaultPayment | yes | yes |  |  |  | Gets or sets the default amount to pay per registrant (if RegistrationTemplate.SetCostOnInstance == true). If this is null, the default payment will be the Cost |
| Details | yes | yes |  |  |  | Gets or sets the details. |
| EncryptedKey |  |  | yes |  |  |  |
| EndDateTime | yes | yes |  |  |  | Gets or sets the end date time. |
| EntityStringValue |  | yes | yes |  |  |  |
| ExternalGatewayFundId | yes | yes |  |  |  | Gets or sets the external gateway fund identifier. |
| ExternalGatewayMerchantId | yes | yes |  |  |  | Gets or sets the external gateway merchant identifier. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is active. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Linkages |  |  | yes |  |  | Gets or sets the linkages. |
| MaxAttendees | yes | yes |  |  |  | Gets or sets the maximum attendees. |
| MinimumInitialPayment | yes | yes |  |  |  | Gets or sets the minimum initial payment (if RegistrationTemplate.SetCostOnInstance == true). |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name. |
| ParentAuthority |  |  | yes |  |  | A parent authority. If a user is not specifically allowed or denied access to this object, Rock will check the default authorization on the current type, and then the authorization on the Rock.Security.GlobalDefault entity |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PaymentDeadlineDate | yes | yes |  |  |  | Gets or sets the payment deadline date. |
| RegistrantRecordSourceValue |  | yes | yes |  |  | Gets or sets the default Record Source Type Defined Value, representing the source of Registration Registrants added to this Registration Instance. If set to null, then the value of RegistrationTemplate.RegistrantRecordSourceValue will be used. This should only be used when editing the registration instance. Call the GetRegistrantRecordSourceValue() method instead to get the value, as that method wll also check the RegistrationTemplate.RegistrantRecordSourceValue property. |
| RegistrantRecordSourceValueId | yes | yes |  |  |  | Gets or sets the default Id of the Record Source Type Defined Value, representing the source of Registration Registrants added to this Registration Instance. If set to null, then the value of RegistrationTemplate.RegistrantRecordSourceValueId will be used. This should only be used when editing the registration instance. Call the GetRegistrantRecordSourceValueId() method instead to get the value, as that method wll also check the RegistrationTemplate.RegistrantRecordSourceValueId property. These are found in the Record Source Defined Type. |
| RegistrationInstanceAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| RegistrationInstructions | yes | yes |  |  |  | Gets or sets the registration instructions. |
| RegistrationMeteringThreshold | yes | yes |  |  |  | Gets or sets the registration metering threshold. |
| RegistrationTemplate |  | yes | yes |  |  | Gets or sets the Registration Template. |
| RegistrationTemplateId | yes | yes |  | yes |  | Gets or sets the Registration Template identifier. |
| RegistrationWorkflowType |  | yes | yes |  |  | Gets or sets the Workflow Type to launch at end of registration. |
| RegistrationWorkflowTypeId | yes | yes |  |  |  | Optional workflow type to launch at end of registration |
| Registrations |  |  | yes |  |  | Gets or sets the registrations. |
| ReminderSent | yes | yes |  |  |  | Gets or sets a value indicating whether [reminder sent]. |
| SendReminderDateTime | yes | yes |  |  |  | Gets or sets the send reminder date time. |
| StartDateTime | yes | yes |  |  |  | Gets or sets the start date time. |
| SupportedActions |  |  | yes |  |  |  |
| TimeoutIsEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether [timeout is enabled]. Is there a time limit for a user submitting a registration? Their spot will be reserved until they submit or the session times out. |
| TimeoutLengthMinutes | yes | yes |  |  |  | Gets or sets the timeout length minutes. The amount of minutes that a spot will be held for a registrant until they submit or timeout occurs. |
| TimeoutThreshold | yes | yes |  |  |  | Gets or sets the timeout threshold. The lower limit of available registrations before the checkout timer is enabled. The checkout timer functionality will only display when there are fewer available registrations than configured. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Account | Gets or sets the account. |
| AttributeValues |  |
| Attributes |  |
| ContactPersonAlias | Gets or sets the Person Alias representing the PersonAlias who is the contact person. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RegistrantRecordSourceValue | Gets or sets the default Record Source Type Defined Value, representing the source of Registration Registrants added to this Registration Instance. If set to null, then the value of RegistrationTemplate.RegistrantRecordSourceValue will be used. This should only be used when editing the registration instance. Call the GetRegistrantRecordSourceValue() method instead to get the value, as that method wll also check the RegistrationTemplate.RegistrantRecordSourceValue property. |
| RegistrationTemplate | Gets or sets the Registration Template. |
| RegistrationWorkflowType | Gets or sets the Workflow Type to launch at end of registration. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Account | account | 798bce48-6aa7-4983-9214-f9bcefb4521d |
| ContactPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| Linkages | linkages | 1479d2b7-65c0-4e98-9e70-0848422fa00c |
| RegistrantRecordSourceValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| RegistrantRecordSourceValue | [Registration Instance](registration-instance.md) | 5cd9c0c8-c047-61a0-4e36-0fdb8496f066 |
| RegistrantRecordSourceValue | [Registration Registrant](registration-registrant.md) | 8a25e5ce-1b4f-4825-bcea-216167836305 |
| RegistrantRecordSourceValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| RegistrantRecordSourceValueId | [Registration Instance](registration-instance.md) | 5cd9c0c8-c047-61a0-4e36-0fdb8496f066 |
| RegistrantRecordSourceValueId | [Registration Registrant](registration-registrant.md) | 8a25e5ce-1b4f-4825-bcea-216167836305 |
| RegistrationTemplate | [Registration Template](registration-template.md) | a01e3e99-a8ad-4c6c-baac-98795738ba70 |
| RegistrationTemplateId | [Registration Template](registration-template.md) | a01e3e99-a8ad-4c6c-baac-98795738ba70 |
| RegistrationWorkflowType | [Workflow Type](workflow-type.md) | c9f3c4a5-1526-474d-803f-d6c7a45cbbae |
| Registrations | registrations | d2f294c6-e161-4a56-85c7-cd74d535f61a |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | RegistrantRecordSourceValueId | enum_values |
