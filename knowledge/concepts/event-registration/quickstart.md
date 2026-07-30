---
concept_id: event-registration
title: Event Registration Quickstart
generated: true
---

# Event Registration Quickstart

Registration instances, templates, payments, forms, event occurrences, and registration operations.

## Agent Entry Points

- Start with a task card when the user has an operational symptom or implementation request.
- Use the entity index when the task mentions a table, model, block, source file, or report.
- Use release caveats before deciding whether behavior is configuration, customization, or version-specific.
- Use the long guide only when planning broadly or when the task card points to a section.

## Primary Tasks

- [Recipe: Summarize A Registration Instance](tasks/recipe-summarize-a-registration-instance.md): Complete Summarize A Registration Instance with evidence-backed checks and a verifiable outcome.
- [Recipe: Verify A Public Registration URL](tasks/recipe-verify-a-public-registration-url.md): Return whether the URL targets the intended registration and why it is open, closed, full, wait-listing, or broken.
- [Recipe: Audit Payment Risk](tasks/recipe-audit-payment-risk.md): Return a prioritized collection list.
- [Recipe: Audit Discount Codes](tasks/recipe-audit-discount-codes.md): Return codes only to authorized staff.
- [Recipe: Audit Wait List](tasks/recipe-audit-wait-list.md): Return who is waiting, what data is missing, and what staff action is needed.
- [Recipe: Build A Registrant Packet Export](tasks/recipe-build-a-registrant-packet-export.md): Complete Build A Registrant Packet Export with evidence-backed checks and a verifiable outcome.
- [Recipe: Add Staff Notes To Registration Detail](tasks/recipe-add-staff-notes-to-registration-detail.md): Complete Add Staff Notes To Registration Detail with evidence-backed checks and a verifiable outcome.
- [Recipe: Investigate API Registration URL Issues](tasks/recipe-investigate-api-registration-url-issues.md): <!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->

## High-Signal Sections

- `1-executive-summary-for-agents` lines 29-45: 1. Executive Summary For Agents (high)
- `2-scope-and-terminology` lines 46-89: 2. Scope And Terminology (high)
- `3-event-registration-mental-model` lines 90-117: 3. Event Registration Mental Model (normal)
- `4-source-authority-and-how-to-use-this-guide` lines 118-141: 4. Source Authority And How To Use This Guide (high)
- `5-core-configuration-and-data-model-configuration-surfaces` lines 144-196: Configuration Surfaces (high)
- `6-primary-entities-and-relationships-registration-instance` lines 235-257: Registration Instance (normal)

## Core Entities

- `Attendance`: Person-specific attendance fact written by check-in, group attendance, rapid attendance, mobile attendance, or related flows.
- `Attribute`: Rock concept/entity referenced by the event-registration guide.
- `Block`: Rock concept/entity referenced by the event-registration guide.
- `Campus`: Rock concept/entity referenced by the event-registration guide.
- `Family`: Rock concept/entity referenced by the event-registration guide.
- `Group`: Concrete attendance destination, room, service, team, class, or group.
- `GroupMember`: Rock concept/entity referenced by the event-registration guide.
- `Label`: Rock concept/entity referenced by the event-registration guide.
- `Page`: Rock concept/entity referenced by the event-registration guide.
- `Person`: Rock concept/entity referenced by the event-registration guide.
- `PersonAlias`: Rock concept/entity referenced by the event-registration guide.
- `Schedule`: Time window that makes groups and locations available for check-in or attendance.

## Version Caveats

- `18.3`: Fixed an issue with internal Event Registration blocks (Registration Instance - Registration List, Registration Details, and Registrant Details) where a Signature Document could be incorrectly shown for a registrant with
- `19.1`: Added a Prevent Duplicate Registrants setting to the Registration Template that prevents the same person record from registering for the same Registration Instance more than once. When enabled, the Registration Entry Blo
- `19.1`: Added Registrant eligibility rules to the Registration Template Detail Block and updated the Registration Entry Block to prevent incorrect family member registrations. Added new "Registrant Eligibility" settings to the R
- `19.1`: Fixed an issue in the Registration Instance Registration List block where the Discount Code column on the Registrations tab was hidden when the registration template had no per-registrant cost, even if a discount code wa

## Files For Agents

- `guide.md`: long-form guide.
- `task-cards.jsonl` and `tasks/*.md`: operational entrypoints.
- `entities.jsonl`: concept-specific entity/model/table map.
- `section-source-map.jsonl`: section citations and source authority.
- `section-status.jsonl`: section review/staleness hints.
- `release-caveats.jsonl`: version-specific source rows.
- `troubleshooting-tree.json`: machine-readable branch selector.
