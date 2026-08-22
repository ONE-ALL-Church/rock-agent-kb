from __future__ import annotations

import importlib.util
import json


def load_monitor_script():
    path = "scripts/check_okf_upstream.py"
    spec = importlib.util.spec_from_file_location("check_okf_upstream", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, sha: str):
        self.sha = sha

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self) -> bytes:
        return json.dumps([{"sha": self.sha}]).encode()


def test_okf_upstream_monitor_accepts_reviewed_v02_commit(monkeypatch, capsys):
    check_okf_upstream = load_monitor_script()
    monkeypatch.setattr(
        check_okf_upstream.request,
        "urlopen",
        lambda request, timeout: FakeResponse(check_okf_upstream.DEFAULT_EXPECTED_COMMIT),
    )
    monkeypatch.setattr("sys.argv", ["check_okf_upstream.py"])

    assert check_okf_upstream.main() == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "current"
    assert report["expected_commit"] == "62432a095456147ee71e70ac6e4dc0d2dea3ac30"


def test_okf_upstream_monitor_still_requires_review_for_new_drift(monkeypatch, capsys):
    check_okf_upstream = load_monitor_script()
    monkeypatch.setattr(
        check_okf_upstream.request,
        "urlopen",
        lambda request, timeout: FakeResponse("a" * 40),
    )
    monkeypatch.setattr("sys.argv", ["check_okf_upstream.py"])

    assert check_okf_upstream.main() == 1
    assert json.loads(capsys.readouterr().out)["status"] == "review_required"
