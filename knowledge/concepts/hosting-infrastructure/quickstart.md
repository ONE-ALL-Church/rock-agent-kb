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
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Inventory Hosting](tasks/recipe-inventory-hosting.md): Follow the guide section for Recipe: Inventory Hosting.
- [Recipe: Validate Azure Hosting](tasks/recipe-validate-azure-hosting.md): Follow the guide section for Recipe: Validate Azure Hosting.
- [Recipe: Review SQL Performance](tasks/recipe-review-sql-performance.md): Follow the guide section for Recipe: Review SQL Performance.
- [Recipe: Review Backup And Restore](tasks/recipe-review-backup-and-restore.md): Follow the guide section for Recipe: Review Backup And Restore.
- [Recipe: Review Web Farm](tasks/recipe-review-web-farm.md): Follow the guide section for Recipe: Review Web Farm.
- [Recipe: Public Launch Hosting Gate](tasks/recipe-public-launch-hosting-gate.md): Follow the guide section for Recipe: Public Launch Hosting Gate.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 27-47: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 48-77: 2. Scope And Terminology (normal)
- `3-hosting-and-infrastructure-mental-model-layer-1-request-entry` lines 82-94: Layer 1: Request Entry (normal)
- `3-hosting-and-infrastructure-mental-model-layer-2-web-runtime` lines 95-110: Layer 2: Web Runtime (normal)
- `3-hosting-and-infrastructure-mental-model-layer-3-database-and-persistence` lines 111-127: Layer 3: Database And Persistence (normal)
- `3-hosting-and-infrastructure-mental-model-layer-4-shared-services` lines 128-146: Layer 4: Shared Services (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the hosting-infrastructure guide.
- `Block`: Rock concept/entity referenced by the hosting-infrastructure guide.
- `DataView`: Rock concept/entity referenced by the hosting-infrastructure guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Label`: Rock concept/entity referenced by the hosting-infrastructure guide.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the hosting-infrastructure guide.
- `Person`: Rock concept/entity referenced by the hosting-infrastructure guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Workflow`: Rock concept/entity referenced by the hosting-infrastructure guide.

## Version Caveats

- `19.1`: Added an automatic data migration that moves File Storage Provider settings from any existing legacy Azure Blob Storage provider plugin (Pillars) to the core Azure Blob Storage provider. This is required because the lega
- `17.5`: Fixed an error that occurred when editing a Content Channel Type with Attributes of type Image, File, or Binary File. The issue happened if the storage location was set to Azure Blob Storage or File System (or newly crea
- `17.0`: Improved database performance with new and revised indexes across multiple tables. These changes improve query efficiency for transactions, person records, group hierarchies, and interactions, based on SQL Server recomme
- `18.1`: Added global attribute "Google API Key Server" for handling server-side Google API requests, such as geocoding and routing. This is separate from the existing client-side key used for JavaScript-based API calls. Fixes: #
- `17.5`: Fixed an issue where loading the Obsidian Attendance History block without person context could cause severe performance issues and possible server crashes by attempting to load all attendance records. The block now prev
- `17.1`: Fixed a performance issue in Next-Gen Check-in that caused delays when printing to Bluetooth printers. The slowdown was due to how label image data was encoded, which has now been optimized. Printing performance should n
- `16.3`: Fixed issue where Communication Entry Wizard block becomes unusable when an SMS image attachment is auto-resized and uploaded to Azure Blob Storage. Fixes: #5719
- `17.2`: Improved the database index fill factor from 80% to 100% to reduce table size and improve maintenance performance. In the past, this was changed due to a common practice of reserving space to reduce page splits in the ta

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
