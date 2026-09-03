# Group Sync Model Detail

- Track: `stable`
- Rock version: `19.3.4`
- Category: `Group`
- Model title: `GroupSync`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `1c011499-1122-4429-9afa-6578798e18a9`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 49 |
| Database-marked properties | 17 |
| Lava-marked properties | 34 |
| Lava-marked non-database properties | 17 |
| Related model links | 8 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

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
| ExitSystemCommunication |  | yes | yes |  |  | Gets or sets the exit System Communication. |
| ExitSystemCommunicationId | yes | yes |  |  |  | Gets or sets the exit System Communication identifier. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| Group |  | yes | yes |  |  | Gets or sets the Group. |
| GroupId | yes | yes |  | yes |  | Gets or sets the Group identifier. |
| GroupSyncAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| GroupTypeRole |  | yes | yes |  |  | Gets or sets the Group Type Role. |
| GroupTypeRoleId | yes | yes |  | yes |  | Gets or sets the Group Type Role identifier. |
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
| SyncDataViewId | yes | yes |  | yes |  | Gets or sets the synchronize Data View identifier. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WelcomeSystemCommunication |  | yes | yes |  |  | Gets or sets the welcome System Communication. |
| WelcomeSystemCommunicationId | yes | yes |  |  |  | Gets or sets the welcome system email identifier. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| ExitSystemCommunication | Gets or sets the exit System Communication. |
| Group | Gets or sets the Group. |
| GroupTypeRole | Gets or sets the Group Type Role. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| SyncDataView | Gets or sets the syncDataview. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |
| WelcomeSystemCommunication | Gets or sets the welcome System Communication. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| ExitSystemCommunication | [System Communication](system-communication.md) | d0cad7c0-10fe-41ef-b89d-e6f0d22456c4 |
| ExitSystemCommunicationId | [System Communication](system-communication.md) | d0cad7c0-10fe-41ef-b89d-e6f0d22456c4 |
| Group | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupId | [Group](group.md) | 9bbfda11-0d22-40d5-902f-60adfbc88987 |
| GroupTypeRole | [Group Type Role](group-type-role.md) | d155c373-9e47-4c6a-badd-792f31af5fba |
| GroupTypeRoleId | [Group Type Role](group-type-role.md) | d155c373-9e47-4c6a-badd-792f31af5fba |
| SyncDataViewId | [Data View](data-view.md) | 57f8fa29-dcf1-4f74-8553-87e90f234139 |
| WelcomeSystemCommunication | [System Communication](system-communication.md) | d0cad7c0-10fe-41ef-b89d-e6f0d22456c4 |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
