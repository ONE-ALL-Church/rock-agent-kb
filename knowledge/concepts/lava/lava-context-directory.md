# Lava Data Context Directory

Generated from public SparkDevNetwork/Rock source files. This directory answers which root objects are available in selected Lava rendering surfaces; use the Model Map after identifying a root object.

## Agent Use

1. Identify the rendering surface and context family.
2. Use this directory to find available root keys and nested paths.
3. Use `agent/model-map-digests.jsonl`, `uvx rock-kb model <slug>`, or `uvx rock-kb model-map get <slug>` to inspect properties for linked model roots.
4. Use `agent/lava-capabilities.jsonl` for filters, commands, and Lava behavior.
5. Treat rows marked for live verification as source-code leads that still depend on the page, block, communication, workflow, or label configuration.

## Coverage

- Lava context rows: `58`
- Public source files: `7`
- Machine-readable rows: `lava-contexts.jsonl` and `../../../agent/lava-contexts.jsonl`
- `check-in-label`: 29
- `cms-block`: 1
- `communication`: 3
- `global`: 18
- `mobile-block`: 1
- `workflow`: 6

## Context Rows

| Family | Surface | Root Key | Nested Path | Type | Model Map | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
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
| `cms-block` | CMS/web block Lava template context | `source-boundary` |  | source-code boundary |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs#L108) |
| `communication` | Communication recipient additional merge values | `AdditionalMergeValues` |  | dynamic entity or scalar |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs#L151) |
| `communication` | Communication recipient merge values | `Communication` |  | Rock.Model.Communication | `communication` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs#L130) |
| `communication` | Communication recipient merge values | `Person` |  | Rock.Model.Person | `person` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs#L135) |
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
| `mobile-block` | Mobile block Lava template context | `source-boundary` |  | source-code boundary |  | live check | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs#L108) |
| `workflow` | Workflow action component Lava merge fields | `Action` |  | Rock.Model.WorkflowAction | `workflow-action` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs#L365) |
| `workflow` | Workflow action component Lava merge fields | `Action` |  | Rock.Model.WorkflowAction | `workflow-action` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs#L388) |
| `workflow` | Workflow action component Lava merge fields | `Activity` |  | Rock.Model.WorkflowActivity | `workflow-activity` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs#L366) |
| `workflow` | Workflow action component Lava merge fields | `Activity` |  | Rock.Model.WorkflowActivity | `workflow-activity` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs#L389) |
| `workflow` | Workflow action component Lava merge fields | `Workflow` |  | Rock.Model.Workflow | `workflow` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs#L367) |
| `workflow` | Workflow action component Lava merge fields | `Workflow` |  | Rock.Model.Workflow | `workflow` | source code | [source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs#L390) |

## Public Source Files

- [Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Communication/CommunicationRecipient/CommunicationRecipient.Logic.cs)
- [Rock/CheckIn/v2/Labels/FieldSourceHelper.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/FieldSourceHelper.cs)
- [Rock/CheckIn/v2/Labels/LabelField.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/LabelField.cs)
- [Rock/Lava/LavaHelper.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Lava/LavaHelper.cs)
- [Rock/CheckIn/v2/Labels/PersonLabelData.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PersonLabelData.cs)
- [Rock/Net/RockRequestContext.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Net/RockRequestContext.cs)
- [Rock/Workflow/ActionComponent.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Workflow/ActionComponent.cs)
