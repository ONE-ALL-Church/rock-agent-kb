# Automation Trigger Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Core`
- Model title: `AutomationTrigger`
- EntityType GUID: `89abfa37-68e5-41b7-b43c-a0cf823dea61`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 44 |
| Database-marked properties | 15 |
| Lava-marked properties | 29 |
| Lava-marked non-database properties | 14 |
| Related model links | 6 |
| Pre-alpha changes touching this model | 3 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AutomationEvents |  | yes | yes |  |  | A collection containing the AutomationEvent items that will be executed when this trigger fires. |
| AutomationTriggerAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| AvailableKeys |  |  | yes |  |  |  |
| ComponentConfigurationJson | yes | yes |  |  |  | The configuration data for the AutomationTriggerComponent. This is stored as a dictionary of string key/value pairs. |
| ComponentEntityType |  | yes | yes |  |  | The EntityType that represents the AutomationTriggerComponent that will handle the logic for this trigger. |
| ComponentEntityTypeId | yes | yes |  |  |  | The EntityType identifier of the AutomationTriggerComponent that will handle the logic for this trigger. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | The description of the trigger. This is used to provide additional details about when the trigger will execute the events and describe the purpose the trigger serves. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  |  |  | Indicates if this trigger is active. If this is set to false then the trigger will not be initialized and no events will execute. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | The name of the trigger. This is used to identify the trigger in the user interface and logs. It should be short, but descriptive. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
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
| AutomationEvents | A collection containing the AutomationEvent items that will be executed when this trigger fires. |
| ComponentEntityType | The EntityType that represents the AutomationTriggerComponent that will handle the logic for this trigger. |
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
| AutomationEvents | [AutomationEvent](automation-event.md) |  |
| ComponentConfigurationJson | AutomationTriggerComponent |  |
| ComponentEntityType | AutomationTriggerComponent |  |
| ComponentEntityType | [EntityType](entity-type.md) |  |
| ComponentEntityTypeId | AutomationTriggerComponent |  |
| ComponentEntityTypeId | [EntityType](entity-type.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | ComponentConfigurationJson | related_entity_links |
| property_changed | ComponentEntityType | related_entity_links |
| property_changed | ComponentEntityTypeId | related_entity_links |
