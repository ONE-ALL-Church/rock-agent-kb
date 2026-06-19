# Workflow Action Form Model Detail

- Track: `stable`
- Rock version: `19.1.8`
- Category: `Workflow`
- Model title: `WorkflowActionForm`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `37`
- Obsolete methods: `4`
- EntityType GUID: `fdab9aeb-b2aa-4fb5-a35d-83254a9b014c`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 85 |
| Database-marked properties | 47 |
| Lava-marked properties | 70 |
| Lava-marked non-database properties | 23 |
| Related model links | 1 |
| Method signatures | 37 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 5 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| ActionAttributeGuid | yes | yes |  |  |  | An optional text attribute that will be updated with the action that was selected |
| Actions | yes | yes |  |  |  | Gets or sets the delimited list of action buttons and actions. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AdditionalSettingsJson | yes | yes |  |  |  |  |
| AllowNotes | yes | yes |  |  |  | Gets or sets whether Notes can be entered |
| AllowPersonEntry | yes | yes |  |  |  | Gets or sets a value indicating whether a new person (and spouse) can be added |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| Buttons |  | yes | yes |  |  | Gets or sets the buttons. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| Footer | yes | yes |  |  |  | Gets or sets the footer. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FormAttributes |  | yes | yes |  |  | Gets or sets the form attributes. |
| FormSections |  | yes | yes |  |  | Gets or sets the form attributes. |
| Guid | yes | yes |  |  |  |  |
| Header | yes | yes |  |  |  | Gets or sets the header. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IncludeActionsInNotification | yes | yes |  |  |  | Gets or sets a value indicating whether [include actions in notification]. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| NotificationSystemCommunication |  | yes | yes |  |  | Gets or sets the notification system communication. |
| NotificationSystemCommunicationId | yes | yes |  |  |  | Gets or sets the notification system communication identifier. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonEntryAddressEntryOption | yes | yes |  |  |  | Gets or sets the person entry address entry option. This is a hard coded list of values defined in the code as an enumeration. |
| PersonEntryAutofillCurrentPerson | yes | yes |  |  |  | Gets or sets a value indicating whether Person Entry should auto-fill with the CurrentPerson |
| PersonEntryBirthdateEntryOption | yes | yes |  |  |  | Gets or sets the person entry birthdate entry option. This is a hard coded list of values defined in the code as an enumeration. |
| PersonEntryCampusIsVisible | yes | yes |  |  |  | Gets or sets a value indicating whether [person entry show campus]. |
| PersonEntryCampusStatusValue |  | yes | yes |  |  | Gets or sets the person entry campus status value. |
| PersonEntryCampusStatusValueId | yes | yes |  |  |  | Gets or sets the person entry campus status value identifier. This and PersonEntryCampusTypeValueId will determine which campuses will selectable These are found in the Campus Status Defined Type. |
| PersonEntryCampusTypeValue |  | yes | yes |  |  | Gets or sets the person entry campus type value. |
| PersonEntryCampusTypeValueId | yes | yes |  |  |  | Gets or sets the person entry campus type value identifier. This and PersonEntryCampusStatusValueId will determine which campuses will selectable These are found in the Campus Type Defined Type. |
| PersonEntryConnectionStatusValue |  | yes | yes |  |  | Gets or sets the person entry connection status value |
| PersonEntryConnectionStatusValueId | yes | yes |  |  |  | Gets or sets the person entry connection status value identifier. These are found in the Connection Status Defined Type. |
| PersonEntryDescription | yes | yes |  |  |  | Gets or sets the Description to display under the PersonEntryTitle |
| PersonEntryEmailEntryOption | yes | yes |  |  |  | Gets or sets the person entry email entry option. This is a hard coded list of values defined in the code as an enumeration. |
| PersonEntryEthnicityEntryOption | yes | yes |  |  |  | Gets or sets the person entry ethnicity entry option. This is a hard coded list of values defined in the code as an enumeration. |
| PersonEntryFamilyAttributeGuid | yes | yes |  |  |  | Gets or sets the person entry family attribute unique identifier. (The one used to set the Added/Edited Person's Family to) |
| PersonEntryGenderEntryOption | yes | yes |  |  |  | Gets or sets the person entry gender entry option. This is a hard coded list of values defined in the code as an enumeration. |
| PersonEntryGroupLocationTypeValue |  | yes | yes |  |  | Gets or sets the person entry address type value identifier. |
| PersonEntryGroupLocationTypeValueId | yes | yes |  |  |  | Gets or sets the person entry address type value identifier. These are found in the Location Type Defined Type. |
| PersonEntryHideIfCurrentPersonKnown | yes | yes |  |  |  | Gets or sets a value indicating whether Person Entry should be hidden if the CurrentPerson is known |
| PersonEntryMaritalStatusEntryOption | yes | yes |  |  |  | Gets or sets the person entry marital status entry option. This is a hard coded list of values defined in the code as an enumeration. |
| PersonEntryMobilePhoneEntryOption | yes | yes |  |  |  | Gets or sets the person entry mobile phone entry option. This is a hard coded list of values defined in the code as an enumeration. |
| PersonEntryPersonAttributeGuid | yes | yes |  |  |  | Gets or sets the person entry person workflow attribute unique identifier. (The one used to set the Added/Edited Person to) |
| PersonEntryPostHtml | yes | yes |  |  |  | Gets or sets the person entry post HTML. |
| PersonEntryPreHtml | yes | yes |  |  |  | Gets or sets the person entry preHTML. |
| PersonEntryRaceEntryOption | yes | yes |  |  |  | Gets or sets the person entry race entry option. This is a hard coded list of values defined in the code as an enumeration. |
| PersonEntryRecordSourceValue |  | yes | yes |  |  | Gets or sets the person entry record source value identifier. |
| PersonEntryRecordSourceValueId | yes | yes |  |  |  | Gets or sets the person entry record source value identifier. These are found in the Record Source Defined Type. |
| PersonEntryRecordStatusValue |  | yes | yes |  |  | Gets or sets the person entry record status value identifier. |
| PersonEntryRecordStatusValueId | yes | yes |  |  |  | Gets or sets the person entry record status value identifier. These are found in the Record Status Defined Type. |
| PersonEntrySectionTypeValue |  | yes | yes |  |  | Gets or sets the person entry section type value. |
| PersonEntrySectionTypeValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the Defined Value that represents the SectionType for the Person Entry Section. These are found in the Section Type Defined Type. |
| PersonEntryShowHeadingSeparator | yes | yes |  |  |  | Gets or sets whether a heading separator should be display under the PersonEntryTitle and PersonEntryDescription |
| PersonEntrySmsOptInEntryOption | yes | yes |  |  |  | Gets or sets the person entry SMS opt in entry option. This is a hard coded list of values defined in the code as an enumeration. |
| PersonEntrySpouseAttributeGuid | yes | yes |  |  |  | Gets or sets the person entry spouse workflow attribute unique identifier. (The one used to set the Added/Edited Person's Spouse to) |
| PersonEntrySpouseEntryOption | yes | yes |  |  |  | Gets or sets the person entry spouse entry option. This is a hard coded list of values defined in the code as an enumeration. |
| PersonEntrySpouseLabel | yes | yes |  |  |  | Gets or sets the person entry spouse label. |
| PersonEntryTitle | yes | yes |  |  |  | Gets or sets the Title to display at the top the Person Entry Section |
| SupportedActions |  |  | yes |  |  |  |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkflowActionFormAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| Buttons | Gets or sets the buttons. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| EntityStringValue |  |
| FormAttributes | Gets or sets the form attributes. |
| FormSections | Gets or sets the form attributes. |
| IdKey |  |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| NotificationSystemCommunication | Gets or sets the notification system communication. |
| PersonEntryCampusStatusValue | Gets or sets the person entry campus status value. |
| PersonEntryCampusTypeValue | Gets or sets the person entry campus type value. |
| PersonEntryConnectionStatusValue | Gets or sets the person entry connection status value |
| PersonEntryGroupLocationTypeValue | Gets or sets the person entry address type value identifier. |
| PersonEntryRecordSourceValue | Gets or sets the person entry record source value identifier. |
| PersonEntryRecordStatusValue | Gets or sets the person entry record status value identifier. |
| PersonEntrySectionTypeValue | Gets or sets the person entry section type value. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| PersonEntrySectionTypeValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_changed | PersonEntryCampusStatusValueId | enum_values |
| property_changed | PersonEntryCampusTypeValueId | enum_values |
| property_changed | PersonEntryGroupLocationTypeValueId | enum_values |
| property_changed | PersonEntryRecordSourceValueId | enum_values |
| property_changed | PersonEntrySectionTypeValueId | enum_values |
