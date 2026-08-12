from __future__ import annotations

import json
from pathlib import Path

import pytest

import rock_kb.source_native_orchestrator as orchestrator
from rock_kb.jsonl import read_jsonl, write_jsonl


def source_record(index: int, *, title: str | None = None) -> dict:
    source_record_id = f"rock_developer:article:{index}"
    return {
        "id": source_record_id,
        "source_id": "rock_developer",
        "source_url": f"https://community.rockrms.com/developer/article-{index}",
        "source_title": title or f"Article {index}",
        "summary": (
            "A bounded official developer article with enough detail for "
            "deterministic low-risk source-native review and exact coverage."
        ),
        "content_hash": f"{index:064x}",
        "documentation_path": f"developer/article-{index}",
        "documentation_branches": ["developer/resources"],
        "topics": ["development"],
    }


def priority_row(record: dict, rank: int) -> dict:
    return {
        "rank": rank,
        "source_record_id": record["id"],
        "source_id": record["source_id"],
        "source_title": record["source_title"],
        "source_url": record["source_url"],
        "source_content_hash": record["content_hash"],
        "documentation_path": record["documentation_path"],
        "documentation_branches": record["documentation_branches"],
        "authority_tiers": ["official"],
        "concept_ids": ["developer-resources"],
        "concept_routing": {
            "concept_ids": ["developer-resources"],
            "confidence": "high",
            "routes": [
                {
                    "concept_id": "developer-resources",
                    "method": "documentation_path",
                }
            ],
        },
        "legacy_concept_ids": ["developer-resources"],
        "legacy_claim_count": 0,
        "legacy_source_summary_count": 1,
        "verification_debt_count": 0,
        "existing_source_native_artifact_count": 0,
        "exact_evaluation_case_count": 0,
        "concept_evaluation_case_count": 1,
        "external_signal_count": 0,
        "freshness": {
            "status": "current",
            "cadence": "weekly",
            "last_checked_at": "2026-08-11T00:00:00+00:00",
            "age_hours": 1,
            "maximum_age_hours": 216,
        },
        "priority_score": 50,
        "priority": "low",
        "score_components": {},
        "recommended_action": "generate_source_native_migration",
        "migration_ready": True,
    }


def priority_report(records: list[dict]) -> dict:
    rows = [priority_row(record, rank) for rank, record in enumerate(records, 1)]
    report = {
        "schema": orchestrator.SOURCE_NATIVE_MIGRATION_PRIORITY_SCHEMA,
        "algorithm_version": orchestrator.SOURCE_NATIVE_MIGRATION_PRIORITY_ALGORITHM,
        "status": "ok",
        "as_of": "2026-08-11T01:00:00+00:00",
        "score_weights": {},
        "counts": {
            "actionable_source_count": len(rows),
            "active_legacy_source_count": len(rows),
            "migration_ready_count": len(rows),
            "reviewed_retained_source_count": 0,
            "unresolved_source_identity_count": 0,
            "reconciled_source_record_alias_count": 0,
            "unsupported_source_family_legacy_count": 0,
            "by_recommended_action": {"generate_source_native_migration": len(rows)},
        },
        "reviewed_retained_source_record_ids": [],
        "unresolved_source_records": [],
        "source_record_aliases": [],
        "bounded_external_signals": [],
        "rows": rows,
        "row_limit": len(rows),
    }
    hash_payload = {
        "algorithm_version": report["algorithm_version"],
        "as_of": report["as_of"],
        "score_weights": report["score_weights"],
        "rows": rows,
        "reviewed_retained": [],
        "unresolved_records": [],
        "source_record_aliases": [],
        "external_signals": [],
    }
    report["input_hash"] = orchestrator.sha256_text(
        orchestrator.priority_canonical_json(hash_payload)
    )
    return report


def rehash_priority_report(report: dict) -> None:
    report["input_hash"] = orchestrator.sha256_text(
        orchestrator.priority_canonical_json(
            {
                "algorithm_version": report["algorithm_version"],
                "as_of": report["as_of"],
                "score_weights": report["score_weights"],
                "rows": report["rows"],
                "reviewed_retained": report["reviewed_retained_source_record_ids"],
                "unresolved_records": [
                    row["source_record_id"]
                    for row in report["unresolved_source_records"]
                ],
                "source_record_aliases": report["source_record_aliases"],
                "external_signals": report["bounded_external_signals"],
            }
        )
    )


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def install_prepare_stubs(monkeypatch, repo_root: Path, records: list[dict]) -> None:
    monkeypatch.setattr(
        orchestrator,
        "_git_state",
        lambda _repo_root, require_clean: {
            "base_commit": "c" * 40,
            "branch": "test",
            "tracked_tree_clean": True,
        },
    )
    monkeypatch.setattr(
        orchestrator,
        "concept_source_records",
        lambda repo_root=None: records,
    )

    def build_candidates(**options):
        destination = options["destination"]
        destination.mkdir(parents=True, exist_ok=True)
        records_by_id = {record["id"]: record for record in options["records"]}
        rows = []
        snapshots = []
        units = []
        for index, source_record_id in enumerate(options["source_record_ids"], 1):
            source_unit = {
                "source_unit_id": f"source-unit:{index}",
                "unit_kind": "paragraph",
                "text": records_by_id[source_record_id]["summary"],
            }
            snapshot = {
                "source_snapshot_id": f"source-snapshot:{index}",
                "source_record_id": source_record_id,
                "content_hash": f"{index + 100:064x}",
            }
            rows.append(
                {
                    "candidate_id": f"candidate:{index}",
                    "source_input_hash": f"{index + 200:064x}",
                    "source_snapshot": snapshot,
                    "source_units": [source_unit],
                    "concept_ids": options["source_record_concept_ids"][
                        source_record_id
                    ],
                }
            )
            snapshots.append(snapshot)
            units.append(source_unit)
        write_jsonl(destination / "distillation-input.jsonl", rows)
        write_jsonl(destination / "source-snapshots.jsonl", snapshots)
        write_jsonl(destination / "source-units.private.jsonl", units)
        write_jsonl(destination / "document-candidates.jsonl", rows)
        write_json(
            destination / "candidate-summary.json",
            {
                "destination": str(destination),
                "output": str(destination / "distillation-input.jsonl"),
            },
        )
        return {
            "status": "ok",
            "article_count": len(rows),
            "source_unit_count": len(units),
        }

    def build_migration_inputs(**options):
        rows = []
        for row in read_jsonl(options["source_native_input_path"]):
            rows.append(
                {
                    **row,
                    "migration_input_hash": "d" * 64,
                    "legacy_items": [
                        {"legacy_knowledge_unit_id": ("legacy:" + row["candidate_id"])}
                    ],
                }
            )
        write_jsonl(options["destination"], rows)
        return {
            "status": "ok",
            "article_count": len(rows),
            "legacy_item_count": len(rows),
        }

    def write_schema(destination):
        write_json(destination, {"type": "object"})
        return {"status": "ok", "sha256": orchestrator.sha256_file(destination)}

    def write_prompt(**options):
        options["destination"].write_text(
            f"Prompt for {options['source_record_id']}\n",
            encoding="utf-8",
        )
        return {"status": "ok"}

    monkeypatch.setattr(
        orchestrator, "build_source_native_document_candidates", build_candidates
    )
    monkeypatch.setattr(
        orchestrator,
        "build_source_native_legacy_migration_inputs",
        build_migration_inputs,
    )
    monkeypatch.setattr(
        orchestrator, "write_source_native_legacy_migration_schema", write_schema
    )
    monkeypatch.setattr(
        orchestrator, "write_source_native_legacy_migration_prompt", write_prompt
    )

    for relative, text in [
        ("docs/prompts/source-knowledge-distillation-v2.3.md", "distillation"),
        ("docs/prompts/source-native-legacy-migration-v1.md", "migration"),
        ("docs/specs/source-knowledge-distillation-v2.3.schema.json", "{}"),
    ]:
        path = repo_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def test_priority_report_must_cover_every_actionable_record():
    records = [source_record(1), source_record(2)]
    report = priority_report(records)
    report["rows"] = report["rows"][:1]

    with pytest.raises(ValueError, match="priority report is truncated"):
        orchestrator.select_migration_batch(
            report=report,
            records=records,
            count=1,
            max_risk="low",
        )


def test_priority_report_rejects_tampered_rows():
    record = source_record(1)
    report = priority_report([record])
    report["rows"][0]["freshness"]["status"] = "current-but-tampered"

    with pytest.raises(ValueError, match="input hash is invalid"):
        orchestrator.select_migration_batch(
            report=report,
            records=[record],
            count=1,
            max_risk="low",
        )


def test_complete_queue_rejects_source_drift_even_for_excluded_record():
    safe = source_record(1)
    stale = source_record(2)
    report = priority_report([safe, stale])
    report["rows"][1]["migration_ready"] = False
    report["rows"][1]["recommended_action"] = "refresh_source_first"
    report["rows"][1]["freshness"]["status"] = "overdue"
    rehash_priority_report(report)
    stale["content_hash"] = "f" * 64

    with pytest.raises(ValueError, match="priority source hash changed"):
        orchestrator.select_migration_batch(
            report=report,
            records=[safe, stale],
            count=1,
            max_risk="low",
        )


def test_complete_queue_rejects_disappeared_normalized_record():
    present = source_record(1)
    missing = source_record(2)
    report = priority_report([present, missing])

    with pytest.raises(ValueError, match="disappeared from normalized data"):
        orchestrator.select_migration_batch(
            report=report,
            records=[present],
            count=1,
            max_risk="low",
        )


def test_low_risk_selection_excludes_sensitive_and_stale_records():
    sensitive = source_record(1, title="SQL Security")
    stale = source_record(2)
    safe = source_record(3)
    report = priority_report([sensitive, stale, safe])
    report["rows"][1]["migration_ready"] = False
    report["rows"][1]["recommended_action"] = "refresh_source_first"
    report["rows"][1]["freshness"]["status"] = "overdue"
    rehash_priority_report(report)

    selected = orchestrator.select_migration_batch(
        report=report,
        records=[sensitive, stale, safe],
        count=1,
        max_risk="low",
    )

    assert selected["selected_source_record_ids"] == [safe["id"]]
    assert selected["excluded_counts"] == {
        "refresh_source_first": 1,
        "risk_high": 1,
    }


def test_low_risk_selection_scans_summary_and_requires_current_source():
    sensitive = source_record(1)
    sensitive["summary"] = (
        "Execute SQL writes and save authentication tokens in this otherwise "
        "innocently titled developer article."
    )
    due_soon = source_record(2)
    safe = source_record(3)
    report = priority_report([sensitive, due_soon, safe])
    report["rows"][1]["freshness"]["status"] = "due_soon"
    rehash_priority_report(report)

    selected = orchestrator.select_migration_batch(
        report=report,
        records=[sensitive, due_soon, safe],
        count=1,
        max_risk="low",
    )

    assert selected["selected_source_record_ids"] == [safe["id"]]
    assert selected["excluded_counts"]["risk_high"] == 2


def test_exact_selection_fails_closed_when_any_record_is_not_low_risk():
    safe = source_record(1)
    sensitive = source_record(2, title="Password Security")

    with pytest.raises(ValueError, match="exact source records failed"):
        orchestrator.select_migration_batch(
            report=priority_report([safe, sensitive]),
            records=[safe, sensitive],
            count=2,
            max_risk="low",
            exact_source_record_ids=[safe["id"], sensitive["id"]],
        )


def test_claim_bearing_record_requires_at_least_standard_risk():
    record = source_record(1)
    report = priority_report([record])
    report["rows"][0]["legacy_claim_count"] = 1
    report["rows"][0]["legacy_source_summary_count"] = 0
    rehash_priority_report(report)

    with pytest.raises(ValueError, match="only 0 satisfied the low risk policy"):
        orchestrator.select_migration_batch(
            report=report,
            records=[record],
            count=1,
            max_risk="low",
        )

    selected = orchestrator.select_migration_batch(
        report=report,
        records=[record],
        count=1,
        max_risk="standard",
    )
    assert selected["selected_source_record_ids"] == [record["id"]]


def test_editorial_community_blog_requires_at_least_standard_risk():
    record = source_record(1)
    record.update(
        {
            "id": "rock_community_blog:article:1",
            "source_id": "rock_community_blog",
            "source_url": "https://community.rockrms.com/connect/article-1",
        }
    )
    report = priority_report([record])

    with pytest.raises(ValueError, match="only 0 satisfied the low risk policy"):
        orchestrator.select_migration_batch(
            report=report,
            records=[record],
            count=1,
            max_risk="low",
        )

    selected = orchestrator.select_migration_batch(
        report=report,
        records=[record],
        count=1,
        max_risk="standard",
    )
    assert selected["selected"][0]["risk"]["reason_codes"] == [
        "editorial_community_blog"
    ]


def test_api_backed_prose_without_exact_article_identity_is_high_risk():
    record = source_record(1)
    record["id"] = "rock_developer:604a7cf9025a8bcc"
    row = priority_row(record, 1)

    result = orchestrator.classify_migration_risk(row, record)

    assert result["level"] == "high"
    assert "exact_article_identity_missing" in result["reason_codes"]


