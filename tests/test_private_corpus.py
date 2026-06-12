import json

import rock_kb.private_corpus as private_corpus
from rock_kb.private_corpus import (
    ignored_private_artifact_report,
    initialize_private_corpus,
    sync_private_text_artifacts,
    verify_private_corpus_rebuild,
    write_large_media_restore_manifest,
)


def test_private_corpus_syncs_text_artifacts_and_manifests_large_media(monkeypatch, tmp_path):
    repo = tmp_path / "public-repo"
    review = repo / "data" / "review"
    media = repo / "data" / "media"
    review.mkdir(parents=True)
    media.mkdir(parents=True)
    (review / "candidate.jsonl").write_text('{"review":"private"}\n', encoding="utf-8")
    (media / "clip.mp3").write_bytes(b"audio")

    corpus = tmp_path / "private-corpus"
    monkeypatch.setattr(private_corpus, "REPO_ROOT", repo)
    monkeypatch.setattr(private_corpus, "SYNCABLE_PRIVATE_ROOTS", [review, media])
    monkeypatch.setattr(private_corpus, "is_git_ignored", lambda path: True)

    init = initialize_private_corpus(corpus)
    report = ignored_private_artifact_report()
    sync = sync_private_text_artifacts(corpus)
    restore = write_large_media_restore_manifest(corpus)
    restore_manifest = json.loads((corpus / "large-media-restore-manifest.json").read_text(encoding="utf-8"))

    assert init["status"] == "ok"
    assert report["text_json_artifact_count"] == 1
    assert report["large_media_artifact_count"] == 1
    assert sync["copied"] == 1
    assert (corpus / "data" / "review" / "candidate.jsonl").exists()
    assert restore["media_object_count"] == 1
    assert restore_manifest["media_objects"][0]["path"] == "data/media/clip.mp3"
    assert restore_manifest["media_objects"][0]["restore_status"] == "external_private_object_required"


def test_verify_private_corpus_rebuild_checks_portable_inputs(monkeypatch, tmp_path):
    repo = tmp_path / "public-repo"
    repo.mkdir()
    corpus = tmp_path / "private-corpus"
    monkeypatch.setattr(private_corpus, "REPO_ROOT", repo)
    monkeypatch.setattr(private_corpus, "audit_private_corpus_leaks", lambda path: {"status": "ok", "errors": []})

    initialize_private_corpus(corpus)
    for rel in [
        "data/raw-manifests/source.jsonl",
        "data/normalized/source.jsonl",
        "data/review/public-media-promotions/source.jsonl",
        "data/media/source.transcripts.jsonl",
    ]:
        path = corpus / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
    (corpus / "large-media-restore-manifest.json").write_text('{"media_objects":[]}\n', encoding="utf-8")

    result = verify_private_corpus_rebuild(corpus)

    assert result["status"] == "ok"
    assert result["artifact_summary"]["raw_manifest_files"] == 1
    assert result["artifact_summary"]["normalized_files"] == 1
    assert result["artifact_summary"]["review_files"] == 1
    assert result["artifact_summary"]["media_text_files"] == 1


def test_verify_private_corpus_rebuild_fails_without_required_inputs(monkeypatch, tmp_path):
    repo = tmp_path / "public-repo"
    repo.mkdir()
    corpus = tmp_path / "private-corpus"
    monkeypatch.setattr(private_corpus, "REPO_ROOT", repo)
    monkeypatch.setattr(private_corpus, "audit_private_corpus_leaks", lambda path: {"status": "ok", "errors": []})

    initialize_private_corpus(corpus)
    result = verify_private_corpus_rebuild(corpus)

    assert result["status"] == "fail"
    assert "private corpus has no raw_manifest_files" in result["errors"]
    assert "large-media-restore-manifest.json is missing; run kb corpus media-manifest" in result["errors"]
