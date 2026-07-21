from __future__ import annotations

import json
from pathlib import Path

import typer
from rich import print_json

from ..jsonl import read_jsonl
from ..paths import DATA_DIR
from ..rock_issues import (
    ROCK_ISSUE_PATH,
    ROCK_ISSUE_SUMMARY_PATH,
    assemble_investigation_packet,
    assess_catalog,
    attach_issue_enrichments,
    find_issue_row,
    investigation_plan,
    issue_enrichments_by_id,
    issue_matches_version,
    load_generated_issue_enrichments,
    load_reviewed_issue_enrichments,
    parse_issue_ref,
    sync_rock_issues,
    validate_rock_issue_rows,
)


app = typer.Typer(help="Rock core and mobile issue intelligence commands.")


@app.command("sync")
def sync_command(
    full: bool = typer.Option(False, "--full", help="Use an expanded timeline-history backfill; issue metadata is always count-reconciled."),
    timeline_days: int = typer.Option(120, "--timeline-days", min=1, max=730, help="Fetch timelines for open and recently updated issues."),
    timeline_backfill_limit: int = typer.Option(
        100,
        "--timeline-backfill-limit",
        min=0,
        max=2000,
        help="Also fetch this many oldest issue timelines that have never been captured.",
    ),
    timeline_issue: list[str] = typer.Option(
        [],
        "--timeline-issue",
        help="Refresh only this exact current/transferred issue timeline; repeat for more refs.",
    ),
) -> None:
    """Refresh the public-safe upstream issue catalog through GitHub's API."""
    print_json(
        data=sync_rock_issues(
            full=full,
            timeline_days=timeline_days,
            timeline_backfill_limit=timeline_backfill_limit,
            timeline_issue_refs=timeline_issue,
        )
    )


@app.command("validate")
def validate_command(path: Path = typer.Option(ROCK_ISSUE_PATH, "--path", exists=True, dir_okay=False)) -> None:
    """Validate issue identities, typed fields, deduplication, and public-safety boundaries."""
    rows = list(read_jsonl(path))
    validate_rock_issue_rows(rows)
    enrichment_count = 0
    if path.resolve() == ROCK_ISSUE_PATH.resolve():
        issue_ids = {str(row.get("issue_id") or "") for row in rows}
        reviewed = load_reviewed_issue_enrichments(issue_ids)
        generated = load_generated_issue_enrichments()
        if reviewed != generated:
            raise ValueError("Generated Rock issue enrichments are stale; run `uv run kb issues sync`")
        enrichment_count = len(generated)
    print_json(
        data={
            "status": "ok",
            "path": str(path),
            "record_count": len(rows),
            "reviewed_enrichment_count": enrichment_count,
        }
    )


@app.command("list")
def list_command(
    repository: str | None = typer.Option(None, "--repository"),
    state: str | None = typer.Option(None, "--state"),
    concept: str | None = typer.Option(None, "--concept"),
    version: str | None = typer.Option(None, "--version"),
    limit: int = typer.Option(50, "--limit", min=1, max=500),
) -> None:
    """List compact local issue rows for maintainer review."""
    enrichments = issue_enrichments_by_id()
    rows = []
    for raw_row in read_jsonl(ROCK_ISSUE_PATH):
        row = attach_issue_enrichments(raw_row, enrichments)
        if repository and str(row.get("repository") or "").lower() != repository.lower():
            continue
        if state and row.get("state") != state:
            continue
        if concept and concept not in (row.get("concept_ids") or []):
            continue
        if version and not issue_matches_version(row, version):
            continue
        rows.append(compact_issue(row))
    rows.sort(key=lambda row: str(row.get("updated_at") or ""), reverse=True)
    print_json(data={"schema": "rock-kb-rock-issue-list-v1", "count": min(len(rows), limit), "issues": rows[:limit]})


@app.command("get")
def get_command(issue_ref: str) -> None:
    """Get one exact local issue record by URL, canonical ID, core number, or mobile:number."""
    repository, number = parse_issue_ref(issue_ref)
    issue_id = f"rock_issue:{repository}#{number}"
    row = find_issue_row(read_jsonl(ROCK_ISSUE_PATH), repository, number)
    if row is None:
        raise typer.BadParameter(f"Issue not found: {issue_id}")
    print_json(data=attach_issue_enrichments(row, issue_enrichments_by_id()))


