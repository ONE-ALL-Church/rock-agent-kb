# Assessment Type Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `CRM`
- Model title: `AssessmentType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `36`
- Obsolete methods: `4`
- EntityType GUID: `d17a28ac-f529-4ab0-a790-c21f9e74ac89`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 21 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 13 |
| Related model links | 11 |
| Method signatures | 36 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AssessmentPath | yes | yes |  | yes |  | Gets or sets the AssessmentPath of the Assessment Type |
| AssessmentResultsPath | yes | yes |  |  |  | Gets or sets the AssessmentResultsPath of the Assessment or the Assessment Type if no requestor required. |
| AssessmentTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Assessments |  | yes | yes |  |  | Gets or sets the Collection of Assessments for each Assessment Type. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BadgeColor | yes | yes |  |  |  | Gets or sets the color of the badge. |
| BadgeSummaryLava | yes | yes |  |  |  | Gets or sets the badge summary lava. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the Description of the Assessment Type |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  | yes |  | Gets or sets the IsActive flag for the Assessment Type. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Assessment Type is a part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MinimumDaysToRetake | yes | yes |  |  |  | Gets or sets the number of days given for the Assessment Type. to be retaken. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RequiresRequest | yes | yes |  | yes |  | Gets or sets the RequiresRequest flag for the Assessment Type. |
| SupportedActions |  |  | yes |  |  |  |
| Title | yes | yes |  | yes |  | Gets or sets the Title of the Assessment Type |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidDuration | yes | yes |  |  |  | Gets or sets the number of days the assessment is valid for Assessment Type. How long (in days) is this assessment valid before it must be taken again. |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Assessments | Gets or sets the Collection of Assessments for each Assessment Type. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| AssessmentPath | [Assessment Type](assessment-type.md) | d17a28ac-f529-4ab0-a790-c21f9e74ac89 |
| AssessmentResultsPath | [Assessment](assessment.md) | 6dcd8ff0-4bfd-4af7-8f4f-e387934775a3 |
| AssessmentResultsPath | [Assessment Type](assessment-type.md) | d17a28ac-f529-4ab0-a790-c21f9e74ac89 |
| Assessments | [Assessment Type](assessment-type.md) | d17a28ac-f529-4ab0-a790-c21f9e74ac89 |
| Description | [Assessment Type](assessment-type.md) | d17a28ac-f529-4ab0-a790-c21f9e74ac89 |
| IsActive | [Assessment Type](assessment-type.md) | d17a28ac-f529-4ab0-a790-c21f9e74ac89 |
| IsSystem | [Assessment Type](assessment-type.md) | d17a28ac-f529-4ab0-a790-c21f9e74ac89 |
| MinimumDaysToRetake | [Assessment Type](assessment-type.md) | d17a28ac-f529-4ab0-a790-c21f9e74ac89 |
| RequiresRequest | [Assessment Type](assessment-type.md) | d17a28ac-f529-4ab0-a790-c21f9e74ac89 |
| Title | [Assessment Type](assessment-type.md) | d17a28ac-f529-4ab0-a790-c21f9e74ac89 |
| ValidDuration | [Assessment Type](assessment-type.md) | d17a28ac-f529-4ab0-a790-c21f9e74ac89 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
