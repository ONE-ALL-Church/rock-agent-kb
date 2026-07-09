from __future__ import annotations

from pathlib import Path

from rock_kb.okf_export import audit_okf_export, build_okf_export, read_frontmatter


def test_okf_export_is_typed_linked_and_conformant(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ROCK_KB_GENERATED_AT", "2026-07-09T12:00:00+00:00")
    destination = tmp_path / "okf"

    report = build_okf_export(destination)

    assert report["status"] == "ok"
    assert report["counts"]["concepts"] > 0
    assert report["counts"]["claims"] > 0
    assert report["counts"]["references"] > 0
    assert audit_okf_export(destination) == []
    assert not (destination / "index.md").read_text(encoding="utf-8").startswith("---")
    assert not (destination / "log.md").read_text(encoding="utf-8").startswith("---")

    concept = destination / "concepts" / "check-in.md"
    concept_text = concept.read_text(encoding="utf-8")
    assert read_frontmatter(concept_text)["type"] == "Concept"
    assert "../claims/" in concept_text
    assert "../references/" in concept_text

    claim = next((destination / "claims").glob("*.md"))
    claim_text = claim.read_text(encoding="utf-8")
    assert read_frontmatter(claim_text)["type"] == "Claim"
    assert "../concepts/" in claim_text
    assert "../references/" in claim_text


def test_okf_audit_rejects_untyped_and_broken_graph_nodes(tmp_path: Path):
    (tmp_path / "index.md").write_text("# Index\n", encoding="utf-8")
    (tmp_path / "log.md").write_text("# Log\n", encoding="utf-8")
    (tmp_path / "bad.md").write_text("[Missing](missing.md)\n", encoding="utf-8")

    errors = audit_okf_export(tmp_path)

    assert "bad.md missing non-empty type frontmatter" in errors
    assert "bad.md has unresolved link: missing.md" in errors
