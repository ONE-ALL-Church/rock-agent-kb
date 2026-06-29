# Lava Data Context Directory

Generated from public SparkDevNetwork/Rock source files. This directory answers which root objects are available in selected Lava rendering surfaces; use the Model Map after identifying a root object.

## Agent Use

1. Identify the rendering surface and context family.
2. Use this directory to find available root keys and nested paths.
3. Use `agent/model-map-digests.jsonl`, `uvx rock-kb model <slug>`, or `uvx rock-kb model-map get <slug>` to inspect properties for linked model roots.
4. Use `agent/lava-capabilities.jsonl` for filters, commands, and Lava behavior.
5. Treat rows marked for live verification as source-code leads that still depend on the page, block, communication, workflow, or label configuration.

## Coverage

- Lava context rows: `176`
- Public source files: `28`
- Machine-readable rows: `lava-contexts.jsonl` and `../../../agent/lava-contexts.jsonl`
- `assessment-lava`: 7
- `check-in-label`: 29
- `cms-block`: 16
- `communication`: 3
- `event-lava`: 11
- `event-registration`: 8
- `finance-lava`: 33
- `following`: 6
- `global`: 18
- `group-lava`: 12
- `mobile-block`: 19
- `utility-lava`: 4
- `workflow`: 10

## Context Rows

