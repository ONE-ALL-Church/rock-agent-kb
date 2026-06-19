# Registration Template Fee Item Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Event`
- Model title: `RegistrationTemplateFeeItem`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `35`
- Obsolete methods: `4`
- EntityType GUID: `cc1db3ff-a145-49ce-adc0-b8960ebf37d4`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 43 |
| Database-marked properties | 15 |
| Lava-marked properties | 28 |
| Lava-marked non-database properties | 13 |
| Related model links | 2 |
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
| IsActive | yes | yes |  | yes |  | Gets or sets a value indicating whether this instance is active. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MaximumUsageCount | yes | yes |  |  |  | Gets or sets the maximum number of times this fee item can be used per registration instance. |
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
| RegistrationTemplateFee |  | yes | yes |  |  | Gets or sets the Registration Template Fee. |
| RegistrationTemplateFeeId | yes | yes |  |  |  | Gets or sets the Registration Template Fee identifier. |
| RegistrationTemplateFeeItemAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
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
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RegistrationTemplateFee | Gets or sets the Registration Template Fee. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| RegistrationTemplateFee | [Registration Template Fee](registration-template-fee.md) | 2db3a441-6ca1-49d1-bb25-c744e2ffa457 |
| RegistrationTemplateFeeId | [Registration Template Fee](registration-template-fee.md) | 2db3a441-6ca1-49d1-bb25-c744e2ffa457 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
