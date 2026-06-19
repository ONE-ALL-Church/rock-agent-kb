# Assessment Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `CRM`
- Model title: `Assessment`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `6dcd8ff0-4bfd-4af7-8f4f-e387934775a3`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 48 |
| Database-marked properties | 18 |
| Lava-marked properties | 33 |
| Lava-marked non-database properties | 15 |
| Related model links | 6 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AssessmentAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| AssessmentResultData | yes | yes |  |  |  | Gets or sets the result data for the Assessment taken. |
| AssessmentType |  | yes | yes |  |  | Gets or sets the Assessment Type that represents the type of the assessment. |
| AssessmentTypeId | yes | yes |  | yes |  | Gets or sets the Id of the Assessment Type |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| CompletedDateTime | yes | yes |  |  |  | Gets or sets the date of when the Assessment was completed. |
| ContextKey |  |  | yes |  |  |  |
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
| LastReminderDate | yes | yes |  |  |  | Gets or sets the result last reminder date. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAlias |  | yes | yes |  |  | Gets or sets the person alias Person associated with the Assessment. |
| PersonAliasId | yes | yes |  | yes |  | Gets or sets the Id of the person Person who is associated with the assessment. |
| RequestedDateTime | yes | yes |  |  |  | Gets or sets the date when the assessment was requested. |
| RequestedDueDate | yes | yes |  |  |  | Gets or sets the date of the requested due date. |
| RequesterPersonAlias |  | yes | yes |  |  | Gets or sets the person alias Person requesting the Assessment. |
| RequesterPersonAliasId | yes | yes |  |  |  | Gets or sets the RequesterPersonAliasId of the Person that requested the assessment. |
| Status | yes | yes |  | yes |  | Gets or sets the enum of the assessment status. Requirement from Jon, a pending assessment will stay in a pending status if it was never taken, even if a new one is requested. This is a hard coded list of values defined in the code as an enumeration. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AssessmentType | Gets or sets the Assessment Type that represents the type of the assessment. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| PersonAlias | Gets or sets the person alias Person associated with the Assessment. |
| RequesterPersonAlias | Gets or sets the person alias Person requesting the Assessment. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AssessmentType | [Assessment Type](assessment-type.md) | d17a28ac-f529-4ab0-a790-c21f9e74ac89 |
| AssessmentTypeId | [Assessment Type](assessment-type.md) | d17a28ac-f529-4ab0-a790-c21f9e74ac89 |
| PersonAlias | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| PersonAliasId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| RequesterPersonAlias | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |
| RequesterPersonAliasId | [Person](person.md) | 72657ed8-d16e-492e-ac12-144c5e7567e7 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
