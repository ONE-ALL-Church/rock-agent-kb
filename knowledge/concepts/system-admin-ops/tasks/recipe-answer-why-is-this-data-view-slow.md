---
concept_id: system-admin-ops
task_id: recipe-answer-why-is-this-data-view-slow
title: Recipe: Answer “Why Is This Data View Slow?”
generated: true
---

# Recipe: Answer “Why Is This Data View Slow?”

Complete Answer “Why Is This Data View Slow?” with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`

## Entities And Tables

- `DataView`

## Steps

1. Identify Data View ID/name/entity.
2. Inspect filter tree and nested Data Views.
3. Check persistence settings.
4. Check last refresh duration if available.
5. Check `Update Persisted DataViews` timeout.
6. Test live result count.
7. Identify expensive filters.
8. Recommend filter/index/report changes only after evidence.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

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
