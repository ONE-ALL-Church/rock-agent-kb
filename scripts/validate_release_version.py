from __future__ import annotations

import argparse
from pathlib import Path

from rock_kb.release import validate_release


REPO_ROOT = Path(__file__).resolve().parents[1]
CLIENT_PROJECT = REPO_ROOT / "clients" / "python" / "pyproject.toml"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Rock KB release tag against package and changelog versions.")
    parser.add_argument("--tag", required=True)
    args = parser.parse_args()
    errors = validate_release(args.tag, CLIENT_PROJECT, CHANGELOG)
    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"Release tag {args.tag} matches the client package and changelog.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
