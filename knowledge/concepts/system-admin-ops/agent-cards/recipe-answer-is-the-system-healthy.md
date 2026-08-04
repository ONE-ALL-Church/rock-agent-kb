---
concept_id: system-admin-ops
task_id: recipe-answer-is-the-system-healthy
title: Recipe: Answer “Is The System Healthy?”
generated: true
---

# Recipe: Answer “Is The System Healthy?”

Do not say “healthy” unless job history, exceptions, and key derived-state jobs have been checked.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`

## Entities And Tables

- `DataView`

## Steps

1. Rock version.
2. Job failures/warnings in the last 24 hours.
3. Exception spike summary.
4. Universal Search Re-Index last status.
5. Update Persisted DataViews last status.
6. Cleanup job last status.
7. Cache-related exceptions.
8. Any release-note caveats for installed version.
9. Items needing live review.

## Do Not Assume

- Do not say “healthy” unless job history, exceptions, and key derived-state jobs have been checked.

## Source Links

- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Communication/CommunicationFlowDetail/CommunicationFlowDetailEnteredDataViewSettingsBag.cs
- https://community.rockrms.com/lava/lava-api
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/DataViewSearch.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/DataViewSearch.ascx
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowPerformance/enteredDataViewSettingsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Communication/CommunicationFlowPerformance/EnteredDataViewSettingsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowDetail/communicationFlowDetailEnteredDataViewSettingsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/DataViewsController.CodeGenerated.cs