@pytest.mark.parametrize("confidence", ["medium", "low"])
def test_non_high_confidence_concept_routing_requires_standard_risk(
    confidence: str,
):
    record = source_record(1)
    report = priority_report([record])
    report["rows"][0]["concept_routing"] = {
        "concept_ids": ["developer-resources"],
        "confidence": confidence,
        "routes": [
            {
                "concept_id": "developer-resources",
                "method": "supported_legacy",
            }
        ],
    }
    rehash_priority_report(report)

    with pytest.raises(ValueError, match="only 0 satisfied the low risk policy"):
        orchestrator.select_migration_batch(
            report=report,
            records=[record],
            count=1,
            max_risk="low",
        )

    selected = orchestrator.select_migration_batch(
        report=report,
        records=[record],
        count=1,
        max_risk="standard",
    )
    assert "concept_routing_not_high_confidence" in (
        selected["selected"][0]["risk"]["reason_codes"]
    )
    assert selected["risk_policy_version"] == "7"


def test_hydrated_preflight_uses_reserve_after_review_limit_skip():
    records = [source_record(1), source_record(2), source_record(3)]
    selection = orchestrator.select_migration_batch(
        report=priority_report(records),
        records=records,
        count=3,
        max_risk="low",
    )
    candidate_rows = [
        {
            "source_snapshot": {"source_record_id": record["id"]},
            "source_units": [
                {
                    "unit_kind": "paragraph",
                    "text": record["summary"],
                }
            ],
        }
        for record in records[1:]
    ]
    result = orchestrator._hydrated_preflight_selection(
        selection=selection,
        candidate_rows=candidate_rows,
        build_result={
            "document_candidate_build": {
                "skipped": [
                    {
                        "source_record_id": records[0]["id"],
                        "reason": (
                            "rockumentation_full_text_exceeds_review_limit"
                        ),
                        "source_input_hash": "a" * 64,
                        "source_context_char_count": 80_000,
                    }
                ]
            }
        },
        records_by_id={record["id"]: record for record in records},
        count=2,
        max_risk="low",
        max_source_units_per_record=200,
    )

    assert [row["source_record_id"] for row in result["accepted"]] == [
        records[1]["id"],
        records[2]["id"],
    ]
    assert result["rejected"] == [
        {
            "source_record_id": records[0]["id"],
            "reason_code": "rockumentation_full_text_exceeds_review_limit",
            "candidate_id": None,
            "source_input_hash": "a" * 64,
            "source_context_char_count": 80_000,
            "source_unit_count": None,
            "risk": {
                "level": "standard",
                "policy_version": "7",
                "reason_codes": [
                    "rockumentation_full_text_exceeds_review_limit"
                ],
                "reasons": [
                    "hydrated source could not enter the bounded review packet"
                ],
            },
        }
    ]


def test_hydrated_preflight_screens_entire_reserve_after_batch_is_full():
    records = [source_record(1), source_record(2), source_record(3)]
    selection = orchestrator.select_migration_batch(
        report=priority_report(records),
        records=records,
        count=3,
        max_risk="low",
    )
    candidate_rows = [
        {
            "candidate_id": f"candidate:{index}",
            "source_input_hash": f"{index + 10:064x}",
            "source_snapshot": {"source_record_id": record["id"]},
            "source_units": [
                {
                    "unit_kind": "paragraph",
                    "text": (
                        record["summary"]
                        if index < 3
                        else record["summary"] + " Execute SQL using a private key."
                    ),
                }
            ],
        }
        for index, record in enumerate(records, 1)
    ]

    result = orchestrator._hydrated_preflight_selection(
        selection=selection,
        candidate_rows=candidate_rows,
        build_result={},
        records_by_id={record["id"]: record for record in records},
        count=2,
        max_risk="low",
        max_source_units_per_record=200,
    )

    assert [row["source_record_id"] for row in result["accepted"]] == [
        records[0]["id"],
        records[1]["id"],
    ]
    assert result["screened_safe_reserve"] == []
    assert result["rejected"][0]["source_record_id"] == records[2]["id"]
    assert result["rejected"][0]["candidate_id"] == "candidate:3"
    assert result["rejected"][0]["source_unit_count"] == 1


def test_prepare_backfills_hydration_skip_and_preserves_queue(
    monkeypatch,
    tmp_path: Path,
):
    records = [source_record(1), source_record(2), source_record(3)]
    install_prepare_stubs(monkeypatch, tmp_path, records)
    original_build = orchestrator.build_source_native_document_candidates
    call_count = 0

    def build_with_one_preflight_skip(**options):
        nonlocal call_count
        call_count += 1
        result = original_build(**options)
        if call_count != 1:
            return result
        skipped_id = records[0]["id"]
        rows = [
            row
            for row in read_jsonl(
                options["destination"] / "distillation-input.jsonl"
            )
            if row["source_snapshot"]["source_record_id"] != skipped_id
        ]
        write_jsonl(
            options["destination"] / "distillation-input.jsonl",
            rows,
        )
        return {
            **result,
            "article_count": len(rows),
            "document_candidate_build": {
                "skipped": [
                    {
                        "source_record_id": skipped_id,
                        "reason": (
                            "rockumentation_full_text_exceeds_review_limit"
                        ),
                    }
                ]
            },
        }

    monkeypatch.setattr(
        orchestrator,
        "build_source_native_document_candidates",
        build_with_one_preflight_skip,
    )
    report_path = tmp_path / "data" / "review" / "priority.json"
    write_json(report_path, priority_report(records))
    destination = tmp_path / "data" / "review" / "batch"

    result = orchestrator.prepare_source_native_migration_batch(
        destination=destination,
        count=2,
        max_risk="low",
        priority_report_path=report_path,
        repo_root=tmp_path,
    )

    selection = json.loads((destination / "selection.json").read_text())
    assert result["status"] == "ok"
    assert call_count == 2
    assert selection["selected_source_record_ids"] == [
        records[1]["id"],
        records[2]["id"],
    ]
    assert selection["hydrated_preflight"]["rejected"][0][
        "source_record_id"
    ] == records[0]["id"]
    assert [
        row["source_record_id"]
        for row in read_jsonl(
            destination / "queues" / "standard-risk.jsonl"
        )
    ] == [records[0]["id"]]
    assert selection["excluded_counts"][
        "rockumentation_full_text_exceeds_review_limit"
    ] == 1
    assert selection["excluded_examples"][
        "rockumentation_full_text_exceeds_review_limit"
    ] == [records[0]["id"]]


