from __future__ import annotations

from pathlib import Path
from typing import Iterable

import typer
from rich import print_json

from ..jsonl import read_jsonl
from ..rock_idea_relationships import (
    ROCK_IDEA_RELATIONSHIP_PATH,
    ROCK_IDEA_VERIFICATION_QUEUE_PATH,
    ROCK_IDEA_VERIFICATION_REVIEW_PATH,
    validate_rock_idea_verification_queue,
    validate_rock_idea_verification_reviews,
    validate_rock_idea_relationship_rows,
)
from ..rock_ideas import ROCK_IDEA_PATH, sync_rock_ideas, validate_rock_idea_rows


app = typer.Typer(help="Rock Community Ideas metadata commands.")


@app.command("sync")
def sync_command(
    workers: int = typer.Option(5, "--workers", min=1, max=10),
    skip_details: bool = typer.Option(False, "--skip-details"),
    detail_refresh_limit: int = typer.Option(120, "--detail-refresh-limit", min=0, max=500),
) -> None:
    """Refresh the complete, public-safe Ideas metadata catalog."""
    print_json(
        data=sync_rock_ideas(
            workers=workers,
            enrich_details=not skip_details,
            detail_refresh_limit=detail_refresh_limit,
        )
    )


@app.command("validate")
def validate_command(
    path: Path = typer.Option(ROCK_IDEA_PATH, "--path", exists=True, dir_okay=False),
    relationships_path: Path = typer.Option(
        ROCK_IDEA_RELATIONSHIP_PATH,
        "--relationships-path",
        exists=True,
        dir_okay=False,
    ),
    verification_queue_path: Path = typer.Option(
        ROCK_IDEA_VERIFICATION_QUEUE_PATH,
        "--verification-queue-path",
        exists=True,
        dir_okay=False,
    ),
    verification_reviews_path: Path = typer.Option(
        ROCK_IDEA_VERIFICATION_REVIEW_PATH,
        "--verification-reviews-path",
        exists=True,
        dir_okay=False,
    ),
) -> None:
    """Validate Ideas identity, lifecycle, trust, and public-safety boundaries."""
    rows = list(read_jsonl(path))
    relationships = list(read_jsonl(relationships_path))
    verification_queue = list(read_jsonl(verification_queue_path))
    verification_reviews = list(read_jsonl(verification_reviews_path))
    validate_rock_idea_rows(rows)
    validate_rock_idea_relationship_rows(relationships, idea_rows=rows)
    validate_rock_idea_verification_queue(verification_queue, idea_rows=rows)
    validate_rock_idea_verification_reviews(verification_reviews, idea_rows=rows)
    print_json(
        data={
            "status": "ok",
            "path": str(path),
            "record_count": len(rows),
            "relationships_path": str(relationships_path),
            "relationship_count": len(relationships),
            "verification_queue_path": str(verification_queue_path),
            "verification_queue_count": len(verification_queue),
            "verification_reviews_path": str(verification_reviews_path),
            "verification_review_count": len(verification_reviews),
        }
    )


@app.command("list")
def list_command(
    status: str | None = typer.Option(None, "--status"),
    category: str | None = typer.Option(None, "--category"),
    concept: str | None = typer.Option(None, "--concept"),
    planned_version: str | None = typer.Option(None, "--planned-version"),
    limit: int = typer.Option(50, "--limit", min=1, max=500),
) -> None:
    """List compact local idea rows for feature-gap and roadmap review."""
    rows = []
    for row in read_jsonl(ROCK_IDEA_PATH):
        if status and str(row.get("status") or "").lower() != status.lower().replace(" ", "_"):
            continue
        if category and str(row.get("category") or "").lower() != category.lower():
            continue
        if concept and concept not in (row.get("concept_ids") or []):
            continue
        if planned_version and str(row.get("planned_version") or "") != planned_version:
            continue
        rows.append(compact_idea(row))
    rows.sort(key=lambda row: int(row.get("number") or 0), reverse=True)
    print_json(data={"schema": "rock-kb-rock-idea-list-v1", "count": min(len(rows), limit), "ideas": rows[:limit]})


@app.command("get")
def get_command(idea_ref: str) -> None:
    """Get one exact local idea and its typed relationships."""
    number = idea_number(idea_ref)
    row = next((value for value in read_jsonl(ROCK_IDEA_PATH) if int(value.get("number") or 0) == number), None)
    if row is None:
        raise typer.BadParameter(f"Idea not found: rock_idea:{number}")
    idea_id = str(row["idea_id"])
    relationships = relationships_for_record(read_jsonl(ROCK_IDEA_RELATIONSHIP_PATH), idea_id)
    print_json(
        data={
            "schema": "rock-kb-rock-idea-result-v1",
            "status": "ok",
            "idea_id": idea_id,
            "idea": row,
            "relationships": relationships,
        }
    )


def idea_number(value: str) -> int:
    text = value.strip().rstrip("/")
    if "/ideas/" in text:
        text = text.split("/ideas/", 1)[1].split("/", 1)[0]
    text = text.removeprefix("rock_idea:")
    if not text.isdigit() or int(text) < 1:
        raise typer.BadParameter("Idea reference must be a number, rock_idea ID, or Rock Community idea URL")
    return int(text)


def compact_idea(row: dict) -> dict:
    keys = [
        "idea_id",
        "number",
        "title",
        "url",
        "category",
        "status",
        "status_label",
        "vote_count",
        "planned_version",
        "feature_size",
        "submitted_at",
        "response_updated_at",
        "concept_ids",
        "needs_live_verification",
    ]
    return {key: row.get(key) for key in keys}


def relationships_for_record(rows: Iterable[dict], record_id: str) -> list[dict]:
    relationships = []
    for value in rows:
        row = dict(value)
        source_id = str(row.get("source_id") or "")
        target_id = str(row.get("target_id") or "")
        if source_id != record_id and target_id != record_id:
            continue
        row["direction"] = "outbound" if source_id == record_id else "inbound"
        row["related_record_id"] = target_id if source_id == record_id else source_id
        relationships.append(row)
    return relationships
