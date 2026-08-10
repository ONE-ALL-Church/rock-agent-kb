---
type: Reference
title: Rock KB OKF Extension Profile v2
description: Interoperable extension fields and distribution rules used by Rock KB OKF v0.2 bundles.
resource: https://github.com/ONE-ALL-Church/rock-agent-kb/blob/main/docs/specs/rock-kb-okf-profile-v2.md
tags:
  - okf
  - interoperability
  - provenance
---

# Rock KB OKF Extension Profile v2

This profile extends Open Knowledge Format v0.2 without changing its required
`type` field or reserved-file behavior. Generic OKF consumers may ignore every
Rock-specific field defined here. Rock-aware consumers can use them for trust,
exact lookup, version routing, integrity, and graph traversal.

## Bundle Metadata

`okf-manifest.json` uses schema `rock-kb-okf-distribution-v2` and declares:

- `okf_version: "0.2"` and the reviewed `okf_spec_commit`.
- `okf_profile: rock-kb-okf-profile-v2`.
- `profile`: `full` or `core`.
- `distribution_version`, `source_commit`, and `generated_at`.
- `read_only: true`.
- canonical scope, exclusions, record counts, changes, licensing, and hashes.

The `full` profile is the lossless public projection. The `core` profile is a
smaller agent-oriented subset containing concepts, answers, non-routing-only
claims, recipes, Lava contexts, stable model digests, task cards, and
source-policy references. Public Rock issue and Idea routing records are
full-profile only because they are numerous, version-sensitive, and routing
context. Approved issue enrichments remain nested on their canonical issue
record rather than becoming duplicate OKF documents. Canonical IDs are shared
between profiles.

## OKF v0.2 Provenance

Every non-reserved Markdown document in a Rock v2 distribution has:

- `generated.by: process:rock-kb-okf-export`.
- `generated.at`: the canonical record's meaningful-change time when known,
  otherwise the deterministic distribution generation time.
- a non-empty `sources` list. The canonical public repository record is
  included when a public source path exists. Registered evidence sources link
  to their bundle `references/` concept, and additional public citations retain
  their external resource URL.

Document-level source links remain in a human-readable `## Sources` body
section when present. The `sources` frontmatter is authoritative for OKF v0.2
provenance. Rock does not fabricate `verified`, usage, author, or freshness
signals when the canonical record does not contain that evidence.

## Rock Concept Frontmatter

Rock KB concept documents may also add:

- `id` and `canonical_id`: the domain record identifier.
- `result_id`: hosted-search identifier when it differs from the canonical ID.
- `authority_tier` and `claim_tier`: trust and answer-use routing.
- `rock_versions`: applicable Rock releases.
- `content_hash` and `source_content_hash`: change and evidence lineage.
- `retrieved_at`: source retrieval time, separate from `generated.at`.
- `source_path`: public repository provenance.
- `structured_record`: bundle-relative JSON representation.
- `relationships`: typed links whose Markdown equivalents remain in the body.
- `okf_profile`: this extension profile identifier.

Unknown fields must be preserved when practical and must never make an
otherwise conformant OKF document invalid.

## Relationships

`relationships.jsonl` contains `rock-kb-okf-relationship-v1` rows with
`source`, `target`, and `type`. Paths omit the `.md` suffix and use OKF concept
IDs. Current relationship types include `about`, `supported_by`, `uses_model`,
`related_model`, and `supersedes`.

Standard Markdown links remain authoritative for generic OKF graph consumers.
The v2 producer writes file-relative links so both the OKF specification and
the reviewed upstream reference parser can traverse the graph. Typed rows are
an optional acceleration and routing layer.

## Integrity And Safety

`checksums.sha256` covers every bundle file except itself.
`file-manifest.jsonl` records path, bytes, and SHA-256 values for the immutable
snapshot. Release archives are rooted, path-safe, size-bounded when consumed,
and accompanied by GitHub release digests and provenance attestations.

Strict Rock verification enforces the exact supported contract tuple:
OKF version, manifest schema, Rock profile, and reviewed upstream commit. It
also enforces public/private boundaries, generated/source provenance,
structured-record integrity, archive limits, and checksum coverage.

The current client continues to verify published Rock v0.1 bundles using their
legacy v1 manifest/profile/spec tuple. It does not reinterpret a mixed or
partially upgraded bundle as valid. Generic v0.2 consumers may use the upstream
`timestamp` and body-citation fallbacks when reading legacy v0.1 documents.

## Import Boundary

These distributions are read-only. Imported OKF records must become review
candidates and pass licensing, redaction, authority, deduplication, concept,
organization, and maintainer approval gates before entering trusted knowledge.
