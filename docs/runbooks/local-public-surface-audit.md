# Local Public Surface Audit

Run these checks before committing public-surface changes:

```bash
python3 scripts/audit_tracked_tree.py
python3 scripts/validate_bundle.py
uv run kb audit source-url-duplicates
uv run kb audit public-export
uv run kb audit readiness
uv run kb audit all
```

If `gitleaks` is installed, also run:

```bash
gitleaks detect --no-git --source .
```

Recommended `.git/hooks/pre-commit` body:

```bash
#!/usr/bin/env bash
set -euo pipefail

python3 scripts/audit_tracked_tree.py
python3 scripts/validate_bundle.py
uv run kb audit source-url-duplicates
uv run kb audit public-export

if command -v gitleaks >/dev/null 2>&1; then
  gitleaks detect --no-git --source .
fi
```

The tracked-tree audit blocks committed scratch exports, candid working logs, split-repo templates, local user paths, private live-evidence pointers, connected database markers, demo credentials, and common secret/token formats in the community-facing public surface. The gitleaks pass uses the checked-in `.gitleaks.toml` config and is the generic secret-pattern scan required before first public push.
