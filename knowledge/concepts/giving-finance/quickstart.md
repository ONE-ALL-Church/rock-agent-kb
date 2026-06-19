---
concept_id: giving-finance
title: Giving And Finance Quickstart
generated: true
---

# Giving And Finance Quickstart

Giving, transactions, batches, statements, pledges, gateways, and finance administration.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Read-Only Finance Record Inspection](tasks/recipe-read-only-finance-record-inspection.md): Follow the guide section for Recipe: Read-Only Finance Record Inspection.
- [Recipe: Statement Eligibility Explanation](tasks/recipe-statement-eligibility-explanation.md): Follow the guide section for Recipe: Statement Eligibility Explanation.
- [Recipe: Safe Account Cleanup Assessment](tasks/recipe-safe-account-cleanup-assessment.md): Follow the guide section for Recipe: Safe Account Cleanup Assessment.
- [Recipe: Giving Automation Review](tasks/recipe-giving-automation-review.md): Follow the guide section for Recipe: Giving Automation Review.
- [Recipe: Pledge Progress Analysis](tasks/recipe-pledge-progress-analysis.md): Follow the guide section for Recipe: Pledge Progress Analysis.

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-63: 1. Executive Summary For Agents (normal)
- `2-scope-and-terminology` lines 64-126: 2. Scope And Terminology (high)
- `3-giving-and-finance-mental-model` lines 127-155: 3. Giving And Finance Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 156-174: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-financial-accounts` lines 177-192: Financial Accounts (normal)
- `5-core-configuration-and-data-model-financial-gateways` lines 193-221: Financial Gateways (high)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the giving-finance guide.
- `Block`: Rock concept/entity referenced by the giving-finance guide.
- `Campus`: Rock concept/entity referenced by the giving-finance guide.
- `Family`: Rock concept/entity referenced by the giving-finance guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the giving-finance guide.
- `Person`: Rock concept/entity referenced by the giving-finance guide.
- `PersonAlias`: Rock concept/entity referenced by the giving-finance guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.
- `Workflow`: Rock concept/entity referenced by the giving-finance guide.

## Version Caveats

- `18.1`: Added Financial Batch Detail block to support check scanning, creation of batch, batch detail viewing, and batch modifications. Also added Financial Batch List to view available batches.
- `18.3`: Fixed two issues in the Giving History API. When "Combine Giving With" was blank, the API incorrectly returned family giving data instead of only the individual's authorized giving. When family giving (includeGivingGroup

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
