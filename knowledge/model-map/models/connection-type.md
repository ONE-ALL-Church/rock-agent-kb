# Connection Type Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Engagement`
- Model title: `ConnectionType`
- EntityType GUID: `b1e52ead-65bd-4c4d-bccd-73368067621d`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 59 |
| Database-marked properties | 25 |
| Lava-marked properties | 43 |
| Lava-marked non-database properties | 19 |
| Related model links | 10 |
| Pre-alpha changes touching this model | 10 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| ConnectionActivityTypes |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionActivityTypes who are associated with the ConnectionType. |
| ConnectionOpportunities |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionOpportunities who are associated with the ConnectionType. |
| ConnectionRequestDetailPage |  | yes | yes |  |  | Gets or sets the connection request detail Page. |
| ConnectionRequestDetailPageId | yes | yes |  |  |  | Gets or sets the connection request detail Page identifier. |
| ConnectionRequestDetailPageRoute |  | yes | yes |  |  | Gets or sets the connection request detail PageRoute. |
| ConnectionRequestDetailPageRouteId | yes | yes |  |  |  | Gets or sets the connection request detail PageRoute identifier. |
| ConnectionStatuses |  | yes | yes |  |  | Gets or sets a collection containing the ConnectionStatuses who are associated with the ConnectionType. |
| ConnectionTypeAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
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
| EnableFullActivityList | yes | yes |  | yes |  | Gets or sets a value indicating whether full activity lists are enabled. |
| EnableFutureFollowup | yes | yes |  | yes |  | Gets or sets a value indicating whether future follow-ups are enabled. |
| EnableRequestSecurity | yes |  |  | yes |  | Gets or sets a value indicating whether [enable request security]. |
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
| OwnerPersonAlias |  | yes | yes |  |  | Gets or sets the owner PersonAlias. |
| OwnerPersonAliasId | yes | yes |  |  |  | Gets or sets the owner PersonAlias identifier. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| RequestBadgeLava | yes | yes |  |  |  | Gets or sets the request badge lava. |
| RequestHeaderLava | yes | yes |  |  |  | Gets or sets the request header lava. |
| RequiresPlacementGroupToConnect | yes | yes |  | yes |  | Gets or sets a value indicating whether this connection type requires a placement group to connect. |
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
| ConnectionRequestDetailPageRoute | Gets or sets the connection request detail PageRoute. |
| ConnectionStatuses | Gets or sets a collection containing the ConnectionStatuses who are associated with the ConnectionType. |
| ConnectionWorkflows | Gets or sets a collection containing the ConnectionWorkflows who are associated with the ConnectionType. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| OwnerPersonAlias | Gets or sets the owner PersonAlias. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ConnectionActivityTypes | ConnectionActivityTypes |  |
| ConnectionOpportunities | ConnectionOpportunities |  |
| ConnectionRequestDetailPage | [Page](page.md) |  |
| ConnectionRequestDetailPageId | [Page](page.md) |  |
| ConnectionRequestDetailPageRoute | [PageRoute](page-route.md) |  |
| ConnectionRequestDetailPageRouteId | [PageRoute](page-route.md) |  |
| ConnectionStatuses | ConnectionStatuses |  |
| ConnectionWorkflows | ConnectionWorkflows |  |
| OwnerPersonAlias | [PersonAlias](person-alias.md) |  |
| OwnerPersonAliasId | [PersonAlias](person-alias.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | AdditionalSettingsJson |  |
| property_added | ConnectionTypeSources |  |
| property_added | DueDateCalculationMode |  |
| property_added | EnabledFeatures |  |
| property_added | EnabledViews |  |
| property_added | IsSequentialStatusEnforced |  |
| property_added | RequestDueDateOffsetInDays |  |
| property_added | RequestDueSoonOffsetInDays |  |
| property_added | SnippetCategory |  |
| property_added | SnippetCategoryId |  |