| Family | Surface | Root Key | Nested Path | Type | Model Map | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `assessment-lava` | Conflict profile Lava template | `Person` |  | Rock.Model.Person | `person` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Crm/ConflictProfile.cs#L390) |
| `assessment-lava` | DISC assessment Lava template | `Person` |  | Rock.Model.Person | `person` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Crm/Disc.cs#L404) |
| `assessment-lava` | Gifts assessment Lava template | `Person` |  | Rock.Model.Person | `person` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Crm/GiftsAssessment.cs#L352) |
| `assessment-lava` | Motivators assessment Lava templates | `GrowthScore` |  | object |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Crm/Motivators.cs#L638) |
| `assessment-lava` | Motivators assessment Lava templates | `MotivatorScores` |  | IEnumerable<MotivatorScore> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Crm/Motivators.cs#L637) |
| `assessment-lava` | Motivators assessment Lava templates | `MotivatorThemeScores` |  | IEnumerable<MotivatorThemeScore> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Crm/Motivators.cs#L636) |
| `assessment-lava` | Motivators assessment Lava templates | `Person` |  | Rock.Model.Person | `person` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Crm/Motivators.cs#L619) |
| `check-in-label` | Check-In Label Designer field definition | `source-boundary` |  | source-code boundary |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/LabelField.cs#L35) |
| `check-in-label` | Check-In Label Designer field-source directory | `source-boundary` |  | source-code boundary |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/FieldSourceHelper.cs#L42) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `AllAttendance` |  | List<LabelAttendanceDetail> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L59) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `AreaNames` |  | List<string> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L118) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `CheckInDateTime` |  | DateTime |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L123) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `CurrentDateTime` |  | DateTime |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L128) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `Family` |  | Rock.Model.Group | `group` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L66) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `GroupNames` |  | List<string> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L133) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `GroupRoleNames` |  | List<string> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L139) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `InProgressAchievementIds` |  | List<int> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L92) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `InProgressAchievements` |  | List<string> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L85) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `IsFirstTime` |  | bool |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L113) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `JustCompletedAchievementIds` |  | List<int> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L78) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `JustCompletedAchievements` |  | List<string> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L72) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `LocationNames` |  | List<string> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L144) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `Person` |  | Rock.Model.Person | `person` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L46) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `PersonAttendance` |  | List<LabelAttendanceDetail> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L52) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `PersonAttendance` | PersonAttendance.Area | Rock.Model.GroupType |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L176) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `PersonAttendance` | PersonAttendance.Group | Rock.Model.Group | `group` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L181) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `PersonAttendance` | PersonAttendance.IsFirstTime | LabelAttendanceDetail |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L175) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `PersonAttendance` | PersonAttendance.Location | Rock.Model.Location | `location` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L182) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `PersonAttendance` | PersonAttendance.Schedule | Rock.Model.Schedule | `schedule` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L183) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `PersonAttendance` | PersonAttendance.SecurityCode | LabelAttendanceDetail |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L184) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `PreviouslyCompletedAchievementIds` |  | List<int> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L106) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `PreviouslyCompletedAchievements` |  | List<string> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L99) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `ScheduleNames` |  | List<string> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L149) |
| `check-in-label` | Check-In Label Designer Person Dynamic Text | `SecurityCode` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs#L154) |
| `check-in-label` | Check-In Label Designer Person field sources | `PersonAttendance` | PersonAttendance.CheckedInByPerson | Rock.Model.Person | `person` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/FieldSourceHelper.cs#L212) |
| `check-in-label` | Check-In Label Designer Person field sources | `PersonAttendance` | PersonAttendance.Schedule | Rock.Model.Schedule | `schedule` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/FieldSourceHelper.cs#L299) |
| `cms-block` | CMS Content Channel Item View Lava template | `DetailPage` |  | int or string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelItemView.cs#L916) |
| `cms-block` | CMS Content Channel Item View Lava template | `DetailPageRoute` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelItemView.cs#L917) |
| `cms-block` | CMS Content Channel Item View Lava template | `Item` |  | Rock.Model.ContentChannelItem | `content-channel-item` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelItemView.cs#L896) |
| `cms-block` | CMS Content Channel Item View Lava template | `RockVersion` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelItemView.cs#L914) |
| `cms-block` | CMS Content Channel View Lava template | `ArchiveSummary` |  | IEnumerable<ArchiveSummary> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs#L1042) |
| `cms-block` | CMS Content Channel View Lava template | `ArchiveSummaryPageUrl` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs#L1048) |
| `cms-block` | CMS Content Channel View Lava template | `CurrentPageUrl` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs#L1044) |
| `cms-block` | CMS Content Channel View Lava template | `DetailPage` |  | PageReference route |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs#L990) |
| `cms-block` | CMS Content Channel View Lava template | `DetailPageRoute` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs#L991) |
| `cms-block` | CMS Content Channel View Lava template | `Item` |  | Rock.Model.ContentChannelItem | `content-channel-item` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs#L1026) |
| `cms-block` | CMS Content Channel View Lava template | `ItemTagList` |  | IEnumerable<Tag> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs#L1041) |
| `cms-block` | CMS Content Channel View Lava template | `Items` |  | IEnumerable<ContentChannelItem> | `content-channel-item` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs#L1040) |
| `cms-block` | CMS Content Channel View Lava template | `LinkedPages` |  | Dictionary<string, object> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs#L1039) |
| `cms-block` | CMS Content Channel View Lava template | `Pagination` |  | PaginationBag |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs#L1038) |
| `cms-block` | CMS Content Channel View Lava template | `Person` |  | Rock.Model.Person | `person` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs#L1019) |
| `cms-block` | CMS Content Channel View Lava template | `RockVersion` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs#L1043) |
| `communication` | Communication recipient additional merge values | `AdditionalMergeValues` |  | dynamic entity or scalar |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs#L151) |
| `communication` | Communication recipient merge values | `Communication` |  | Rock.Model.Communication | `communication` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs#L130) |
| `communication` | Communication recipient merge values | `Person` |  | Rock.Model.Person | `person` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs#L135) |
| `event-lava` | Calendar Lava block | `CurrentPerson` |  | Rock.Model.Person | `person` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/CalendarLava.ascx.cs#L587) |
| `event-lava` | Calendar Lava block | `DetailsPage` |  | PageReference route |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/CalendarLava.ascx.cs#L584) |
| `event-lava` | Calendar Lava block | `EventItemOccurrences` |  | IEnumerable<EventItemOccurrence> | `event-item-occurrence` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/CalendarLava.ascx.cs#L586) |
| `event-lava` | Calendar Lava block | `EventItems` |  | IEnumerable<EventItem> | `event-item` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/CalendarLava.ascx.cs#L585) |
| `event-lava` | Event Item Occurrence Lava block | `CampusContext` |  | Rock.Model.Campus | `campus` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/EventItemOccurrenceLava.ascx.cs#L190) |
| `event-lava` | Event Item Occurrence Lava block | `CurrentPerson` |  | Rock.Model.Person | `person` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/EventItemOccurrenceLava.ascx.cs#L246) |
| `event-lava` | Event Item Occurrence Lava block | `Event` |  | Rock.Model.EventItem | `event-item` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/EventItemOccurrenceLava.ascx.cs#L245) |
| `event-lava` | Event Item Occurrence Lava block | `EventItemOccurrence` |  | Rock.Model.EventItemOccurrence | `event-item-occurrence` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/EventItemOccurrenceLava.ascx.cs#L244) |
| `event-lava` | Event Item Occurrence Lava block | `RegistrationPage` |  | PageReference route |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/EventItemOccurrenceLava.ascx.cs#L183) |
| `event-lava` | Event Item Occurrence Lava block | `RegistrationStatusLabel` |  | string |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/EventItemOccurrenceLava.ascx.cs#L238) |
| `event-lava` | Event Item Occurrence Lava block | `RegistrationStatusLabels` |  | Dictionary<string, string> |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/EventItemOccurrenceLava.ascx.cs#L242) |
| `event-registration` | Registrant wait-list transition email Lava | `AdditionalFieldsNeeded` |  | bool |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Event/RegistrantWaitListMove.cs#L246) |
| `event-registration` | Registrant wait-list transition email Lava | `Registration` |  | Rock.Model.Registration | `registration` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Event/RegistrantWaitListMove.cs#L244) |
| `event-registration` | Registrant wait-list transition email Lava | `RegistrationInstance` |  | Rock.Model.RegistrationInstance | `registration-instance` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Event/RegistrantWaitListMove.cs#L243) |
| `event-registration` | Registrant wait-list transition email Lava | `TransitionedRegistrants` |  | List<RegistrationRegistrant> | `registration-registrant` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Event/RegistrantWaitListMove.cs#L245) |
| `event-registration` | Event Registration Entry Lava templates | `Registration` |  | Rock.Model.Registration | `registration` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Event/RegistrationEntry.cs#L1365) |
| `event-registration` | Event Registration Entry Lava templates | `RegistrationInstance` |  | Rock.Model.RegistrationInstance | `registration-instance` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Event/RegistrationEntry.cs#L1356) |
| `event-registration` | Event Registration signature document Lava | `Registrant` |  | Rock.Model.RegistrationRegistrant | `registration-registrant` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Event/RegistrationEntry.cs#L855) |
| `event-registration` | Event Registration signature document Lava | `Registration` |  | Rock.Model.Registration | `registration` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Event/RegistrationEntry.cs#L854) |
| `finance-lava` | Fundraising Opportunity View Lava template | `AmountLeft` |  | decimal |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L380) |
| `finance-lava` | Fundraising Opportunity View Lava template | `Block` |  | BlockCache |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L212) |
| `finance-lava` | Fundraising Opportunity View Lava template | `ContentChannelItems` |  | IEnumerable<ContentChannelItem> | `content-channel-item` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L422) |
| `finance-lava` | Fundraising Opportunity View Lava template | `CurrentRegistrationCount` |  | int |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L273) |
| `finance-lava` | Fundraising Opportunity View Lava template | `FamilyMemberGroupMembers` |  | IEnumerable<GroupMember> | `group-member` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L361) |
| `finance-lava` | Fundraising Opportunity View Lava template | `Group` |  | Rock.Model.Group | `group` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L213) |
| `finance-lava` | Fundraising Opportunity View Lava template | `GroupMember` |  | Rock.Model.GroupMember | `group-member` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L310) |
| `finance-lava` | Fundraising Opportunity View Lava template | `MakeDonationButtonText` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L400) |
| `finance-lava` | Fundraising Opportunity View Lava template | `MakeDonationUrl` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L387) |
| `finance-lava` | Fundraising Opportunity View Lava template | `MaxRegistrantCount` |  | int |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L276) |
| `finance-lava` | Fundraising Opportunity View Lava template | `ParticipantPageUrl` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L388) |
| `finance-lava` | Fundraising Opportunity View Lava template | `ParticipationMode` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L311) |
| `finance-lava` | Fundraising Opportunity View Lava template | `PercentMet` |  | decimal |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L381) |
| `finance-lava` | Fundraising Opportunity View Lava template | `ProgressTitle` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L318) |
| `finance-lava` | Fundraising Opportunity View Lava template | `RegistrationInstance` |  | Rock.Model.RegistrationInstance | `registration-instance` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L260) |
| `finance-lava` | Fundraising Opportunity View Lava template | `RegistrationInstanceLinkages` |  | IEnumerable<RegistrationInstanceLinkage> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L261) |
| `finance-lava` | Fundraising Opportunity View Lava template | `RegistrationPage` |  | PageReference route |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L256) |
| `finance-lava` | Fundraising Opportunity View Lava template | `RegistrationSpotsAvailable` |  | int |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs#L277) |
| `finance-lava` | Transaction Entry confirm account email Lava | `ConfirmAccountUrl` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L1704) |
| `finance-lava` | Transaction Entry confirm account email Lava | `Person` |  | Rock.Model.Person | `person` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L1705) |
| `finance-lava` | Transaction Entry confirm account email Lava | `User` |  | UserLogin |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L1706) |
| `finance-lava` | Transaction Entry finish Lava template | `BillingLocation` |  | Rock.Model.Location | `location` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L3153) |
| `finance-lava` | Transaction Entry finish Lava template | `PaymentDetail` |  | Rock.Model.FinancialPaymentDetail | `financial-payment-detail` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L3148) |
| `finance-lava` | Transaction Entry finish Lava template | `Person` |  | Rock.Model.Person | `person` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L1705) |
| `finance-lava` | Transaction Entry finish Lava template | `Transaction` |  | FinancialTransaction or FinancialScheduledTransaction | `financial-transaction` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L3131) |
| `finance-lava` | Transaction Entry finish Lava template | `TransactionEntity` |  | IEntity |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L3123) |
| `finance-lava` | Transaction Entry intro message Lava | `TransactionEntity` |  | IEntity |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L1864) |
| `finance-lava` | Transaction Entry payment comment Lava template | `CurrencyType` |  | DefinedValueCache |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L3500) |
| `finance-lava` | Transaction Entry payment comment Lava template | `TransactionAccountDetails` |  | IEnumerable<FinancialTransactionDetail> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L3503) |
| `finance-lava` | Transaction Entry payment comment Lava template | `TransactionDateTime` |  | DateTime |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L3496) |
| `finance-lava` | Transaction Entry scheduled transactions Lava template | `GiftTerm` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L1506) |
| `finance-lava` | Transaction Entry scheduled transactions Lava template | `LinkedPages` |  | Dictionary<string, object> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L1510) |
| `finance-lava` | Transaction Entry scheduled transactions Lava template | `ScheduledTransactions` |  | IEnumerable<FinancialScheduledTransaction> | `financial-scheduled-transaction` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs#L1551) |
| `following` | Following By Entity Lava block | `BlockId` |  | int |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/FollowingByEntityLava.cs#L171) |
| `following` | Following By Entity Lava block | `EntityType` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/FollowingByEntityLava.cs#L168) |
| `following` | Following By Entity Lava block | `FollowingItems` |  | IEnumerable<Following> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/FollowingByEntityLava.cs#L166) |
| `following` | Following By Entity Lava block | `HasMore` |  | bool |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/FollowingByEntityLava.cs#L167) |
| `following` | Following By Entity Lava block | `LinkUrl` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/FollowingByEntityLava.cs#L169) |
| `following` | Following By Entity Lava block | `Quantity` |  | int |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/FollowingByEntityLava.cs#L170) |
| `global` | Global common Lava merge fields | `Campuses` |  | IEnumerable<CampusCache> | `campus` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs#L214) |
| `global` | Global common Lava merge fields | `Context` |  | Dictionary<string, object> |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs#L155) |
| `global` | Global common Lava merge fields | `CurrentPerson` |  | Rock.Model.Person | `person` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs#L202) |
| `global` | Global common Lava merge fields | `CurrentVisitor` |  | Rock.Model.PersonAlias | `person-alias` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs#L209) |
| `global` | Global common Lava merge fields | `DeviceFamily` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs#L193) |
| `global` | Global common Lava merge fields | `ExperienceMode` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs#L223) |
| `global` | Global common Lava merge fields | `Geolocation` |  | Rock.Net.Geolocation |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs#L220) |
| `global` | Global common Lava merge fields | `OSFamily` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs#L188) |
| `global` | Global common Lava merge fields | `PageParameter` |  | IDictionary<string, string> |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs#L178) |
| `global` | Rock request-context common Lava merge fields | `Campuses` |  | IEnumerable<CampusCache> | `campus` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Net/RockRequestContext.cs#L1048) |
| `global` | Rock request-context common Lava merge fields | `Context` |  | Dictionary<string, object> |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Net/RockRequestContext.cs#L1021) |
| `global` | Rock request-context common Lava merge fields | `CurrentPerson` |  | Rock.Model.Person | `person` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Net/RockRequestContext.cs#L1043) |
| `global` | Rock request-context common Lava merge fields | `Device` |  | Rock.Common.Mobile.DeviceData |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Net/RockRequestContext.cs#L1053) |
| `global` | Rock request-context common Lava merge fields | `DeviceFamily` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Net/RockRequestContext.cs#L1037) |
| `global` | Rock request-context common Lava merge fields | `ExperienceMode` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Net/RockRequestContext.cs#L1057) |
| `global` | Rock request-context common Lava merge fields | `Geolocation` |  | Rock.Net.Geolocation |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Net/RockRequestContext.cs#L1056) |
| `global` | Rock request-context common Lava merge fields | `OSFamily` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Net/RockRequestContext.cs#L1032) |
| `global` | Rock request-context common Lava merge fields | `PageParameter` |  | IDictionary<string, string> |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Net/RockRequestContext.cs#L1027) |
| `group-lava` | Group Detail Lava block | `AllowedActions` |  | Dictionary<string, bool> |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupDetailLava.ascx.cs#L980) |
| `group-lava` | Group Detail Lava block | `ButtonVisibility` |  | Dictionary<string, bool> |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupDetailLava.ascx.cs#L991) |
| `group-lava` | Group Detail Lava block | `CurrentPage` |  | Dictionary<string, object> |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupDetailLava.ascx.cs#L985) |
| `group-lava` | Group Detail Lava block | `Group` |  | Rock.Model.Group | `group` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupDetailLava.ascx.cs#L963) |
| `group-lava` | Group Detail Lava block | `LinkedPages` |  | Dictionary<string, object> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupDetailLava.ascx.cs#L972) |
| `group-lava` | Group Finder Lava block | `AllowedActions` |  | Dictionary<string, bool> |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupFinder.ascx.cs#L1565) |
| `group-lava` | Group Finder Lava block | `CampusContext` |  | Rock.Model.Campus | `campus` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupFinder.ascx.cs#L1558) |
| `group-lava` | Group Finder Lava block | `Fences` |  | IEnumerable<GeoFence> |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupFinder.ascx.cs#L1633) |
| `group-lava` | Group Finder Lava block | `Group` |  | Rock.Model.Group | `group` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupFinder.ascx.cs#L1542) |
| `group-lava` | Group Finder Lava block | `Groups` |  | IEnumerable<Group> | `group` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupFinder.ascx.cs#L1640) |
| `group-lava` | Group Finder Lava block | `LinkedPages` |  | Dictionary<string, object> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupFinder.ascx.cs#L1557) |
| `group-lava` | Group Finder Lava block | `Location` |  | Rock.Model.Location | `location` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupFinder.ascx.cs#L1543) |
| `mobile-block` | Mobile CMS Content command Lava | `Command` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Cms/Content.cs#L195) |
| `mobile-block` | Mobile CMS Content command Lava | `CurrentPage` |  | PageCache |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Cms/Content.cs#L137) |
| `mobile-block` | Mobile CMS Content command Lava | `Parameters` |  | IDictionary<string, object> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Cms/Content.cs#L196) |
| `mobile-block` | Mobile CMS Content block server Lava | `CurrentPage` |  | PageCache |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Cms/Content.cs#L137) |
| `mobile-block` | Mobile Communication View block Lava template | `AdditionalRecipientMergeValues` |  | dynamic recipient merge values |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Communication/CommunicationView.cs#L235) |
| `mobile-block` | Mobile Communication View block Lava template | `Communication` |  | Rock.Model.Communication | `communication` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Communication/CommunicationView.cs#L225) |
| `mobile-block` | Mobile Communication View block Lava template | `Content` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Communication/CommunicationView.cs#L241) |
| `mobile-block` | Mobile Communication View block Lava template | `CurrentPage` |  | PageCache |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Communication/CommunicationView.cs#L224) |
| `mobile-block` | Mobile Communication View block Lava template | `Person` |  | Rock.Model.Person | `person` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Communication/CommunicationView.cs#L226) |
| `mobile-block` | Mobile Group View block Lava template | `AllowedActions` |  | Dictionary<string, bool> |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Groups/GroupView.cs#L225) |
| `mobile-block` | Mobile Group View block Lava template | `Group` |  | Rock.Model.Group | `group` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Groups/GroupView.cs#L190) |
| `mobile-block` | Mobile Group View block Lava template | `GroupEditPage` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Groups/GroupView.cs#L191) |
| `mobile-block` | Mobile Group View block Lava template | `ShowLeaderList` |  | bool |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Groups/GroupView.cs#L192) |
| `mobile-block` | Mobile Group View block Lava template | `VisibleAttributes` |  | IEnumerable<AttributeCache> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Groups/GroupView.cs#L213) |
| `mobile-block` | Mobile Prayer Session block Lava template | `PrayedButtonText` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Prayer/PrayerSession.cs#L393) |
| `mobile-block` | Mobile Prayer Session block Lava template | `Request` |  | Rock.Model.PrayerRequest | `prayer-request` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Prayer/PrayerSession.cs#L397) |
| `mobile-block` | Mobile Prayer Session block Lava template | `SessionContext` |  | encrypted JSON string |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Prayer/PrayerSession.cs#L396) |
| `mobile-block` | Mobile Prayer Session block Lava template | `ShowFollowButton` |  | bool |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Prayer/PrayerSession.cs#L394) |
| `mobile-block` | Mobile Prayer Session block Lava template | `ShowInappropriateButton` |  | bool |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Prayer/PrayerSession.cs#L395) |
| `utility-lava` | Real Time Visualizer message Lava | `Args` |  | Lava object converted from JavaScript arguments |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Utility/RealTimeVisualizer.cs#L335) |
| `utility-lava` | Real Time Visualizer message Lava | `Message` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Utility/RealTimeVisualizer.cs#L334) |
| `utility-lava` | Real Time Visualizer message Lava | `Topic` |  | string |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Utility/RealTimeVisualizer.cs#L333) |
| `utility-lava` | Real Time Visualizer settings Lava | `Settings` |  | Dictionary<string, object> |  | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Utility/RealTimeVisualizer.cs#L127) |
| `workflow` | Workflow action component Lava merge fields | `Action` |  | Rock.Model.WorkflowAction | `workflow-action` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs#L365) |
| `workflow` | Workflow action component Lava merge fields | `Action` |  | Rock.Model.WorkflowAction | `workflow-action` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs#L388) |
| `workflow` | Workflow action component Lava merge fields | `Activity` |  | Rock.Model.WorkflowActivity | `workflow-activity` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs#L366) |
| `workflow` | Workflow action component Lava merge fields | `Activity` |  | Rock.Model.WorkflowActivity | `workflow-activity` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs#L389) |
| `workflow` | Workflow action component Lava merge fields | `Workflow` |  | Rock.Model.Workflow | `workflow` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs#L367) |
| `workflow` | Workflow action component Lava merge fields | `Workflow` |  | Rock.Model.Workflow | `workflow` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs#L390) |
| `workflow` | Workflow Entry block form Lava | `Action` |  | Rock.Model.WorkflowAction | `workflow-action` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/WorkFlow/WorkflowEntry.cs#L923) |
| `workflow` | Workflow Entry block form Lava | `Activity` |  | Rock.Model.WorkflowActivity | `workflow-activity` | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/WorkFlow/WorkflowEntry.cs#L924) |
| `workflow` | Workflow Entry block form Lava | `Item` |  | Rock.Model.WorkflowType | `workflow-type` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/WorkFlow/WorkflowEntry.cs#L1211) |
| `workflow` | Workflow Entry block form Lava | `Workflow` |  | Rock.Model.Workflow | `workflow` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/WorkFlow/WorkflowEntry.cs#L925) |

