---
id: authored-hosting-infrastructure
title: Hosting And Infrastructure
generated: true
guide_status: starter_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Hosting And Infrastructure

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Hosting And Infrastructure index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Use this concept for Rock hosting, infrastructure sizing, Azure hosting, SSL, SMTP, storage, backups, web farms, performance posture, and operational readiness.

The primary official branch is `documentation/supporting-rock/hosting` ([Rock Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting)). This branch is operationally important enough to be separate from general system administration because hosting decisions affect reliability, performance, upgrade safety, storage, security, and email delivery.

Agents should distinguish hosting guidance from in-application administration. Service jobs, exception logs, and cache troubleshooting usually belong in System Administration And Operations. Server topology, deployment environment, storage, SMTP, SSL, backup, and scaling questions belong here.

## 2. Agent Workflow

Start by identifying the environment: self-hosted, Azure, hosted provider, development, staging, or production. Then identify which layer is involved: web server, database, storage, SMTP, DNS, SSL, job runner, cache, load balancer, or external service dependency ([Azure Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting/azure-hosting)).

For recommendations, avoid one-size-fits-all sizing. Confirm Rock version, database size, traffic, check-in load, communication volume, media/document storage, integrations, job workload, and backup/restore requirements.

For troubleshooting, separate application symptoms from infrastructure causes. A slow page, failed job, failed email, missing file, or timeout may be caused by Rock configuration, custom code, database performance, storage permissions, SMTP settings, SSL/DNS, or resource saturation.

## 3. Boundaries

Do not provide secret values, private hostnames, internal IPs, database names, or environment-specific credentials in public KB artifacts. Public guidance should stay at the pattern level and point agents to local verification steps ([Hosting](https://community.rockrms.com/documentation/supporting-rock/hosting)).

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

- `documentation/supporting-rock/hosting`
- `documentation/supporting-rock/caching` as a subguide-level dependency
- `documentation/core-concepts/search` as a subguide-level dependency

Use release notes for hosting-affecting changes, especially database, job, cache, search, web farm, and infrastructure compatibility changes. Use this concept with System Administration And Operations for incident triage and with Security And Permissions for SSL, access, and exposure questions ([Caching](https://community.rockrms.com/documentation/supporting-rock/caching)).
