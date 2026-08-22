from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace


def load_compatibility_script():
    path = "scripts/validate_okf_openknowledge.py"
    spec = importlib.util.spec_from_file_location("validate_okf_openknowledge", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_openknowledge_compatibility_runner_is_pinned_and_cleans_config(monkeypatch, tmp_path):
    compatibility = load_compatibility_script()
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "index.md").write_text("# Index\n", encoding="utf-8")

    def fake_run(command, *, cwd, env, check, capture_output, text):
        assert command[:3] == ["npx", "--yes", "@inkeep/open-knowledge@0.61.3"]
        assert cwd == bundle.resolve()
        assert env["NODE_NO_WARNINGS"] == "1"
        assert (cwd / ".ok" / "config.yml").read_text(encoding="utf-8") == compatibility.CONFIG_TEXT
        return SimpleNamespace(
            returncode=1,
            stderr="",
            stdout=json.dumps(
                {
                    "fileCount": 1,
                    "files": [
                        {
                            "file": "index.md",
                            "diagnostics": [
                                {"severity": "warning", "code": "index-shape"},
                            ],
                        }
                    ],
                }
            ),
        )

    monkeypatch.setattr(compatibility.subprocess, "run", fake_run)

    report = compatibility.lint_bundle(bundle)

    assert report == {
        "path": str(bundle.resolve()),
        "file_count": 1,
        "error_count": 0,
        "warning_count": 1,
        "diagnostics_by_code": {"index-shape": 1},
        "sample_diagnostics": [
            {
                "file": "index.md",
                "severity": "warning",
                "code": "index-shape",
                "message": "",
            }
        ],
        "linter_exit_code": 1,
    }
    assert not (bundle / ".ok").exists()


def test_openknowledge_monitor_is_nonblocking_and_uses_node_24():
    workflow = Path(".github/workflows/okf-upstream.yml").read_text(encoding="utf-8")

    assert "openknowledge-compatibility:" in workflow
    assert "continue-on-error: true" in workflow
    assert 'node-version: "24"' in workflow
    assert "scripts/validate_okf_openknowledge.py" in workflow
