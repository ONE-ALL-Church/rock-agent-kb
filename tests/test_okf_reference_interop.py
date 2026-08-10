from __future__ import annotations

import importlib.util
from types import SimpleNamespace


def load_interop_script():
    path = "scripts/validate_okf_reference_interop.py"
    spec = importlib.util.spec_from_file_location("validate_okf_reference_interop", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_reference_interop_requires_all_documents_edges_and_v02_provenance(
    tmp_path,
    monkeypatch,
):
    interop = load_interop_script()
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "index.md").write_text("# Index\n", encoding="utf-8")
    (bundle / "log.md").write_text("# Log\n", encoding="utf-8")
    (bundle / "one.md").write_text("---\ntype: Knowledge\n---\n", encoding="utf-8")
    (bundle / "two.md").write_text("---\ntype: Knowledge\n---\n", encoding="utf-8")
    upstream = tmp_path / "upstream"
    (upstream / "okf" / "src").mkdir(parents=True)

    complete = [
        SimpleNamespace(
            id=name,
            generated={"by": "process:rock-kb-okf-export", "at": "2026-07-27T23:00:00Z"},
            sources=[{"resource": "https://example.test/source"}],
        )
        for name in ("one", "two")
    ]
    generator = SimpleNamespace(
        _walk_concepts=lambda root: complete,
        _build_graph=lambda concepts: {"nodes": [{}, {}], "edges": [{}]},
    )
    monkeypatch.setattr(interop.importlib, "import_module", lambda name: generator)

    report = interop.validate_reference_interop(bundle, upstream)

    assert report["status"] == "ok"
    assert report["expected_documents"] == 2
    assert report["parsed_documents"] == 2
    assert report["generated_documents"] == 2
    assert report["sourced_documents"] == 2

    complete[1].sources = []
    assert interop.validate_reference_interop(bundle, upstream)["status"] == "failed"