def test_missing_concept_routing_provenance_is_high_risk():
    record = source_record(1)
    report = priority_report([record])
    del report["rows"][0]["concept_routing"]
    rehash_priority_report(report)

    result = orchestrator.classify_migration_risk(report["rows"][0], record)

    assert result["level"] == "high"
    assert "concept_routing_provenance_missing" in result["reason_codes"]
    with pytest.raises(ValueError, match="only 0 satisfied the low risk policy"):
        orchestrator.select_migration_batch(
            report=report,
            records=[record],
            count=1,
            max_risk="low",
        )


def test_missing_per_concept_routing_method_is_high_risk():
    record = source_record(1)
    row = priority_row(record, 1)
    del row["concept_routing"]["routes"][0]["method"]

    result = orchestrator.classify_migration_risk(row, record)

    assert result["level"] == "high"
    assert "concept_routing_provenance_missing" in result["reason_codes"]


def test_prepare_is_immutable_and_idempotent(monkeypatch, tmp_path: Path):
    records = [source_record(1), source_record(2)]
    install_prepare_stubs(monkeypatch, tmp_path, records)
    report_path = tmp_path / "data" / "review" / "priority.json"
    write_json(report_path, priority_report(records))
    destination = tmp_path / "data" / "review" / "batch"

    first = orchestrator.prepare_source_native_migration_batch(
        destination=destination,
        count=2,
        max_risk="low",
        priority_report_path=report_path,
        repo_root=tmp_path,
    )
    state_before = (destination / "batch-state.json").read_bytes()
    second = orchestrator.prepare_source_native_migration_batch(
        destination=destination,
        count=2,
        max_risk="low",
        priority_report_path=report_path,
        repo_root=tmp_path,
    )

    assert first["status"] == "ok"
    assert second["status"] == "unchanged"
    assert first["batch_id"] == second["batch_id"]
    assert (destination / "batch-state.json").read_bytes() == state_before
    state = json.loads(state_before)
    manifest = json.loads((destination / "batch-manifest.json").read_text())
    assert state["promotion_permitted"] is False
    assert state["manual_review_required"] is True
    assert len(manifest["selected_records"]) == 2
    assert len(manifest["expected_shards"]) == 2
    assert all(not Path(path).is_absolute() for path in manifest["prepared_files"])
    assert (destination / "queues" / "refresh-first.jsonl").exists()
    assert (destination / "queues" / "high-risk.jsonl").exists()
    candidate_summary = json.loads(
        (destination / "candidates" / "candidate-summary.json").read_text()
    )
    assert candidate_summary == {
        "destination": "candidates",
        "output": "candidates/distillation-input.jsonl",
    }


def test_prepare_manifest_tampering_fails_closed(monkeypatch, tmp_path: Path):
    records = [source_record(1)]
    install_prepare_stubs(monkeypatch, tmp_path, records)
    report_path = tmp_path / "data" / "review" / "priority.json"
    write_json(report_path, priority_report(records))
    destination = tmp_path / "data" / "review" / "batch"
    orchestrator.prepare_source_native_migration_batch(
        destination=destination,
        count=1,
        priority_report_path=report_path,
        repo_root=tmp_path,
    )
    manifest_path = destination / "batch-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["selected_records"][0]["concept_ids"] = ["tampered"]
    write_json(manifest_path, manifest)

    with pytest.raises(ValueError, match="manifest identity is invalid"):
        orchestrator._validate_batch_runtime(
            destination,
            repo_root=tmp_path,
            require_clean=True,
        )


def test_runtime_rejects_normalized_source_drift(monkeypatch, tmp_path: Path):
    records = [source_record(1)]
    install_prepare_stubs(monkeypatch, tmp_path, records)
    report_path = tmp_path / "data" / "review" / "priority.json"
    write_json(report_path, priority_report(records))
    destination = tmp_path / "data" / "review" / "batch"
    orchestrator.prepare_source_native_migration_batch(
        destination=destination,
        count=1,
        priority_report_path=report_path,
        repo_root=tmp_path,
    )
    records[0]["content_hash"] = "e" * 64

    with pytest.raises(ValueError, match="normalized source changed"):
        orchestrator._validate_batch_runtime(
            destination,
            repo_root=tmp_path,
            require_clean=True,
        )


def test_exact_selection_keeps_complete_remaining_queues():
    selected = source_record(1)
    stale = source_record(2)
    high = source_record(3, title="Password Security")
    standard = source_record(4)
    report = priority_report([selected, stale, high, standard])
    report["rows"][1]["migration_ready"] = False
    report["rows"][1]["recommended_action"] = "refresh_source_first"
    report["rows"][1]["freshness"]["status"] = "overdue"
    report["rows"][3]["legacy_claim_count"] = 1
    report["rows"][3]["legacy_source_summary_count"] = 0
    rehash_priority_report(report)

    result = orchestrator.select_migration_batch(
        report=report,
        records=[selected, stale, high, standard],
        count=1,
        max_risk="low",
        exact_source_record_ids=[selected["id"]],
    )

    assert [row["source_record_id"] for row in result["queues"]["refresh_first"]] == [
        stale["id"]
    ]
    assert [row["source_record_id"] for row in result["queues"]["high_risk"]] == [
        high["id"]
    ]
    assert [
        row["source_record_id"] for row in result["queues"]["standard_risk"]
    ] == [standard["id"]]


def test_hydrated_candidate_risk_rejects_sensitive_source_text():
    record = source_record(1)
    candidate = {
        "source_units": [
            {
                "unit_kind": "paragraph",
                "text": record["summary"] + " Execute SQL using a private key.",
            }
        ]
    }

    result = orchestrator.classify_hydrated_candidate_risk(candidate, record)

    assert result["level"] == "high"
    assert "execute sql" in result["reasons"][0]


def test_hydrated_candidate_binding_allows_metadata_prefix_variation():
    original = source_record(1)
    record = {
        **original,
        "summary": "Published Developer Article One. " + original["summary"],
    }
    candidate = {
        "source_units": [
            {
                "unit_kind": "paragraph",
                "text": (
                    "Article One\n" + original["summary"]
                    + " Additional bounded details appear here."
                ),
            }
        ]
    }

    result = orchestrator.classify_hydrated_candidate_risk(candidate, record)

    assert result["level"] == "low"
    assert result["source_binding_overlap"] >= 0.6


def test_hydrated_candidate_binding_rejects_unrelated_page():
    record = source_record(1)
    candidate = {
        "source_units": [
            {
                "unit_kind": "paragraph",
                "text": (
                    "An unrelated page discusses gardens, weather, music, travel, "
                    "buildings, meals, seating, parking, and weekend activities."
                ),
            }
        ]
    }

    result = orchestrator.classify_hydrated_candidate_risk(candidate, record)

    assert result["level"] == "high"
    assert "insufficient normalized preview coverage" in result["reasons"][0]


