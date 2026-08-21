#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


OPENKNOWLEDGE_PACKAGE = "@inkeep/open-knowledge@0.61.0"
CONFIG_TEXT = "contentRules:\n  okf:\n    enabled: true\n"


def lint_bundle(bundle: Path) -> dict[str, Any]:
    bundle = bundle.resolve()
    if not bundle.is_dir():
        raise ValueError(f"OpenKnowledge compatibility check requires a bundle directory: {bundle}")
    config_dir = bundle / ".ok"
    if config_dir.exists():
        raise ValueError(f"Refusing to replace existing OpenKnowledge configuration: {config_dir}")
    config_dir.mkdir()
    (config_dir / "config.yml").write_text(CONFIG_TEXT, encoding="utf-8")
    env = dict(os.environ)
    env["NODE_NO_WARNINGS"] = "1"
    try:
        completed = subprocess.run(
            ["npx", "--yes", OPENKNOWLEDGE_PACKAGE, "lint", "--json", "."],
            cwd=bundle,
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )
    finally:
        shutil.rmtree(config_dir)
    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        detail = (completed.stderr or completed.stdout).strip()[:1000]
        if completed.returncode != 0:
            raise RuntimeError(f"OpenKnowledge lint failed for {bundle}: {detail}") from exc
        raise RuntimeError(f"OpenKnowledge lint returned invalid JSON for {bundle}") from exc
    if not isinstance(report, dict) or not isinstance(report.get("files"), list):
        raise RuntimeError(f"OpenKnowledge lint returned an unexpected report for {bundle}")

    diagnostics = [
        {"file": str(file_row.get("file") or ""), **diagnostic}
        for file_row in report.get("files") or []
        for diagnostic in file_row.get("diagnostics") or []
        if isinstance(diagnostic, dict)
    ]
    by_code = Counter(str(row.get("code") or "unknown") for row in diagnostics)
    return {
        "path": str(bundle),
        "file_count": int(report.get("fileCount") or 0),
        "error_count": sum(1 for row in diagnostics if row.get("severity") == "error"),
        "warning_count": sum(1 for row in diagnostics if row.get("severity") == "warning"),
        "diagnostics_by_code": dict(sorted(by_code.items())),
        "sample_diagnostics": [
            {
                key: str(row.get(key) or "")
                for key in ("file", "severity", "code", "message")
            }
            for row in diagnostics[:10]
        ],
        "linter_exit_code": completed.returncode,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a pinned, advisory OpenKnowledge OKF compatibility check."
    )
    parser.add_argument("bundles", nargs="+", type=Path)
    args = parser.parse_args()

    rows = [lint_bundle(bundle) for bundle in args.bundles]
    findings = sum(row["error_count"] + row["warning_count"] for row in rows)
    report = {
        "schema": "rock-kb-openknowledge-compatibility-v1",
        "status": "ok" if findings == 0 else "advisory_findings",
        "package": OPENKNOWLEDGE_PACKAGE,
        "bundles": rows,
        "finding_count": findings,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if findings == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
