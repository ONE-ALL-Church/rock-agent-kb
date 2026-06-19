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
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Answer “Is The System Healthy?”](tasks/recipe-answer-is-the-system-healthy.md): Follow the guide section for Recipe: Answer “Is The System Healthy?”.
- [Recipe: Answer “Why Is This Data Wrong?”](tasks/recipe-answer-why-is-this-data-wrong.md): Follow the guide section for Recipe: Answer “Why Is This Data Wrong?”.
- [Recipe: Answer “Can I Clear Cache?”](tasks/recipe-answer-can-i-clear-cache.md): Follow the guide section for Recipe: Answer “Can I Clear Cache?”.
- [Recipe: Answer “Why Did This Workflow Not Start?”](tasks/recipe-answer-why-did-this-workflow-not-start.md): Follow the guide section for Recipe: Answer “Why Did This Workflow Not Start?”.
- [Recipe: Answer “Why Is This Data View Slow?”](tasks/recipe-answer-why-is-this-data-view-slow.md): Follow the guide section for Recipe: Answer “Why Is This Data View Slow?”.
- [Recipe: Answer “What Changed In This Version That Matters Operationally?”](tasks/recipe-answer-what-changed-in-this-version-that-matters-operationally.md): Follow the guide section for Recipe: Answer “What Changed In This Version That Matters Operationally?”.

## High-Signal Sections

- `2-scope-and-terminology` lines 55-107: 2. Scope And Terminology (high)
- `3-system-administration-and-operations-mental-model-layer-2-runtime-execution` lines 118-123: Layer 2: Runtime Execution (normal)
- `3-system-administration-and-operations-mental-model-layer-3-derived-state` lines 124-129: Layer 3: Derived State (high)
- `3-system-administration-and-operations-mental-model-layer-4-security-and-authorization` lines 130-135: Layer 4: Security And Authorization (normal)
- `3-system-administration-and-operations-mental-model-layer-5-version-behavior` lines 136-139: Layer 5: Version Behavior (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 140-168: 4. Source Authority And How To Use This Guide (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the system-admin-ops guide.
- `Block`: Rock concept/entity referenced by the system-admin-ops guide.
- `Campus`: Rock concept/entity referenced by the system-admin-ops guide.
- `DataView`: Rock concept/entity referenced by the system-admin-ops guide.
- `Family`: Rock concept/entity referenced by the system-admin-ops guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the system-admin-ops guide.
- `Person`: Rock concept/entity referenced by the system-admin-ops guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the system-admin-ops guide.

## Version Caveats

- `19.1`: Fixed issue where refreshing cache displayed an error when the App_Data/Cache folder did not exist. The Rock Cleanup job deletes the App_Data/Cache folder, and if no file types are configured to cache to the server, the
- `19.1`: Fixed an issue in multiple attribute editing blocks where the Category dropdown included Global Attribute categories instead of categories for the attribute’s actual entity type. Fixes: #6729

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