@pytest.mark.parametrize(
    ("conflict_text", "reason_code"),
    [
        (
            (
                "Use RockPage.GetScopedEntityContexts for the collection. "
                "The example calls RockPage.GetScopedContextEntities instead."
            ),
            "hydrated_conflicting_context_api_identifiers",
        ),
        (
            (
                "Let the administrator decide how many minutes to keep it cached. "
                "The field description says Number of seconds to cache the content."
            ),
            "hydrated_conflicting_cache_duration_units",
        ),
    ],
)
def test_hydrated_candidate_escalates_exact_source_conflicts(
    conflict_text: str,
    reason_code: str,
):
    record = source_record(1)
    candidate = {
        "source_units": [
            {
                "unit_kind": "paragraph",
                "text": record["summary"] + " " + conflict_text,
            }
        ]
    }

    result = orchestrator.classify_hydrated_candidate_risk(candidate, record)

    assert result["level"] == "standard"
    assert reason_code in result["reason_codes"]


@pytest.mark.parametrize(
    ("signal", "expected_level", "reason_code"),
    [
        ("The member has a RockInternal attribute.", "high", "hydrated_sensitive_terms"),
        ("Call SaveChanges() after updating the entity.", "high", "hydrated_sensitive_terms"),
        ("The helper can save changes to the entity.", "high", "hydrated_sensitive_terms"),
        (
            "This is an internal API for infrastructure use.",
            "standard",
            "hydrated_internal_api",
        ),
        (
            "These members may change in the near term.",
            "standard",
            "hydrated_near_term_change_warning",
        ),
        (
            "This feature is currently supported. This feature is no longer supported.",
            "standard",
            "hydrated_contradictory_release_status",
        ),
    ],
)
def test_hydrated_candidate_escalates_internal_mutable_and_status_signals(
    signal: str,
    expected_level: str,
    reason_code: str,
):
    record = source_record(1)
    candidate = {
        "source_units": [
            {
                "unit_kind": "paragraph",
                "text": record["summary"] + " " + signal,
            }
        ]
    }

    result = orchestrator.classify_hydrated_candidate_risk(candidate, record)

    assert result["level"] == expected_level
    assert reason_code in result["reason_codes"]


def test_hydrated_candidate_escalates_contradictory_core_status():
    record = source_record(1)
    candidate = {
        "source_units": [
            {
                "unit_kind": "paragraph",
                "text": (
                    record["summary"]
                    + " Helix is now in core. Support could change if Helix "
                    "were ever added to the core product."
                ),
            }
        ]
    }

    result = orchestrator.classify_hydrated_candidate_risk(candidate, record)

    assert result["level"] == "standard"
    assert "hydrated_contradictory_core_status" in result["reason_codes"]


def test_hydrated_candidate_rejects_differing_legacy_episode_identity():
    record = source_record(1)
    candidate = {
        "source_units": [
            {
                "unit_kind": "paragraph",
                "text": record["summary"] + " Episode 220 covers current adoption.",
            }
        ],
        "legacy_items": [
            {
                "title": "Episode 219",
                "retrieval_text": "Ep 219 covers a previous outreach feature.",
            }
        ],
    }

    result = orchestrator.classify_hydrated_candidate_risk(candidate, record)

    assert result["level"] == "high"
    assert "hydrated_legacy_episode_mismatch" in result["reason_codes"]
    assert result["identity_checks"]["legacy_episode_numbers"] == [219]
    assert result["identity_checks"]["hydrated_episode_numbers"] == [220]


def test_hydrated_candidate_rejects_generic_landing_page_legacy_mismatch():
    record = source_record(1)
    record.update(
        {
            "source_id": "rock_community_blog",
            "source_url": "https://community.rockrms.com/connect",
        }
    )
    candidate = {
        "source_snapshot": {
            "source_id": "rock_community_blog",
            "canonical_url": "https://community.rockrms.com/connect",
            "source_path": "knowledge/community/connect.md",
            "title": "Blog",
        },
        "source_units": [
            {
                "unit_kind": "paragraph",
                "text": record["summary"] + " New homepage announcements appear here.",
            }
        ],
        "legacy_items": [
            {
                "title": "Volunteer Onboarding",
                "retrieval_text": (
                    "Coordinate volunteer onboarding forms, background checks, "
                    "training milestones, ministry placement, and leader follow-up."
                ),
            }
        ],
    }

    result = orchestrator.classify_hydrated_candidate_risk(candidate, record)

    assert result["level"] == "high"
    assert "hydrated_generic_landing_legacy_mismatch" in result["reason_codes"]
    assert result["identity_checks"]["generic_landing_snapshot"] is True


def test_prepare_rechecks_hydrated_risk_after_legacy_items_are_attached(
    monkeypatch,
    tmp_path: Path,
):
    record = source_record(1)
    record["summary"] += " Episode 220 covers current adoption."
    install_prepare_stubs(monkeypatch, tmp_path, [record])

    def build_migration_inputs(**options):
        rows = []
        for row in read_jsonl(options["source_native_input_path"]):
            rows.append(
                {
                    **row,
                    "migration_input_hash": "d" * 64,
                    "legacy_items": [
                        {
                            "legacy_knowledge_unit_id": "legacy:episode-219",
                            "title": "Episode 219",
                            "retrieval_text": "Ep 219 covers a previous outreach feature.",
                        }
                    ],
                }
            )
        write_jsonl(options["destination"], rows)
        return {
            "status": "ok",
            "article_count": len(rows),
            "legacy_item_count": len(rows),
        }

    monkeypatch.setattr(
        orchestrator,
        "build_source_native_legacy_migration_inputs",
        build_migration_inputs,
    )
    report_path = tmp_path / "data" / "review" / "priority.json"
    write_json(report_path, priority_report([record]))
    destination = tmp_path / "data" / "review" / "batch"

    with pytest.raises(ValueError, match="hydrated candidate exceeds the low risk"):
        orchestrator.prepare_source_native_migration_batch(
            destination=destination,
            count=1,
            max_risk="low",
            priority_report_path=report_path,
            repo_root=tmp_path,
        )

    assert not destination.exists()


def test_prepare_rejects_destination_outside_ignored_review(tmp_path: Path):
    with pytest.raises(ValueError, match="under the ignored data/review"):
        orchestrator.prepare_source_native_migration_batch(
            destination=tmp_path / "public-batch",
            count=1,
            repo_root=tmp_path,
            require_clean=False,
        )


