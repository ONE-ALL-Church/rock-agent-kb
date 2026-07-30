---
concept_id: system-admin-ops
task_id: recipe-answer-why-is-this-data-wrong
title: Recipe: Answer “Why Is This Data Wrong?”
generated: true
---

# Recipe: Answer “Why Is This Data Wrong?”

Complete Answer “Why Is This Data Wrong?” with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`

## Entities And Tables

- `DataView`

## Steps

1. Identify displayed value.
2. Identify source entity.
3. Identify whether display uses Data View, report, Lava, cache, or search.
4. Compare source-of-truth row to displayed row.
5. Check cache/index/persistence.
6. Check security filtering.
7. Check recent job history.
8. Report exact mismatch and refresh path.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://github.com/SparkDevNetwork/Rock
- https://community.rockrms.com/lava/lava-api
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/DataViewSearch.ascx.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Communication/CommunicationFlowDetail/CommunicationFlowDetailEnteredDataViewSettingsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/Actions/DataViewsActionsController.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/RockWeb/Blocks/Reporting/DataViewSearch.ascx
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowPerformance/enteredDataViewSettingsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Communication/CommunicationFlowPerformance/EnteredDataViewSettingsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Jobs/UpdatePersistedDataviews.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Communication/CommunicationFlowDetail/communicationFlowDetailEnteredDataViewSettingsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/DataViewsController.CodeGenerated.cs
