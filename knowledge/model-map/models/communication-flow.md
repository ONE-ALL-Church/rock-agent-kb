# Communication Flow Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Communication`
- Model title: `CommunicationFlow`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `c7a67172-9a41-4421-94b0-f59dfeacf705`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 56 |
| Database-marked properties | 24 |
| Lava-marked properties | 39 |
| Lava-marked non-database properties | 17 |
| Related model links | 0 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Category |  | yes | yes |  |  | Gets or sets the Category. |
| CategoryId | yes | yes |  |  |  | Gets or sets the Category identifier. |
| CommunicationFlowAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| CommunicationFlowCommunications |  | yes | yes |  |  | Gets or sets the communications for this Communication Flow. |
| CommunicationFlowInstances |  | yes | yes |  |  | Gets or sets the instances for this Communication Flow. |
| ContextKey |  |  | yes |  |  |  |
| ConversionGoalTargetPercent | yes | yes |  |  |  | Gets or sets the percentage of recipients expected to complete the conversion goal. |
| ConversionGoalTimeframeInDays | yes | yes |  |  |  | Gets or sets the timeframe (in days) for achieving the conversion goal. |
| ConversionGoalType | yes | yes |  |  |  | Gets or sets the conversion goal type for this Communication Flow. This is a hard coded list of values defined in the code as an enumeration. |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Description | yes | yes |  |  |  | Gets or sets the description. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ExitConditionType | yes | yes |  |  |  | Gets or sets the condition for when a recipient no longer receives messages from this Communication Flow. This is a hard coded list of values defined in the code as an enumeration. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  | yes |  | Gets or sets a flag indicating if this is an active Communication Flow. |
| IsConversionGoalTrackingClosed | yes |  |  |  |  | Gets or sets a value indicating whether conversion goal tracking is complete for all instances in this flow and no future instances will be created. |
| IsMessagingClosed | yes |  |  |  |  | Gets or sets a value indicating whether all flow instances are messaging-complete and the flow schedule will not create any new instances. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name of the Communication Flow (maximum 100 characters). |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PublicName | yes | yes |  |  |  | Gets or sets the public name (maximum 500 characters). |
| Schedule |  | yes | yes |  |  | Gets or sets the Schedule for this Communication Flow. |
| ScheduleId | yes | yes |  |  |  | Gets or sets the Schedule identifier. |
| SupportedActions |  |  | yes |  |  |  |
| TargetAudienceDataView |  | yes | yes |  |  | Gets or sets the Data View used to define the initial target audience for this Communication Flow. |
| TargetAudienceDataViewId | yes | yes |  |  |  | Gets or sets the identifier of the Data View that defines the initial target audience for this Communication Flow. |
| TriggerType | yes | yes |  |  |  | Gets or sets a value indicating how this Communication Flow is triggered. This is a hard coded list of values defined in the code as an enumeration. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Category | Gets or sets the Category. |
| CommunicationFlowCommunications | Gets or sets the communications for this Communication Flow. |
| CommunicationFlowInstances | Gets or sets the instances for this Communication Flow. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| Schedule | Gets or sets the Schedule for this Communication Flow. |
| TargetAudienceDataView | Gets or sets the Data View used to define the initial target audience for this Communication Flow. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

No related entity links were present in the scraped Model Map for this model.

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