def test_prepare_requires_fixed_as_of_when_generating_priority(tmp_path: Path):
    with pytest.raises(ValueError, match="requires a fixed as_of"):
        orchestrator.prepare_source_native_migration_batch(
            destination=tmp_path / "data" / "review" / "batch",
            count=1,
            repo_root=tmp_path,
            require_clean=False,
        )


def test_prepared_file_verification_rejects_state_path_escape(tmp_path: Path):
    batch_dir = tmp_path / "data" / "review" / "batch"
    batch_dir.mkdir(parents=True)
    outside = batch_dir.parent / "outside.json"
    outside.write_text("{}\n", encoding="utf-8")
    state = {
        "prepared_files": {
            "../outside.json": {"sha256": orchestrator.sha256_file(outside)}
        }
    }

    with pytest.raises(ValueError, match="path escape"):
        orchestrator._verify_prepared_files(batch_dir, state)


def test_runtime_cleanup_removes_only_known_atomic_residue(tmp_path: Path):
    batch_dir = tmp_path / "batch"
    batch_dir.mkdir()
    known = batch_dir / ".batch-state.json.tmp"
    unrelated = batch_dir / ".unrelated.tmp"
    known.write_text("partial", encoding="utf-8")
    unrelated.write_text("preserve", encoding="utf-8")

    orchestrator._cleanup_runtime_residue(batch_dir)

    assert not known.exists()
    assert unrelated.read_text() == "preserve"


def test_prepare_removes_partial_batch_after_upstream_failure(
    monkeypatch, tmp_path: Path
):
    records = [source_record(1)]
    install_prepare_stubs(monkeypatch, tmp_path, records)
    monkeypatch.setattr(
        orchestrator,
        "build_source_native_document_candidates",
        lambda **_options: (_ for _ in ()).throw(ValueError("source split required")),
    )
    report_path = tmp_path / "data" / "review" / "priority.json"
    write_json(report_path, priority_report(records))
    destination = tmp_path / "data" / "review" / "batch"

    with pytest.raises(ValueError, match="source split required"):
        orchestrator.prepare_source_native_migration_batch(
            destination=destination,
            count=1,
            priority_report_path=report_path,
            repo_root=tmp_path,
        )

    assert not destination.exists()


def test_assemble_rejects_changed_shards_after_success(monkeypatch, tmp_path: Path):
    batch_dir = tmp_path / "data" / "review" / "batch"
    batch_dir.mkdir(parents=True)
    first_shard = batch_dir / "model-output" / "first.json"
    second_shard = batch_dir / "model-output" / "second.json"
    write_json(first_shard, {"articles": [{"candidate_id": "candidate:1"}]})
    write_json(second_shard, {"articles": [{"candidate_id": "candidate:2"}]})
    state = {
        "schema": orchestrator.BATCH_STATE_SCHEMA,
        "batch_id": "batch:test",
        "overall_state": "awaiting_model_generation",
        "phases": {"assemble": {"status": "pending"}},
    }
    monkeypatch.setattr(
        orchestrator,
        "_validate_batch_runtime",
        lambda *_args, **_kwargs: state,
    )

    def merge_stub(**options):
        write_json(options["destination"], {"articles": []})
        return {"article_count": 0}

    monkeypatch.setattr(
        orchestrator,
        "merge_source_native_legacy_migration_outputs",
        merge_stub,
    )

    first = orchestrator.assemble_source_native_migration_batch(
        batch_dir=batch_dir,
        model_output_paths=[first_shard],
        model="gpt-5.6-sol",
        repo_root=tmp_path,
        require_clean=False,
    )

    assert first["status"] == "ok"
    with pytest.raises(ValueError, match="requested model shards differ"):
        orchestrator.assemble_source_native_migration_batch(
            batch_dir=batch_dir,
            model_output_paths=[second_shard],
            model="gpt-5.6-sol",
            repo_root=tmp_path,
            require_clean=False,
        )


def test_assemble_recovers_interrupted_state_update(monkeypatch, tmp_path: Path):
    batch_dir = tmp_path / "data" / "review" / "batch"
    batch_dir.mkdir(parents=True)
    shard = batch_dir / "model-output" / "first.json"
    write_json(shard, {"articles": []})
    write_json(batch_dir / "generated-output.json", {"articles": []})
    state = {
        "schema": orchestrator.BATCH_STATE_SCHEMA,
        "batch_id": "batch:test",
        "overall_state": "awaiting_model_generation",
        "phases": {"assemble": {"status": "pending"}},
    }
    monkeypatch.setattr(
        orchestrator,
        "_validate_batch_runtime",
        lambda *_args, **_kwargs: state,
    )

    def merge_stub(**options):
        write_json(options["destination"], {"articles": []})
        return {"article_count": 0}

    monkeypatch.setattr(
        orchestrator,
        "merge_source_native_legacy_migration_outputs",
        merge_stub,
    )

    result = orchestrator.assemble_source_native_migration_batch(
        batch_dir=batch_dir,
        model_output_paths=[shard],
        model="gpt-5.6-sol",
        repo_root=tmp_path,
        require_clean=False,
    )

    assert result["status"] == "recovered"
    assert state["overall_state"] == "awaiting_maintainer_review"
    assert state["generated_output"]["recovered_after_interrupted_state_update"]


def test_low_risk_assembly_rejects_unmatched_routing_terms(
    monkeypatch,
    tmp_path: Path,
):
    batch_dir = tmp_path / "data" / "review" / "batch"
    batch_dir.mkdir(parents=True)
    shard = batch_dir / "model-output" / "first.json"
    write_json(shard, {"articles": [{"candidate_id": "candidate:1"}]})
    state = {
        "schema": orchestrator.BATCH_STATE_SCHEMA,
        "batch_id": "batch:test",
        "overall_state": "awaiting_model_generation",
        "phases": {"assemble": {"status": "pending"}},
        "_manifest": {"policy": {"max_risk": "low"}},
    }
    monkeypatch.setattr(
        orchestrator,
        "_validate_batch_runtime",
        lambda *_args, **_kwargs: state,
    )

    def merge_stub(**options):
        write_json(
            options["destination"],
            {
                "articles": [
                    {
                        "candidate_id": "candidate:1",
                        "unmatched_routing_terms": ["uncertain-feature"],
                    }
                ]
            },
        )
        return {"article_count": 1}

    monkeypatch.setattr(
        orchestrator,
        "merge_source_native_legacy_migration_outputs",
        merge_stub,
    )

    with pytest.raises(ValueError, match="low-risk assembly contains unmatched"):
        orchestrator.assemble_source_native_migration_batch(
            batch_dir=batch_dir,
            model_output_paths=[shard],
            model="gpt-5.6-sol",
            repo_root=tmp_path,
            require_clean=False,
        )

    assert state["overall_state"] == "awaiting_model_generation"
    assert not (batch_dir / "generated-output.json").exists()
    assert not (batch_dir / ".generated-output.pending.json").exists()


