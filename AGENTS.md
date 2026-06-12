# Agent Instructions

This repository is the public, community-facing Rock RMS knowledge base. Keep the tracked tree public-safe and contributor-focused.

- Do not add candid implementation logs, maintainer handoffs, live-instance evidence, private SQL notes, private source paths, raw transcripts, raw media details, secrets, or local machine paths to this repo.
- Put dated working notes and private review evidence in the private corpus, not under `docs/log/`.
- Public contributions belong under `community-contributions/<org-id>/` or `source-suggestions/<org-id>/` until maintainer review promotes them into tracked public artifacts.
- Generated public files under `agent/`, `claims/`, `knowledge/`, `concepts/`, and `sources/` should be changed through the pipeline and audited before commit.
- Run `python3 scripts/audit_tracked_tree.py`, `python3 scripts/validate_bundle.py`, `uv run kb audit public-export`, and the relevant tests after changes that affect the public surface.
- Before any public launch, follow `docs/runbooks/github-public-repo-hardening.md`; local checks alone do not satisfy branch protection, ruleset, secret scanning, or push-protection requirements.
