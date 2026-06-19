# Registration Template Form Field Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Event`
- Model title: `RegistrationTemplateFormField`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `38`
- Obsolete methods: `4`
- EntityType GUID: `a773caa2-2211-416b-bdd7-d907085b4441`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 54 |
| Database-marked properties | 24 |
| Lava-marked properties | 38 |
| Lava-marked non-database properties | 14 |
| Related model links | 4 |
| Method signatures | 38 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Attribute |  | yes | yes |  |  | Gets or sets the Attribute. |
| AttributeId | yes | yes |  |  |  | Gets or sets the Attribute identifier. |
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
| FieldSource | yes | yes |  |  |  | Gets or sets the source of the field value. This is a hard coded list of values defined in the code as an enumeration. |
| FieldVisibilityRules |  |  | yes |  |  | Gets or sets the field visibility rules. |
| FieldVisibilityRulesJSON | yes | yes |  |  |  | JSON Serialized FieldVisibilityRules |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsGridField | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is grid field. |
| IsInternal | yes | yes |  |  |  | Gets or sets a value indicating whether this field is only for administrative, and not shown in the public form |
| IsLockedIfValuesExist | yes | yes |  |  |  | Gets or sets a value indicating whether editing the field is restricted when a value is already on the person's record. |
| IsRequired | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is required. |
| IsSharedValue | yes | yes |  |  |  | Gets or sets a value indicating whether this is a 'shared value'. If so, the value entered will default to the value entered for first person registered. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonFieldType | yes | yes |  |  |  | Gets or sets the type of the person field. This is a hard coded list of values defined in the code as an enumeration. |
| PostText | yes | yes |  |  |  | Gets or sets the Post-HTML. |
| PreText | yes | yes |  |  |  | Gets or sets the Pre-HTML. |
| RegistrationTemplateForm |  | yes | yes |  |  | Gets or sets the Registration Template Form. |
| RegistrationTemplateFormFieldAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| RegistrationTemplateFormId | yes | yes |  |  |  | Gets or sets the Registration Template Form identifier. |
| ShowCurrentValue | yes | yes |  |  |  | Gets or sets a value indicating whether [show current value]. |
| ShowOnWaitlist | yes | yes |  |  |  | Gets or sets a value indicating whether the field should be shown on a waitlist. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Attribute | Gets or sets the Attribute. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RegistrationTemplateForm | Gets or sets the Registration Template Form. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Attribute | [Attribute](attribute.md) | 5997c8d3-8840-4591-99a5-552919f90cbd |
| AttributeId | [Attribute](attribute.md) | 5997c8d3-8840-4591-99a5-552919f90cbd |
| RegistrationTemplateForm | [Registration Template Form](registration-template-form.md) | 2f0b3a6a-4e47-45a8-a331-7234ce711356 |
| RegistrationTemplateFormId | [Registration Template Form](registration-template-form.md) | 2f0b3a6a-4e47-45a8-a331-7234ce711356 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