def test_compare_migration_outputs_uses_stable_list_keys_and_categories():
    generated = {
        "articles": [
            {
                "candidate_id": "candidate:1",
                "artifacts": [
                    {
                        "artifact_key": "second",
                        "content": "Original second content",
                        "rock_versions": [],
                    },
                    {
                        "artifact_key": "first",
                        "content": "First content",
                        "rock_versions": [],
                    },
                ],
                "legacy_decisions": [],
            }
        ]
    }
    reviewed = {
        "articles": [
            {
                "candidate_id": "candidate:1",
                "artifacts": [
                    {
                        "artifact_key": "first",
                        "content": "First content",
                        "rock_versions": [],
                    },
                    {
                        "artifact_key": "second",
                        "content": "Narrowed second content",
                        "rock_versions": ["19"],
                    },
                ],
                "legacy_decisions": [],
            }
        ]
    }

    report = orchestrator.compare_migration_outputs(generated, reviewed)

    assert report["changed_article_count"] == 1
    assert report["correction_count"] == 2
    assert report["correction_category_counts"] == {
        "evidence_scope": 1,
        "version_scope": 1,
    }


def test_review_decisions_require_exact_judge_adjudication(tmp_path: Path):
    article = {"candidate_id": "candidate:1", "artifacts": []}
    output = {"articles": [article]}
    decision_path = tmp_path / "decisions.jsonl"
    judge_path = tmp_path / "judge.json"
    write_jsonl(
        decision_path,
        [
            {
                "schema": orchestrator.BATCH_REVIEW_SCHEMA,
                "candidate_id": "candidate:1",
                "source_record_id": "rock_developer:article:1",
                "generated_article_hash": orchestrator._article_hash(article),
                "reviewed_article_hash": orchestrator._article_hash(article),
                "decision": "approved",
                "reviewer": "maintainer",
                "reviewed_at": "2026-08-11T02:00:00+00:00",
                "notes": [],
                "adjudications": [],
            }
        ],
    )
    write_json(
        judge_path,
        {
            "articles": [
                {
                    "candidate_id": "candidate:1",
                    "recommendations": [
                        {"recommendation_id": "judge:recommendation:1"}
                    ],
                }
            ]
        },
    )

    with pytest.raises(ValueError, match="require exact adjudication"):
        orchestrator._validate_review_decisions(
            decisions_path=decision_path,
            generated=output,
            reviewed=output,
            expected_records={"candidate:1": "rock_developer:article:1"},
            judge_review_path=judge_path,
        )


def test_review_decisions_reject_extra_fields(tmp_path: Path):
    article = {"candidate_id": "candidate:1", "artifacts": []}
    output = {"articles": [article]}
    decision_path = tmp_path / "decisions.jsonl"
    write_jsonl(
        decision_path,
        [
            {
                "schema": orchestrator.BATCH_REVIEW_SCHEMA,
                "candidate_id": "candidate:1",
                "source_record_id": "rock_developer:article:1",
                "generated_article_hash": orchestrator._article_hash(article),
                "reviewed_article_hash": orchestrator._article_hash(article),
                "decision": "approved",
                "reviewer": "maintainer",
                "reviewed_at": "2026-08-11T02:00:00+00:00",
                "notes": [],
                "adjudications": [],
                "unexpected": "must fail",
            }
        ],
    )

    with pytest.raises(ValueError, match="unexpected"):
        orchestrator._validate_review_decisions(
            decisions_path=decision_path,
            generated=output,
            reviewed=output,
            expected_records={"candidate:1": "rock_developer:article:1"},
            judge_review_path=None,
        )


def test_promotion_rejects_reviewed_output_changed_after_validation(
    monkeypatch, tmp_path: Path
):
    batch_dir = tmp_path / "data" / "review" / "batch"
    batch_dir.mkdir(parents=True)
    reviewed_output = batch_dir / "validated-reviewed-output.json"
    generated_output = batch_dir / "generated-output.json"
    comparison_report = batch_dir / "comparison-report.json"
    decisions_path = tmp_path / "data" / "review" / "review-decisions.jsonl"
    article = {"candidate_id": "candidate:1", "artifacts": []}
    write_json(reviewed_output, {"articles": [article]})
    write_json(generated_output, {"articles": [article]})
    write_json(comparison_report, {"status": "ready_for_explicit_promotion"})
    write_jsonl(
        decisions_path,
        [
            {
                "schema": orchestrator.BATCH_REVIEW_SCHEMA,
                "candidate_id": "candidate:1",
                "source_record_id": "rock_developer:article:1",
                "generated_article_hash": orchestrator._article_hash(article),
                "reviewed_article_hash": orchestrator._article_hash(article),
                "decision": "approved",
                "reviewer": "maintainer",
                "reviewed_at": "2026-08-11T02:00:00+00:00",
                "notes": [],
                "adjudications": [],
            }
        ],
    )
    state = {
        "schema": orchestrator.BATCH_STATE_SCHEMA,
        "batch_id": "batch:test",
        "overall_state": "ready_for_explicit_promotion",
    }
    validation_payload = {
        "batch_id": "batch:test",
        "generation_model": "gpt-5.6-sol",
        "files": {
            "generated_output_sha256": orchestrator.sha256_file(generated_output),
            "validated_reviewed_output_sha256": orchestrator.sha256_file(
                reviewed_output
            ),
            "review_decisions_sha256": orchestrator.sha256_file(decisions_path),
            "comparison_report_sha256": orchestrator.sha256_file(comparison_report),
            "judge_review_sha256": None,
        },
        "reviewers": ["maintainer"],
        "reviewed_at": ["2026-08-11T02:00:00+00:00"],
    }
    validation_id = orchestrator._review_validation_manifest_id(validation_payload)
    state["review_validation_manifest_id"] = validation_id
    write_json(
        batch_dir / "review-validation-manifest.json",
        {
            "schema": orchestrator.BATCH_REVIEW_VALIDATION_MANIFEST_SCHEMA,
            "validation_id": validation_id,
            **validation_payload,
        },
    )
    monkeypatch.setattr(
        orchestrator,
        "_validate_batch_runtime",
        lambda *_args, **_kwargs: state,
    )
    write_json(reviewed_output, {"articles": [{**article, "changed": True}]})

    with pytest.raises(ValueError, match="validated reviewed output changed"):
        orchestrator.promote_validated_source_native_migration_batch(
            batch_dir=batch_dir,
            review_decisions_path=decisions_path,
            destination=tmp_path / "canonical" / "source-native" / "v1",
            base_dir=tmp_path / "canonical" / "source-native" / "v1",
            reviewer="maintainer",
            model="gpt-5.6-sol",
            reviewed_at="2026-08-11T02:00:00+00:00",
            repo_root=tmp_path,
            require_clean=False,
        )


