# Rock Ideas Intelligence

Rock Community [Ideas](https://community.rockrms.com/ideas) records community-submitted feature requests and their public lifecycle labels. The KB ingests only bounded metadata so agents can find known product gaps, relate them to concepts, and research roadmap state without treating community proposals as product documentation.

## Why This Belongs In The KB

Ideas answer a different question from documentation and GitHub issues:

- Documentation describes supported behavior and operating guidance.
- GitHub issues report possible defects in existing behavior.
- Ideas describe desired capabilities, unmet workflows, and public planning labels.

The Ideas catalog is therefore a first-class routing surface with `kind: rock_idea`, `authority_tier: community-unreviewed`, and `claim_tier: routing_context_only`. It does not feed approved claims or ordinary source summaries.

## Observed Public Shape

The public list and detail surfaces expose enough structured metadata for a useful catalog:

- Identity: stable idea number, canonical ID, title, and public URL.
- Classification: category and lifecycle status.
- Community signal: vote count.
- Planning metadata: planned-version label, ministry-strength score, and feature-size label when present.
- Timing: submitted and staff-response update timestamps when public markup exposes them.
- KB routing: concept IDs plus route provenance derived conservatively from official category and exact title signals.
- Related evidence: allowlisted link targets found in proposal or staff-response sections, without retaining anchor text or surrounding content.
- Sparse model links: exact multiword model names or their code-style aliases in the public title; ambiguous one-word domain names are excluded.
- Release corroboration: high-confidence official release-note matches require an exact planned version and full meaningful-title-token coverage. Partial matches remain in a private maintainer review queue.
- Freshness: separate `last_checked_at`, `detail_last_checked_at`, `content_changed_at`, and `content_hash` values.

Observed categories include API, Apple TV, CMS, Check-in, Communication, Connection, Core, CRM, Engagement, Event, Farm, Finance, Group, Lava, LMS, Mobile, Other, Prayer, Reminders, Reporting, Security, and Workflow.

Observed lifecycle labels are `Open`, `Pending`, `Under Review`, `Planned`, `Started`, `Complete`, and `Not Planned`. The generated rows normalize these labels to stable snake-case values while retaining the display label.

## Discovery Method

The Ideas list and detail pages are legacy feature-request blocks. No public first-class enumerate-all Ideas REST resource was found. The Community site's Obsidian Universal Search block action exposes search results, but live testing found that it stops after roughly 200 results per query even when it reports a much larger total. It is useful for discovery, not complete catalog ingestion.

The refresh therefore:

1. Traverses the public Feature Request View's native ASP.NET partial-postback pager from the first page to the final page.
2. Parses only bounded metadata from each response and deduplicates by idea number; raw response HTML is never persisted.
3. Rejects the refresh before replacing artifacts if a page is empty, repeats, omits the expected update panel, or fails before the final page.
4. Enriches a bounded set of new, lifecycle-changed, old-shape, and least-recently checked ideas from public detail pages.
5. Preserves previously enriched detail metadata until that row is selected for another detail check.

The legacy pager is an implementation detail and can change. Parser fixtures, completeness reporting, record-count checks, newest-ID checks, and public-shape validation must fail visibly when the source changes.

## Public-Safety Boundary

The KB deliberately does not republish:

- proposal descriptions or attached media;
- submitter or organization identity;
- staff response text or staff identity;
- comments or commenter identity.

Those fields remain available only at the linked canonical public page. This keeps the KB focused on routing metadata and avoids creating a derivative mirror of community-authored content.

The parser may retain only the canonical target URL, target ID/kind, link origin (`proposal` or `staff_response`), and authority tier for allowlisted official Rock documentation, release notes, SparkDevNetwork source/issues, or another Rock Idea. It never stores anchor text, surrounding text, arbitrary external links, URL credentials, or query strings.

## Relationship Rules

`agent/rock-idea-relationships.jsonl` is the canonical typed-edge projection. It contains deterministic `about` concept routes, conservative exact-model links, explicit public-page links, and high-confidence release corroboration. It does not claim that title similarity proves an issue implements an Idea.

- `implemented_by_issue` requires both a high-confidence official release-note match and an issue reference in that release note.
- `references_issue` means only that the public Idea page explicitly links to the issue.
- `corroborated_by_release_note` means the planned version and all meaningful Idea-title tokens matched one official release row.
- Every edge carries its basis, evidence URL, authority, confidence, review state, and `needs_live_verification: true`.
- Partial release matches are written only to ignored maintainer review data and never published automatically.

Exact Idea retrieval returns outbound relationships. Exact issue retrieval returns matching inbound Idea relationships. Concept packages expose a bounded Idea summary and at most eight lifecycle-prioritized highlights; use Ideas search/list for the full concept-filtered catalog.

## Verification Queue

`agent/rock-idea-verification-queue.jsonl` prioritizes every `Complete`,
`Planned`, `Started`, and `Under Review` lifecycle row for evidence review. It
uses vote count, lifecycle state, planned-version metadata, explicit references,
and the presence of private release-note candidates to assign a bounded priority.

- `officially_corroborated` requires deterministic high-confidence official release evidence.
- `maintainer_reviewed_references_only` means a maintainer checked the current
  Idea, explicit references, and candidate set, but those references do not
  confirm the claimed release.
- `maintainer_reviewed_no_official_match` means the current bounded official
  inputs produced no match. It does not prove that the feature is absent or
  that no older source can corroborate it.
- `candidate_review_pending` means a possible release match exists only in ignored maintainer data; candidate details are not public evidence.
- `references_available` means useful explicit links exist but do not prove implementation.
- `evidence_needed` means no corroborating or reference edge is currently available.

Each queue row stores the source content hash, evidence relationship hashes, a
candidate-set hash, and a combined `review_input_hash`. A changed Idea,
relationship, or candidate set therefore changes the review input and returns
the lifecycle claim to maintainer attention. Queue state never changes the
Idea's `community-unreviewed` and `routing_context_only` trust level.

Maintainer dispositions live in
`ideas/verification-reviews.jsonl`. The ledger accepts only stable IDs, exact
input hashes, fixed outcomes and reason codes, reviewer/timestamp metadata, and
redaction and license attestations. It rejects free-form notes and raw Idea or
staff-response content. A current reviewed release match can produce an
official `corroborated_by_release_note` edge; negative and reference-only
reviews only close the current queue input. Any changed Idea, relationship,
candidate set, or reviewed release evidence makes the disposition stale and
requeues the Idea automatically.

For a bounded review batch:

1. Start with high-priority rows in the generated verification queue.
2. Inspect explicit public references and the ignored release candidates under
   `data/review/rock-ideas/`, then verify any proposed match against the exact
   official release record.
3. Record only one fixed-vocabulary disposition for the current hashes. Use
   `no_official_match` when the bounded inputs do not establish a match; never
   convert that outcome into a product-absence claim.
4. Run `uv run kb ideas sync --skip-details` and `uv run kb ideas validate`.
   Confirm that stale dispositions reopened and current dispositions moved out
   of the high-priority queue.

## Trust Rules

- An idea is evidence that someone requested a capability, not proof that Rock lacks every equivalent workflow.
- `Planned` and `Started` are planning signals, not release guarantees.
- `Complete` is not by itself proof that the feature shipped in a particular build or works on a particular instance.
- `Not Planned` does not prove that no plugin, recipe, workaround, or later implementation exists.
- Vote counts are prioritization context, not technical authority.

Before making a product claim, corroborate an idea with official documentation, release notes, public source code, and authorized read-only instance verification. The [Ideas and Core Changes](https://community.rockrms.com/ideas-changes) guidance remains the official context for how proposals and core changes are handled.

## Commands

Maintainer refresh and local inspection:

```bash
uv run kb ideas sync
uv run kb ideas validate
uv run kb ideas list --status planned --concept workflows
uv run kb ideas get 2250
```

Published agent CLI:

```bash
uvx rock-kb ideas search "workflow feature request"
uvx rock-kb ideas list --status complete --planned-version 20.0
uvx rock-kb idea 2250
```

MCP tools:

- `kb_search_rock_ideas`
- `kb_list_rock_ideas`
- `kb_get_rock_idea`

Use these tools only for explicit idea, feature-request, known-gap, or roadmap questions. Start ordinary implementation and troubleshooting questions with `kb_search`.

## Generated Artifacts

- `agent/rock-ideas.jsonl`: public-safe canonical metadata rows.
- `agent/rock-idea-relationships.jsonl`: canonical typed edges to concepts, models, issues, other Ideas, official documentation/source, and corroborating release records.
- `agent/rock-idea-verification-queue.jsonl`: prioritized lifecycle verification rows with hash-based revalidation inputs and no speculative candidate details.
- `ideas/verification-reviews.jsonl`: bounded public-safe maintainer
  dispositions tied to exact source, relationship, candidate, and release
  evidence hashes.
- `agent/rock-idea-summary.json`: counts, discovery coverage, and trust boundary.
- `knowledge/ideas/index.md`: concise agent and human usage guidance.
- `data/normalized/rock_ideas.jsonl`: private pipeline source records.

Ideas refresh weekly with the comprehensive public-source refresh. `last_checked_at` means the row was seen in a complete catalog traversal; `detail_last_checked_at` records the separate rolling detail-page check. Source freshness reports track the normalized rows like other registered sources.
