# Group Sync Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `Group`
- Model title: `GroupSync`
- EntityType GUID: `1c011499-1122-4429-9afa-6578798e18a9`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 53 |
| Database-marked properties | 19 |
| Lava-marked properties | 38 |
| Lava-marked non-database properties | 19 |
| Related model links | 8 |
| Pre-alpha changes touching this model | 4 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AddUserAccountsDuringSync | yes | yes |  |  |  | Gets or sets a value indicating whether [add user accounts during synchronize]. |
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
| ExitSystemCommunication |  | yes | yes |  |  | Gets or sets the exit SystemCommunication. |
| ExitSystemCommunicationId | yes | yes |  |  |  | Gets or sets the exit SystemCommunication identifier. |
| ExitSystemEmail |  | yes | yes |  |  | [Obsoleted in v10] Use ExitSystemCommunication instead. Gets or sets the exit system email. |
| ExitSystemEmailId | yes | yes |  |  |  | [Obsoleted in v10] Use ExitSystemCommunicationId instead. Gets or sets the exit system email identifier. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Group. |
| GroupId | yes | yes |  | yes |  | Gets or sets the Group identifier. |
| GroupSyncAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupTypeRole |  | yes | yes |  |  | Gets or sets the GroupTypeRole. |
| GroupTypeRoleId | yes | yes |  | yes |  | Gets or sets the GroupTypeRole identifier. |
| Guid | yes | yes |  |  |  |  |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastRefreshDateTime | yes | yes |  |  |  | Gets or sets the last refresh date time. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ScheduleIntervalMinutes | yes | yes |  |  |  | Gets or sets the schedule interval minutes. |
| SupportedActions |  |  | yes |  |  |  |
| SyncDataView |  | yes | yes |  |  | Gets or sets the syncDataview. |
| SyncDataViewId | yes | yes |  | yes |  | Gets or sets the synchronize DataView identifier. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WelcomeSystemCommunication |  | yes | yes |  |  | Gets or sets the welcome SystemCommunication. |
| WelcomeSystemCommunicationId | yes | yes |  |  |  | Gets or sets the welcome system email identifier. |
| WelcomeSystemEmail |  | yes | yes |  |  | [Obsoleted in v10] Use WelcomeSystemCommunication instead. Gets or sets the welcome system email. |
| WelcomeSystemEmailId | yes | yes |  |  |  | [Obsoleted in v10] Use WelcomeSystemCommunicationId instead. Gets or sets the welcome system email identifier. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| ExitSystemCommunication | Gets or sets the exit SystemCommunication. |
| ExitSystemEmail | [Obsoleted in v10] Use ExitSystemCommunication instead. Gets or sets the exit system email. |
| Group | Gets or sets the Group. |
| GroupTypeRole | Gets or sets the GroupTypeRole. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| SyncDataView | Gets or sets the syncDataview. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WelcomeSystemCommunication | Gets or sets the welcome SystemCommunication. |
| WelcomeSystemEmail | [Obsoleted in v10] Use WelcomeSystemCommunication instead. Gets or sets the welcome system email. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ExitSystemCommunication | [SystemCommunication](system-communication.md) |  |
| ExitSystemCommunicationId | [SystemCommunication](system-communication.md) |  |
| Group | [Group](group.md) |  |
| GroupId | [Group](group.md) |  |
| GroupTypeRole | [GroupTypeRole](group-type-role.md) |  |
| GroupTypeRoleId | [GroupTypeRole](group-type-role.md) |  |
| SyncDataViewId | [DataView](data-view.md) |  |
| WelcomeSystemCommunication | [SystemCommunication](system-communication.md) |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_removed | ExitSystemEmail |  |
| property_removed | ExitSystemEmailId |  |
| property_removed | WelcomeSystemEmail |  |
| property_removed | WelcomeSystemEmailId |  |
