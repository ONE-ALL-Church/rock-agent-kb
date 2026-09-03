---
concept_id: hosting-infrastructure
title: Hosting And Infrastructure Quickstart
generated: true
---

# Hosting And Infrastructure Quickstart

Rock hosting, sizing, Azure and infrastructure guidance, web farms, backups, SSL, SMTP, storage, performance posture, and operational readiness.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Select a hosting model](tasks/recipe-select-a-hosting-model.md): A documented hosting choice with explicit ownership, workload, security, and verification conditions.
- [Recipe: Build an Azure capacity baseline](tasks/recipe-build-an-azure-capacity-baseline.md): A provisional Azure tier supported by workload evidence and marked for validation.
- [Recipe: Prepare a SaaS migration](tasks/recipe-prepare-a-saas-migration.md): A provider-ready migration plan with a reserved test window and clear responsibility boundary.
- [Recipe: Provision the documented Azure layout](tasks/recipe-provision-the-documented-azure-layout.md): A resource group containing the intended Rock web VM and Azure SQL resources.
- [Recipe: Prepare an internal Rock 19 web server](tasks/recipe-prepare-an-internal-rock-19-web-server.md): A Windows/IIS host ready for the documented Rock 19 installer.
- [Recipe: Activate a Rock 19 web farm](tasks/recipe-activate-a-rock-19-web-farm.md): All expected Rock nodes are visible and coordinated without duplicate job runners.
- [Recipe: Offload reports and analytics to a read-only database](tasks/recipe-offload-reports-and-analytics-to-a-read-only-database.md): Eligible Rock 19 reporting or analytics traffic uses the intended read-only target.
- [Recipe: Diagnose a slow Rock 19 page](tasks/recipe-diagnose-a-slow-rock-19-page.md): A repeatable diagnosis identifies either a page component or a broader infrastructure constraint.
- [Recipe: Perform a pre-launch infrastructure review](tasks/recipe-perform-a-pre-launch-infrastructure-review.md): A go/no-go record separates verified readiness from unresolved conditions.

## High-Signal Sections

- `agent-summary` lines 18-33: Agent Summary (normal)
- `mental-model-1-workload` lines 65-68: 1. Workload (normal)
- `mental-model-2-service-ownership` lines 69-74: 2. Service ownership (normal)
- `mental-model-4-rock-specific-invariants` lines 79-91: 4. Rock-specific invariants (normal)
- `sizing-and-service-options-choose-the-ownership-model-first` lines 100-110: Choose the ownership model first (normal)
- `sizing-and-service-options-use-sizing-tables-as-baselines` lines 111-131: Use sizing tables as baselines (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Block`: Rock concept/entity referenced by the hosting-infrastructure guide.
- `DataView`: Rock concept/entity referenced by the hosting-infrastructure guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Page`: Rock concept/entity referenced by the hosting-infrastructure guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Step`: Person-specific engagement milestone instance.
- `Workflow`: Rock concept/entity referenced by the hosting-infrastructure guide.

## Version Caveats

- `19.1`: Added an automatic data migration that moves File Storage Provider settings from any existing legacy Azure Blob Storage provider plugin (Pillars) to the core Azure Blob Storage provider. This is required because the lega
- `17.5`: Fixed an error that occurred when editing a Content Channel Type with Attributes of type Image, File, or Binary File. The issue happened if the storage location was set to Azure Blob Storage or File System (or newly crea
- `17.0`: Improved database performance with new and revised indexes across multiple tables. These changes improve query efficiency for transactions, person records, group hierarchies, and interactions, based on SQL Server recomme

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
