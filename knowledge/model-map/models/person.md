# Person Model Detail

- Track: `stable`
- Rock version: `18.2.4`
- Category: `CRM`
- Model title: `Person`
- EntityType GUID: `72657ed8-d16e-492e-ac12-144c5e7567e7`
- Source: [Model Map](https://rocksolidchurchdemo.com/admin/power-tools/model-map)

## Summary

| Metric | Count |
| --- | ---: |
| Properties | 143 |
| Database-marked properties | 72 |
| Lava-marked properties | 123 |
| Lava-marked non-database properties | 51 |
| Related model links | 38 |
| Pre-alpha changes touching this model | 14 |

## Properties

| Property | DB | Lava | NotMapped | Required | Obsolete | Description |
| --- | --- | --- | --- | --- | --- | --- |
| AccountProtectionProfile | yes | yes |  |  |  | Gets or sets the person's account protection profile, which determines the level of security applied to their account. Higher levels enforce stricter safeguards and limit automated changes. This is a hard coded list of values defined in the code as an enumeration. |
| AdditionalLavaFields |  |  | yes |  |  |  |
| Age | yes | yes |  |  |  | Gets the Person's age. |
| AgeBracket | yes | yes |  |  |  | Gets or sets the age bracket. This is a hard coded list of values defined in the code as an enumeration. |
| AgeClassification | yes | yes |  |  |  | Gets or sets the age classification of the Person. Note: This is computed on save, so any manual changes to this will be ignored. This is a hard coded list of values defined in the code as an enumeration. |
| AgePrecise |  | yes | yes |  |  | Gets the Person's precise age (includes the fraction of the year). |
| Aliases |  | yes | yes |  |  | Gets or sets the aliases for this person. |
| AllowsInteractiveBulkIndexing |  |  | yes |  |  | Gets a value indicating whether [allows interactive bulk indexing]. |
| AnniversaryDate | yes | yes |  |  |  | Gets or sets the date of the Person's wedding anniversary. This property is nullable if the Person is not married or their anniversary date is not known. |
| AttributeValueDefaults |  |  | yes |  |  |  |
| AttributeValues |  | yes | yes |  |  |  |
| Attributes |  | yes | yes |  |  |  |
| AvailableKeys |  |  | yes |  |  |  |
| BirthDate | yes | yes |  |  |  | Gets the Person's birth date. Note: Use set the Birthdate |
| BirthDateKey | yes | yes |  |  |  | Gets or sets the birth date key. |
| BirthDay | yes | yes |  |  |  | Gets or sets the day of the month portion of the Person's birth date. |
| BirthMonth | yes | yes |  |  |  | Gets or sets the month portion of the Person's birth date. |
| BirthYear | yes | yes |  |  |  | Gets or sets the year portion of the Person's birth date. |
| BirthdayDayOfWeek |  | yes | yes |  |  | Gets the day of the week the person's birthday falls on for the current year. |
| BirthdayDayOfWeekShort |  | yes | yes |  |  | Gets the day of the week the person's birthday falls on for the current year as a shortened string (e.g. Wed.) |
| CommunicationPreference | yes | yes |  |  |  | Gets or sets the communication preference. This is a hard coded list of values defined in the code as an enumeration. |
| ConnectionStatusValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the Person's connection status |
| ConnectionStatusValueId | yes | yes |  |  |  | Gets or sets the Id of the Connection Status DefinedValue representing the connection status of the Person. These are found in the "Connection Status" Defined Type. |
| ContextKey |  |  | yes |  |  |  |
| ContributionFinancialAccount |  |  | yes |  |  | Gets or sets the person's default FinancialAccount gift designation. |
| ContributionFinancialAccountId | yes | yes |  |  |  | Gets or sets the person's default financial account gift designation. |
| CreatedByPersonAlias |  |  | yes |  |  |  |
| CreatedByPersonAliasId | yes | yes |  |  |  |  |
| CreatedByPersonId |  | yes | yes |  |  |  |
| CreatedByPersonName |  | yes | yes |  |  |  |
| CreatedDateTime | yes | yes |  |  |  |  |
| CustomSortValue |  |  | yes |  |  |  |
| DaysToAnniversary |  | yes | yes |  |  | [Obsoleted in v0] Use the DaysToAnniversaryOrNull property instead. Gets the number of days until the Person's anniversary. This is an in-memory calculation. If needed in a LinqToSql query use DaysUntilAnniversary property instead |
| DaysToAnniversaryOrNull |  | yes | yes |  |  | Gets the number of days until the Person's next anniversary. This is an in-memory calculation. If needed in a LinqToSql query, use the DaysUntilAnniversary property instead. |
| DaysToBirthday |  | yes | yes |  |  | [Obsoleted in v0] Use the DaysToBirthdayOrNull property instead. Gets the number of days until the Person's birthday. This is an in-memory calculation. If needed in a LinqToSql query use DaysUntilBirthday property instead |
| DaysToBirthdayOrNull |  | yes | yes |  |  | Gets the number of days until the Person's next birthday. This is an in-memory calculation. If needed in a LinqToSql query, use the DaysUntilBirthday property instead. |
| DaysUntilAnniversary | yes | yes |  |  |  | Gets or sets the number of days until their next anniversary. This is a computed column and can be used in LinqToSql queries, but there is no in-memory calculation. Avoid using property outside of a linq query. Use DaysToAnniversary instead. NOTE: If their anniversary is Feb 29, and this isn't a leap year, it'll treat Feb 28th as their anniversary when doing this calculation |
| DaysUntilBirthday | yes | yes |  |  |  | Gets or sets the number of days until their next birthday. This is a computed column and can be used in LinqToSql queries, but there is no in-memory calculation. Avoid using this property outside of a linq query. Use DaysToBirthday property instead NOTE: If their birthday is Feb 29, and this isn't a leap year, it'll treat Feb 28th as their birthday when doing this calculation |
| DeceasedDate | yes | yes |  |  |  | Gets or sets the deceased date. |
| Email | yes | yes |  |  |  | Gets or sets the Person's email address. |
| EmailNote | yes | yes |  |  |  | Gets or sets a note about the Person's email address. |
| EmailPreference | yes | yes |  |  |  | Gets or sets the email preference. This is a hard coded list of values defined in the code as an enumeration. |
| EncryptedKey |  |  | yes |  |  | Creates and stores a new PersonToken for a person using the default ExpireDateTime and UsageLimit. Returns the encrypted URLEncoded Token which can be used as a rckipid. NOTE: Use the GetImpersonationParameter(...) methods to specify an expiration date, usage limit or pageid |
| EntityStringValue |  | yes | yes |  |  |  |
| EthnicityValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the Person's Ethnicity |
| EthnicityValueId | yes | yes |  |  |  | Gets or sets the Id of the Ethnicity DefinedValue representing the ethnicity of this person These are found in the "Person Ethnicity" Defined Type. |
| FirstName | yes | yes |  |  |  | Gets or sets the first name of the Person. |
| FirstNamePronunciationOverride | yes | yes |  |  |  | Gets or sets the First Name pronunciation override. |
| ForeignGuid | yes | yes |  |  |  |  |
| ForeignId | yes | yes |  |  |  |  |
| ForeignKey | yes | yes |  |  |  |  |
| FullName |  | yes | yes |  |  | Gets the Full Name of the Person using the NickName LastName Suffix format. |
| FullNameFormal |  | yes | yes |  |  | Gets the Full Name of the Person using the Title FirstName LastName Suffix format. |
| FullNameFormalReversed |  |  | yes |  |  | Gets the full name of the Person using the LastName, FirstName format. |
| FullNameReversed |  |  | yes |  |  | Gets the full name of the Person using the LastName, FirstName format. |
| Gender | yes | yes |  | yes |  | Gets or sets the gender of the Person. This property is required. This is a hard coded list of values defined in the code as an enumeration. |
| GivingGroup |  | yes | yes |  |  | Gets or sets the giving group. |
| GivingGroupId | yes | yes |  |  |  | Gets or sets the giving group id. If an individual would like their giving to be grouped with the rest of their family, this will be the id of their family group. If they elect to contribute on their own, this value will be null. |
| GivingId | yes | yes |  |  |  | Gets the computed giver identifier in the format G{GivingGroupId} if they are part of a GivingGroup, or P{Personid} if they give individually |
| GivingLeaderId | yes | yes |  |  |  | Gets or sets the giving leader's Person Id. Note: This is computed on save, so any manual changes to this will be ignored. |
| GradeFormatted |  | yes | yes |  |  | Gets the grade string. |
| GradeOffset |  | yes | yes |  |  | Gets or sets the grade offset, which is the number of years until their graduation date. This is used to determine which Grade (Defined Value) they are in |
| GraduationYear | yes | yes |  |  |  | Gets or sets the date of the Person's projected or actual high school graduation year. This value is used to determine what grade a student is in. |
| Guid | yes | yes |  |  |  |  |
| HasChatAlias |  | yes | yes |  |  | Gets a value indicating whether this Person has a chat-specific PersonAlias, indicating they have a presence in Rock's chat system. |
| HasGraduated |  | yes | yes |  |  | Gets the has graduated. |
| Id | yes | yes |  |  |  |  |
| IdKey |  | yes | yes |  |  |  |
| ImpersonationParameter |  | yes | yes |  |  | Creates and stores a new PersonToken for a person using the default ExpireDateTime and UsageLimit. Returns the encrypted URLEncoded Token along with the ImpersonationParameter key in the form of "rckipid={ImpersonationParameter}" |
| InactiveReasonNote | yes | yes |  |  |  | Gets or sets the Inactive Reason Note |
| Initials |  | yes | yes |  |  | Gets the initials for the person based on the nick name and last name. |
| IsChatOpenDirectMessageAllowed | yes | yes |  |  |  | Gets or sets whether the person can receive direct messages from anybody in the external chat system. Otherwise, only people that are members of a shared, non-public chat channel may initiate a new direct message with this person. If then the system default will be used. |
| IsChatProfilePublic | yes | yes |  |  |  | Gets or sets whether the person's profile is visible in chat. If then the system default will be used. |
| IsDeceased | yes | yes |  |  |  | Gets or sets a flag indicating if the Person is deceased. |
| IsEmailActive | yes | yes |  |  |  | Gets or sets a flag indicating if the Person's email address is active. |
| IsLockedAsChild | yes | yes |  |  |  | Gets or sets a flag indicating if the Person is locked as child. |
| IsSystem | yes | yes |  | yes |  | Gets or sets a flag indicating if this Person is part of the Rock core system/framework. This property is required. |
| IsValid |  |  | yes |  |  |  |
| Item |  |  | yes |  |  |  |
| LastName | yes | yes |  |  |  | Gets or sets the last name (Sir Name) of the Person. |
| LastNamePronunciationOverride | yes | yes |  |  |  | Gets or sets the last Name pronunciation override. |
| MaritalStatusValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the Person's marital status. |
| MaritalStatusValueId | yes | yes |  |  |  | Gets or sets Id of the Marital Status DefinedValue representing the Person's marital status. These are found in the "Marital Status" Defined Type. |
| Members |  | yes | yes |  |  | Gets or sets a collection of GroupMember entities representing the group memberships that are associated with this Person. |
| MiddleName | yes | yes |  |  |  | Gets or sets the middle name of the Person. |
| ModifiedAuditValuesAlreadyUpdated |  | yes | yes |  |  |  |
| ModifiedByPersonAlias |  |  | yes |  |  |  |
| ModifiedByPersonAliasId | yes | yes |  |  |  |  |
| ModifiedByPersonId |  | yes | yes |  |  |  |
| ModifiedByPersonName |  | yes | yes |  |  |  |
| ModifiedDateTime | yes | yes |  |  |  |  |
| NextAnniversary |  | yes | yes |  |  | Gets the next anniversary. |
| NextBirthDay |  | yes | yes |  |  | Gets the next birth day. |
| NickName | yes | yes |  |  |  | Gets or sets the nick name of the Person. If a nickname was not entered, the first name is used. |
| NickNamePronunciationOverride | yes | yes |  |  |  | Gets or sets the nick Name pronunciation override. |
| ParentAuthority |  |  | yes |  |  |  |
| ParentAuthorityPre |  |  | yes |  |  |  |
| PersonAttributeValues |  |  | yes |  |  | Gets the entity attribute values. This should only be used inside LINQ statements when building a where clause for the query. This property should only be used inside LINQ statements for filtering or selecting values. Do not use it for accessing the attributes after the entity has been loaded. |
| PhoneNumbers |  | yes | yes |  |  | Gets or sets a collection of PhoneNumbers |
| Photo |  | yes | yes |  |  | Gets or sets the BinaryFile that contains the Person's photo. |
| PhotoId | yes | yes |  |  |  | Gets or sets the Id of the BinaryFile that contains the photo of the Person. |
| PhotoUrl |  | yes | yes |  |  | Gets the URL of the person's photo. |
| PreferredLanguageValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the Person's preferred language. |
| PreferredLanguageValueId | yes | yes |  |  |  | Gets or sets the DefinedValueId of the DefinedValue that represents the Preferred Language for this person. |
| PrimaryAlias |  | yes | yes |  |  | Gets the primary alias. |
| PrimaryAliasGuid | yes | yes |  |  |  | Gets the primary alias identifier. |
| PrimaryAliasId | yes | yes |  |  |  | Gets the primary alias identifier. |
| PrimaryCampus |  | yes | yes |  |  | Gets or sets the person's primary campus. |
| PrimaryCampusId | yes | yes |  |  |  | Gets or sets the campus id for the primary family. Note: This is computed on save, so any manual changes to this will be ignored. |
| PrimaryFamily |  | yes | yes |  |  | Gets or sets the primary family. |
| PrimaryFamilyId | yes | yes |  |  |  | Gets or sets the group id for the PrimaryFamily. Note: This is computed on save, so any manual changes to this will be ignored. |
| PronunciationNote | yes | yes |  |  |  | Gets or sets the notes for the pronunciation. |
| RaceValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the Person's Race |
| RaceValueId | yes | yes |  |  |  | Gets or sets the Id of the Race DefinedValue representing the race of this person These are found in the "Person Race" Defined Type. |
| RecordSourceValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the record source. |
| RecordSourceValueId | yes | yes |  |  |  | Gets or sets the Id of the Record Source DefinedValue representing the source of this entity These are found in the "Record Source" Defined Type. |
| RecordStatusLastModifiedDateTime | yes | yes |  |  |  | Gets or sets the record status last modified date time. |
| RecordStatusReasonValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the Record Status Reason. |
| RecordStatusReasonValueId | yes | yes |  |  |  | Gets or sets the Id of the Record Status Reason DefinedValue representing the reason why a person record status would have a set status. These are found in the "Inactive Record Reason" Defined Type. |
| RecordStatusValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the record status. |
| RecordStatusValueId | yes | yes |  |  |  | Gets or sets the Id of the Record Status DefinedValue representing the status of this entity These are found in the "Record Status" Defined Type. |
| RecordTypeValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the RecordType. |
| RecordTypeValueId | yes | yes |  |  |  | Gets or sets the Id of the Person Record Type DefinedValue representing what type of Person Record this is. These are found in the "Record Type" Defined Type. |
| ReminderCount | yes | yes |  |  |  | Gets or sets the reminder count associated with the Person. |
| ReviewReasonNote | yes | yes |  |  |  | Gets or sets notes about why a person profile needs to be reviewed |
| ReviewReasonValue |  | yes | yes |  |  | Gets or sets the review reason value. |
| ReviewReasonValueId | yes | yes |  |  |  | Gets or sets the Id of the Defined Value DefinedValue representing the reason a record needs to be reviewed. These are found in the "Review Reason" Defined Type. |
| Signals |  |  | yes |  |  | Gets or sets the signals applied to this person. |
| SuffixValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the Person's name suffix. |
| SuffixValueId | yes | yes |  |  |  | Gets or sets the Id of the Person's name Suffix DefinedValue. These are found in the "Suffix" Defined Type. |
| SupportedActions |  |  | yes |  |  |  |
| SystemNote | yes | yes |  |  |  | Gets or sets the System Note |
| TitleValue |  | yes | yes |  |  | Gets or sets the DefinedValue representing the Person's salutation title. |
| TitleValueId | yes | yes |  |  |  | Gets or sets Id of the (Salutation) Tile DefinedValue that is associated with the Person These are found in the "Title" Defined Type. |
| TopSignalColor | yes | yes |  |  |  | Gets or sets the name of the top signal color. This property is used to indicate the icon color on a person if they have a related signal. |
| TopSignalIconCssClass | yes | yes |  |  |  | Gets or sets the name of the top signal CSS class. This property is used to indicate which icon to display on a person if they have a related signal. |
| TopSignalId | yes | yes |  |  |  | Gets or sets the highest priority PersonSignal associated with this person. |
| TypeId |  | yes | yes |  |  |  |
| TypeName |  | yes | yes |  |  |  |
| UrlEncodedKey |  | yes | yes |  |  | Creates and stores a new PersonToken for a person using the default ExpireDateTime and UsageLimit. Returns the encrypted URLEncoded Token which can be used as a rckipid. NOTE: Use the GetImpersonationParameter(...) methods to specify an expiration date, usage limit or pageid |
| Users |  | yes | yes |  |  | Gets or sets a collection containing the Person's UserLogins. |
| ValidationResults |  |  | yes |  |  |  |
| ViewedCount | yes | yes |  |  |  | Gets or sets the count of the number of times that the Person has been viewed. |

## Lava-Marked Non-Database Properties

| Property | Description |
| --- | --- |
| AgePrecise | Gets the Person's precise age (includes the fraction of the year). |
| Aliases | Gets or sets the aliases for this person. |
| AttributeValues |  |
| Attributes |  |
| BirthdayDayOfWeek | Gets the day of the week the person's birthday falls on for the current year. |
| BirthdayDayOfWeekShort | Gets the day of the week the person's birthday falls on for the current year as a shortened string (e.g. Wed.) |
| ConnectionStatusValue | Gets or sets the DefinedValue representing the Person's connection status |
| CreatedByPersonId |  |
| CreatedByPersonName |  |
| DaysToAnniversary | [Obsoleted in v0] Use the DaysToAnniversaryOrNull property instead. Gets the number of days until the Person's anniversary. This is an in-memory calculation. If needed in a LinqToSql query use DaysUntilAnniversary property instead |
| DaysToAnniversaryOrNull | Gets the number of days until the Person's next anniversary. This is an in-memory calculation. If needed in a LinqToSql query, use the DaysUntilAnniversary property instead. |
| DaysToBirthday | [Obsoleted in v0] Use the DaysToBirthdayOrNull property instead. Gets the number of days until the Person's birthday. This is an in-memory calculation. If needed in a LinqToSql query use DaysUntilBirthday property instead |
| DaysToBirthdayOrNull | Gets the number of days until the Person's next birthday. This is an in-memory calculation. If needed in a LinqToSql query, use the DaysUntilBirthday property instead. |
| EntityStringValue |  |
| EthnicityValue | Gets or sets the DefinedValue representing the Person's Ethnicity |
| FullName | Gets the Full Name of the Person using the NickName LastName Suffix format. |
| FullNameFormal | Gets the Full Name of the Person using the Title FirstName LastName Suffix format. |
| GivingGroup | Gets or sets the giving group. |
| GradeFormatted | Gets the grade string. |
| GradeOffset | Gets or sets the grade offset, which is the number of years until their graduation date. This is used to determine which Grade (Defined Value) they are in |
| HasChatAlias | Gets a value indicating whether this Person has a chat-specific PersonAlias, indicating they have a presence in Rock's chat system. |
| HasGraduated | Gets the has graduated. |
| IdKey |  |
| ImpersonationParameter | Creates and stores a new PersonToken for a person using the default ExpireDateTime and UsageLimit. Returns the encrypted URLEncoded Token along with the ImpersonationParameter key in the form of "rckipid={ImpersonationParameter}" |
| Initials | Gets the initials for the person based on the nick name and last name. |
| MaritalStatusValue | Gets or sets the DefinedValue representing the Person's marital status. |
| Members | Gets or sets a collection of GroupMember entities representing the group memberships that are associated with this Person. |
| ModifiedAuditValuesAlreadyUpdated |  |
| ModifiedByPersonId |  |
| ModifiedByPersonName |  |
| NextAnniversary | Gets the next anniversary. |
| NextBirthDay | Gets the next birth day. |
| PhoneNumbers | Gets or sets a collection of PhoneNumbers |
| Photo | Gets or sets the BinaryFile that contains the Person's photo. |
| PhotoUrl | Gets the URL of the person's photo. |
| PreferredLanguageValue | Gets or sets the DefinedValue representing the Person's preferred language. |
| PrimaryAlias | Gets the primary alias. |
| PrimaryCampus | Gets or sets the person's primary campus. |
| PrimaryFamily | Gets or sets the primary family. |
| RaceValue | Gets or sets the DefinedValue representing the Person's Race |
| RecordSourceValue | Gets or sets the DefinedValue representing the record source. |
| RecordStatusReasonValue | Gets or sets the DefinedValue representing the Record Status Reason. |
| RecordStatusValue | Gets or sets the DefinedValue representing the record status. |
| RecordTypeValue | Gets or sets the DefinedValue representing the RecordType. |
| ReviewReasonValue | Gets or sets the review reason value. |
| SuffixValue | Gets or sets the DefinedValue representing the Person's name suffix. |
| TitleValue | Gets or sets the DefinedValue representing the Person's salutation title. |
| TypeId |  |
| TypeName |  |
| UrlEncodedKey | Creates and stores a new PersonToken for a person using the default ExpireDateTime and UsageLimit. Returns the encrypted URLEncoded Token which can be used as a rckipid. NOTE: Use the GetImpersonationParameter(...) methods to specify an expiration date, usage limit or pageid |
| Users | Gets or sets a collection containing the Person's UserLogins. |

## Related Model Map Links

| Property | Related Model | EntityType GUID |
| --- | --- | --- |
| Aliases | aliases |  |
| ConnectionStatusValue | [DefinedValue](defined-value.md) |  |
| ConnectionStatusValueId | [DefinedValue](defined-value.md) |  |
| ContributionFinancialAccount | [FinancialAccount](financial-account.md) |  |
| EthnicityValue | [DefinedValue](defined-value.md) |  |
| EthnicityValueId | [DefinedValue](defined-value.md) |  |
| GivingGroupId | giving group |  |
| HasChatAlias | [Person](person.md) |  |
| HasChatAlias | [PersonAlias](person-alias.md) |  |
| MaritalStatusValue | [DefinedValue](defined-value.md) |  |
| MaritalStatusValueId | [DefinedValue](defined-value.md) |  |
| Members | [GroupMember](group-member.md) |  |
| PhoneNumbers | PhoneNumbers |  |
| Photo | [BinaryFile](binary-file.md) |  |
| PhotoId | [BinaryFile](binary-file.md) |  |
| PreferredLanguageValue | [DefinedValue](defined-value.md) |  |
| PreferredLanguageValueId | [DefinedValue](defined-value.md) |  |
| PrimaryAlias | primary alias |  |
| PrimaryAliasGuid | primary alias |  |
| PrimaryAliasId | primary alias |  |
| PrimaryCampus | primary campus |  |
| PrimaryFamily | primary family |  |
| RaceValue | [DefinedValue](defined-value.md) |  |
| RaceValueId | [DefinedValue](defined-value.md) |  |
| RecordSourceValue | [DefinedValue](defined-value.md) |  |
| RecordSourceValueId | [DefinedValue](defined-value.md) |  |
| RecordStatusReasonValue | [DefinedValue](defined-value.md) |  |
| RecordStatusReasonValueId | [DefinedValue](defined-value.md) |  |
| RecordStatusValue | [DefinedValue](defined-value.md) |  |
| RecordStatusValueId | [DefinedValue](defined-value.md) |  |
| RecordTypeValue | [DefinedValue](defined-value.md) |  |
| RecordTypeValueId | [DefinedValue](defined-value.md) |  |
| ReviewReasonValueId | [DefinedValue](defined-value.md) |  |
| SuffixValue | [DefinedValue](defined-value.md) |  |
| SuffixValueId | [DefinedValue](defined-value.md) |  |
| TitleValue | [DefinedValue](defined-value.md) |  |
| TitleValueId | [DefinedValue](defined-value.md) |  |
| Users | UserLogins |  |

## Stable To Pre-Alpha Changes

| Change | Property | Fields |
| --- | --- | --- |
| property_added | OutreachEnableDailyNotification |  |
| property_added | OutreachEnableSpecialEventsNotification |  |
| property_added | OutreachNotificationTimeOfDay |  |
| property_added | OutreachTouchpointGenerationEnabled |  |
| property_added | OutreachTouchpointSchedule |  |
| property_changed | BirthDate | description |
| property_changed | DaysToAnniversary | description, is_obsolete |
| property_changed | DaysToBirthday | description, is_obsolete |
| property_changed | EthnicityValueId | enum_values |
| property_changed | IsChatOpenDirectMessageAllowed | description |
| property_changed | IsChatProfilePublic | description |
| property_changed | RaceValueId | enum_values |
| property_changed | RecordSourceValueId | enum_values |
| property_changed | RecordTypeValueId | enum_values |
