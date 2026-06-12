# Interactive Experience Action Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Event`
- Model title: `InteractiveExperienceAction`
- EntityType GUID: `8635e7e7-3576-47ff-92de-30a69eb5d011`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 47 |
| Database-marked properties | 17 |
| Lava-marked properties | 32 |
| Lava-marked non-database properties | 15 |
| Related model links | 6 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| ActionEntityType |  | yes | yes |  |  | Gets or sets the EntityType of the action. |
| ActionEntityTypeId | yes | yes |  | yes |  | Gets or sets the EntityTypeId for the EntityType of action. This property is required. |
| ActionSettingsJson | yes | yes |  |  |  | Gets or sets the action settings json. |
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
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| InteractiveExperience |  | yes | yes |  |  | Gets or sets the InteractiveExperience that the InteractiveExperienceAction belongs to. |
| InteractiveExperienceActionAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| InteractiveExperienceId | yes | yes |  | yes |  | Gets or sets the Id of the InteractiveExperience that this InteractiveExperienceAction is associated with. This property is required. |
| IsModerationRequired | yes | yes |  | yes |  | Gets or sets a value indicating whether this instance is moderation required. |
| IsMultipleSubmissionAllowed | yes | yes |  | yes |  | Gets or sets a flag indicating if multiple submission allowed. |
| IsResponseAnonymous | yes | yes |  | yes |  | Gets or sets a value indicating if response anonymous. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Order | yes | yes |  |  |  | Gets or sets the sort order of this action. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ResponseVisualEntityType |  | yes | yes |  |  | Gets or sets the EntityType of the response visual. |
| ResponseVisualEntityTypeId | yes | yes |  |  |  | Gets or sets the EntityTypeId for the EntityType of the response visual. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| ActionEntityType | Gets or sets the EntityType of the action. |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| InteractiveExperience | Gets or sets the InteractiveExperience that the InteractiveExperienceAction belongs to. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| ResponseVisualEntityType | Gets or sets the EntityType of the response visual. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ActionEntityType | [EntityType](entity-type.md) |  |
| ActionEntityTypeId | [EntityType](entity-type.md) |  |
| InteractiveExperience | [InteractiveExperience](interactive-experience.md) |  |
| InteractiveExperienceId | [InteractiveExperience](interactive-experience.md) |  |
| ResponseVisualEntityType | [EntityType](entity-type.md) |  |
| ResponseVisualEntityTypeId | [EntityType](entity-type.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
