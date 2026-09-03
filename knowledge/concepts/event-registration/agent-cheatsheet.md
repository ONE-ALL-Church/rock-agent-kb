---
concept_id: event-registration
title: Event Registration Agent Cheatsheet
generated: true
---

# Event Registration Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |
| [Recipe: Create a reusable registration and one event instance](tasks/recipe-create-a-reusable-registration-and-one-event-instance.md) | `Person`, `Group`, `Campus`, `Workflow`, `Block` | `Person`, `Group`, `Campus`, `Workflow`, `Block` |
| [Recipe: Validate a paid registration before launch](tasks/recipe-validate-a-paid-registration-before-launch.md) | `Schedule` | `Schedule` |
| [Recipe: Promote a wait-listed person to full registration](tasks/recipe-promote-a-wait-listed-person-to-full-registration.md) | `Person`, `Group`, `Attribute` | `Person`, `Group`, `Attribute` |
| [Recipe: Audit an event-registration dashboard](tasks/recipe-audit-an-event-registration-dashboard.md) | `Person`, `Label` | `Person`, `Label` |
| [Recipe: Launch family preregistration with follow-up](tasks/recipe-launch-family-preregistration-with-follow-up.md) | `Person`, `Campus`, `Check-in Configuration`, `Family`, `Workflow`, `Page`, `Attribute` | `Person`, `Campus`, `Check-in Configuration`, `Family`, `Workflow`, `Page`, `Attribute` |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Attendance` | `AttendanceOccurrence`, `PersonAlias` | Filter `DidAttend` when counting actual attendance. Do not infer group/schedule/location without joining occurrence context. |
| `Attribute` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Campus` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Check-in Configuration` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Family` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Label` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Location` | `Group`, `AttendanceOccurrence`, `Device` | Check active state, campus, location hierarchy, and printer behavior. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Schedule` | `Group`, `AttendanceOccurrence` | Schedule windows are a frequent reason eligible rooms do not appear. |
| `Step` | `StepType`, `StepProgram`, `Person` | Verify the Step row exists before troubleshooting badge display or engagement reporting. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |
| `18.3` | core | Fixed an issue with internal Event Registration blocks (Registration Instance - Registration List, Registration Details, and Registrant Details) where a Signature Document could be incorrectly shown for a registrant without a valid Signatur |
| `19.1` | core | Added a Prevent Duplicate Registrants setting to the Registration Template that prevents the same person record from registering for the same Registration Instance more than once. When enabled, the Registration Entry Block checks for existi |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `agent-summary` | normal | live verification |
| `registration-instances-put-occurrence-specific-settings-on-the-instance` | normal | live verification |
| `forms-identity-eligibility-and-communications-test-combined-eligibility` | citation-only | live verification |
| `forms-identity-eligibility-and-communications-verify-communications-as-part-of-the-lifecycle` | normal | live verification |
| `payments-configure-the-finance-path-deliberately` | normal | live verification |
| `payments-match-externally-entered-transactions` | normal | live verification |
| `event-calendar-link-the-occurrence-registration-and-group` | normal | live verification |
| `family-preregistration-and-follow-up` | community-supported | live verification |
| `reporting-and-reconciliation` | normal | live verification |
| `permissions-and-operational-control` | normal | live verification |
| `troubleshooting-decision-tree-the-public-event-has-no-register-button` | normal | live verification |
| `troubleshooting-decision-tree-a-representative-person-is-unexpectedly-ineligible` | citation-only | live verification |
| `troubleshooting-decision-tree-a-duplicate-registration-warning-exposes-sensitive-participation` | normal | live verification |
| `troubleshooting-decision-tree-a-person-moved-from-the-wait-list-is-missing-payment-or-form-data` | high | live verification |
| `troubleshooting-decision-tree-a-registration-balance-no-longer-matches-its-payment-plan` | normal | live verification |
| `troubleshooting-decision-tree-a-batch-transaction-is-not-attached-to-the-registration` | normal | live verification |
| `troubleshooting-decision-tree-registrants-are-not-entering-the-expected-group` | normal | live verification |
| `troubleshooting-decision-tree-dashboard-totals-disagree` | normal | live verification |
| `troubleshooting-decision-tree-a-signature-document-is-missing-or-belongs-to-the-wrong-registration` | normal | live verification |
| `agent-task-recipes-recipe-create-a-reusable-registration-and-one-event-instance` | normal | live verification |
| `agent-task-recipes-recipe-validate-a-paid-registration-before-launch` | normal | live verification |
| `agent-task-recipes-recipe-promote-a-wait-listed-person-to-full-registration` | normal | live verification |
| `agent-task-recipes-recipe-audit-an-event-registration-dashboard` | community-supported | live verification |
| `agent-task-recipes-recipe-launch-family-preregistration-with-follow-up` | citation-only | live verification |
| `known-gaps-and-live-verification` | structural | live verification |
| `source-map-approved-community-guidance-and-examples` | community-supported | community-supported |
