# GitHub Public Repo Hardening

Milestone 0.5 is not complete until these protections are active on the fresh public repository. The current private build repo can carry the files and CI, but it should not be flipped public in place.

## Local Gate

Run these before creating the public repo or pushing the curated initial tree:

```bash
python3 scripts/audit_tracked_tree.py
python3 scripts/validate_bundle.py
uv run kb audit all
uv run --extra dev pytest
```

If `gitleaks` is installed, also run:

```bash
gitleaks detect --no-git --source .
```

The tracked-tree audit is the repo-specific leak gate. The gitleaks pass is the generic secret-pattern gate and uses the checked-in `.gitleaks.toml` config.

## Create Public Repo

Create a new public repository, expected name:

```text
ONE-ALL-Church/rock-agent-kb
```

Push a single curated initial commit to that repo. Do not make this private repo public in place, because its history contains working states that were never intended to be the public trust surface.

After the public repo is live, archive this private build repo read-only and update local checkouts, agent workflows, and CI references to point at the public repo.

## Required GitHub Settings

Enable these repository settings before intake or deploy automation is allowed:

- Secret scanning: enabled.
- Push protection: enabled.
- Branch protection or repository ruleset for `main`: require pull requests, require status checks, require CODEOWNERS review, block force pushes, and restrict direct pushes to maintainers.
- Required checks: `Public Surface / public-surface` and `Validate Contributions / validate-contributions`.
- GitHub Environment for deploy secrets: scope to `main`, require maintainer approval before secret-backed deploys, and keep intake PR workflows on plain `pull_request` without secrets.

Do not use `pull_request_target` to check out or execute untrusted contributor code.

## Intake Boundary

Before auto-merge exists, all PRs require maintainer review.

When auto-merge is later introduced, its server-side path boundary must be:

- Allowed for registered org intake only: `community-contributions/<org-id>/**` and `source-suggestions/<org-id>/**`.
- Never auto-merge: `.github/**`, `scripts/**`, `src/**`, `tests/**`, `docs/**`, `agent/**`, `claims/**`, `concepts/**`, `contributions/**`, `knowledge/**`, `sources/**`, `orgs/**`, `public-export-manifest.json`, dependency files, and repo root policy files.

Actions checks are useful evidence, but they are not the security boundary. Path restrictions must be enforced by GitHub branch protection, repository rulesets, or an equivalent GitHub App with no deploy secrets.

## Proof Tests

Record these before calling Milestone 0.5 complete:

```bash
gh repo view ONE-ALL-Church/rock-agent-kb --json nameWithOwner,visibility,isPrivate,defaultBranchRef,url
gh api repos/ONE-ALL-Church/rock-agent-kb/branches/main/protection
gh api repos/ONE-ALL-Church/rock-agent-kb/rulesets
```

Also verify:

- A PR touching `.github/workflows/*` cannot auto-merge.
- A push containing a planted test secret is blocked server-side.
- A fresh clone can run `uv run kb status`, `uv run kb build`, and `uv run kb audit all`.
- CI is green on the initial public commit.
