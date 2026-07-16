# Registration Registrant Fee Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Event`
- Model title: `RegistrationRegistrantFee`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `35`
- Obsolete methods: `4`
- EntityType GUID: `ab66f63a-3e79-438f-8c52-c9a8c70a0511`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 46 |
| Database-marked properties | 15 |
| Lava-marked properties | 31 |
| Lava-marked non-database properties | 16 |
| Related model links | 0 |
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
| Cost | yes | yes |  |  |  | Gets or sets the cost. |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
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
| Option | yes | yes |  |  |  | Gets or sets the name of the FeeItem that was selected at the time of the registration. See also RegistrationTemplateFeeItem. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| Quantity | yes | yes |  |  |  | Gets or sets the quantity. |
| RegistrationRegistrant |  | yes | yes |  |  | Gets or sets the registration registrant. |
| RegistrationRegistrantFeeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| RegistrationRegistrantId | yes | yes |  |  |  | Gets or sets the registration registrant identifier. |
| RegistrationTemplateFee |  | yes | yes |  |  | Gets or sets the registration template fee. See also RegistrationTemplateFeeItem. |
| RegistrationTemplateFeeId | yes | yes |  |  |  | Gets or sets the registration template fee identifier. See also RegistrationTemplateFeeItemId. |
| RegistrationTemplateFeeItem |  | yes | yes |  |  | Gets or sets the registration template fee item. |
| RegistrationTemplateFeeItemId | yes | yes |  |  |  | Gets or sets the registration template fee item identifier. |
| SupportedActions |  |  | yes |  |  |  |
| TotalCost |  | yes | yes |  |  | Gets the total cost. |
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
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RegistrationRegistrant | Gets or sets the registration registrant. |
| RegistrationTemplateFee | Gets or sets the registration template fee. See also RegistrationTemplateFeeItem. |
| RegistrationTemplateFeeItem | Gets or sets the registration template fee item. |
| TotalCost | Gets the total cost. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