@app.command("plan")
def plan_command(
    issue_ref: str,
    include_private_instance: bool = typer.Option(False, "--include-private-instance", help="Add a permission-scoped, private-only instance investigator."),
) -> None:
    """Create a typed, read-only orchestrator-worker investigation packet."""
    repository, number = parse_issue_ref(issue_ref)
    issue_id = f"rock_issue:{repository}#{number}"
    row = find_issue_row(read_jsonl(ROCK_ISSUE_PATH), repository, number)
    if row is None:
        raise typer.BadParameter(f"Issue not found: {issue_id}")
    print_json(data=investigation_plan(row, include_private_instance=include_private_instance))


@app.command("assess")
def assess_command(
    profile: Path = typer.Argument(..., exists=True, dir_okay=False, help="Bounded JSON instance profile; never provide logs or private identifiers."),
    scope: str = typer.Option(
        "open",
        "--scope",
        help="Issue population: open, historical-unresolved, or all-relevant.",
    ),
    limit: int = typer.Option(100, "--limit", min=1, max=500),
    offset: int = typer.Option(0, "--offset", min=0),
) -> None:
    """Conservatively route catalog issues against a structured instance profile."""
    payload = json.loads(profile.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise typer.BadParameter("Profile must be a JSON object")
    enrichments = issue_enrichments_by_id()
    rows = (attach_issue_enrichments(row, enrichments) for row in read_jsonl(ROCK_ISSUE_PATH))
    catalog_metadata = (
        json.loads(ROCK_ISSUE_SUMMARY_PATH.read_text(encoding="utf-8"))
        if ROCK_ISSUE_SUMMARY_PATH.exists()
        else None
    )
    try:
        assessment = assess_catalog(
            rows,
            payload,
            scope=scope,
            limit=limit,
            offset=offset,
            catalog_metadata=catalog_metadata,
        )
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    print_json(data=assessment)


@app.command("assemble")
def assemble_command(
    issue_ref: str = typer.Argument(..., help="Issue URL, canonical ID, core number, or mobile:number."),
    worker_results: list[Path] = typer.Argument(..., exists=True, dir_okay=False, help="Typed worker-result JSON files."),
    include_private_instance: bool = typer.Option(False, "--include-private-instance"),
    output: Path | None = typer.Option(None, "--output", dir_okay=False, help="Private review-packet path under data/review/rock-issues."),
) -> None:
    """Validate typed worker results and assemble a private human-review packet."""
    repository, number = parse_issue_ref(issue_ref)
    issue_id = f"rock_issue:{repository}#{number}"
    issue = find_issue_row(read_jsonl(ROCK_ISSUE_PATH), repository, number)
    if issue is None:
        raise typer.BadParameter(f"Issue not found: {issue_id}")
    rows = []
    for path in worker_results:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise typer.BadParameter(f"Worker result must be a JSON object: {path}")
        rows.append(payload)
    packet = assemble_investigation_packet(
        issue,
        rows,
        include_private_instance=include_private_instance,
    )
    review_root = (DATA_DIR / "review" / "rock-issues").resolve()
    repository_slug = "mobile" if repository.endswith("Mobile-Issues") else "core"
    target = (output or review_root / "investigations" / f"{repository_slug}-{number}.json").resolve()
    if not target.is_relative_to(review_root):
        raise typer.BadParameter(f"Review packets must stay under {review_root}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print_json(
        data={
            "schema": packet["schema"],
            "issue_id": issue_id,
            "output": str(target),
            "packet_hash": packet["packet_hash"],
            "completed_tasks": packet["completed_tasks"],
            "missing_tasks": packet["missing_tasks"],
            "ready_for_skeptic": packet["ready_for_skeptic"],
            "ready_for_public_review": packet["ready_for_public_review"],
        }
    )


def compact_issue(row: dict) -> dict:
    return {
        key: row.get(key)
        for key in [
            "issue_id",
            "repository",
            "number",
            "title",
            "url",
            "state",
            "validation_state",
            "updated_at",
            "concept_ids",
            "version_evidence",
            "remediation_state",
            "evidence_state",
        ]
    } | {"reviewed_enrichment_count": len(row.get("reviewed_enrichments") or [])}
