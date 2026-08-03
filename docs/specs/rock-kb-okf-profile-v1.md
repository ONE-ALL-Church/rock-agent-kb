---
type: Reference
title: Rock KB OKF Extension Profile v1
description: Interoperable extension fields and distribution rules used by Rock KB OKF v0.1 bundles.
resource: https://github.com/ONE-ALL-Church/rock-agent-kb/blob/main/docs/specs/rock-kb-okf-profile-v1.md
tags:
  - okf
  - interoperability
  - provenance
---

# Rock KB OKF Extension Profile v1

This profile extends Open Knowledge Format v0.1 without changing its required
fields or reserved-file behavior. Generic OKF consumers may ignore every field
defined here. Rock-aware consumers can use them for trust, exact lookup,
version routing, integrity, and graph traversal.

## Bundle Metadata

`okf-manifest.json` uses schema `rock-kb-okf-distribution-v1` and declares:

- `okf_version`: targeted upstream OKF version.
- `okf_spec_commit`: reviewed upstream specification commit.
- `okf_profile`: `rock-kb-okf-profile-v1`.
- `profile`: `full` or `core`.
- `distribution_version`, `source_commit`, and `generated_at`.
- `read_only: true`.
- canonical scope, exclusions, record counts, changes, licensing, and hashes.

The `full` profile is the lossless public projection. The `core` profile is a
smaller agent-oriented subset containing concepts, bounded source-backed guide
sections, answers, non-routing-only claims, recipes, Lava contexts, stable model
digests, task cards, and source-policy references. Guide sections are grouped at
`guide-sections/<concept-id>/` so each directory index remains bounded and an
agent can browse detail within the relevant concept. Public Rock issue routing
records are full-profile only because they are numerous, version-sensitive, and
always `routing_context_only`. Approved issue enrichments remain nested on their
one canonical issue record rather than becoming duplicate OKF documents.
Canonical IDs are shared between profiles.

## Concept Frontmatter

Rock KB concept documents may add:

- `id` and `canonical_id`: the domain record identifier.
- `result_id`: hosted-search identifier when it differs from the canonical ID.
- `authority_tier` and `claim_tier`: trust and answer-use routing.
- `rock_versions`: applicable Rock releases.
- `content_hash` and `source_content_hash`: change and evidence lineage.
- `retrieved_at`: source retrieval time, separate from meaningful-change
  `timestamp`.
- `source_path`: public repository provenance.
- `structured_record`: bundle-relative JSON representation.
- `relationships`: typed links whose Markdown equivalents remain in the body.
- `okf_profile`: extension profile identifier.

Unknown fields must be preserved when practical and must never make an
otherwise conformant OKF document invalid.

## Relationships

`relationships.jsonl` contains `rock-kb-okf-relationship-v1` rows with
`source`, `target`, and `type`. Paths omit the `.md` suffix and use OKF concept
IDs. Current relationship types include `about`, `supported_by`, `uses_model`,
`related_model`, and `supersedes`. Rock issue records link to concept, source,
and explicit model records without making the issue report an approved claim.

Standard Markdown links remain authoritative for generic OKF graph consumers.
Typed rows are an optional acceleration and routing layer.

## Integrity And Safety

`checksums.sha256` covers every bundle file except itself.
`file-manifest.jsonl` records path, bytes, and SHA-256 values for the immutable
snapshot. Release archives are rooted, path-safe, size-bounded when consumed,
and accompanied by GitHub release digests and provenance attestations.

Strict Rock verification also enforces public/private boundaries. Standard OKF
conformance does not imply that content is authoritative, safe to publish, or
approved for import.

## Import Boundary

These distributions are read-only. Imported OKF records must become review
candidates and pass licensing, redaction, authority, deduplication, concept,
organization, and maintainer approval gates before entering trusted knowledge.
