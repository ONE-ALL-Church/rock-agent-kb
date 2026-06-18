---
concept_id: documents-signatures
title: Documents And Signatures Agent Cheatsheet
generated: true
---

# Documents And Signatures Agent Cheatsheet

## Tasks

| Task | Inspect | Entities |
| --- | --- | --- |

## Entities

| Entity | Common Joins | Agent Notes |
| --- | --- | --- |
| `Block` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Group` | `GroupType`, `Location`, `Schedule`, `AttendanceOccurrence` | Verify active state, campus, group type, location, schedule, and capacity assumptions. |
| `Page` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Person` |  | Verify the exact record/entity shape in the live Rock version before making changes. |
| `Workflow` |  | Verify the exact record/entity shape in the live Rock version before making changes. |

## Release Caveats

| Version | Channel | Summary |
| --- | --- | --- |

## Sections Needing Review

| Section | Confidence | Reason |
| --- | --- | --- |
| `generated-model-map-pointers` | citation-only | live verification |
| `2-agent-workflow` | normal | live verification |
