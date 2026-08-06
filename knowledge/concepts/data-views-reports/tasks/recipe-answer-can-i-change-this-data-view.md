---
concept_id: data-views-reports
task_id: recipe-answer-can-i-change-this-data-view
title: Recipe: Answer "Can I Change This Data View?"
generated: true
---

# Recipe: Answer "Can I Change This Data View?"

Complete Answer "Can I Change This Data View?" with evidence-backed checks and a verifiable outcome.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `DataView`
- `Group`
- `Workflow`
- `Page`
- `Block`

## Entities And Tables

- `DataView`
- `Group`
- `Workflow`
- `Page`
- `Block`

## Steps

1. Find Data View.
2. Inspect usage panel.
3. Query dependent Reports.
4. Query dependent Data View filters.
5. Query blocks/pages.
6. Query group syncs/workflows if relevant.
7. Check last run/count.
8. Identify owner.
9. Recommend edit, copy, or deprecate.
10. Do not change until owner/risk is clear.
11. Installed Rock version.
12. Filter component entity type exists.
13. Plugin installed/enabled.
14. Selection string deserializes.
15. Referenced IDs/GUIDs still exist.
16. Obsidian component data migration.
17. Cache invalidation.
18. Exception logs.
19. Source-code changes between versions.
20. Rebuild filter on a copy if necessary.

## Do Not Assume

- Do not change until owner/risk is clear.

## Source Links

- https://community.rockrms.com/rocku/reporting/dynamic-report-block
- https://community.rockrms.com/recipes/264
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.cs
- https://community.rockrms.com/documentation/bookcontent/6/331
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/DataViewFilter/DataViewFilter.Logic.cs
- https://community.rockrms.com/recipes/397
- https://community.rockrms.com/rocku/business-intelligence-bi/bi-template
- https://community.rockrms.com/rocku/business-intelligence-bi/bi-embed-report
- https://community.rockrms.com/rocku/reporting/reports
- https://community.rockrms.com/rocku/reporting
- https://community.rockrms.com/recipes/262
- https://community.rockrms.com/recipes/240
- https://community.rockrms.com/lava/commands/sql-commands
