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
- Inspect the exact live records before changing production behavior; generated guidance does not prove current configuration.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Trace a public gift end to end](tasks/recipe-trace-a-public-gift-end-to-end.md): Account for a gift from donor action through its Rock records and reporting treatment.
- [Recipe: Validate an online giving page before launch](tasks/recipe-validate-an-online-giving-page-before-launch.md): Establish that the page’s configuration expresses the intended finance path.
- [Recipe: Reconcile an online batch](tasks/recipe-reconcile-an-online-batch.md): Explain every batch total and variance at the correct grain.
- [Recipe: Generate and validate contribution statements](tasks/recipe-generate-and-validate-contribution-statements.md): Produce a reviewable statement set whose population and finance rules are explicit.
- [Recipe: Build a detail-preserving finance report](tasks/recipe-build-a-detail-preserving-finance-report.md): Show each account allocation with transaction-level context without accidental row collapse.
- [Recipe: Transfer scheduled giving to a new gateway](tasks/recipe-transfer-scheduled-giving-to-a-new-gateway.md): Route new gifts to the new provider while giving existing scheduled donors a controlled transfer path.

## High-Signal Sections

- `scope-and-boundaries` lines 34-47: Scope And Boundaries (normal)
- `mental-model` lines 48-67: Mental Model (normal)
- `transactions` lines 68-79: Transactions (normal)
- `payment-gateways` lines 80-94: Payment Gateways (normal)
- `online-giving-and-receipts` lines 95-106: Online Giving And Receipts (normal)
- `text-giving` lines 107-116: Text Giving (normal)

## Core Entities

- `Attribute`: Rock concept/entity referenced by the giving-finance guide.
- `Block`: Rock concept/entity referenced by the giving-finance guide.
- `Campus`: Rock concept/entity referenced by the giving-finance guide.
- `Family`: Rock concept/entity referenced by the giving-finance guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `Location`: Named physical or logical location used for rooms, campuses, buildings, and printer routing.
- `Page`: Rock concept/entity referenced by the giving-finance guide.
- `Person`: Rock concept/entity referenced by the giving-finance guide.
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