def test_promotion_rejects_forged_ready_state_without_review_manifest(
    monkeypatch, tmp_path: Path
):
    batch_dir = tmp_path / "data" / "review" / "batch"
    batch_dir.mkdir(parents=True)
    decisions_path = tmp_path / "data" / "review" / "decisions.jsonl"
    write_jsonl(decisions_path, [])
    monkeypatch.setattr(
        orchestrator,
        "_validate_batch_runtime",
        lambda *_args, **_kwargs: {
            "schema": orchestrator.BATCH_STATE_SCHEMA,
            "batch_id": "batch:test",
            "overall_state": "ready_for_explicit_promotion",
            "review_validation_manifest_id": "forged",
        },
    )

    with pytest.raises(ValueError, match="review validation manifest is missing"):
        orchestrator.promote_validated_source_native_migration_batch(
            batch_dir=batch_dir,
            review_decisions_path=decisions_path,
            destination=tmp_path / "canonical" / "source-native" / "v1",
            base_dir=tmp_path / "canonical" / "source-native" / "v1",
            reviewer="maintainer",
            model="gpt-5.6-sol",
            reviewed_at="2026-08-11T02:00:00+00:00",
            repo_root=tmp_path,
            require_clean=False,
        )


def test_interrupted_promotion_recovers_previous_directory(tmp_path: Path):
    destination = tmp_path / "canonical" / "source-native" / "v1"
    destination.mkdir(parents=True)
    (destination / "old.txt").write_text("old", encoding="utf-8")
    staging = destination.parent / f".{destination.name}.promotion-staging-test"
    staging.mkdir()
    (staging / "new.txt").write_text("new", encoding="utf-8")
    backup = destination.parent / f".{destination.name}.promotion-backup-test"
    destination.replace(backup)
    journal_path = orchestrator._promotion_journal_path(destination)
    write_json(
        journal_path,
        {
            "schema": "rock-kb-source-native-promotion-journal-v1",
            "phase": "old_moved",
            "destination": str(destination.resolve()),
            "staging": str(staging.resolve()),
            "backup": str(backup.resolve()),
        },
    )

    orchestrator._recover_source_native_promotion(destination)

    assert (destination / "old.txt").read_text() == "old"
    assert not staging.exists()
    assert not backup.exists()
    assert not journal_path.exists()


def test_validate_then_promote_revalidates_sealed_review(
    monkeypatch, tmp_path: Path
):
    batch_dir = tmp_path / "data" / "review" / "batch"
    batch_dir.mkdir(parents=True)
    reviewed_input = tmp_path / "data" / "review" / "reviewed.json"
    decisions_path = tmp_path / "data" / "review" / "decisions.jsonl"
    article = {"candidate_id": "candidate:1", "artifacts": [], "legacy_decisions": []}
    output = {"articles": [article]}
    write_json(batch_dir / "generated-output.json", output)
    write_json(reviewed_input, output)
    write_jsonl(
        batch_dir / "migration-input.jsonl",
        [
            {
                "candidate_id": "candidate:1",
                "source_snapshot": {
                    "source_record_id": "rock_developer:article:1"
                },
                "source_units": [],
            }
        ],
    )
    write_jsonl(
        decisions_path,
        [
            {
                "schema": orchestrator.BATCH_REVIEW_SCHEMA,
                "candidate_id": "candidate:1",
                "source_record_id": "rock_developer:article:1",
                "generated_article_hash": orchestrator._article_hash(article),
                "reviewed_article_hash": orchestrator._article_hash(article),
                "decision": "approved",
                "reviewer": "maintainer",
                "reviewed_at": "2026-08-11T02:00:00+00:00",
                "notes": [],
                "adjudications": [],
            }
        ],
    )
    state = {
        "schema": orchestrator.BATCH_STATE_SCHEMA,
        "batch_id": "batch:test",
        "overall_state": "awaiting_maintainer_review",
        "generated_output": {
            "sha256": orchestrator.sha256_file(
                batch_dir / "generated-output.json"
            ),
            "model": "gpt-5.6-sol",
        },
        "phases": {
            "prepare": {"duration": {"evidence_status": "measured", "value": 1}},
            "assemble": {"duration": {"evidence_status": "measured", "value": 1}},
            "validate_review": {"status": "pending"},
        },
        "model_metrics": {"cost": {"evidence_status": "unavailable"}},
        "_manifest": {
            "git": {"base_commit": "c" * 40},
            "priority": {"input_hash": "p" * 64},
            "selection_hash": "s" * 64,
        },
    }
    monkeypatch.setattr(
        orchestrator,
        "_validate_batch_runtime",
        lambda *_args, **_kwargs: state,
    )

    def merge_stub(**options):
        value = json.loads(options["batch_paths"][0].read_text())
        write_json(options["destination"], value)
        return {"article_count": len(value["articles"])}

    promoted = {}

    def promote_stub(**options):
        promoted.update(options)
        return {"schema": "promotion", "status": "ok"}

    monkeypatch.setattr(
        orchestrator, "merge_source_native_legacy_migration_outputs", merge_stub
    )
    monkeypatch.setattr(
        orchestrator, "_promote_source_native_migration_transactionally", promote_stub
    )

    validated = orchestrator.validate_source_native_migration_batch_review(
        batch_dir=batch_dir,
        reviewed_output_path=reviewed_input,
        review_decisions_path=decisions_path,
        repo_root=tmp_path,
        require_clean=False,
    )
    result = orchestrator.promote_validated_source_native_migration_batch(
        batch_dir=batch_dir,
        review_decisions_path=decisions_path,
        destination=tmp_path / "canonical" / "source-native" / "v1",
        base_dir=tmp_path / "canonical" / "source-native" / "v1",
        reviewer="maintainer",
        model="gpt-5.6-sol",
        reviewed_at="2026-08-11T02:00:00+00:00",
        repo_root=tmp_path,
        require_clean=False,
    )

    assert validated["overall_state"] == "ready_for_explicit_promotion"
    assert result["status"] == "ok"
    assert promoted["model"] == "gpt-5.6-sol"
    assert (batch_dir / "review-validation-manifest.json").exists()
