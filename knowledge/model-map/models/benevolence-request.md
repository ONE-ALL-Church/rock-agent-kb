# Benevolence Request Model Detail

- Track: `stable`
- Rock version: `19.2.0`
- Category: `Finance`
- Model title: `BenevolenceRequest`
- Table name: `not provided`
- Obsolete: `no`
- Method signatures: `34`
- Obsolete methods: `4`
- EntityType GUID: `cf0ce5c1-9286-4310-9b50-10d040f8ebd2`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 68 |
| Database-marked properties | 28 |
| Lava-marked properties | 50 |
| Lava-marked non-database properties | 22 |
| Related model links | 13 |
| Method signatures | 34 |
| Obsolete methods | 4 |
| Pre-alpha changes touching this model | 0 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AdditionalLavaFields |  |  | yes |  |  |  |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BenevolenceRequestAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| BenevolenceResults |  | yes | yes |  |  | Gets or sets a collection of BenevolenceResults |
| BenevolenceType |  | yes | yes |  |  | Gets or sets the benevolence type. |
| BenevolenceTypeId | yes | yes |  |  |  | Gets or sets the benevolence type identifier. |
| Campus |  | yes | yes |  |  | Gets or sets the Campus that this Benevolence Request is associated with. |
| CampusId | yes | yes |  |  |  | Gets or sets the campus identifier. |
| CaseWorkerPersonAlias |  | yes | yes |  |  | Gets or sets the case worker Person Alias. |
| CaseWorkerPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAliasId of the Person Alias who is the case worker for this request. |
| CellPhoneNumber | yes | yes |  |  |  | Gets or sets the Cell Phone Number of the person who requested benevolence. |
| ConnectionStatusValue |  | yes | yes |  |  | Gets or sets the Defined Value representing the Requester's connection status. |
| ConnectionStatusValueId | yes | yes |  |  |  | Gets or sets the Id of the Defined Value Defined Value representing the connection status of the Requester. These are found in the Connection Status Defined Type. |
| ContextKey |  |  | yes |  |  |  |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| Documents |  | yes | yes |  |  | Gets or sets the documents. |
| Email | yes | yes |  |  |  | Gets or sets the email address of the person requesting benevolence. |
| EncryptedKey |  |  | yes |  |  |  |
| EntityStringValue |  | yes | yes |  |  |  |
| FirstName | yes | yes |  | yes |  | Gets or sets the First Name of the person that this benevolence request is about. This property is required. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FullName |  |  | yes |  |  | Gets full name of the person for who the benevolence request is about. |
| FullNameReversed |  |  | yes |  |  | Gets the full name of the person who this benevolence request is about in Last Name, First Name format. |
| GovernmentId | yes | yes |  |  |  | Gets or sets the GovernmentId of the person who requested benevolence. |
| Guid | yes | yes |  |  |  |  |
| HomePhoneNumber | yes | yes |  |  |  | Gets or sets the Home Phone Number of the person who requested benevolence. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastName | yes | yes |  | yes |  | Gets or sets the Last Name of the person that this benevolence request is about. This property is required. |
| Location |  | yes | yes |  |  | Gets or sets the Location that is associated with this Benevolence Request. |
| LocationId | yes | yes |  |  |  | Gets or sets the Id of the Location that is associated with this BenevolenceRequest. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| ProvidedNextSteps | yes | yes |  |  |  | Gets or sets the provided next steps. |
| RequestDateKey | yes | yes |  |  |  | Gets the request date key. |
| RequestDateTime | yes | yes |  | yes |  | Gets or sets the date that this benevolence request was entered. |
| RequestSourceDate |  | yes | yes |  |  | Gets or sets the request source date. |
| RequestStatusValue |  | yes | yes |  |  | Gets or sets the Defined Value representing the Benevolence Request's status. |
| RequestStatusValueId | yes | yes |  | yes |  | Gets or sets the Id of the Defined Value Defined Value representing the status of the Benevolence Request. These are found in the Benevolence Request Status Defined Type. |
| RequestText | yes | yes |  | yes |  | Gets or sets the text/content of the request. |
| RequestedByPersonAlias |  | yes | yes |  |  | Gets or sets the requested by Person Alias. |
| RequestedByPersonAliasId | yes | yes |  |  |  | Gets or sets the PersonAliasId of the Person Alias who is submitting the BenevolenceRequest |
| ResultSummary | yes | yes |  |  |  | Gets or sets the summary of the request result. |
| SupportedActions |  |  | yes |  |  |  |
| TotalAmount |  |  | yes |  |  | Gets the total amount of benevolence given. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  |  |
| ValidationResults |  |  | yes |  |  |  |
| WorkPhoneNumber | yes | yes |  |  |  | Gets or sets the Work Phone Number of the person who requested benevolence. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AttributeValues |  |
| Attributes |  |
| BenevolenceResults | Gets or sets a collection of BenevolenceResults |
| BenevolenceType | Gets or sets the benevolence type. |
| Campus | Gets or sets the Campus that this Benevolence Request is associated with. |
| CaseWorkerPersonAlias | Gets or sets the case worker Person Alias. |
| ConnectionStatusValue | Gets or sets the Defined Value representing the Requester's connection status. |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| Documents | Gets or sets the documents. |
| EntityStringValue |  |
| IdKey |  |
| Location | Gets or sets the Location that is associated with this Benevolence Request. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| RequestSourceDate | Gets or sets the request source date. |
| RequestStatusValue | Gets or sets the Defined Value representing the Benevolence Request's status. |
| RequestedByPersonAlias | Gets or sets the requested by Person Alias. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey |  |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| BenevolenceResults | BenevolenceResults | a4929a2d-5b83-4535-a1d4-8a2c84fba581 |
| Campus | [Campus](campus.md) | 00096bed-9587-415e-8ad4-4e076ae8fbf0 |
| CaseWorkerPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| CaseWorkerPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| ConnectionStatusValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| ConnectionStatusValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| Documents | documents | 3d627f51-e262-454b-95a0-2ef97103bce1 |
| Location | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| LocationId | [Location](location.md) | 0d6410ad-c83c-47ac-af3d-616d09edf63b |
| RequestStatusValue | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| RequestStatusValueId | [Defined Value](defined-value.md) | 53d4bf38-c49e-4a52-8b0e-5e016fb9574e |
| RequestedByPersonAlias | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |
| RequestedByPersonAliasId | [Person Alias](person-alias.md) | 90f5e87b-f0d5-4617-8ae9-eb57e673f36f |

## Stable To Pre-Alpha Changes

No stable-to-pre-alpha changes were detected for this model.
