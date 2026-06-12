# Registration Template Discount Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Event`
- Model title: `RegistrationTemplateDiscount`
- EntityType GUID: `88d94ecb-fcee-4a00-acb9-ff90bdba7a17`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 50 |
| Database-marked properties | 20 |
| Lava-marked properties | 35 |
| Lava-marked non-database properties | 15 |
| Related model links | 2 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AutoApplyDiscount | yes | yes |  |  |  | Gets or sets a value indicating whether the discount applies automatically. |
| AvailableKeys |  |  | yes |  |  |  |
| Code | yes | yes |  | yes |  | Gets or sets the code. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DiscountAmount | yes | yes |  |  |  | Gets or sets the discount amount. |
| DiscountLimitsString |  | yes | yes |  |  | String representation of any discount limits. |
| DiscountPercentage | yes | yes |  |  |  | Gets or sets the discount percentage. |
| DiscountString |  | yes | yes |  |  | Gets the discount string. |
| EncryptedKey |  |  | yes |  |  |  |
| EndDate | yes | yes |  |  |  | Gets or sets the last day that the discount code can be used |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MaxRegistrants | yes | yes |  |  |  | Gets or sets the maximum number of registrants per registration that the discount code can used for. |
| MaxUsage | yes | yes |  |  |  | Gets or sets the maximum number of registrations that can use this discount code. |
| MinRegistrants | yes | yes |  |  |  | Gets or sets the minimum number of registrants a registration is required to have in order to be able to use this discount code. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RegistrationTemplate |  | yes | yes |  |  | Gets or sets the RegistrationTemplate. |
| RegistrationTemplateDiscountAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| RegistrationTemplateId | yes | yes |  |  |  | Gets or sets the RegistrationTemplate identifier. |
| StartDate | yes | yes |  |  |  | Gets or sets the first day that the discount code can be used. |
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
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DiscountLimitsString | String representation of any discount limits. |
| DiscountString | Gets the discount string. |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RegistrationTemplate | Gets or sets the RegistrationTemplate. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| RegistrationTemplate | [RegistrationTemplate](registration-template.md) |  |
| RegistrationTemplateId | [RegistrationTemplate](registration-template.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
