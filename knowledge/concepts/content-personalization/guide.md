---
id: authored-content-personalization
title: Content And Personalization
generated: true
guide_status: starter_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Content And Personalization

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Content And Personalization index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Use this concept for content channels, content items, assets, structured content, adaptive messages, personalization, segments, publishing workflows, and website content operations.

The durable official branches are:

- `documentation/digital-publishing/content-management` ([Content Management](https://community.rockrms.com/documentation/digital-publishing/content-management))
- `documentation/digital-publishing/personalization`

This concept narrows the broad CMS And Websites area. Use CMS And Websites for pages, blocks, themes, navigation, and site structure. Use Content And Personalization when the task is about the content inventory, content channel modeling, publishing, adaptive content, or audience-specific presentation.

## 2. Agent Workflow

Start by identifying the content object: content channel, content channel item, structured content item, asset, adaptive message, segment, or page block that renders content ([Personalization](https://community.rockrms.com/documentation/digital-publishing/personalization)).

For content-channel work, inspect the channel type, item attributes, status, start/end dates, slugs, security, Lava rendering, and any workflows or jobs that create or publish items. For personalization, inspect the segment or adaptive message configuration, matching criteria, fallback behavior, block/page placement, and whether the local person context is available.

For troubleshooting, separate content existence from rendering. A content item can exist but fail to display because of status, dates, security, Lava errors, missing attributes, routing/slugs, cache, block settings, or personalization criteria.

## 3. Boundaries

Do not use this concept for generic page layout unless content or personalization is the core issue. Media storage may belong here when tied to content operations, but app publishing assets belong under Mobile or TV concepts ([Content Management](https://community.rockrms.com/documentation/digital-publishing/content-management)).

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

Use official documentation branches for content and personalization first. Use Lava when rendering logic or entity commands are involved. Use Security And Permissions for audience visibility. Use Communications when content is reused in email/SMS. Use model-map landmarks for `Content Channel`, `Content Channel Item`, `Adaptive Message`, and related CMS entities ([Adaptive Messages](https://community.rockrms.com/documentation/digital-publishing/personalization/adaptive-messages)).
