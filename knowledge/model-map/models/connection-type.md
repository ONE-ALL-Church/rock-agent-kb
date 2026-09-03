# Connection Type Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Engagement`
- Model title: `ConnectionType`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `38`
- Obsolete methods: `5`
- EntityType GUID: `b1e52ead-65bd-4c4d-bccd-73368067621d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 69 |
| Database-marked properties | 33 |
| Lava-marked properties | 53 |
| Lava-marked non-database properties | 21 |
| Related model links | 11 |
| Method signatures | 38 |
| Obsolete methods | 5 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  | Additional configuration settings stored as JSON. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ConnectionActivityTypes |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionActivityTypes who are associated with the ConnectionType. |
| ConnectionOpportunities |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionOpportunities who are associated with the ConnectionType. |
| ConnectionRequestDetailPage |  | yes | yes |  |  | Gets or sets the connection request detail Page. |
| ConnectionRequestDetailPageId | yes | yes |  |  |  | Gets or sets the connection request detail Page identifier. |
| ConnectionRequestDetailPageRoute |  | yes | yes |  |  | Gets or sets the connection request detail Page Route. |
| ConnectionRequestDetailPageRouteId | yes | yes |  |  |  | Gets or sets the connection request detail Page Route identifier. |
| ConnectionStatuses |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionStatuses who are associated with the ConnectionType. |
| ConnectionTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| ConnectionTypeSources |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionTypeSources that are associated with the ConnectionType. |
| ConnectionWorkflows |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionWorkflows who are associated with the ConnectionType. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DaysUntilRequestIdle | yes | yes |  |  |  | Gets or sets the number of days until the request is considered idle. |
| DefaultView | yes | yes |  |  |  | Gets or sets the default view mode (list or board). This is a hard coded list of values defined in the code as an enumeration. |
| Description | yes | yes |  |  |  | Gets or sets the description. |
| DueDateCalculationMode | yes | yes |  |  |  | Determines how the due date for a request is calculated. This is a hard coded list of values defined in the code as an enumeration. |
| EnableFullActivityList | yes | yes |  | yes |  | Gets or sets a value indicating whether full activity lists are enabled. |
| EnableFutureFollowup | yes | yes |  | yes |  | Gets or sets a value indicating whether future follow-ups are enabled. |
| EnableRequestSecurity | yes |  |  | yes |  | Gets or sets a value indicating whether [enable request security]. |
| EnabledFeatures | yes | yes |  |  |  | Flags that specify which optional features are enabled for this connection type. This is a hard coded list of values defined in the code as an enumeration. |
| EnabledViews | yes | yes |  |  |  | Flags that specify which request views are enabled for this connection type. This is a hard coded list of values defined in the code as an enumeration. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Guid | yes | yes |  |  |  |  |
| IconCssClass | yes | yes |  |  |  | Gets or sets the icon CSS class. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsActive | yes | yes |  | yes |  | Gets or sets a value indicating whether this instance is active. |
| IsSequentialStatusEnforced | yes | yes |  |  |  | Determines whether requests must move through statuses in a defined sequence. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| Name | yes | yes |  | yes |  | Gets or sets the name. |
| Order | yes | yes |  |  |  | Gets or sets the order. |
| OwnerPersonAlias |  | yes | yes |  |  | Gets or sets the owner Person Alias. |
| OwnerPersonAliasId | yes | yes |  |  |  | Gets or sets the owner Person Alias identifier. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RequestBadgeLava | yes | yes |  |  |  | Gets or sets the request badge lava. |
| RequestDueDateOffsetInDays | yes | yes |  |  |  | Number of days added to the calculated due date for a request. |
| RequestDueSoonOffsetInDays | yes | yes |  |  |  | Number of days before the due date when a request is considered "due soon." |
| RequestHeaderLava | yes | yes |  |  |  | Gets or sets the request header lava. |
| RequiresPlacementGroupToConnect | yes | yes |  | yes |  | Gets or sets a value indicating whether this connection type requires a placement group to connect. |
| SnippetCategory |  | yes | yes |  |  | The category used to organize and filter snippets for this connection type. |
| SnippetCategoryId | yes | yes |  |  |  | The category Id used to organize and filter snippets for this connection type. |
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
| ConnectionActivityTypes | Gets or sets a collection containing the ConnectionActivityTypes who are associated with the ConnectionType. |
| ConnectionOpportunities | Gets or sets a collection containing the ConnectionOpportunities who are associated with the ConnectionType. |
| ConnectionRequestDetailPage | Gets or sets the connection request detail Page. |
| ConnectionRequestDetailPageRoute | Gets or sets the connection request detail Page Route. |
| ConnectionStatuses | Gets or sets a collection containing the ConnectionStatuses who are associated with the ConnectionType. |
| ConnectionTypeSources | Gets or sets a collection containing the ConnectionTypeSources that are associated with the ConnectionType. |
| ConnectionWorkflows | Gets or sets a collection containing the ConnectionWorkflows who are associated with the ConnectionType. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| OwnerPersonAlias | Gets or sets the owner Person Alias. |
| SnippetCategory | The category used to organize and filter snippets for this connection type. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ConnectionActivityTypes | ConnectionActivityTypes | 97b143f0-cb9d-4652-8ff1-ff2fa1ea4945 |
| ConnectionOpportunities | ConnectionOpportunities | 79f64363-bc90-4109-9d31-a5eeb397cb2f |
| ConnectionRequestDetailPage | [Page](page.md) | e104dcdf-247c-4ced-a119-8cc51632761f |
| ConnectionRequestDetailPageId | [Page](page.md) | e104dcdf-247c-4ced-a119-8cc51632761f |
| ConnectionRequestDetailPageRoute | [Page Route](page-route.md) | 42c14361-67b2-472c-95be-ea8a9c511837 |
| ConnectionRequestDetailPageRouteId | [Page Route](page-route.md) | 42c14361-67b2-472c-95be-ea8a9c511837 |
| ConnectionStatuses | ConnectionStatuses | f3840c8b-63bf-4f98-ac4a-9336896e589b |
| ConnectionTypeSources | ConnectionTypeSources | 06fd04c5-8a18-43d1-ae13-3611344fb40a |
| ConnectionWorkflows | ConnectionWorkflows | 4eb8711f-7301-4699-a223-0505a7ceb20a |
| OwnerPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| OwnerPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
