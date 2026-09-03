---
concept_id: system-admin-ops
task_id: recipe-configure-a-bounded-site-index-crawl
title: Recipe: Configure a bounded site-index crawl
generated: true
---

# Recipe: Configure a bounded site-index crawl

Index the intended site pages without unintentionally exposing or omitting secured content.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Location`
- `Schedule`
- `Page`

## Entities And Tables

- `Location`
- `Schedule`
- `Page`

## Steps

1. Enable indexing in the site’s advanced settings.
2. Choose a crawling starting location that links to every intended page.
3. If secured content is required, use a dedicated crawler identity and restrict the link page to that identity and administrators.
4. Ensure the crawler cannot access a logout action that would terminate its session.
5. Configure an `Index Rock Site` job with the intended schedule.
6. Inspect job history after execution.
7. Verify representative public and authorized results separately.

## Do Not Assume

- Unlinked pages will be discovered.
- The nightly Universal Search Re-Index job crawls Site entities.
- Hiding a link page from navigation alone provides the documented security boundary.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/intro-to-caching
- https://community.rockrms.com/documentation/supporting-rock/data/data-integrity/location-editor
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/supporting-rock/data/advanced-data/view-the-exception-list
- https://community.rockrms.com/documentation/supporting-rock/caching/caching-fundamentals/cache-persisted-datasets
- https://community.rockrms.com/documentation/core-concepts/search/universal-search/specifics-for-entities
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/ScheduledJobHistoryList/ScheduledJobHistoryListOptionsBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/Core/ScheduledJobHistoryList.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/specs/completed/core/260731-servicejobhistory-sub-second-orphaned-incomplete-rows.md
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/ScheduledJobHistoryList/scheduledJobHistoryListOptionsBag.d.ts
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/ServiceJobHistory/ServiceJobHistory.cs
- https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s
