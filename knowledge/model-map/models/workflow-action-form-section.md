# Workflow Action Form Section Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Workflow`
- Model title: `WorkflowActionFormSection`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `90af7254-87a2-42cb-b2f6-d4d53d7e30a0`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 46 |
| Database-marked properties | 16 |
| Lava-marked properties | 30 |
| Lava-marked non-database properties | 14 |
| Related model links | 2 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 1 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
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
| Description | yes | yes |  |  |  | Gets or sets the description to display under the Title. |
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
| Order | yes | yes |  | yes |  | Gets or sets the order. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| SectionType |  | yes | yes |  |  | Gets or sets the Section Type Defined Value for this Action Form Section. |
| SectionTypeValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the Defined Value that represents the SectionType for this Workflow Action Form Section. These are found in the Section Type Defined Type. |
| SectionVisibilityRules |  |  | yes |  |  | Gets or sets the section visibility rules. |
| SectionVisibilityRulesJSON | yes | yes |  |  |  | Gets or sets the section visibility rules json. |
| ShowHeadingSeparator | yes | yes |  |  |  | Gets or sets a value indicating whether to show heading separator after the Title/Description |
| SupportedActions |  |  | yes |  |  |  |
| Title | yes | yes |  |  |  | Gets or sets the title to display in the Section |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowActionForm |  | yes | yes |  |  | Gets or sets the workflow action form. |
| WorkflowActionFormId | yes | yes |  | yes |  | Gets or sets the header. |
| WorkflowActionFormSectionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |

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
| SectionType | Gets or sets the Section Type Defined Value for this Action Form Section. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WorkflowActionForm | Gets or sets the workflow action form. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| SectionType | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| SectionTypeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | SectionTypeValueId | enum_values |
