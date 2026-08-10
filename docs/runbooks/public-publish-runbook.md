# Public Surface Runbook

The public target is now this repository's committed public surface, not a tracked `data/public-export/` copy. `kb publish export` still builds a local scratch payload and manifest for audit compatibility, but `data/public-export/` is ignored and should not be committed.

Recommended public repo layout:

```text
/
  README.md                      # public entry point
  agent/                         # generated public agent entrypoints
  claims/                        # generated/approved public claims
  concepts/                      # generated concept registry
  contributions/                 # reviewed contributions already imported into the build repo
  docs/                          # public docs and runbooks
  knowledge/                     # generated public guides and indexes
  sources/                       # public source registry
  public-export-manifest.json    # release manifest
  community-contributions/       # public intake; preserved by publish
  source-suggestions/            # public intake; preserved by publish
  .github/                       # public repo templates/workflows; preserved by publish
```

The default public docs are intentionally small: contributor workflow, public export policy, and this publish runbook. Build planning notes, topic split reports, rebuild orchestration notes, evaluation files, conflict reports, and claim review queues stay in the build repo unless maintainers intentionally decide to expose a specific artifact later.

Milestone 0.5 publishes by creating a fresh public repo with a single curated initial commit. Do not make this private build repo public in place. Use [GitHub Public Repo Hardening](github-public-repo-hardening.md) for the required GitHub settings, proof tests, and launch checklist.

## Transitional Scratch Export

From the build repo, generate the scratch payload only when you need a release-manifest-style audit view:

```bash
uv run kb publish export
uv run kb audit public-export
```

The export command:

1. Rebuilds ignored `data/public-export/`.
2. Writes `data/public-export/public-export-manifest.json`.
3. Runs the same public file projection used by `kb audit public-export`.

Do not use the scratch tree as a contributor edit target or a second source of truth. Milestone 1 replaces this with `kb deploy-service`, which will project directly from the committed public surface.

Before committing or publishing, run the local public-surface checks from [Local Public Surface Audit](local-public-surface-audit.md):

```bash
python3 scripts/audit_tracked_tree.py
python3 scripts/validate_bundle.py
uv run kb audit public-export
uv run kb audit all
```

## OKF Release Distribution

Tagged releases publish synchronized full and core read-only OKF v0.2 projections. Build them from the same canonical tracked records, commit, and `SOURCE_DATE_EPOCH`; verify the prior v0.1 full/core assets for backward compatibility; compare each with its prior profile; validate them independently; run the pinned official v0.2 reference parser against both profiles; attest the archives; and attach both profile asset sets to the release. The OKF trees remain ignored generated output and are never a second source of truth.

```bash
uv run kb publish okf --version X.Y.Z --source-commit "$(git rev-parse HEAD)" --archive-dir release-assets
uv run kb publish okf --profile core --destination data/okf-export-core --version X.Y.Z --source-commit "$(git rev-parse HEAD)" --archive-dir release-assets
uv run kb publish okf-validate data/okf-export
uv run kb publish okf-validate data/okf-export-core
uv run --project clients/python rock-kb okf verify release-assets/rock-agent-kb-okf-vX.Y.Z.zip
uv run --project clients/python rock-kb okf verify release-assets/rock-agent-kb-okf-core-vX.Y.Z.zip
uv run python scripts/validate_okf_reference_interop.py data/okf-export
uv run python scripts/validate_okf_reference_interop.py data/okf-export-core
```

See [Open Knowledge Format Distribution](okf-distribution.md) for scope and consumer commands.

## Public Contributions

Accepted public PRs should add reviewed bundles under:

```text
community-contributions/<org-id>/bundle.jsonl
```

Validate accepted single-repo intake bundles:

```bash
python scripts/validate_bundle.py
uv run kb contributions check --path contributions
```

Then rebuild and audit the public surface:

```bash
uv run kb build --stage concepts
uv run kb build --stage refresh-claims
uv run kb build --stage agent-pack
uv run kb audit public-export
uv run kb audit readiness
```

## Rules

- The public repo is the community-facing surface.
- Generated files are not hand-edited.
- Review queues and evaluation artifacts are build-internal by default.
- Contributions affect guides only after maintainer review, promotion, and rebuild.
- Org-specific observations must be generalized, version-scoped, plugin-scoped, or kept out of the public core.
