---
id: authored-obsidian-development
title: Obsidian Development
generated: true
guide_status: starter_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Obsidian Development

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Obsidian Development index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Use this concept for Obsidian block development, TypeScript components, C# block actions, grid reference, field types, browser bus, custom actions, development environment, and migration from older WebForms patterns.

The durable official branch is `developer/obsidian` ([Obsidian](https://community.rockrms.com/developer/obsidian)). This deserves first-class routing because the developer documentation now has a meaningful Obsidian branch with many articles, and agents need to distinguish Obsidian-specific patterns from general Rock developer guidance.

## 2. Agent Workflow

Start by identifying whether the task is a list block, detail block, field type, grid behavior, browser-side interaction, block action/API boundary, security concern, or development environment issue ([Creating Blocks](https://community.rockrms.com/developer/obsidian/blocks/creating-blocks)).

For implementation questions, inspect the relevant official Obsidian branch first, then source-code examples in SparkDevNetwork/Rock when available. Verify whether the pattern applies to plugins or only to core blocks; some code-generation and core-development notes may not apply to plugin authors.

For security questions, check page/block security, block action authorization, entity authorization, request inputs, and whether the UI is relying on client-side state that must be revalidated server-side.

## 3. Boundaries

Do not route all developer questions here. General API, REST, jobs, migrations, coding standards, and packaging still belong in Developer Resources or API And Integrations unless the task specifically uses Obsidian UI architecture ([Grid Reference](https://community.rockrms.com/developer/obsidian/grid-reference)).

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

No approved claims are currently routed to this concept.
<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

No approved media distillations are currently routed to this concept.
<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 4. Source Map And Dependency Notes

Durable official routing:

- `developer/obsidian`
- `developer/obsidian/blocks`
- `developer/obsidian/grid-reference`
- `developer/obsidian/creating-field-types`
- `developer/obsidian/core-development-environment`

Use release notes for Obsidian behavior changes and use source code for current implementation examples. Treat generated docs as implementation guidance, then verify against the target Rock version and plugin/core context ([Core Development Environment](https://community.rockrms.com/developer/obsidian/core-development-environment)).
