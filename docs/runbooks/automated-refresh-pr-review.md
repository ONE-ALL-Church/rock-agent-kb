# Automated Refresh Pull Request Review

Automated source and Rock issue refreshes use the repository `GITHUB_TOKEN` to
create pull requests. GitHub intentionally holds `pull_request` workflows
created by that token in an approval-required state. A separately dispatched
workflow can validate the same commit, but it is not the pull request's normal
required-check run and must not be treated as a substitute.

Refresh workflows therefore create draft pull requests. This preserves the
human review boundary without adding a PAT, GitHub App credential, or branch
protection bypass. A maintainer marks the reviewed draft ready; that human event
starts the required checks on the pull request itself.

## Review Sequence

1. Confirm the repository, pull request number, target branch, head SHA, bot
   author, `automated-refresh` label, and expected automation branch.
2. Review the complete diff. Rock issue refreshes may change only:
   `agent/rock-issue-summary.json`, `agent/rock-issues.jsonl`,
   `agent/rock-kb-manifest.json`, and `knowledge/issues/index.md`.
3. Confirm there are no unresolved review threads and run the relevant source
   validator, public-boundary audits, and tracked-file secret scan.
4. Mark the draft ready for review:

   ```bash
   gh pr ready <number> --repo ONE-ALL-Church/rock-agent-kb
   ```

5. Wait for the PR-associated `public-surface` and
   `validate-contributions` checks. Confirm both successful on the exact head
   SHA. Do not rely on a `workflow_dispatch` run as the required PR check.
6. Approve only after the final diff and checks are reviewed, then use an
   allowed repository merge method. Never bypass branch protection.

## Merge Versus Deploy

Merging changes under `agent/**`, `canonical/**`, `knowledge/**`, `sources/**`,
or the other paths listed in `.github/workflows/deploy-service.yml` starts the
production deployment workflow. Treat merge authorization and deployment
authorization as separate decisions.

When deployment is authorized, use the normal squash merge and verify the
deployment plus hosted source/projection parity. When a task explicitly
authorizes merge but forbids deployment, all required PR checks must still pass
before using a squash merge message containing `[skip ci]`. GitHub applies that
instruction only to workflows triggered by the resulting push commit. Record
that the hosted projection remains behind until a separately authorized manual
deployment runs.

Do not disable workflows, cancel a running deployment as a race workaround,
change required checks, weaken review rules, or add a broader credential to
avoid this gate.
