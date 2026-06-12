# Attribute Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `Attribute`
- EntityType GUID: `5997c8d3-8840-4591-99a5-552919f90cbd`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 73 |
| Database-marked properties | 43 |
| Lava-marked properties | 59 |
| Lava-marked non-database properties | 16 |
| Related model links | 7 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AbbreviatedName | yes | yes |  |  |  | Gets or sets the shortened name of the attribute. If null or whitespace then the full name is returned. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AllowSearch | yes | yes |  | yes |  | Gets or sets whether this Attribute should be used in 'search by attribute value' UIs. For example, if you had a UI where you would allow the user to find people based on a list of attributes |
| AttributeColor | yes | yes |  |  |  | The color to visually distinguish the attribute. For example, AttributeColor might be used to set the color for the IconCssClass of the icon. |
| AttributeQualifiers |  | yes | yes |  |  | Gets or sets a collection containing the AttributeQualifiers for this Attribute. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Categories |  | yes | yes |  |  | Gets or sets the collection of Categories that this Attribute is associated with. NOTE: Since changes to Categories isn't tracked by ChangeTracker, set the ModifiedDateTime if Categories are modified. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DefaultPersistedCondensedHtmlValue | yes | yes |  |  |  | Gets or sets the default persisted condensed HTML value. |
| DefaultPersistedCondensedTextValue | yes | yes |  |  |  | Gets or sets the default persisted condensed text value. |
| DefaultPersistedHtmlValue | yes | yes |  |  |  | Gets or sets the default persisted HTML value. |
| DefaultPersistedTextValue | yes | yes |  |  |  | Gets or sets the default persisted text value. |
| DefaultValue | yes | yes |  |  |  | Gets or sets the Attribute's default value. |
| DefaultValueChecksum | yes | yes |  |  |  | Gets the value checksum. This is a hash of DefaultValue that is automatically calculated by the database. |
| Description | yes | yes |  |  |  | Gets or sets the description of the Attribute. |
| EnableHistory | yes | yes |  |  |  | Gets or sets a value indicating whether changes to this attribute's attribute values should be logged in AttributeValueHistorical |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| EntityType |  | yes | yes |  |  | Gets or sets the EntityType that this Attribute is used to configure. This property will not be populated if the Attribute is a Global (system) Attribute. |
| EntityTypeId | yes | yes |  |  |  | Gets or sets the EntityTypeId of the EntityType that this Attribute is used to configure. This property will not be populated if the Attribute is a Global (system) Attribute. |
| EntityTypeQualifierColumn | yes | yes |  |  |  | Gets or sets the entity type qualifier column that contains the value (see EntityTypeQualifierValue) that is used narrow the scope of the Attribute to a subset or specific instance of an EntityType. |
| EntityTypeQualifierValue | yes | yes |  |  |  | Gets or sets the entity type qualifier value that is used to narrow the scope of the Attribute to a subset or specific instance of an EntityType. |
| FieldType |  | yes | yes |  |  | Gets or sets the FieldType that is used to get/capture the value of the Attribute |
| FieldTypeId | yes | yes |  | yes |  | Gets or sets the FieldTypeId of the FieldType that is used to select/set the AttributeValue for this Attribute setting. The FieldType can also be used to enforce formatting of the attribute setting. This property is required. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the name of the icon CSS class. This property is only used for CSS based icons. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Gets or sets a value indicating whether this attribute is active. |
| IsAnalytic | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is analytic. NOTE: Only applies if this is an Attribute on an Entity that implements IAnalytic and has an [AnalyticAttributes] Attribute If this is true, the Analytic table for this entity should include a field for this attribute |
| IsAnalyticHistory | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is analytic history. Only applies if this is an Attribute on an Entity that implements IAnalyticHistorical and IsAnalytic is True If this is true and IsAnalytic is also true, a change in value of this Attribute on the Entity makes the CurrentRowIndicator=1 record to become CurrentRowIndicator=0, sets the ExpireDate, then a new row with CurrentRowIndicator=1 to be created |
| IsDefaultPersistedValueDirty | yes | yes |  |  |  | Gets or sets a value indicating whether the persisted values are considered dirty. If the values are dirty then it should be assumed that they are not in sync with the DefaultValue property. |
| IsGridColumn | yes | yes |  | yes |  | Gets or sets a flag indicating if this Attribute is a Grid Column? |
| IsIndexEnabled | yes | yes |  |  |  | Gets or sets a value indicating whether this instance is index enabled. |
| IsMultiValue | yes | yes |  | yes |  | Gets or sets a flag indicating if the Attribute supports multiple values. |
| IsPublic | yes | yes |  |  |  | Indicates whether or not this attribute should be displayed in public contexts (e.g., responding to an RSVP without logging in). |
| IsRequired | yes | yes |  | yes |  | Gets or sets a flag indicating if a value is required. |
| IsSuppressHistoryLogging | yes | yes |  |  |  | Gets or sets a flag indicating if changes to the attribute values should be recorded into the generic History log table. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Attribute is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| Key | yes | yes |  | yes |  | Gets sets the Key value that is used to reference and call the Attribute. This property is required. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the Name of the Attribute. This property is required. |
| Order | yes | yes |  | yes |  | Gets or sets the display order of the attribute. |
| ParentAuthority |  |  | yes |  |  | Gets the parent authority. |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PostHtml | yes | yes |  |  |  | Gets or sets any HTML to be rendered after the attribute's edit control |
| PreHtml | yes | yes |  |  |  | Gets or sets any HTML to be rendered before the attribute's edit control |
| ShowOnBulk | yes | yes |  |  |  | Gets or sets a flag indicating if this attribute shows when doing a bulk entry form. |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeQualifiers | Gets or sets a collection containing the AttributeQualifiers for this Attribute. |
| AttributeValues |  |
| Attributes |  |
| Categories | Gets or sets the collection of Categories that this Attribute is associated with. NOTE: Since changes to Categories isn't tracked by ChangeTracker, set the ModifiedDateTime if Categories are modified. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| EntityType | Gets or sets the EntityType that this Attribute is used to configure. This property will not be populated if the Attribute is a Global (system) Attribute. |
| FieldType | Gets or sets the FieldType that is used to get/capture the value of the Attribute |
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
| AttributeQualifiers | AttributeQualifiers |  |
| Categories | Categories |  |
| EntityType | [EntityType](entity-type.md) |  |
| EntityTypeId | [EntityType](entity-type.md) |  |
| FieldType | [FieldType](field-type.md) |  |
| FieldTypeId | [AttributeValue](attribute-value.md) |  |
| FieldTypeId | [FieldType](field-type.md) |  |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
