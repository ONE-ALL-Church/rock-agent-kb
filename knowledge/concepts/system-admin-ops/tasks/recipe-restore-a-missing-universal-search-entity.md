---
concept_id: system-admin-ops
task_id: recipe-restore-a-missing-universal-search-entity
title: Recipe: Restore a missing Universal Search entity
generated: true
---

# Recipe: Restore a missing Universal Search entity

Return one known eligible record to search without rebuilding unrelated indexes first.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Group`
- `GroupType`
- `Schedule`
- `Attribute`
- `Person`

## Entities And Tables

- `Group`
- `GroupType`
- `Schedule`
- `Attribute`
- `Person`

## Steps

1. Verify provider connectivity.
2. Confirm the entity is enabled.
3. Confirm the entity-specific eligibility setting.
4. Confirm that intended attributes are permitted and safe to index.
5. Inspect the relevant re-index or site-crawl job.
6. Correct connectivity or eligibility before initiating a bulk operation.
7. Run the supported entity-specific bulk load or allow the scheduled job to complete.
8. Search for one known eligible record and verify its destination URL.
9. Confirm that Person indexing is enabled.
10. Confirm that the specific attribute is selected for indexing.
11. Assess whether the attribute is safe to expose, because Universal Search does not enforce person-attribute security.
12. Run the supported Person bulk load or wait for the nightly re-index.
13. If the installed version predates v19.3, check applicability of the documented Person Attribute Values defect.
14. Stop if the desired attribute is sensitive or version applicability is unknown. Specifics for Entities

## Do Not Assume

- A record in Rock is automatically eligible for Universal Search.
- Attribute security carries into Universal Search.
- Re-indexing corrects a wrong provider or eligibility setting.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities
- https://community.rockrms.com/documentation/core-concepts/search/universal-search/enable-entities-for-universal-search
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/ScheduledJobHistoryList/ScheduledJobHistoryListOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Core/ScheduledJobHistoryList.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/specs/completed/core/260731-servicejobhistory-sub-second-orphaned-incomplete-rows.md
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/ScheduledJobHistoryList/scheduledJobHistoryListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs
