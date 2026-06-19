import json
import subprocess
from pathlib import Path

import pytest

from rock_kb.audit import audit_duplicate_source_urls, audit_license_records, validate_markdown_frontmatter
from rock_kb.contributions import (
    CONTRIBUTION_SCHEMA,
    contribution_check_report,
    contribution_example_paths,
    contribution_paths,
    create_contribution_template,
    distill_private_scan,
    private_review_report,
    promote_private_contributions,
    report_private_staleness,
    validate_contribution_file,
    validate_contribution_paths,
    validate_contribution_row,
)
from rock_kb.extract import grep_sensitive_values
from rock_kb.jsonl import read_jsonl, write_jsonl
from rock_kb.paths import REPO_ROOT
from rock_kb.private_dependencies import report_private_impact
from rock_kb.private_scan import (
    candidate_concepts,
    classify_private_document,
    private_risk_flags,
    scan_private_repo,
    should_skip_private_path,
)
from rock_kb.publish import (
    audit_agent_entrypoint_coverage,
    audit_forbidden_public_text,
    audit_json_public_fields,
    audit_json_public_traceability,
    audit_source_policy,
    iter_public_file_entries,
    iter_public_files,
    is_public_source,
    is_private_path,
    public_export_text_for_path,
    sanitize_public_claim,
    strip_private_provenance,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_tracked_tree_excludes_retired_public_export_paths():
    tracked = subprocess.check_output(["git", "ls-files"], cwd=REPO_ROOT, text=True).splitlines()
    forbidden_prefixes = ("data/public-export/", "docs/log/", "templates/public-repo/")
    offenders = [path for path in tracked if path.startswith(forbidden_prefixes)]
    assert offenders == []


def test_license_audit_blocks_full_text_without_permission(tmp_path):
    path = tmp_path / "records.jsonl"
    write_jsonl(
        path,
        [
            {
                "id": "bad",
                "license_status": "public_rights_reserved",
                "allowed_extraction_mode": "cite_and_summarize",
                "full_text": "not allowed",
                "citations": [{"url": "https://example.com"}],
            }
        ],
    )
    errors = audit_license_records([path])
    assert any("full_text" in error for error in errors)


def test_duplicate_source_url_audit_flags_unapproved_source_pairs(tmp_path):
    path = tmp_path / "records.jsonl"
    write_jsonl(
        path,
        [
            {"id": "a", "source_id": "rock_community_site", "source_url": "https://community.rockrms.com/developer/helix"},
            {"id": "b", "source_id": "rock_developer", "source_url": "https://community.rockrms.com/developer/helix/"},
            {"id": "c", "source_id": "public_rock_repos", "source_url": "https://github.com/SparkDevNetwork/Rock"},
            {"id": "d", "source_id": "sparkdevnetwork_rock", "source_url": "https://github.com/SparkDevNetwork/Rock"},
        ],
    )

    errors = audit_duplicate_source_urls([path])

    assert errors == ["duplicate source_url pair rock_community_site vs rock_developer: 1"]


def test_frontmatter_validation(tmp_path):
    page = tmp_path / "page.md"
    page.write_text(
        "---\n"
        "id: test\n"
        "source_ids: [rock_documentation]\n"
        "license_status: public_rights_reserved\n"
        "last_verified: '2026-05-27'\n"
        "topics: [admin]\n"
        "rock_versions: []\n"
        "agent_notes: test\n"
        "---\n"
        "# Test\n",
        encoding="utf-8",
    )
    assert validate_markdown_frontmatter(page) == []


def test_public_export_requires_agent_entrypoints():
    assert audit_agent_entrypoint_coverage() == []


def test_private_scan_respects_allowlist_and_flags_secrets():
    records = scan_private_repo(FIXTURES / "private_repo", FIXTURES / "private_allowlist.txt")
    assert [record["path"] for record in records] == ["allowed.md"]
    assert records[0]["publishability_status"] == "review_required"
    assert records[0]["review_classification"] == "generalizable_pattern"
    assert records[0]["candidate_concepts"] == ["workflows"]
    assert records[0]["source_id"] == "private_rock_repo_candidates"


def test_private_scan_blocks_sensitive_values():
    records = scan_private_repo(FIXTURES / "private_repo")
    secret = next(record for record in records if record["path"] == "secret.txt")
    assert secret["publishability_status"] == "blocked_sensitive_findings"
    assert secret["review_classification"] == "instance_private"
    assert secret["public_contribution_mode"] == "private_only_until_reviewed"
    assert secret["summary_candidate"] == ""


def test_private_scan_accepts_source_and_org_ids():
    records = scan_private_repo(
        FIXTURES / "private_repo",
        FIXTURES / "private_allowlist.txt",
        source_id="rockproduction_docs_private_candidates",
        org_id="oneall",
    )
    assert records[0]["source_id"] == "rockproduction_docs_private_candidates"
    assert records[0]["org_id"] == "oneall"
    assert records[0]["private_path_hash"]


def test_private_doc_risk_flags_and_classification():
    text = "PageId = 1234\nContact brian@example.org about this Rock workflow."
    flags = private_risk_flags(text)
    assert "email" in flags
    assert "rock_numeric_id" in flags
    assert classify_private_document(text, [], flags) == "needs_human_review"


def test_private_doc_candidate_concepts():
    concepts = candidate_concepts("This Lava workflow updates groups and check-in labels.")
    assert "lava" in concepts
    assert "workflows" in concepts


def test_private_scan_skips_hidden_metadata(tmp_path):
    hidden = tmp_path / ".obsidian" / "community-plugins.json"
    hidden.parent.mkdir()
    hidden.write_text('["plugin"]', encoding="utf-8")
    assert should_skip_private_path(hidden, tmp_path)
    assert scan_private_repo(tmp_path) == []


def test_public_contribution_row_requires_review_and_traceability():
    row = {
        "schema": CONTRIBUTION_SCHEMA,
        "contribution_id": "oneall:test",
        "org_id": "oneall",
        "concept_ids": ["workflows"],
        "contribution_type": "guide_section",
        "title": "Workflow Intake Pattern",
        "distilled_summary": "Use a workflow intake page for repeatable request handling.",
        "source_urls": [],
        "source_record_ids": [],
        "redaction_attestation": True,
        "review_status": "draft_private",
        "license_attestation": True,
        "confidence": "medium",
        "needs_live_verification": True,
    }
    errors = validate_contribution_row(row, "row", public=True)
    assert any("public contribution must be redaction reviewed" in error for error in errors)
    assert any("must include source_urls or source_record_ids" in error for error in errors)


def test_public_contribution_blocks_private_metadata():
    row = {
        "schema": CONTRIBUTION_SCHEMA,
        "contribution_id": "org:test",
        "org_id": "org",
        "concept_ids": ["groups"],
        "contribution_type": "task_card",
        "title": "Review Group Finder",
        "distilled_summary": "Review group finder behavior against public source guidance.",
        "source_urls": ["https://community.rockrms.com/documentation"],
        "source_record_ids": [],
        "private_source_hashes": ["abc"],
        "private_source_paths": ["internal/runbook.md"],
        "redaction_attestation": True,
        "review_status": "approved_for_public_distillation",
        "license_attestation": True,
        "confidence": "high",
        "needs_live_verification": True,
    }
    errors = validate_contribution_row(row, "row", public=True)
    assert any("private_source_hashes" in error for error in errors)
    assert any("private_source_paths" in error for error in errors)


def test_public_json_fields_block_private_transcript_derivation_marker():
    text = '{"id":"media-insight","derived_from_private_transcript":true}\n'

    errors = audit_json_public_fields("agent/topic-index.json", text)

    assert any("derived_from_private_transcript" in error for error in errors)


def test_contribution_file_validation_passes_reviewed_public_bundle(tmp_path):
    path = tmp_path / "bundle.jsonl"
    write_jsonl(
        path,
        [
            {
                "schema": CONTRIBUTION_SCHEMA,
                "contribution_id": "org:pattern-1",
                "org_id": "org",
                "concept_ids": ["lava"],
                "contribution_type": "troubleshooting_pattern",
                "title": "Lava Review Pattern",
                "distilled_summary": "Review custom Lava against official Lava docs and release caveats before publishing.",
                "source_urls": ["https://community.rockrms.com/lava"],
                "source_record_ids": [],
                "redaction_attestation": True,
                "review_status": "redaction_reviewed",
                "license_attestation": True,
                "confidence": "medium",
                "needs_live_verification": True,
            }
        ],
    )
    assert validate_contribution_file(path) == []


def test_contribution_template_is_not_validated_as_public_bundle(tmp_path):
    output = create_contribution_template("example_org", root=tmp_path, org_display_name="Example Org")
    assert output.name == "bundle.example.jsonl"
    assert contribution_paths(tmp_path) == []
    assert contribution_example_paths(output) == [output]
    assert validate_contribution_paths(contribution_paths(tmp_path)) == []


def test_contribution_check_report_summarizes_public_bundle(tmp_path):
    org_dir = tmp_path / "example-org"
    path = org_dir / "bundle.jsonl"
    write_jsonl(
        path,
        [
            {
                "schema": CONTRIBUTION_SCHEMA,
                "contribution_id": "example-org:workflow-pattern",
                "org_id": "example-org",
                "org_display_name": "Example Org",
                "concept_ids": ["workflows"],
                "contribution_type": "troubleshooting_pattern",
                "title": "Workflow launch checks",
                "distilled_summary": "Before publishing a workflow-backed process, verify triggers, permissions, notifications, and rollback expectations against official Rock guidance.",
                "source_urls": ["https://community.rockrms.com/documentation"],
                "source_record_ids": [],
                "redaction_attestation": True,
                "review_status": "redaction_reviewed",
                "license_attestation": True,
                "confidence": "medium",
                "needs_live_verification": True,
            }
        ],
    )
    report = contribution_check_report(org_dir)
    assert report["status"] == "ok"
    assert report["bundle_count"] == 1
    assert report["example_count"] == 0
    assert report["row_count"] == 1
    assert {"value": "troubleshooting_pattern", "count": 1} in report["contribution_types"]
    assert {"value": "workflows", "count": 1} in report["concept_ids"]
    assert {"value": "redaction_reviewed", "count": 1} in report["review_statuses"]
    assert report["errors"] == []


def test_contribution_check_report_tracks_examples_without_validating(tmp_path):
    output = create_contribution_template("example_org", root=tmp_path, org_display_name="Example Org")
    directory_report = contribution_check_report(tmp_path / "example_org")
    file_report = contribution_check_report(output)
    for report in [directory_report, file_report]:
        assert report["status"] == "ok"
        assert report["bundle_count"] == 0
        assert report["example_count"] == 1
        assert report["row_count"] == 0
        assert report["errors"] == []


def test_contribution_check_report_fails_unreviewed_public_bundle(tmp_path):
    path = tmp_path / "example-org" / "bundle.jsonl"
    write_jsonl(
        path,
        [
            {
                "schema": CONTRIBUTION_SCHEMA,
                "contribution_id": "example-org:draft",
                "org_id": "example-org",
                "org_display_name": "Example Org",
                "concept_ids": ["groups"],
                "contribution_type": "guide_section",
                "title": "Draft group pattern",
                "distilled_summary": "This draft should remain private until redaction and license review are complete.",
                "source_urls": ["https://community.rockrms.com/documentation"],
                "source_record_ids": [],
                "redaction_attestation": False,
                "review_status": "draft_private",
                "license_attestation": False,
                "confidence": "needs_review",
                "needs_live_verification": True,
            }
        ],
    )
    report = contribution_check_report(path)
    assert report["status"] == "fail"
    assert report["bundle_count"] == 1
    assert report["row_count"] == 1
    assert any("public contribution must be redaction reviewed" in error for error in report["errors"])


def test_distill_private_scan_creates_private_draft_without_paths(tmp_path):
    scan_path = tmp_path / "scan.jsonl"
    output = tmp_path / "distilled.jsonl"
    write_jsonl(
        scan_path,
        [
            {
                "source_id": "rockproduction_docs_private_candidates",
                "org_id": "oneall",
                "path": "ops/workflow.md",
                "private_path_hash": "path-hash",
                "content_hash": "content-hash",
                "review_classification": "generalizable_pattern",
                "public_contribution_mode": "distill_then_review",
                "candidate_concepts": ["workflows"],
                "risk_flags": [],
                "sensitive_findings": [],
                "summary_candidate": "Rock workflow intake patterns should be reviewed before launch.",
            },
            {
                "source_id": "rockproduction_docs_private_candidates",
                "org_id": "oneall",
                "path": "ops/private.md",
                "private_path_hash": "blocked",
                "content_hash": "blocked",
                "review_classification": "needs_human_review",
                "public_contribution_mode": "private_only_until_reviewed",
                "candidate_concepts": ["workflows"],
                "risk_flags": ["email"],
                "sensitive_findings": [],
                "summary_candidate": "Do not use this.",
            },
        ],
    )
    rows = distill_private_scan(
        scan_path,
        source_id="rockproduction_docs_private_candidates",
        concept_id="workflows",
        org_id="oneall",
        output_path=output,
        dependency_output_path=tmp_path / "deps.jsonl",
    )
    assert len(rows) == 1
    assert rows[0]["review_status"] == "draft_private"
    assert rows[0]["private_source_hashes"] == ["content-hash"]
    assert "private_source_paths" not in rows[0]
    assert "ops/workflow.md" not in rows[0]["distilled_summary"]


def test_distill_private_scan_writes_private_dependency_map(tmp_path):
    scan_path = tmp_path / "scan.jsonl"
    output = tmp_path / "distilled.jsonl"
    dependency_path = tmp_path / "deps.jsonl"
    write_jsonl(
        scan_path,
        [
            {
                "source_id": "rockproduction_docs_private_candidates",
                "org_id": "oneall",
                "path": "ops/workflow.md",
                "private_path_hash": "path-hash",
                "content_hash": "content-hash",
                "review_classification": "generalizable_pattern",
                "public_contribution_mode": "distill_then_review",
                "candidate_concepts": ["workflows"],
                "risk_flags": [],
                "sensitive_findings": [],
                "summary_candidate": "Rock workflow intake patterns should be reviewed before launch.",
            }
        ],
    )
    rows = distill_private_scan(
        scan_path,
        source_id="rockproduction_docs_private_candidates",
        concept_id="workflows",
        org_id="oneall",
        output_path=output,
        dependency_output_path=dependency_path,
    )
    assert len(list(dependency_path.read_text(encoding="utf-8").splitlines())) == len(rows)
    stale = report_private_staleness(scan_path, dependency_path)
    assert stale == [
        {
            "contribution_id": rows[0]["contribution_id"],
            "source_id": "rockproduction_docs_private_candidates",
            "org_id": "oneall",
            "concept_ids": ["workflows"],
            "needs_rebuild": False,
            "reason": "current",
            "private_source_hash_count": 1,
            "missing_private_source_hashes": [],
            "public_artifact_path": None,
        }
    ]


def test_private_staleness_reports_missing_hash_without_private_content(tmp_path):
    scan_path = tmp_path / "scan.jsonl"
    dependency_path = tmp_path / "deps.jsonl"
    write_jsonl(scan_path, [{"content_hash": "new-hash"}])
    write_jsonl(
        dependency_path,
        [
            {
                "contribution_id": "private-distill:abc",
                "source_id": "rockproduction_docs_private_candidates",
                "org_id": "oneall",
                "concept_ids": ["workflows"],
                "private_source_hashes": ["old-hash"],
                "private_path_hashes": ["path-hash"],
                "public_artifact_path": None,
            }
        ],
    )
    rows = report_private_staleness(scan_path, dependency_path)
    assert rows[0]["needs_rebuild"] is True
    assert rows[0]["missing_private_source_hashes"] == ["old-hash"]
    assert "private_path_hashes" not in rows[0]


def test_private_review_report_summarizes_without_private_paths(tmp_path):
    scan_path = tmp_path / "scan.jsonl"
    write_jsonl(
        scan_path,
        [
            {
                "source_id": "rockproduction_docs_private_candidates",
                "org_id": "oneall",
                "path": "ops/private-workflow.md",
                "private_path_hash": "path-hash",
                "content_hash": "content-hash",
                "publishability_status": "review_required",
                "review_classification": "generalizable_pattern",
                "public_contribution_mode": "distill_then_review",
                "candidate_concepts": ["workflows", "lava"],
                "risk_flags": [],
                "redaction_required": False,
                "sensitive_findings": [],
                "summary_candidate": "Rock workflow intake patterns should be reviewed before launch.",
            },
            {
                "source_id": "rockproduction_docs_private_candidates",
                "org_id": "oneall",
                "path": "ops/person-data.md",
                "private_path_hash": "private-hash",
                "content_hash": "private-content",
                "publishability_status": "blocked_sensitive_findings",
                "review_classification": "instance_private",
                "public_contribution_mode": "private_only_until_reviewed",
                "candidate_concepts": ["groups"],
                "risk_flags": ["email"],
                "redaction_required": True,
                "sensitive_findings": ["email on line 1"],
                "summary_candidate": "",
            },
        ],
    )
    report = private_review_report(scan_path, source_id="rockproduction_docs_private_candidates", org_id="oneall")
    assert report["records"] == 2
    assert report["eligible_for_private_distill"] == 1
    assert report["blocked_or_sensitive"] == 1
    assert report["redaction_required"] == 1
    assert {"value": "workflows", "count": 1} in report["candidate_concepts"]
    report_text = str(report)
    assert "ops/private-workflow.md" not in report_text
    assert "ops/person-data.md" not in report_text
    assert "private_path_hash" not in report_text


def test_contribution_promote_stages_private_drafts_without_private_hashes(tmp_path):
    draft_path = tmp_path / "drafts.jsonl"
    output = tmp_path / "staging.jsonl"
    write_jsonl(
        draft_path,
        [
            {
                "schema": CONTRIBUTION_SCHEMA,
                "contribution_id": "private-distill:abc",
                "org_id": "oneall",
                "org_display_name": "private",
                "source_id": "rockproduction_docs_private_candidates",
                "concept_ids": ["workflows"],
                "contribution_type": "guide_section",
                "title": "Draft Private Pattern: Workflow Intake",
                "distilled_summary": "Private draft summary that must be rewritten before publication.",
                "source_urls": [],
                "source_record_ids": [],
                "private_source_hashes": ["content-hash"],
                "private_path_hashes": ["path-hash"],
                "redaction_attestation": False,
                "review_status": "draft_private",
                "license_attestation": False,
                "confidence": "needs_review",
                "needs_live_verification": True,
            }
        ],
    )
    result = promote_private_contributions(draft_path, org_id="oneall", output_path=output)
    rows = list(output.read_text(encoding="utf-8").splitlines())
    assert result["status"] == "private_staging"
    assert len(rows) == 1
    staged = json.loads(rows[0])
    assert staged["review_status"] == "needs_followup"
    assert staged["source_private_contribution_id"] == "private-distill:abc"
    assert "private_source_hashes" not in staged
    assert "private_path_hashes" not in staged
    assert validate_contribution_row(staged, "staged", public=True)


def test_contribution_promote_reviewed_requires_rewrite_and_attestations(tmp_path):
    draft_path = tmp_path / "drafts.jsonl"
    write_jsonl(
        draft_path,
        [
            {
                "schema": CONTRIBUTION_SCHEMA,
                "contribution_id": "private-distill:abc",
                "org_id": "oneall",
                "concept_ids": ["workflows"],
                "contribution_type": "guide_section",
                "title": "Draft Private Pattern: Workflow Intake",
                "distilled_summary": "Private draft summary that must be rewritten before publication.",
                "source_urls": [],
                "source_record_ids": [],
                "review_status": "draft_private",
                "confidence": "needs_review",
                "needs_live_verification": True,
            }
        ],
    )
    with pytest.raises(ValueError, match="requires --rewrite-file"):
        promote_private_contributions(draft_path, org_id="oneall", reviewed=True)


def test_contribution_promote_reviewed_public_bundle_passes_validation(tmp_path):
    draft_path = tmp_path / "drafts.jsonl"
    rewrite_path = tmp_path / "rewrites.jsonl"
    output = tmp_path / "bundle.jsonl"
    write_jsonl(
        draft_path,
        [
            {
                "schema": CONTRIBUTION_SCHEMA,
                "contribution_id": "private-distill:abc",
                "org_id": "oneall",
                "org_display_name": "private",
                "concept_ids": ["workflows"],
                "contribution_type": "guide_section",
                "title": "Draft Private Pattern: Workflow Intake",
                "distilled_summary": "Private draft summary that must be rewritten before publication.",
                "source_urls": [],
                "source_record_ids": [],
                "review_status": "draft_private",
                "confidence": "needs_review",
                "needs_live_verification": True,
            }
        ],
    )
    write_jsonl(
        rewrite_path,
        [
            {
                "contribution_id": "private-distill:abc",
                "public_contribution_id": "oneall:workflow-intake-review",
                "org_display_name": "ONE&ALL Church",
                "title": "Workflow intake patterns need launch review",
                "distilled_summary": "Use this pattern as a generalized launch-review reminder: workflow intake pages should be checked against official workflow behavior, permissions, notifications, and rollback expectations before they are used by staff or guests.",
                "source_urls": ["https://community.rockrms.com/documentation"],
                "source_record_ids": [],
                "confidence": "medium",
                "needs_live_verification": True,
                "reviewer_notes": "Generalized from private operational review.",
            }
        ],
    )
    result = promote_private_contributions(
        draft_path,
        org_id="oneall",
        output_path=output,
        rewrite_path=rewrite_path,
        reviewed=True,
        redaction_attestation=True,
        license_attestation=True,
    )
    assert result["status"] == "public_bundle"
    assert result["private_dependency_output"]
    assert validate_contribution_file(output) == []
    row_text = output.read_text(encoding="utf-8")
    assert "source_private_contribution_id" not in row_text
    assert "private_source_hashes" not in row_text
    assert "source_review_origin" in row_text


def test_contribution_promote_detects_duplicate_public_rows(tmp_path):
    draft_path = tmp_path / "drafts.jsonl"
    rewrite_path = tmp_path / "rewrites.jsonl"
    write_jsonl(
        draft_path,
        [
            {
                "schema": CONTRIBUTION_SCHEMA,
                "contribution_id": "private-distill:one",
                "org_id": "oneall",
                "concept_ids": ["workflows"],
                "contribution_type": "guide_section",
                "title": "Draft One",
                "distilled_summary": "Private one.",
                "source_urls": [],
                "source_record_ids": [],
                "review_status": "draft_private",
                "confidence": "needs_review",
                "needs_live_verification": True,
            },
            {
                "schema": CONTRIBUTION_SCHEMA,
                "contribution_id": "private-distill:two",
                "org_id": "oneall",
                "concept_ids": ["workflows"],
                "contribution_type": "guide_section",
                "title": "Draft Two",
                "distilled_summary": "Private two.",
                "source_urls": [],
                "source_record_ids": [],
                "review_status": "draft_private",
                "confidence": "needs_review",
                "needs_live_verification": True,
            },
        ],
    )
    rewrite_rows = []
    for private_id in ["private-distill:one", "private-distill:two"]:
        rewrite_rows.append(
            {
                "contribution_id": private_id,
                "public_contribution_id": "oneall:duplicate",
                "title": f"Public rewrite {private_id}",
                "distilled_summary": f"This reviewed public rewrite for {private_id} is long enough and source-linked so duplicate detection is the only failing condition in this promotion test.",
                "source_urls": [f"https://community.rockrms.com/documentation/{private_id[-3:]}"],
                "source_record_ids": [],
                "confidence": "medium",
                "needs_live_verification": True,
            }
        )
    write_jsonl(rewrite_path, rewrite_rows)
    with pytest.raises(ValueError, match="duplicate contribution_id"):
        promote_private_contributions(
            draft_path,
            org_id="oneall",
            rewrite_path=rewrite_path,
            reviewed=True,
            redaction_attestation=True,
            license_attestation=True,
        )


def test_contribution_promote_reviewed_writes_private_public_dependency_map(tmp_path):
    draft_path = tmp_path / "drafts.jsonl"
    rewrite_path = tmp_path / "rewrites.jsonl"
    output = tmp_path / "bundle.jsonl"
    dependency_output = REPO_ROOT / "data" / "review" / "private-promotion-dependencies" / "testorg.jsonl"
    if dependency_output.exists():
        dependency_output.unlink()
    write_jsonl(
        draft_path,
        [
            {
                "schema": CONTRIBUTION_SCHEMA,
                "contribution_id": "private-distill:dependency-test",
                "org_id": "testorg",
                "source_id": "rockproduction_docs_private_candidates",
                "concept_ids": ["workflows"],
                "contribution_type": "guide_section",
                "title": "Draft Private Pattern: Dependency Test",
                "distilled_summary": "Private draft summary that must be rewritten before publication.",
                "source_urls": [],
                "source_record_ids": [],
                "private_source_hashes": ["old-private-hash"],
                "private_path_hashes": ["path-hash"],
                "review_status": "draft_private",
                "confidence": "needs_review",
                "needs_live_verification": True,
            }
        ],
    )
    write_jsonl(
        rewrite_path,
        [
            {
                "contribution_id": "private-distill:dependency-test",
                "public_contribution_id": "testorg:dependency-test",
                "title": "Workflow dependency test",
                "distilled_summary": "This public rewrite describes a generalized workflow review pattern with enough detail for validation and without copying private text from the source draft.",
                "source_urls": ["https://community.rockrms.com/documentation"],
                "source_record_ids": [],
                "confidence": "medium",
                "needs_live_verification": True,
            }
        ],
    )
    result = promote_private_contributions(
        draft_path,
        org_id="testorg",
        output_path=output,
        rewrite_path=rewrite_path,
        reviewed=True,
        redaction_attestation=True,
        license_attestation=True,
    )
    dependency_path = Path(result["private_dependency_output"])
    rows = list(read_jsonl(dependency_path))
    assert rows[-1]["public_contribution_id"] == "testorg:dependency-test"
    assert rows[-1]["private_source_hashes"] == ["old-private-hash"]
    assert rows[-1]["private_path_hashes"] == ["path-hash"]
    assert rows[-1]["public_artifact_path"] == str(output)
    dependency_path.unlink()


def test_private_impact_reports_public_artifacts_without_private_paths(tmp_path):
    scan_path = tmp_path / "scan.jsonl"
    dependency_path = tmp_path / "deps.jsonl"
    write_jsonl(scan_path, [{"source_id": "rockproduction_docs_private_candidates", "org_id": "oneall", "content_hash": "new-private-hash"}])
    write_jsonl(
        dependency_path,
        [
            {
                "schema": "rock-kb-private-promotion-dependency-v1",
                "public_contribution_id": "oneall:workflow-pattern",
                "private_contribution_id": "private-distill:abc",
                "source_id": "rockproduction_docs_private_candidates",
                "org_id": "oneall",
                "concept_ids": ["workflows"],
                "private_source_hashes": ["old-private-hash"],
                "private_path_hashes": ["private-path-hash"],
                "public_artifact_path": "contributions/oneall/bundle.jsonl",
            }
        ],
    )
    report = report_private_impact(scan_path, dependency_path=dependency_path, source_id="rockproduction_docs_private_candidates", org_id="oneall")
    assert report["impacted"] == 1
    assert report["impacted_concepts"] == ["workflows"]
    assert report["rows"][0]["needs_rebuild"] is True
    report_text = str(report)
    assert "private-path-hash" not in report_text
    assert "old-private-hash" in report_text


def test_source_policy_audit_passes_registry():
    assert audit_source_policy() == []


def test_public_export_blocks_private_paths():
    assert is_private_path("data/review/concept-synthesis/check-in.hydrated-source-pack.json")
    assert is_private_path("data/review/private-dependencies/rockproduction_docs_private_candidates-workflows.jsonl")
    assert is_private_path("data/review/private-distill/rockproduction_docs_private_candidates-workflows.jsonl")
    assert is_private_path("data/raw-manifests/rock_documentation.jsonl")
    assert is_private_path("data/media/rock_podcast_rss.transcripts.jsonl")
    assert not is_private_path("knowledge/concepts/check-in/quickstart.md")


def test_public_json_audit_blocks_raw_fields():
    text = '{"id": "bad", "full_text": "raw mirror", "source_url": "https://example.com"}'
    errors = audit_json_public_fields("agent/bad.json", text)
    assert any("full_text" in error for error in errors)


def test_public_json_audit_blocks_nested_raw_fields():
    text = '{"id": "bad", "records": [{"content": "raw mirror"}]}'
    errors = audit_json_public_fields("agent/bad.json", text)
    assert any("$.records[0].content" in error for error in errors)


def test_public_release_caveat_audit_requires_traceability():
    text = '{"concept_id": "groups", "version": "99", "summary": "untraced"}'
    errors = audit_json_public_traceability("knowledge/concepts/groups/release-caveats.jsonl", text)
    assert any("no source_url or source_record_id" in error for error in errors)


def test_public_entity_audit_requires_traceability():
    text = '{"concept_id": "groups", "entity": "Group"}'
    errors = audit_json_public_traceability("knowledge/concepts/groups/entities.jsonl", text)
    assert any("entity row has no source_urls or source_keys" in error for error in errors)


def test_public_section_status_audit_requires_traceability():
    text = '{"concept_id": "groups", "section_id": "overview", "status": "current"}'
    errors = audit_json_public_traceability("knowledge/concepts/groups/section-status.jsonl", text)
    assert any("section status row has no depends_on_sources" in error for error in errors)


def test_public_export_is_distilled_artifacts_only():
    exported = {path.relative_to(REPO_ROOT).as_posix() for path in iter_public_files()}
    assert "knowledge/concepts/check-in/quickstart.md" in exported
    assert "agent/rock-kb-manifest.json" in exported
    assert "agent/concept-dependencies.jsonl" not in exported
    assert "knowledge/concepts/check-in/guide-dependencies.json" not in exported
    assert "knowledge/concepts/check-in/guide-quality.json" not in exported
    assert "agent/topic-index.jsonl" not in exported
    assert "knowledge/sources/rock_documentation.md" not in exported
    assert "knowledge/topics/api.md" not in exported


def test_public_export_surface_stays_community_focused():
    exported = {public_path: source_path.relative_to(REPO_ROOT).as_posix() for public_path, source_path in iter_public_file_entries()}

    assert exported["README.md"] == "docs/public-repo-readme.md"
    assert "community-contributions/example-org/bundle.example.jsonl" in exported
    assert "contributions/example-org/bundle.example.jsonl" not in exported
    assert "docs/project-goal.md" not in exported
    assert "docs/topic-gap-report.md" not in exported

    for path in [
        "agent/claim-review-dashboard.md",
        "agent/claim-review-queue.jsonl",
        "agent/evaluation-report.json",
        "agent/evaluation-results.jsonl",
        "agent/evaluation-set.jsonl",
        "agent/source-conflicts.jsonl",
    ]:
        assert path not in exported

    manifest = json.loads(public_export_text_for_path(REPO_ROOT / "agent" / "rock-kb-manifest.json"))
    for key in [
        "claim_review_dashboard",
        "claim_review_queue",
        "evaluation_report",
        "evaluation_results",
        "evaluation_set",
        "private_media",
        "source_conflicts",
    ]:
        assert key not in manifest["agent_entrypoints"]


def test_public_claim_sanitizer_removes_private_live_probe_details():
    row = {
        "id": "claim-1",
        "private_corpus_pointer": {"path": "/Users/briand/private.md"},
        "derived_from": {
            "type": "approved_candidate",
            "source_id": "private_rock_repo_candidates",
            "schema": "private-candidate-v1",
            "path": "/Users/briand/private.md",
        },
        "live_verification": {
            "instance": "ONE&ALL RockDB",
            "verification_method": "targeted_operational_probe",
            "verified_at": "2026-06-11T00:00:00Z",
            "evidence_refs": [
                {
                    "evidence_id": "oneall-rockdb-targeted-operational-probe",
                    "path": "data/review/live-verification-evidence/oneall-rockdb.md",
                    "probe_type": "targeted_operational_probe",
                    "tables": ["Attribute", "AttributeValue"],
                }
            ],
            "notes": ["Verified against ONE&ALL RockDB."],
        },
    }
    sanitized = sanitize_public_claim(row)
    text = json.dumps(sanitized)
    assert "private_corpus_pointer" not in sanitized
    assert "ONE&ALL" not in text
    assert "RockDB" not in text
    assert "oneall-rockdb" not in text
    assert sanitized["derived_from"] == {
        "type": "approved_candidate",
        "source_id": "private_rock_repo_candidates",
        "schema": "private-candidate-v1",
    }
    assert sanitized["live_verification"]["evidence_refs"] == [
        {"probe_type": "targeted_operational_probe", "tables": ["Attribute", "AttributeValue"]}
    ]


def test_public_model_map_sanitizer_removes_private_provenance_paths():
    sanitized = strip_private_provenance(
        {
            "entity": "GroupMember",
            "source_path": "/Users/briand/Documents/GitHub/Rock General Knowledge Base/data/review/model-map/stable.jsonl",
            "stable": {
                "path": "/Users/briand/Documents/GitHub/Rock General Knowledge Base/data/review/model-map/stable.jsonl",
                "version": "17.4",
            },
            "properties": [{"name": "PersonId", "path": "knowledge/model-map/models/group-member.md"}],
        }
    )
    assert "source_path" not in sanitized
    assert "path" not in sanitized["stable"]
    assert sanitized["properties"][0]["path"] == "knowledge/model-map/models/group-member.md"


def test_public_source_policy_allows_public_github_examples():
    assert is_public_source(
        {
            "id": "oneall_rock_sql_library",
            "root_url": "https://github.com/ONE-ALL-Church/Rock-SQL-Library",
            "public_publish_mode": "public_cite_and_summarize_only",
        }
    )


def test_public_export_blocks_internal_markers():
    errors = audit_forbidden_public_text("agent/bad.json", "instance: ONE&ALL RockDB\npath: /Users/briand/file.md")
    assert any("RockDB" in error for error in errors)
    assert any("/Users/" in error for error in errors)


def test_sensitive_scanner_does_not_flag_section_metadata():
    lines = ['{"section_id":"19-agent-task-recipes-recipe-verify-a-check-in-configuration"}']
    assert grep_sensitive_values(lines) == []
    assert grep_sensitive_values(["password = hello"])
