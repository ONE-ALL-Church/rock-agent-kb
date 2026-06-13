# Documentation Index

## Runbooks

- [CLI Reference](runbooks/cli-reference.md) - grouped `kb` command reference and old-command disposition table.
- [Pipeline Overview](runbooks/pipeline-overview.md) - rebuild, media, claim, corpus, answer-pack, source-summary, and readiness workflow overview.
- [Agent Serving Runbook](runbooks/agent-serving.md) - local MCP server, hosted Worker service, terminal client, and deployed evaluation gate.
- [Model Map Rebuild Runbook](runbooks/model-map-rebuild-runbook.md) - stable/latest generic Rock Model Map scrape, rebuild, validation, and review workflow.
- [Contributor Reviewer Workflow](runbooks/contributor-reviewer-workflow.md) - community contribution, media review, claim promotion, and rebuild workflow.
- [Community Onboarding](community-onboarding.md) - how another church and its agents consume and contribute to the public KB.
- [Public Surface Runbook](runbooks/public-publish-runbook.md) - public surface, scratch export, and contribution workflow.
- [Local Public Surface Audit](runbooks/local-public-surface-audit.md) - local pre-commit checks for public/private boundary and contribution bundles.
- [Source Rebuild Orchestration Runbook](runbooks/source-rebuild-orchestration-runbook.md) - source scan, refresh, dry-run, rebuild, and PR automation workflow.
- [Local Transcription](runbooks/local-transcription.md) - local and hosted transcription model decision and media promotion process.
- [Private Corpus Cloud Runbook](runbooks/private-corpus-cloud-runbook.md) - restore/sync/autonomous ingest plan for private transcripts and review artifacts.
- [Public Repo README Template](public-repo-readme.md) - public export README template intentionally kept at the root of `docs/` because `src/rock_kb/publish.py` reads this exact path.

## Decisions

- [Agent Knowledge Network Goal](decisions/agent-knowledge-network-goal.md) - north-star networked KB, hosted service, and autonomous contribution goal.
- [Incremental Architecture Refactor Goal](decisions/incremental-architecture-refactor-goal.md) - detailed Milestone 0 execution plan.
- [Project Goal](decisions/project-goal.md) - durable project goal and readiness framing.
- [Public Private Knowledge System Goal](decisions/public-private-knowledge-system-goal.md) - public/private boundary and system posture.
- [Claim Graph Refactor Goal](decisions/claim-graph-refactor-goal.md) - claim graph architecture goal.
- [Claim Graph Research Notes](decisions/claim-graph-research-notes.md) - research behind the claim graph approach.
- [Claim Tier Policy](decisions/claim-tier-policy.md) - claim tier definitions and promotion policy.
- [Data Organization Decision](decisions/data-organization-decision.md) - data layout decision record.
- [Current Tooling Research](decisions/current-tooling-research.md) - crawler, document conversion, and transcription tooling decisions.
- [Public Export Policy](decisions/public-export-policy.md) - public export privacy, licensing, and allowed-content policy.
- [Topic Split Rules](decisions/topic-split-rules.md) - routing rules for deciding whether a domain belongs in a new concept or an existing guide.
- [Private And Org Data Integration Plan](decisions/private-and-org-data-integration-plan.md) - owner-private docs and outside-org contribution bundle plan.
- [Org Data Implementation Roadmap](decisions/org-data-implementation-roadmap.md) - roadmap for private org data, outside-org bundles, review gates, and rebuild tracking.

## Working Notes

Dated implementation logs, candid review notes, live-instance details, and maintainer handoffs belong in the private corpus, not in this community-facing public tree.
