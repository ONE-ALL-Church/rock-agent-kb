# Release Cadence

Rock KB uses unified `rock-kb-vMAJOR.MINOR.PATCH` releases for the hosted public
service contract and the `rock-kb` Python client.

## Cadence

- Patch: compatible client fixes, documentation corrections, source refreshes
  that materially change public answers, and low-risk retrieval corrections.
- Minor: new client commands, service response fields, concepts, recipe
  capabilities, model-map surfaces, or backward-compatible retrieval behavior.
- Major: removal or incompatible changes to CLI commands, MCP tools, result
  identity, contribution schemas, or hosted response contracts.
- Routine automated refreshes with no material public answer change do not
  require a release.
- Skill-instruction-only changes may bump
  `skills/rock-kb-agent/manifest.json` and deploy the hosted artifact without a
  new Python client release, provided the existing updater contract still
  supports them. Bump `minimum_client_version` and publish a client release
  when the skill depends on new CLI behavior.

Prepare releases after meaningful changes are merged and the production Worker
is healthy. Avoid batching unrelated high-risk changes solely to meet a date;
at least one reviewed release per month keeps the public client and service
contract explicit when active development continues.

## Release Procedure

1. Update `clients/python/pyproject.toml`.
2. Move notable entries from `Unreleased` into a dated version section in
   `CHANGELOG.md`.
3. Run:

```bash
uv run python scripts/validate_release_version.py --tag rock-kb-vX.Y.Z
uv run kb quality-gate
python3 scripts/audit_tracked_tree.py
python3 scripts/validate_bundle.py
uv run kb audit public-export
```

4. Merge the release commit and verify the production Worker deployment.
5. Tag the verified `main` commit and push the tag:

```bash
git tag -a rock-kb-vX.Y.Z -m "rock-kb vX.Y.Z"
git push origin rock-kb-vX.Y.Z
```

The `Release Client` workflow revalidates the tag, package version, changelog,
public surface, and lexical retrieval quality; builds and smoke-tests the wheel
and source distribution; publishes to PyPI; and creates the GitHub release.
Never retag or overwrite an existing release.

## Release Notes Scope

Call out changes in these categories when present:

- Public sources and refresh behavior.
- Concepts and guide routing.
- Community recipes and compatibility.
- Stable/latest model-map versions and diffs.
- Search ranking, exact identity, telemetry, and evaluation.
- CLI, MCP, contribution, or response contract changes.
- Explicit decisions not to promote experimental infrastructure.
