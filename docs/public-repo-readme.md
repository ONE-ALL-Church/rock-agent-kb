# Rock General Knowledge Base

This repository is the public, community-facing export of a generated Rock RMS knowledge base. It is designed for AI agents and human reviewers who need source-linked guidance about Rock concepts, model-map details, release caveats, Lava capabilities, and operational patterns.

This public tree is the canonical public workspace. Generated files should be updated by changing reviewed sources or contribution bundles, then rebuilding through the checked-in `kb` pipeline and audits.

## Start Here

- `agent/README.md` explains the agent-ready indexes, answer pack, model map, and source summaries.
- `knowledge/README.md` explains the generated concept guides and model-map pages.
- `sources/registry.yaml` lists public source families and their publish policy.
- `community-contributions/README.md` explains how outside organizations and agents can submit reviewed public-safe contribution bundles.
- `docs/community-recipes.md` explains how code owners publish reusable recipes while the KB tracks immutable source, compatibility, security, and learnings.
- `docs/decisions/public-export-policy.md` explains what is allowed in the public export.
- `docs/runbooks/pipeline-overview.md` explains the rebuild and audit flow.

## Contribution Model

External contributors should open PRs against `community-contributions/<org-id>/bundle.jsonl` or `source-suggestions/`. Do not hand-edit generated `agent/`, `claims/`, `concepts/`, `knowledge/`, `sources/`, or `contributions/` files in the public repo.

The PR workflow validates accepted contribution bundles in place. Maintainers rebuild generated artifacts through the normal pipeline, audit the public boundary, and promote authority tiers only through the review workflow.

## Public Boundary

This export may include source links, distilled public summaries, approved public claims, generic live-verification notes, and public model-map data. It should not include private transcripts, raw private docs, SQL dumps, internal IDs, secrets, connected-instance evidence details, or copied proprietary content.
