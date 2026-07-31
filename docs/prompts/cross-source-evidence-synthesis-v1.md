# Cross-Source Evidence Synthesis V1

Prompt ID: `cross-source-evidence-synthesis`

Prompt version: `1.0.0`

Use this contract only to create a maintainer-reviewed canonical artifact when
two or more public source types materially clarify the same Rock behavior.
Ordinary documents, issues, release notes, and source files remain independently
retrievable; a synthesis is not justified merely because they share keywords.

## Inputs

Provide bounded public-safe source snapshots and addressable source units. Each
unit must retain:

- stable source and snapshot identity;
- canonical public URL;
- immutable revision identity when the source supports it;
- exact public locator, such as an article section, issue number, release
  record, source symbol, and pinned line span;
- authority tier, observed timestamp, content hash, and source-work identity;
- a public summary rather than copied expressive source text.

Do not provide private repositories, production-instance evidence, SQL output,
logs, secrets, person data, organization identifiers, or mutable source-code
links without a pinned commit.

## Evidence Semantics

Keep source roles explicit:

- An issue `reports` a symptom, affected version, or proposed explanation. It
  does not prove cause, applicability, or remediation.
- An official release record `supports` a shipped product-version statement.
- Immutable public source code `demonstrates` the implementation at that exact
  commit and line span.
- Documentation may `supports`, `qualifies`, or `supersedes` a statement
  according to its text and revision.
- Contradictory evidence remains `contradicts`; do not average it into a
  confident claim.

Treat mirrors of one underlying work as one independence group. A linked issue,
release note, and commit are not automatically independent corroboration.

## Required Reasoning

1. Identify the narrow behavior shared by the supplied source units.
2. Separate reported affected versions, implementation versions, officially
   fixed versions, documentation revisions, and current behavior.
3. Preserve unknown scope. Do not convert an issue's reporter version into a
   universal affected range or a release-note version into proof about earlier
   versions.
4. Prefer one complete, declarative retrieval unit. Create a task card,
   troubleshooting node, or structured reference only when the evidence
   supports that operational shape.
5. Add concept and topic facets for routing without copying the same artifact
   into concept-specific rows.
6. Add typed relationships only when the supplied source units support the
   edge. Every edge must cite its evidence unit IDs and include a rationale.
7. Preserve public result IDs and source locators. Never invent model slugs,
   issue IDs, versions, fields, settings, causes, fixes, or links.
8. Write one exact and one paraphrased retrieval evaluation. A question naming
   an issue may legitimately rank the exact issue before the synthesis, so set
   the bounded accepted rank accordingly.

## Output And Review

Return only `rock-kb-reviewed-cross-source-artifact-v1` JSON after a maintainer
has reviewed the wording, evidence roles, version scope, relationships, and
evaluations. Record the exact model, this prompt ID and version, reviewer,
review timestamp, and review rationale.

Promotion must fail when evidence comes from fewer than two distinct public
sources, source units contain private text, a relationship cites unknown
evidence, a scoped statement has no Rock version, or evaluations do not cover
both exact and paraphrased retrieval.

The resulting bundle is canonical shadow input. Promotion alone must not change
the default public reader. A separately authorized canary may expose it only to
anonymous opted-in `external-test` or `maintainer` cohorts.
