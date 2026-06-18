---
id: authored-documents-signatures
title: Documents And Signatures
generated: true
guide_status: starter_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Documents And Signatures

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Documents And Signatures index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Use this concept when the task involves Rock documents, document types, merge documents, generated PDFs, electronic signatures, signature templates, signature documents, or document-driven workflow and registration steps.

The primary official branch is `documentation/core-concepts/documents` ([Rock Documents](https://community.rockrms.com/documentation/core-concepts/documents)). Treat that branch as the routing anchor for source selection. Documents can cross People, Groups, Workflows, Event Registration, Communications, Security, CMS, and file storage, so do not answer from a single page title or model name alone.

The main operational distinction is:

- Entity documents attach files or documents to an entity such as a person or group.
- Merge documents produce document output from Rock data.
- Electronic signatures collect signed documents through workflows or registrations.
- Generated PDFs may involve server workload, external PDF generation choices, and delivery to the signer.

## 2. Agent Workflow

Start with the concept index and source map, then inspect official document articles before using recipes or community rows ([Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures)).

For setup questions, identify the document type, template, file type, storage provider, and target entity. For signature questions, identify the signature document template, workflow action or registration requirement, signed document record, signer identity, and PDF-generation path. For access questions, inspect file type security, document type security, entity security, page or block security, and whether a workflow or registration is exposing the document.

For troubleshooting, verify the exact local Rock version and whether the problem is template configuration, merge field data, workflow context, registration context, missing signer identity, PDF generation, communication delivery, or security.

## 3. Boundaries

Do not treat this as a general file-management concept. If the user is asking about website media, route to CMS or content personalization. If the user is asking about registration eligibility or payments, route to Event Registration and use this concept only for the signature/document part ([Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents)).

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

No approved claims are currently routed to this concept.
<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `2`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Electronic Signatures Transcript Insight](https://community.rockrms.com/rocku/event-registration/electronic-signatures) | approved_for_public_distillation | 2 | media-insight:7ededa8a19f050ad |
| [Electronic Signatures Transcript Insight](https://community.rockrms.com/rocku/workflows/electronic-signatures-1) | approved_for_public_distillation | 2 | media-insight:ddfbf4b112e0b7a8 |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 4. Source Map And Dependency Notes

Durable official routing:

- `documentation/core-concepts/documents`
- `documentation/core-concepts/documents/entity-documents`
- `documentation/core-concepts/documents/merge-documents`
- `documentation/core-concepts/documents/electronic-signatures`

Use release notes for version-sensitive fixes around signature document templates, generated PDFs, registration signature documents, and workflow document actions. Use model-map landmarks for `Document`, `Document Type`, `Signature Document`, and `Signature Document Template` when an answer needs entity or API orientation ([Generated PDFs](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume)).
