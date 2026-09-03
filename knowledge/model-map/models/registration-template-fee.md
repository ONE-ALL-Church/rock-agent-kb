# Registration Template Fee Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Event`
- Model title: `RegistrationTemplateFee`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `2db3a441-6ca1-49d1-bb25-c744e2ffa457`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 48 |
| Database-marked properties | 19 |
| Lava-marked properties | 33 |
| Lava-marked non-database properties | 14 |
| Related model links | 2 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AllowMultiple | yes | yes |  |  |  | Gets or sets a value indicating if registrant can select multiple values for this fee. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ContextKey |  |  | yes |  |  |  |
| CostValue | yes | yes |  |  | yes | Gets or sets the cost(s) of the fee. Value is stored like: single = 20, multiple = L\|20,XL\|20,XXL\|25 or Small^10\|Medium^20\|Large^30\|XXL^40 |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DiscountApplies | yes | yes |  |  |  | Discount codes apply to this fee |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FeeItems |  | yes | yes |  |  | Gets or sets the fee items. |
| FeeType | yes | yes |  |  |  | Gets or sets the fee type ( single option vs multiple options ). This is a hard coded list of values defined in the code as an enumeration. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| HideWhenNoneRemaining | yes | yes |  |  |  | Gets or sets a value indicating whether [hide when none remaining]. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  | yes |  | Gets or sets a value indicating whether this instance is active. |
| IsRequired | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RegistrationTemplate |  | yes | yes |  |  | Gets or sets the Registration Template. |
| RegistrationTemplateFeeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| RegistrationTemplateId | yes | yes |  |  |  | Gets or sets the Registration Template identifier. |
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
| EntityStringValue |  |
| FeeItems | Gets or sets the fee items. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RegistrationTemplate | Gets or sets the Registration Template. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| RegistrationTemplate | [Registration Template](registration-template.md) | a01e3e99-a8ad-4c6c-baac-98795738ba70 |
| RegistrationTemplateId | [Registration Template](registration-template.md) | a01e3e99-a8ad-4c6c-baac-98795738ba70 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
