---
concept_id: system-admin-ops
title: System Administration And Operations Quickstart
generated: true
---

# System Administration And Operations Quickstart

Service jobs, exception logs, cache, cleanup, indexing, data integrity, settings, diagnostics, and operational health.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Triage a recurring exception](tasks/recipe-triage-a-recurring-exception.md): Identify the narrowest supported failure boundary without claiming an unverified root cause.
- [Recipe: Refresh stale cached output with minimum scope](tasks/recipe-refresh-stale-cached-output-with-minimum-scope.md): Refresh the affected output without unnecessarily clearing unrelated caches.
- [Recipe: Create and assign a cache tag](tasks/recipe-create-and-assign-a-cache-tag.md): Establish a durable, targeted invalidation boundary for related cached blocks.
- [Recipe: Audit a scheduled job’s recent health](tasks/recipe-audit-a-scheduled-job-s-recent-health.md): Determine whether recorded executions match the expected schedule and whether the downstream result is current.
- [Recipe: Restore a missing Universal Search entity](tasks/recipe-restore-a-missing-universal-search-entity.md): Return one known eligible record to search without rebuilding unrelated indexes first.
- [Recipe: Configure a bounded site-index crawl](tasks/recipe-configure-a-bounded-site-index-crawl.md): Index the intended site pages without unintentionally exposing or omitting secured content.
- [Recipe: Review and resolve a duplicate-person candidate](tasks/recipe-review-and-resolve-a-duplicate-person-candidate.md): Merge only records demonstrated to belong to the same person while preserving the intended values.
- [Recipe: Review a Data Automation change before execution](tasks/recipe-review-a-data-automation-change-before-execution.md): Define the expected affected population and side effects before a job mutates records.

## High-Signal Sections

- `jobs-and-scheduling-job-configuration-and-history` lines 71-78: Job configuration and history (high)
- `jobs-and-scheduling-version-specific-job-history-failures` lines 79-89: Version-specific job-history failures (normal)
- `jobs-and-scheduling-job-backed-operational-processes` lines 90-101: Job-backed operational processes (high)
- `diagnostics-and-exceptions-exception-history` lines 104-117: Exception history (normal)
- `diagnostics-and-exceptions-page-performance-diagnostics` lines 118-123: Page performance diagnostics (normal)
- `diagnostics-and-exceptions-auditing` lines 124-129: Auditing (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the system-admin-ops guide.
- `Block`: Rock concept/entity referenced by the system-admin-ops guide.
- `Campus`: Rock concept/entity referenced by the system-admin-ops guide.
- `Check-in Configuration`: Rock concept/entity referenced by the system-admin-ops guide.
- `DataView`: Rock concept/entity referenced by the system-admin-ops guide.
- `Family`: Rock concept/entity referenced by the system-admin-ops guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupType`: Rule container for groups, including attendance/check-in settings and inherited behavior.
- `Label`: Rock concept/entity referenced by the system-admin-ops guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the system-admin-ops guide.
- `Person`: Rock concept/entity referenced by the system-admin-ops guide.

## Version Caveats

- `19.1`: Fixed issue where refreshing cache displayed an error when the App_Data/Cache folder did not exist. The Rock Cleanup job deletes the App_Data/Cache folder, and if no file types are configured to cache to the server, the
- `19.3`: Fixed Person Attribute Values configured for indexing not being included in Universal Search results after a bulk re-index, and restored the missing "Indexing Enabled" option in the Attributes block so Attributes can be

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
