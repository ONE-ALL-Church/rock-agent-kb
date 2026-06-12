# Assessment Type Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `CRM`
- Model title: `AssessmentType`
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
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AssessmentPath | yes | yes |  | yes |  | Gets or sets the AssessmentPath of the AssessmentType |
| AssessmentResultsPath | yes | yes |  |  |  | Gets or sets the AssessmentResultsPath of the Assessment or the AssessmentType if no requestor required. |
| AssessmentTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| Assessments |  | yes | yes |  |  | Gets or sets the Collection of Assessments for each AssessmentType. |
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
| Description | yes | yes |  |  |  | Gets or sets the Description of the AssessmentType |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  | yes |  | Gets or sets the IsActive flag for the AssessmentType. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this AssessmentType is a part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| MinimumDaysToRetake | yes | yes |  |  |  | Gets or sets the number of days given for the AssessmentType. to be retaken. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RequiresRequest | yes | yes |  | yes |  | Gets or sets the RequiresRequest flag for the AssessmentType. |
| SupportedActions |  |  | yes |  |  |  |
| Title | yes | yes |  | yes |  | Gets or sets the Title of the AssessmentType |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidDuration | yes | yes |  |  |  | Gets or sets the number of days the assessment is valid for AssessmentType. How long (in days) is this assessment valid before it must be taken again. |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| Assessments | Gets or sets the Collection of Assessments for each AssessmentType. |
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
| AssessmentPath | [AssessmentType](assessment-type.md) |  |
| AssessmentResultsPath | [Assessment](assessment.md) |  |
| AssessmentResultsPath | [AssessmentType](assessment-type.md) |  |
| Assessments | [AssessmentType](assessment-type.md) |  |
| Description | [AssessmentType](assessment-type.md) |  |
| IsActive | [AssessmentType](assessment-type.md) |  |
| IsSystem | [AssessmentType](assessment-type.md) |  |
| MinimumDaysToRetake | [AssessmentType](assessment-type.md) |  |
| RequiresRequest | [AssessmentType](assessment-type.md) |  |
| Title | [AssessmentType](assessment-type.md) |  |
| ValidDuration | [AssessmentType](assessment-type.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