## Public Source Files

- [RockWeb/Blocks/Event/CalendarLava.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/CalendarLava.ascx.cs)
- [Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs)
- [Rock.Blocks/Crm/ConflictProfile.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Crm/ConflictProfile.cs)
- [Rock.Blocks/Cms/ContentChannelItemView.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelItemView.cs)
- [Rock.Blocks/Cms/ContentChannelView.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Cms/ContentChannelView.cs)
- [Rock.Blocks/Crm/Disc.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Crm/Disc.cs)
- [RockWeb/Blocks/Event/EventItemOccurrenceLava.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Event/EventItemOccurrenceLava.ascx.cs)
- [Rock/CheckIn/v2/Labels/FieldSourceHelper.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/FieldSourceHelper.cs)
- [Rock.Blocks/Core/FollowingByEntityLava.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Core/FollowingByEntityLava.cs)
- [RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Fundraising/FundraisingOpportunityView.ascx.cs)
- [Rock.Blocks/Crm/GiftsAssessment.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Crm/GiftsAssessment.cs)
- [RockWeb/Blocks/Groups/GroupDetailLava.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupDetailLava.ascx.cs)
- [RockWeb/Blocks/Groups/GroupFinder.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Groups/GroupFinder.ascx.cs)
- [Rock/CheckIn/v2/Labels/LabelField.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/LabelField.cs)
- [Rock/Lava/LavaHelper.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs)
- [Rock/Blocks/Types/Mobile/Cms/Content.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Cms/Content.cs)
- [Rock/Blocks/Types/Mobile/Communication/CommunicationView.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Communication/CommunicationView.cs)
- [Rock/Blocks/Types/Mobile/Groups/GroupView.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Groups/GroupView.cs)
- [Rock/Blocks/Types/Mobile/Prayer/PrayerSession.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Blocks/Types/Mobile/Prayer/PrayerSession.cs)
- [Rock.Blocks/Crm/Motivators.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Crm/Motivators.cs)
- [Rock/CheckIn/v2/Labels/PersonLabelData.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs)
- [Rock.Blocks/Utility/RealTimeVisualizer.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Utility/RealTimeVisualizer.cs)
- [Rock.Blocks/Event/RegistrantWaitListMove.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Event/RegistrantWaitListMove.cs)
- [Rock.Blocks/Event/RegistrationEntry.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/Event/RegistrationEntry.cs)
- [Rock/Net/RockRequestContext.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Net/RockRequestContext.cs)
- [RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Finance/TransactionEntryV2.ascx.cs)
- [Rock/Workflow/ActionComponent.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs)
- [Rock.Blocks/WorkFlow/WorkflowEntry.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Blocks/WorkFlow/WorkflowEntry.cs)
