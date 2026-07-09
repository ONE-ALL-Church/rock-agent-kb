from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import httpx
import typer
from rich.console import Console
from rich.table import Table

from ..agent_answer_pack import build_agent_answer_pack
from ..audit import audit_duplicate_source_urls, audit_license_records, audit_rockumentation_api_coverage
from ..cloudflare_markdown import cloudflare_markdown_env_ready, extract_cloudflare_markdown
from ..claim_evaluation import build_claim_model_evaluation_sample, claim_provenance_report
from ..claims import approved_claims_path, build_approved_claims, validate_claim_file
from ..concepts import (
    build_all_concepts,
    build_single_concept,
    concept_synthesis_pack,
    load_concepts,
    refresh_long_form_approved_claims,
    report_concept_staleness,
    report_guide_refresh_plan,
    synthesis_output_path,
)
from ..contributions import (
    contribution_check_report,
    contribution_paths,
    create_contribution_template,
    distill_private_scan,
    private_dependency_path,
    private_distill_path,
    private_review_report,
    promote_private_contributions,
    report_private_staleness,
    validate_contribution_paths,
)
from ..community import discover_community_urls, fetch_community_pages, normalize_community_fetch, probe_endpoints
from ..extract import build_raw_manifest, fetch_url, main_markdown, now_iso, optional_command
from ..github_sources import discover_github_repositories, normalize_github_search_records
from ..guide_intel import (
    audit_guide_quality,
    build_entity_rows,
    build_guide_intelligence,
    build_source_index,
    build_task_cards,
    parse_markdown_sections,
    read_latest_source_pack,
    section_source_map,
)
from ..hydrate import hydrated_concept_synthesis_pack
from ..indexes import build_agent_pack, build_sqlite_index
from ..jsonl import read_jsonl, write_jsonl
from ..live_verification import build_live_verification_probe_plan
from ..media import (
    build_media_insights,
    build_media_priority_queue,
    build_media_public_candidates,
    build_media_public_rewrite_drafts,
    build_media_sidecars,
    build_media_understanding_benchmark,
    discover_media,
    media_insights_path,
    media_manifest_path,
    media_priority_queue_path,
    media_priority_report_path,
    media_public_candidates_path,
    media_public_promotions_path,
    media_public_rewrite_drafts_path,
    media_review_sources,
    media_review_status_report,
    media_status_report,
    media_tool_status,
    prepare_media_understanding_benchmark_assets,
    run_ollama_media_understanding_benchmark,
    load_media_public_rewrites,
    promote_media_public_candidates,
    prune_dry_run_transcript_rows,
    run_media_batch,
    transcribe_media,
)
from ..mobile_selector_audit import build_mobile_selector_audit, mobile_selector_audit_status
from ..model_map import (
    DEMO_MODEL_MAP_SCRAPE_PATH,
    DEMO_ROCK_VERSION_ENDPOINT,
    LATEST_MODEL_MAP_SCRAPE_PATH,
    MODEL_MAP_VERSION_DIFF_JSONL_PATH,
    MODEL_MAP_VERSION_DIFF_PATH,
    build_model_map,
    build_model_map_version_diff,
    model_map_scrape_freshness,
    stamp_model_map_scrape_version,
)
from ..normalize import normalize_github_repo_metadata, normalize_raw_record, records_from_source_content
from ..paths import AGENT_DIR, MEDIA_DIR, NORMALIZED_DIR, PUBLIC_EXPORT_DIR, RAW_MANIFEST_DIR, REPO_ROOT, REVIEW_DIR, ensure_generated_dirs, source_output_path
from ..pipeline.build import run_build
from ..pipeline.status import build_status_report
from ..private_dependencies import report_private_impact
from ..private_corpus import (
    audit_private_corpus_leaks,
    autosync_private_corpus,
    ignored_private_artifact_report,
    initialize_private_corpus,
    restore_private_text_artifacts,
    sync_private_text_artifacts,
    validate_private_corpus,
    verify_private_corpus_rebuild,
    write_large_media_restore_manifest,
)
from ..private_scan import scan_private_repo
from ..publish import audit_public_export_manifest, audit_source_policy, build_public_export
from ..readiness import goal_readiness_report
from ..sources import get_source, load_sources, validate_registry
from ..source_orchestration import (
    DEFAULT_REFRESH_DASHBOARD_DIR,
    DEFAULT_REBUILD_PLAN_DIR,
    DEFAULT_SOURCE_SCAN_DIR,
    build_refresh_dashboard,
    build_rebuild_plan,
    build_source_scan_report,
)

console = Console()

DEFAULT_MODEL_MAP_NODE_PATH = Path("/tmp/rock-model-map-scrape/node_modules")


def list_sources() -> None:
    """List registered sources."""
    table = Table(title="Registered Sources")
    table.add_column("ID")
    table.add_column("Kind")
    table.add_column("Mode")
    table.add_column("Tier")
    table.add_column("Root URL")
    for source in load_sources():
        table.add_row(
            source.id,
            source.kind,
            source.allowed_extraction_mode,
            str(source.extraction_tier),
            source.root_url,
        )
    console.print(table)


def validate_sources() -> None:
    """Validate sources/registry.yaml."""
    errors = validate_registry()
    if errors:
        for error in errors:
            console.print(f"[red]ERROR[/red] {error}")
        raise typer.Exit(code=1)
    console.print("[green]Source registry is valid.[/green]")


def list_concepts() -> None:
    """List registered concept guides."""
    table = Table(title="Registered Concepts")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Max Records")
    table.add_column("Rebuild Policy")
    for concept in load_concepts():
        table.add_row(concept.id, concept.title, str(concept.max_records), concept.rebuild_policy)
    console.print(table)


def stale_concepts() -> None:
    """Report concept guides whose source hashes changed."""
    rows = report_concept_staleness()
    table = Table(title="Concept Staleness")
    table.add_column("Concept")
    table.add_column("Needs Rebuild")
    table.add_column("Reason")
    table.add_column("Source Count")
    table.add_column("Private Impacts")
    table.add_column("Guide")
    for row in rows:
        table.add_row(
            str(row.get("concept_id")),
            str(row.get("needs_rebuild")),
            str(row.get("reason")),
            str(row.get("source_count") or ""),
            str(row.get("private_dependency_impact_count") or 0),
            str(row.get("guide_path") or ""),
        )
    console.print(table)


def status_command() -> None:
    """Show pipeline freshness, review queues, and suggested next rebuild commands."""
    report = build_status_report()
    table = Table(title="Pipeline Status")
    table.add_column("Stage")
    table.add_column("Status")
    table.add_column("Changed Inputs")
    for row in report["pipeline"]:
        table.add_row(row["name"], row["status"], "\n".join(row.get("changed_inputs") or []))
    console.print(table)

    queues = report.get("queues") or {}
    queue_table = Table(title="Review Queues")
    queue_table.add_column("Queue")
    queue_table.add_column("Count")
    media = queues.get("media_review") or {}
    claims = queues.get("claim_review_queue") or {}
    guide = queues.get("guide_refresh") or {}
    concepts = queues.get("concept_staleness") or {}
    mobile = queues.get("mobile_selector_audit") or {}
    model_map_versions = queues.get("model_map_versions") or {}
    queue_table.add_row("pending media candidates", str(media.get("pending_candidate_count", 0)))
    queue_table.add_row("claim review rows", str(claims.get("rows", 0)))
    queue_table.add_row("guide index rebuilds", str(len(guide.get("needs_generated_index_rebuild") or [])))
    queue_table.add_row("long-form guide refreshes", str(len(guide.get("needs_long_form_guide_refresh") or [])))
    queue_table.add_row("stale concepts", str(len(concepts.get("stale") or [])))
    queue_table.add_row("mobile selector audit", mobile_selector_audit_label(mobile))
    queue_table.add_row("model-map versions", model_map_version_label(model_map_versions))
    console.print(queue_table)

    command_table = Table(title="Suggested Next Commands")
    command_table.add_column("Stage")
    command_table.add_column("Reason")
    command_table.add_column("Command")
    for command in report["suggested_commands"]:
        command_table.add_row(command["stage"], command["reason"], command["command"])
    console.print(command_table)


def mobile_selector_audit_label(mobile: dict[str, Any]) -> str:
    missing = len(mobile.get("missing_paths") or [])
    stale = int(mobile.get("stale_dependency_count") or 0)
    errors = int(mobile.get("inventory_error_count") or 0)
    if missing or stale or errors:
        return f"needs review ({missing} missing, {stale} stale, {errors} errors)"
    dependency = mobile.get("dependency") or {}
    selector_count = dependency.get("selector_row_count")
    if selector_count is not None:
        return f"current ({selector_count} selectors)"
    return "current"


def model_map_version_label(freshness: dict[str, Any]) -> str:
    status = freshness.get("status") or "unknown"
    tracks = freshness.get("tracks") or []
    if status == "current":
        return "current"
    if status == "stale":
        changes = [
            f"{row.get('label') or row.get('track')}: {row.get('recorded_version')} -> {row.get('live_version')}"
            for row in tracks
            if row.get("status") == "stale"
        ]
        return "stale (" + "; ".join(changes) + ")"
    if status == "unknown":
        unknown = [
            f"{row.get('label') or row.get('track')}: {row.get('probe_status')}"
            for row in tracks
            if row.get("status") == "unknown"
        ]
        return "unknown (" + "; ".join(unknown) + ")"
    if status == "missing":
        missing = [
            f"{row.get('label') or row.get('track')}: {row.get('probe_status')}"
            for row in tracks
            if row.get("status") in {"missing", "missing-version"}
        ]
        return "missing (" + "; ".join(missing) + ")"
    return str(status)


def build_command(
    stage: Optional[str] = typer.Option(None, "--stage", help="Run one stage plus stale upstream dependencies."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print the build plan without executing stages."),
    force: bool = typer.Option(False, "--force", help="Run selected stages even when their inputs are fresh."),
) -> None:
    """Run stale automatic pipeline stages and update build-state after each success."""
    try:
        result = run_build(stage_name=stage, dry_run=dry_run, force=force)
    except KeyError as exc:
        console.print(f"[red]ERROR[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print_json(json.dumps(result))


def discover(source: str = typer.Option(..., "--source", "-s")) -> None:
    """Discover child URLs for a source and write a raw manifest record."""
    ensure_generated_dirs()
    src = get_source(source)
    fetched = fetch_url(src.root_url)
    manifest = build_raw_manifest(src, fetched)
    count = write_jsonl(source_output_path(src.id, "raw"), [manifest])
    console.print(f"Discovered {len(manifest['discovered_urls'])} URLs; wrote {count} raw manifest row.")
    for url in manifest["discovered_urls"][:25]:
        console.print(url)
    if len(manifest["discovered_urls"]) > 25:
        console.print(f"... {len(manifest['discovered_urls']) - 25} more")


def fetch(
    source: str = typer.Option(..., "--source", "-s"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """Fetch a source root and write a raw manifest unless --dry-run is used."""
    ensure_generated_dirs()
    src = get_source(source)
    fetched = fetch_url(src.root_url)
    manifest = build_raw_manifest(src, fetched)
    preview = {
        key: manifest[key]
        for key in [
            "source_id",
            "source_url",
            "source_title",
            "status_code",
            "content_type",
            "content_hash",
            "license_status",
            "allowed_extraction_mode",
            "extraction_tier",
        ]
    }
    preview["discovered_url_count"] = len(manifest["discovered_urls"])
    console.print_json(json.dumps(preview))
    if dry_run:
        console.print("[yellow]Dry run only; no files written.[/yellow]")
        return
    count = write_jsonl(source_output_path(src.id, "raw"), [manifest])
    console.print(f"Wrote {count} raw manifest row to {source_output_path(src.id, 'raw')}")


def extract_markdown(
    url: Optional[str] = typer.Option(None, "--url", help="URL to convert to Markdown."),
    html_path: Optional[Path] = typer.Option(None, "--html-path", help="Local HTML file to convert to Markdown."),
    tool: str = typer.Option("local", "--tool", help="Extractor to use: local or cloudflare."),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Write Markdown to a file instead of stdout."),
    wait_until: Optional[str] = typer.Option(None, "--wait-until", help="Cloudflare gotoOptions.waitUntil value."),
    reject_request_pattern: Optional[list[str]] = typer.Option(
        None,
        "--reject-request-pattern",
        help="Cloudflare regex pattern for requests to reject. May be repeated.",
    ),
) -> None:
    """Convert a URL or local HTML file to Markdown."""
    if bool(url) == bool(html_path):
        console.print("[red]Provide exactly one of --url or --html-path.[/red]")
        raise typer.Exit(code=1)

    html = html_path.read_text(encoding="utf-8") if html_path else None
    if tool == "local":
        source_html = html if html is not None else fetch_url(str(url))["content"]
        markdown = main_markdown(source_html)
    elif tool == "cloudflare":
        goto_options = {"waitUntil": wait_until} if wait_until else None
        markdown = extract_cloudflare_markdown(
            url=url,
            html=html,
            reject_request_patterns=reject_request_pattern,
            goto_options=goto_options,
        )
    else:
        console.print("[red]--tool must be local or cloudflare.[/red]")
        raise typer.Exit(code=1)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8")
        console.print(f"Wrote Markdown to {output}")
        return
    console.print(markdown)


def extractor_doctor() -> None:
    """Report local and optional hosted extractor readiness."""
    table = Table(title="Extractor Readiness")
    table.add_column("Extractor")
    table.add_column("Ready")
    table.add_column("Notes")
    table.add_row("local", "yes", "Uses httpx + markdownify; default rebuild path.")
    table.add_row(
        "cloudflare",
        "yes" if cloudflare_markdown_env_ready() else "no",
        "Optional. Requires CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN.",
    )
    console.print(table)


def normalize(source: str = typer.Option(..., "--source", "-s")) -> None:
    """Normalize a source into data/normalized JSONL."""
    ensure_generated_dirs()
    src = get_source(source)
    _normalize_source(src)


@dataclass(frozen=True)
class RefreshStep:
    source_id: str
    discover: bool = False
    max_pages: int = 120
    id_sweep: bool = False
    sweep_window: int = 75


REFRESH_STEPS = [
    RefreshStep("rock_documentation", discover=True, max_pages=160),
    RefreshStep("rock_recipes", discover=True, max_pages=160, id_sweep=True, sweep_window=110),
    RefreshStep("rock_qa", discover=True, max_pages=12),
    RefreshStep("rock_rocku", discover=True, max_pages=140),
    RefreshStep("rock_developer", discover=True, max_pages=180),
    RefreshStep("rock_api_docs", discover=True, max_pages=20),
    RefreshStep("rock_lava_docs", discover=True, max_pages=160),
    RefreshStep("rock_community_hubs", discover=True, max_pages=100),
    RefreshStep("rock_community_blog", discover=True, max_pages=120),
    RefreshStep("rock_shop_plugins", discover=True, max_pages=180),
    RefreshStep("triumph_resources", discover=True, max_pages=180),
    RefreshStep("rock_community_site", discover=True, max_pages=40),
    RefreshStep("rock_mobile_docs", discover=True, max_pages=250),
    RefreshStep("rock_model_map"),
    RefreshStep("rock_core_release_notes"),
    RefreshStep("rock_mobile_release_notes"),
    RefreshStep("rock_podcast_rss"),
    RefreshStep("rock_youtube"),
    RefreshStep("rock_demo_api_docs_v1"),
    RefreshStep("rock_demo_api_docs_v2"),
    RefreshStep("sparkdevnetwork_rock"),
    RefreshStep("sparkdevnetwork_slingshot"),
    RefreshStep("oneall_rock_sql_library"),
    RefreshStep("public_rock_repos"),
]


def refresh(
    source: Optional[list[str]] = typer.Option(None, "--source", "-s", help="Limit refresh to one or more source IDs."),
    skip_discovery: bool = typer.Option(False, "--skip-discovery"),
    skip_probe: bool = typer.Option(False, "--skip-probe"),
    skip_indexes: bool = typer.Option(False, "--skip-indexes"),
) -> None:
    """Run the repeatable import pipeline for the registered public sources."""
    ensure_generated_dirs()
    selected = set(source or [])
    steps = [step for step in REFRESH_STEPS if not selected or step.source_id in selected]
    if selected:
        missing = selected - {step.source_id for step in steps}
        if missing:
            console.print(f"[red]Unknown or non-refresh source IDs: {', '.join(sorted(missing))}[/red]")
            raise typer.Exit(code=1)

    if not skip_probe:
        rows = probe_endpoints()
        write_jsonl(REVIEW_DIR / "endpoint-probes.jsonl", rows)
        console.print(f"Probed {len(rows)} endpoints.")

    for step in steps:
        src = get_source(step.source_id)
        if step.discover and not skip_discovery:
            urls = discover_community_urls(
                src,
                max_pages=step.max_pages,
                id_sweep=step.id_sweep,
                sweep_window=step.sweep_window,
            )
            write_jsonl(
                source_output_path(src.id, "raw"),
                [
                    {
                        "id": src.id,
                        "source_id": src.id,
                        "source_kind": src.kind,
                        "source_url": src.root_url,
                        "source_title": src.name,
                        "retrieved_at": now_iso(),
                        "status_code": 200,
                        "content_type": "text/html",
                        "content_hash": "",
                        "license_status": src.license_status,
                        "allowed_extraction_mode": src.allowed_extraction_mode,
                        "extraction_tool": "refresh_discovery",
                        "extraction_tier": src.extraction_tier,
                        "topics": src.topics,
                        "discovered_urls": urls,
                        "markdown": "",
                        "excerpt": "",
                    }
                ],
            )
            console.print(f"{src.id}: discovered {len(urls)} URLs.")
        _normalize_source(src)

    errors = audit_license_records()
    if errors:
        for error in errors:
            console.print(f"[red]ERROR[/red] {error}")
        raise typer.Exit(code=1)
    console.print("[green]License and citation audit passed.[/green]")

    if not skip_indexes:
        counts = build_agent_pack()
        counts.update(build_all_concepts())
        index_path = build_sqlite_index()
        console.print_json(json.dumps(counts))
        console.print(f"Built SQLite index at {index_path}")


def _normalize_source(src) -> int:
    records = []
    if src.kind == "github_repo":
        records = [_fetch_github_repo_record(src)]
    elif src.kind == "github_search":
        repos = discover_github_repositories()
        records = normalize_github_search_records(src, repos)
    elif src.kind in {
        "rock_documentation",
        "rock_recipes",
        "rock_qa",
        "rocku",
        "rock_developer",
        "rock_mobile_docs",
        "rock_community_hubs",
        "rock_community_blog",
        "rock_community_site",
        "rock_api_docs",
        "rock_lava_docs",
        "rock_shop_plugins",
        "triumph_resources",
    }:
        raw_path = source_output_path(src.id, "raw")
        raw_records = list(read_jsonl(raw_path))
        urls = []
        for raw in raw_records:
            urls.extend(raw.get("discovered_urls") or [])
            if raw.get("source_url"):
                urls.append(raw["source_url"])
        if not urls:
            urls = discover_community_urls(src, max_pages=250, id_sweep=src.kind in {"rock_recipes", "rock_qa"})
        fetched_pages = fetch_community_pages(urls, source=src)
        records = [record for record in (normalize_community_fetch(src, row) for row in fetched_pages) if record]
    elif src.kind in {"rock_release_notes", "rock_mobile_release_notes", "podcast_rss", "rss", "rock_model_map"}:
        fetched = fetch_url(src.root_url)
        records = records_from_source_content(src, fetched["content"])
    else:
        raw_path = source_output_path(src.id, "raw")
        raw_records = list(read_jsonl(raw_path))
        if not raw_records:
            fetched = fetch_url(src.root_url)
            raw_records = [build_raw_manifest(src, fetched)]
        records = [normalize_raw_record(src, row) for row in raw_records]
    count = write_jsonl(source_output_path(src.id, "normalized"), records)
    console.print(f"{src.id}: wrote {count} normalized records.")
    return count


def discover_community(
    source: str = typer.Option(..., "--source", "-s"),
    max_pages: int = typer.Option(250, "--max-pages"),
    id_sweep: bool = typer.Option(False, "--id-sweep"),
    sweep_window: int = typer.Option(75, "--sweep-window"),
) -> None:
    """Discover Rock Community child URLs with bounded crawling and optional numeric detail sweeps."""
    ensure_generated_dirs()
    src = get_source(source)
    urls = discover_community_urls(src, max_pages=max_pages, id_sweep=id_sweep, sweep_window=sweep_window)
    row = {
        "id": src.id,
        "source_id": src.id,
        "source_kind": src.kind,
        "source_url": src.root_url,
        "source_title": src.name,
        "retrieved_at": now_iso(),
        "status_code": 200,
        "content_type": "text/html",
        "content_hash": "",
        "license_status": src.license_status,
        "allowed_extraction_mode": src.allowed_extraction_mode,
        "extraction_tool": "community_static_discovery",
        "extraction_tier": src.extraction_tier,
        "topics": src.topics,
        "discovered_urls": urls,
        "markdown": "",
        "excerpt": "",
    }
    count = write_jsonl(source_output_path(src.id, "raw"), [row])
    console.print(f"Discovered {len(urls)} URLs; wrote {count} raw manifest row to {source_output_path(src.id, 'raw')}")
    for url in urls[:50]:
        console.print(url)
    if len(urls) > 50:
        console.print(f"... {len(urls) - 50} more")


def probe_endpoint_command() -> None:
    """Probe known Rock public/API endpoints and write review evidence."""
    ensure_generated_dirs()
    rows = probe_endpoints()
    output = REVIEW_DIR / "endpoint-probes.jsonl"
    count = write_jsonl(output, rows)
    console.print(f"Wrote {count} endpoint probe rows to {output}")
    table = Table(title="Endpoint Probe Summary")
    table.add_column("Status")
    table.add_column("Class")
    table.add_column("URL")
    for row in rows:
        table.add_row(str(row.get("status_code")), str(row.get("classification")), str(row.get("url")))
    console.print(table)


def summarize(
    source: str = typer.Option(..., "--source", "-s"),
    model: str = typer.Option("local-extractive", "--model"),
) -> None:
    """Create traceable summary records for a normalized source."""
    ensure_generated_dirs()
    src = get_source(source)
    records = list(read_jsonl(source_output_path(src.id, "normalized")))
    if not records:
        console.print(f"[red]No normalized records found for {src.id}. Run normalize first.[/red]")
        raise typer.Exit(code=1)
    llm_path = optional_command("llm")
    summary_rows = []
    for record in records:
        summary = record.get("summary") or ""
        if model != "local-extractive" and llm_path:
            summary = _summarize_with_llm(llm_path, model, record)
        summary_rows.append(
            {
                "id": record["id"] + ":summary",
                "source_record_ids": [record["id"]],
                "source_id": src.id,
                "prompt_id": "rock-kb-summary-v1",
                "model": model if llm_path or model == "local-extractive" else "local-extractive",
                "summary": summary,
                "created_at": record.get("retrieved_at"),
                "confidence": "needs-review" if record.get("needs_review") else "normal",
                "needs_review": bool(record.get("needs_review")),
                "citations": record.get("citations") or [],
            }
        )
    output = NORMALIZED_DIR / f"{src.id}.summaries.jsonl"
    count = write_jsonl(output, summary_rows)
    console.print(f"Wrote {count} summary records to {output}")


def repo_pack(repo: str = typer.Option(..., "--repo")) -> None:
    """Pack or describe a repository using installed repo-pack tools."""
    ensure_generated_dirs()
    output = REVIEW_DIR / "repo-pack-results.jsonl"
    tool = None
    command: Optional[list[str]] = None
    if optional_command("repomix"):
        tool = "repomix"
        command = ["repomix", repo, "--style", "markdown", "--stdout"]
    elif optional_command("gitingest"):
        tool = "gitingest"
        command = ["gitingest", repo]
    elif optional_command("files-to-prompt") and Path(repo).exists():
        tool = "files-to-prompt"
        command = ["files-to-prompt", repo, "--markdown"]

    if command:
        result = subprocess.run(command, check=False, text=True, capture_output=True, timeout=120)
        row = {
            "repo": repo,
            "tool": tool,
            "returncode": result.returncode,
            "stdout_preview": result.stdout[:2000],
            "stderr_preview": result.stderr[:2000],
        }
    else:
        row = {
            "repo": repo,
            "tool": None,
            "returncode": None,
            "stdout_preview": "",
            "stderr_preview": "No repo-pack tool installed. Install repomix, gitingest, or files-to-prompt.",
        }
    existing = list(read_jsonl(output))
    existing.append(row)
    write_jsonl(output, existing)
    console.print(f"Wrote repo-pack result to {output}")


def media_discover(
    source: str = typer.Option(..., "--source", "-s"),
    limit: Optional[int] = typer.Option(None, "--limit", help="Limit source records inspected."),
    include_empty: bool = typer.Option(False, "--include-empty", help="Write private rows for pages with no media URL found."),
) -> None:
    """Discover podcast/video media URLs into the private media queue."""
    ensure_generated_dirs()
    src = get_source(source)
    rows = discover_media(src, limit=limit, include_empty=include_empty)
    count = write_jsonl(media_manifest_path(src.id), rows)
    pending = sum(1 for row in rows if row.get("transcript_status") == "pending")
    console.print(f"{src.id}: wrote {count} private media rows to {media_manifest_path(src.id)} ({pending} pending transcription).")
    for row in rows[:20]:
        console.print(f"{row.get('transcript_status')}: {row.get('source_title')} -> {row.get('media_url')}")
    if len(rows) > 20:
        console.print(f"... {len(rows) - 20} more")


def media_transcribe(
    source: str = typer.Option(..., "--source", "-s"),
    limit: Optional[int] = typer.Option(None, "--limit"),
    media_id: Optional[list[str]] = typer.Option(None, "--media-id", help="Limit processing to one or more stable media IDs."),
    tool: str = typer.Option("auto", "--tool", help="auto, cloudflare, openai, mlx_whisper, parakeet, whisper-cli, or whisper."),
    model: str = typer.Option("auto", "--model"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """Transcribe queued private media when a local transcription CLI is available."""
    ensure_generated_dirs()
    src = get_source(source)
    if not media_manifest_path(src.id).exists():
        console.print(f"[red]No media manifest found for {src.id}. Run media-discover first.[/red]")
        raise typer.Exit(code=1)
    rows = transcribe_media(src, limit=limit, tool=tool, model=model, dry_run=dry_run, media_ids=media_id)
    statuses = {}
    for row in rows:
        statuses[row.get("transcript_status")] = statuses.get(row.get("transcript_status"), 0) + 1
    console.print_json(json.dumps({"source_id": src.id, "rows": len(rows), "statuses": statuses, "output_dir": str(MEDIA_DIR)}))


def media_batch(
    source: str = typer.Option(..., "--source", "-s"),
    limit: int = typer.Option(1, "--limit", min=1, help="Number of pending media rows to process."),
    media_id: Optional[list[str]] = typer.Option(None, "--media-id", help="Limit processing to one or more stable media IDs."),
    tool: str = typer.Option("auto", "--tool", help="auto, cloudflare, openai, mlx_whisper, parakeet, whisper-cli, or whisper."),
    model: str = typer.Option("auto", "--model"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview the next pending rows without writing transcripts or indexes."),
    skip_normalize: bool = typer.Option(False, "--skip-normalize", help="Do not rebuild transcript-derived private insight records after transcription."),
    skip_sidecars: bool = typer.Option(False, "--skip-sidecars", help="Do not rebuild private media sidecars/indexes after transcription."),
    min_transcript_chars: int = typer.Option(80, "--min-transcript-chars"),
) -> None:
    """Run a bounded private media transcription batch and refresh local media artifacts."""
    ensure_generated_dirs()
    src = get_source(source)
    if not media_manifest_path(src.id).exists():
        console.print(f"[red]No media manifest found for {src.id}. Run media-discover first.[/red]")
        raise typer.Exit(code=1)
    result = run_media_batch(
        src,
        limit=limit,
        tool=tool,
        model=model,
        dry_run=dry_run,
        normalize=not skip_normalize,
        sidecars=not skip_sidecars,
        min_transcript_chars=min_transcript_chars,
        media_ids=media_id,
    )
    console.print_json(json.dumps(result))


def media_doctor() -> None:
    """Report private media downloader/transcription tool readiness."""
    console.print_json(json.dumps(media_tool_status()))


def media_understanding_benchmark(
    tool: str = typer.Option("gemma4-12b", "--tool", help="Experimental media understanding tool name."),
    include_media_url: bool = typer.Option(False, "--include-media-url", help="Include direct media URLs in the private benchmark artifact."),
) -> None:
    """Build a private benchmark plan for optional audio/video understanding tools."""
    ensure_generated_dirs()
    result = build_media_understanding_benchmark(load_sources(), tool=tool, include_media_url=include_media_url)
    console.print_json(json.dumps(result))


def media_understanding_prepare(
    tool: str = typer.Option("gemma4-12b", "--tool", help="Experimental media understanding tool name."),
    seconds: int = typer.Option(30, "--seconds", min=5, max=300, help="Seconds of audio to extract per benchmark item."),
    manifest_path: Path = typer.Option(
        Path("data/tmp/gemma-benchmark/clip-manifest.json"),
        "--manifest-path",
        help="Private clip/frame manifest path for the Ollama run.",
    ),
) -> None:
    """Prepare private audio clips and video frames for the Gemma benchmark run."""
    ensure_generated_dirs()
    result = prepare_media_understanding_benchmark_assets(
        load_sources(),
        tool=tool,
        seconds=seconds,
        manifest_path=manifest_path,
    )
    console.print_json(json.dumps(result))


def media_understanding_run_ollama(
    model: str = typer.Option("gemma4:12b", "--model", help="Ollama model name."),
    manifest_path: Path = typer.Option(
        Path("data/tmp/gemma-benchmark/clip-manifest.json"),
        "--manifest-path",
        help="Private clip/frame manifest produced for the benchmark run.",
    ),
    endpoint: str = typer.Option("http://127.0.0.1:11434/api/chat", "--endpoint", help="Ollama chat endpoint."),
    output_path: Path = typer.Option(
        REVIEW_DIR / "media-understanding-benchmarks" / "gemma4-12b-ollama-run.json",
        "--output-path",
        help="Private benchmark run output path.",
    ),
    include_transcript_excerpt: bool = typer.Option(
        True,
        "--include-transcript-excerpt/--no-transcript-excerpt",
        help="Include private transcript excerpts as comparison grounding.",
    ),
) -> None:
    """Run Gemma 4 through Ollama against prepared private media benchmark clips."""
    ensure_generated_dirs()
    result = run_ollama_media_understanding_benchmark(
        model=model,
        manifest_path=manifest_path,
        endpoint=endpoint,
        output_path=output_path,
        include_transcript_excerpt=include_transcript_excerpt,
    )
    console.print_json(json.dumps(result))


def media_report(source: Optional[list[str]] = typer.Option(None, "--source", "-s")) -> None:
    """Report private media queue, transcript, and distilled insight counts."""
    selected = set(source or [])
    rows = []
    for src in load_sources():
        if selected and src.id not in selected:
            continue
        if src.kind == "podcast_rss" or "media_discovery" in src.preferred_tooling or "local_transcription" in src.preferred_tooling:
            rows.append(media_status_report(src))
    if selected:
        found = {row["source_id"] for row in rows}
        missing = selected - found
        if missing:
            console.print(f"[red]No media-capable source IDs found: {', '.join(sorted(missing))}[/red]")
            raise typer.Exit(code=1)
    console.print_json(json.dumps(rows))


def media_prune_dry_runs(source: Optional[list[str]] = typer.Option(None, "--source", "-s")) -> None:
    """Remove stale dry-run transcript rows from private transcript indexes."""
    ensure_generated_dirs()
    selected = set(source or [])
    rows = []
    for src in load_sources():
        if selected and src.id not in selected:
            continue
        if src.kind == "podcast_rss" or "media_discovery" in src.preferred_tooling or "local_transcription" in src.preferred_tooling:
            rows.append(prune_dry_run_transcript_rows(src))
    if selected:
        found = {row["source_id"] for row in rows}
        missing = selected - found
        if missing:
            console.print(f"[red]No media-capable source IDs found: {', '.join(sorted(missing))}[/red]")
            raise typer.Exit(code=1)
    console.print_json(json.dumps(rows))


def media_queue(
    source: Optional[list[str]] = typer.Option(None, "--source", "-s"),
    limit: Optional[int] = typer.Option(None, "--limit", min=1),
) -> None:
    """Build a private prioritized transcription queue across media-capable sources."""
    ensure_generated_dirs()
    selected = set(source or [])
    sources = [
        src
        for src in load_sources()
        if (not selected or src.id in selected)
        and (src.kind == "podcast_rss" or "media_discovery" in src.preferred_tooling or "local_transcription" in src.preferred_tooling)
    ]
    if selected:
        found = {src.id for src in sources}
        missing = selected - found
        if missing:
            console.print(f"[red]No media-capable source IDs found: {', '.join(sorted(missing))}[/red]")
            raise typer.Exit(code=1)
    result = build_media_priority_queue(sources, limit=limit)
    result["queue_path"] = str(media_priority_queue_path())
    result["report_path"] = str(media_priority_report_path())
    console.print_json(json.dumps(result))


def media_normalize(
    source: str = typer.Option(..., "--source", "-s"),
    min_transcript_chars: int = typer.Option(80, "--min-transcript-chars"),
) -> None:
    """Distill private transcript rows into normalized source-linked insight records."""
    ensure_generated_dirs()
    src = get_source(source)
    rows = build_media_insights(src, min_transcript_chars=min_transcript_chars)
    console.print(f"{src.id}: wrote {len(rows)} transcript-derived insight records to {media_insights_path(src.id)}")


def media_sidecars(source: str = typer.Option(..., "--source", "-s")) -> None:
    """Write private per-media Markdown sidecars and JSONL indexes for agent retrieval."""
    ensure_generated_dirs()
    src = get_source(source)
    if not media_manifest_path(src.id).exists():
        console.print(f"[red]No media manifest found for {src.id}. Run media-discover first.[/red]")
        raise typer.Exit(code=1)
    result = build_media_sidecars(src)
    console.print_json(json.dumps(result))


def media_public_candidates(
    source: Optional[str] = typer.Option(None, "--source", "-s"),
    all_sources: bool = typer.Option(False, "--all-sources", help="Build candidates for every transcribed media source."),
    min_transcript_chars: int = typer.Option(80, "--min-transcript-chars"),
) -> None:
    """Build reviewable public episode-note candidates without raw transcript text."""
    ensure_generated_dirs()
    if all_sources:
        results = []
        for src in media_review_sources(load_sources()):
            rows = build_media_public_candidates(src, min_transcript_chars=min_transcript_chars)
            results.append({"source_id": src.id, "candidate_count": len(rows), "candidate_path": str(media_public_candidates_path(src.id))})
        console.print_json(json.dumps({"sources": len(results), "results": results}))
        return
    if not source:
        console.print("[red]Provide --source or --all-sources.[/red]")
        raise typer.Exit(code=1)
    src = get_source(source)
    rows = build_media_public_candidates(src, min_transcript_chars=min_transcript_chars)
    console.print(f"{src.id}: wrote {len(rows)} media public-summary candidates to {media_public_candidates_path(src.id)}")


def media_review_status(source: Optional[list[str]] = typer.Option(None, "--source", "-s")) -> None:
    """Report transcript candidate/review coverage by media source and affected concept."""
    ensure_generated_dirs()
    sources = [get_source(value) for value in source] if source else media_review_sources(load_sources())
    console.print_json(json.dumps(media_review_status_report(sources)))


def media_public_draft_rewrites(
    source: Optional[str] = typer.Option(None, "--source", "-s"),
    all_sources: bool = typer.Option(False, "--all-sources", help="Draft rewrites for every transcribed media source."),
    candidate_id: Optional[list[str]] = typer.Option(None, "--candidate-id"),
    include_approved: bool = typer.Option(False, "--include-approved", help="Also regenerate rows for already approved candidates."),
    max_insights: int = typer.Option(3, "--max-insights"),
) -> None:
    """Draft transcript-backed public rewrite rows without raw transcript text."""
    ensure_generated_dirs()
    sources = media_review_sources(load_sources()) if all_sources else [get_source(source)] if source else []
    if not sources:
        console.print("[red]Provide --source or --all-sources.[/red]")
        raise typer.Exit(code=1)
    results = []
    for src in sources:
        try:
            result = build_media_public_rewrite_drafts(
                src,
                candidate_ids=candidate_id if len(sources) == 1 else None,
                pending_only=not include_approved,
                max_insights=max_insights,
            )
        except (FileNotFoundError, ValueError) as exc:
            console.print(f"[red]{src.id}: {exc}[/red]")
            raise typer.Exit(code=1) from exc
        results.append(result)
    console.print_json(json.dumps({"sources": len(results), "results": results}))


def candidate_ids_from_file(path: Path) -> list[str]:
    """Read candidate IDs from a JSONL rewrite file or newline-delimited ID file."""
    ids: list[str] = []
    seen: set[str] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        value = line.strip()
        if not value:
            continue
        if value.startswith("{"):
            try:
                row = json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number} is not valid JSON") from exc
            value = str(row.get("candidate_id") or row.get("id") or "").strip()
            if not value:
                raise ValueError(f"{path}:{line_number} JSON row is missing candidate_id")
        if value not in seen:
            ids.append(value)
            seen.add(value)
    return ids


def media_public_promote(
    source: str = typer.Option(..., "--source", "-s"),
    candidate_id: Optional[list[str]] = typer.Option(None, "--candidate-id"),
    candidate_id_file: Optional[Path] = typer.Option(
        None,
        "--candidate-id-file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="JSONL rewrite file or newline-delimited file containing candidate IDs to promote.",
    ),
    all_candidates: bool = typer.Option(False, "--all", help="Promote every candidate for the source."),
    review_status: str = typer.Option("approved_for_public_distillation", "--review-status"),
    reviewer: str = typer.Option("local-review", "--reviewer"),
    concept_id: Optional[list[str]] = typer.Option(None, "--concept-id"),
    rewrite_file: Optional[Path] = typer.Option(
        None,
        "--rewrite-file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="JSONL reviewer rewrite rows keyed by candidate_id. Required for placeholder candidates.",
    ),
    review_model: Optional[str] = typer.Option(None, "--review-model", help="Exact model ID used for the rewrite."),
    prompt_id: Optional[str] = typer.Option(None, "--prompt-id", help="Versioned prompt identifier used for the rewrite."),
    prompt_version: Optional[str] = typer.Option(None, "--prompt-version", help="Prompt version used for the rewrite."),
    review_method: Optional[str] = typer.Option(None, "--review-method", help="Review method, such as agent_reviewed_whole_source."),
) -> None:
    """Promote reviewed media transcript candidates into public-safe insight rows."""
    ensure_generated_dirs()
    src = get_source(source)
    try:
        selected_candidate_ids = list(candidate_id or [])
        if candidate_id_file:
            selected_candidate_ids.extend(candidate_ids_from_file(candidate_id_file))
        if not selected_candidate_ids:
            selected_candidate_ids = None
        rewrites = load_media_public_rewrites(rewrite_file) if rewrite_file else None
        provenance_values = [review_model, prompt_id, prompt_version, review_method]
        if any(provenance_values) and not all(provenance_values):
            raise ValueError(
                "--review-model, --prompt-id, --prompt-version, and --review-method must be provided together"
            )
        review_provenance = None
        if all(provenance_values):
            review_provenance = {
                "model": str(review_model),
                "prompt_id": str(prompt_id),
                "prompt_version": str(prompt_version),
                "method": str(review_method),
            }
        result = promote_media_public_candidates(
            src,
            candidate_ids=selected_candidate_ids,
            review_status=review_status,
            reviewer=reviewer,
            concept_ids=concept_id,
            promote_all=all_candidates,
            rewrites_by_candidate_id=rewrites,
            review_provenance=review_provenance,
        )
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print_json(json.dumps(result))
    console.print(f"{src.id}: promotions written to {media_public_promotions_path(src.id)}")


def build_claims_command() -> None:
    """Build the public approved claim graph from reviewed, public-safe promotions."""
    ensure_generated_dirs()
    try:
        result = build_approved_claims()
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print_json(json.dumps(result))


def validate_claims_command(
    path: Path = typer.Option(approved_claims_path(), "--path", exists=True, file_okay=True, dir_okay=False),
) -> None:
    """Validate a public claim JSONL file for schema, traceability, and private-data safety."""
    errors = validate_claim_file(path, public=True)
    if errors:
        for error in errors:
            console.print(f"[red]ERROR[/red] {error}")
        raise typer.Exit(code=1)
    console.print_json(json.dumps({"schema": "rock-kb-claim-validation-result-v1", "status": "ok", "path": str(path)}))


def claim_provenance_command(
    path: Path = typer.Option(approved_claims_path(), "--path", exists=True, file_okay=True, dir_okay=False),
) -> None:
    """Report which models, prompts, and methods produced approved claims."""
    console.print_json(json.dumps(claim_provenance_report(path)))


def claim_evaluation_sample_command(
    model: str = typer.Option(..., "--model", "-m"),
    sample_size: int = typer.Option(48, "--sample-size", min=1),
    output: Optional[Path] = typer.Option(None, "--output", file_okay=True, dir_okay=False),
    include_provenance: bool = typer.Option(
        False,
        "--include-provenance",
        help="Include claims that already record generation provenance.",
    ),
) -> None:
    """Build a private, source-context-backed sample for cross-model claim review."""
    result = build_claim_model_evaluation_sample(
        model=model,
        sample_size=sample_size,
        output_path=output,
        legacy_only=not include_provenance,
    )
    console.print_json(json.dumps(result))


def live_verification_plan() -> None:
    """Batch live-verification claim review rows into read-only probe groups."""
    ensure_generated_dirs()
    console.print_json(json.dumps(build_live_verification_probe_plan()))


def private_corpus_init(path: Path = typer.Option(..., "--path", file_okay=False, dir_okay=True)) -> None:
    """Initialize a portable private corpus checkout for ignored text/JSON artifacts."""
    result = initialize_private_corpus(path)
    console.print_json(json.dumps(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)


def private_corpus_validate(path: Path = typer.Option(..., "--path", file_okay=False, dir_okay=True)) -> None:
    """Validate a private corpus checkout structure."""
    result = validate_private_corpus(path)
    console.print_json(json.dumps(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)


def private_corpus_report(
    include_artifacts: bool = typer.Option(False, "--include-artifacts", help="Include every ignored artifact row instead of a bounded sample."),
    sample_limit: int = typer.Option(25, "--sample-limit", min=0),
) -> None:
    """Report ignored local artifacts that belong in the private corpus or object storage."""
    console.print_json(json.dumps(ignored_private_artifact_report(include_artifacts=include_artifacts, sample_limit=sample_limit)))


def private_corpus_sync(
    path: Path = typer.Option(..., "--path", file_okay=False, dir_okay=True),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """Copy ignored private text/JSON artifacts into a mounted private corpus checkout."""
    result = sync_private_text_artifacts(path, dry_run=dry_run)
    console.print_json(json.dumps(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)


def private_corpus_autosync(
    path: Path = typer.Option(..., "--path", file_okay=False, dir_okay=True),
    dry_run: bool = typer.Option(False, "--dry-run"),
    commit: bool = typer.Option(False, "--commit", help="Commit synced private corpus text artifacts in the corpus repo."),
) -> None:
    """Sync text artifacts, refresh media restore pointers, and optionally commit in the private corpus repo."""
    result = autosync_private_corpus(path, dry_run=dry_run, commit=commit)
    console.print_json(json.dumps(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)


def private_corpus_restore(
    path: Path = typer.Option(..., "--path", file_okay=False, dir_okay=True),
    dry_run: bool = typer.Option(False, "--dry-run"),
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite existing local ignored artifacts."),
) -> None:
    """Restore private text/JSON artifacts from a mounted private corpus checkout into this workspace."""
    result = restore_private_text_artifacts(path, dry_run=dry_run, overwrite=overwrite)
    console.print_json(json.dumps(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)


def private_corpus_media_manifest(path: Path = typer.Option(..., "--path", file_okay=False, dir_okay=True)) -> None:
    """Write a restore manifest for large media objects that should live outside normal git."""
    result = write_large_media_restore_manifest(path)
    console.print_json(json.dumps(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)


def private_corpus_audit(path: Optional[Path] = typer.Option(None, "--path", file_okay=False, dir_okay=True)) -> None:
    """Audit that private corpus data and private paths are absent from public artifacts."""
    result = audit_private_corpus_leaks(path)
    console.print_json(json.dumps(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)


def private_corpus_verify_rebuild(
    path: Path = typer.Option(..., "--path", file_okay=False, dir_okay=True),
    public_export_destination: Optional[Path] = typer.Option(
        None,
        "--public-export-destination",
        file_okay=False,
        dir_okay=True,
        help="Optional scratch destination for a public export rebuild check.",
    ),
) -> None:
    """Verify a mounted private corpus has portable rebuild inputs and public export still audits cleanly."""
    result = verify_private_corpus_rebuild(path, public_export_destination=public_export_destination)
    console.print_json(json.dumps(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)


def build_index() -> None:
    """Build the generated SQLite FTS index."""
    ensure_generated_dirs()
    path = build_sqlite_index()
    console.print(f"Built SQLite index at {path}")


def build_answer_pack_command() -> None:
    """Build generated answer, live checklist, review queue, and source conflict artifacts."""
    ensure_generated_dirs()
    console.print_json(json.dumps(build_agent_answer_pack()))


def build_concept_command(concept: str = typer.Option(..., "--concept", "-c")) -> None:
    """Build one generated concept guide and update dependency metadata."""
    ensure_generated_dirs()
    result = build_single_concept(concept)
    console.print_json(json.dumps(result))


def build_concepts_command() -> None:
    """Build all generated concept guides and dependency metadata."""
    ensure_generated_dirs()
    counts = build_all_concepts()
    console.print_json(json.dumps(counts))


def guide_refresh_plan() -> None:
    """Report concepts whose approved media dependencies require index rebuilds or guide refreshes."""
    ensure_generated_dirs()
    console.print_json(json.dumps(report_guide_refresh_plan()))


def refresh_guide_claims(
    concept: Optional[str] = typer.Option(None, "--concept", "-c", help="Refresh one concept guide instead of all long-form guides."),
) -> None:
    """Insert or update generated approved-claim coverage in long-form guides."""
    ensure_generated_dirs()
    console.print_json(json.dumps(refresh_long_form_approved_claims(concept)))


def synthesize_concept_command(
    concept: str = typer.Option(..., "--concept", "-c"),
    model: str = typer.Option("gpt-5.5", "--model", "-m"),
    limit: int = typer.Option(40, "--limit"),
    profile: str = typer.Option(
        "standard",
        "--profile",
        help="Synthesis profile: standard or comprehensive.",
    ),
    hydrate_sources: bool = typer.Option(
        False,
        "--hydrate-sources/--no-hydrate-sources",
        help="Refetch cited pages and public Rock source files into a bounded synthesis pack.",
    ),
    github_file_limit: int = typer.Option(18, "--github-file-limit"),
    max_page_chars: int = typer.Option(2600, "--max-page-chars"),
    max_code_chars: int = typer.Option(3200, "--max-code-chars"),
    include_contributions: bool = typer.Option(True, "--include-contributions/--no-include-contributions"),
    include_private_drafts: bool = typer.Option(False, "--include-private-drafts"),
    private_draft_path: Optional[list[Path]] = typer.Option(None, "--private-draft-path", exists=True, file_okay=True, dir_okay=False),
    codex_path: Optional[Path] = typer.Option(None, "--codex-path", exists=True, file_okay=True, dir_okay=False),
) -> None:
    """Use the local Codex login to write an authored concept guide draft."""
    ensure_generated_dirs()
    codex = str(codex_path or optional_command("codex") or "/Applications/Codex.app/Contents/Resources/codex")
    if not Path(codex).exists():
        console.print("[red]Codex CLI was not found. Pass --codex-path or install Codex CLI.[/red]")
        raise typer.Exit(code=1)

    pack = (
        hydrated_concept_synthesis_pack(
            concept,
            limit=limit,
            max_page_chars=max_page_chars,
            max_code_chars=max_code_chars,
            github_file_limit=github_file_limit,
            include_contributions=include_contributions,
            include_private_drafts=include_private_drafts,
            private_draft_paths=private_draft_path,
        )
        if hydrate_sources
        else concept_synthesis_pack(concept, limit=limit, include_contributions=include_contributions)
    )
    if include_private_drafts and not hydrate_sources:
        console.print("[red]--include-private-drafts requires --hydrate-sources so private records are written only to private hydrated packs.[/red]")
        raise typer.Exit(code=1)
    pack["synthesis_profile"] = profile
    review_dir = REVIEW_DIR / "concept-synthesis"
    review_dir.mkdir(parents=True, exist_ok=True)
    pack_suffix = "hydrated-source-pack" if hydrate_sources else "source-pack"
    prompt_suffix = "hydrated-prompt" if hydrate_sources else "prompt"
    pack_path = review_dir / f"{concept}.{pack_suffix}.json"
    prompt_path = review_dir / f"{concept}.{prompt_suffix}.md"
    output_path = synthesis_output_path(concept)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pack_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    prompt = concept_synthesis_prompt(pack)
    prompt_path.write_text(prompt, encoding="utf-8")

    result = subprocess.run(
        [
            codex,
            "exec",
            "-C",
            str(REPO_ROOT),
            "-m",
            model,
            "-s",
            "read-only",
            "-c",
            'approval_policy="never"',
            "--output-last-message",
            str(output_path),
            "-",
        ],
        input=prompt,
        text=True,
        capture_output=True,
        timeout=900,
    )
    row = {
        "concept_id": concept,
        "model": model,
        "profile": profile,
        "hydrate_sources": hydrate_sources,
        "returncode": result.returncode,
        "prompt_path": str(prompt_path),
        "source_pack_path": str(pack_path),
        "output_path": str(output_path),
        "stdout_preview": result.stdout[-4000:],
        "stderr_preview": result.stderr[-4000:],
        "created_at": now_iso(),
    }
    write_jsonl(review_dir / "runs.jsonl", [*read_jsonl(review_dir / "runs.jsonl"), row])
    if result.returncode != 0:
        console.print(f"[red]Codex synthesis failed with code {result.returncode}.[/red]")
        console.print(result.stderr[-4000:])
        raise typer.Exit(code=result.returncode)
    guide_intel = build_guide_intelligence(concept)
    console.print_json(json.dumps({"concept_id": concept, "model": model, "output_path": str(output_path), "guide_intel": guide_intel}))


def hydrate_concept_command(
    concept: str = typer.Option(..., "--concept", "-c"),
    limit: int = typer.Option(40, "--limit"),
    github_file_limit: int = typer.Option(18, "--github-file-limit"),
    max_page_chars: int = typer.Option(2600, "--max-page-chars"),
    max_code_chars: int = typer.Option(3200, "--max-code-chars"),
    include_contributions: bool = typer.Option(True, "--include-contributions/--no-include-contributions"),
    include_private_drafts: bool = typer.Option(False, "--include-private-drafts"),
    private_draft_path: Optional[list[Path]] = typer.Option(None, "--private-draft-path", exists=True, file_okay=True, dir_okay=False),
) -> None:
    """Build a bounded, source-hydrated pack for concept synthesis without running Codex."""
    ensure_generated_dirs()
    pack = hydrated_concept_synthesis_pack(
        concept,
        limit=limit,
        max_page_chars=max_page_chars,
        max_code_chars=max_code_chars,
        github_file_limit=github_file_limit,
        include_contributions=include_contributions,
        include_private_drafts=include_private_drafts,
        private_draft_paths=private_draft_path,
    )
    review_dir = REVIEW_DIR / "concept-synthesis"
    review_dir.mkdir(parents=True, exist_ok=True)
    pack_path = review_dir / f"{concept}.hydrated-source-pack.json"
    pack_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    console.print_json(
        json.dumps(
            {
                "concept_id": concept,
                "source_records": len(pack.get("source_records") or []),
                "hydrated_sources": len(pack.get("hydrated_sources") or []),
                "contribution_records": len(pack.get("contribution_records") or []),
                "private_draft_contribution_records": len(pack.get("private_draft_contribution_records") or []),
                "github_source_files": len(pack.get("github_source_files") or []),
                "pack_path": str(pack_path),
            }
        )
    )


def concept_synthesis_prompt(pack: dict) -> str:
    concept = pack["concept"]
    profile = str(pack.get("synthesis_profile") or "standard")
    hydrated_sources = pack.get("hydrated_sources") or []
    github_files = pack.get("github_source_files") or []
    contribution_records = pack.get("contribution_records") or []
    private_drafts = pack.get("private_draft_contribution_records") or []
    hydration_note = ""
    if hydrated_sources or github_files:
        hydration_note = (
            "This pack includes hydrated source excerpts and GitHub source-code snippets. "
            "Use those deeper records first, then use compact source records as coverage and citation metadata. "
            "Do not copy long passages from hydrated excerpts or source files.\n"
        )
    contribution_note = ""
    if contribution_records:
        contribution_note = (
            "This pack includes reviewed public contribution records. Treat them as community/org-derived examples, "
            "not official Rock guidance. Use them to identify operational patterns, and support important claims with official docs, release notes, source code, or live verification.\n"
        )
    private_note = ""
    if private_drafts:
        private_note = (
            "This pack includes private draft contribution records for local synthesis only. Do not quote them, cite them publicly, "
            "or treat them as public source material. Any guidance influenced by private drafts must be rewritten, source-supported with public links, "
            "and marked for live verification when appropriate.\n"
        )
    depth_note = ""
    required_sections = (
        "1. What This Is\n"
        "2. Mental Model\n"
        "3. Core Rock Areas And Entities\n"
        "4. Common Implementation Tasks\n"
        "5. Configuration And Operational Checklist\n"
        "6. Version And Release Caveats\n"
        "7. Troubleshooting Playbook\n"
        "8. Agent Playbook\n"
        "9. Source Map\n\n"
    )
    if profile == "comprehensive":
        depth_note = (
            "Write a comprehensive authoritative guide, not an overview. The target is a long-form concept manual "
            "that should be more detailed and more operationally useful than any single source page in the pack. "
            "Prefer 10,000-18,000 words when the source material supports it. Do not omit details merely to be concise. "
            "Integrate official docs, RockU, release notes, Model Map, developer docs, source-code snippets, and community examples into one coherent guide. "
            "Include precise configuration fields, entity relationships, implementation paths, version caveats, operational checks, and troubleshooting branches. "
            "When source material is thin, say what must be verified in a live Rock instance instead of inventing behavior.\n"
        )
        required_sections = comprehensive_required_sections(concept)
    return (
        "You are writing an original, agent-first Rock RMS concept guide from a machine-readable source pack.\n"
        "Do not copy long passages from sources. Write a transformative synthesis in your own words.\n"
        "Use citations as Markdown links to the provided source URLs. Prefer official/docs/RockU/source-code/model-map/release-note records over community Q&A/recipes.\n"
        + hydration_note
        + contribution_note
        + private_note
        + depth_note
        + "Output Markdown only. Do not mention that you are an AI. Do not run shell commands.\n\n"
        + "Required structure:\n"
        "---\n"
        f"id: authored-{concept['id']}\n"
        f"title: {concept['title']}\n"
        "generated: true\n"
        "guide_status: llm_generated_needs_review\n"
        "authority_level: draft\n"
        "reviewed_by:\n"
        "reviewed_at:\n"
        "---\n\n"
        f"# {concept['title']}\n\n"
        "Then include these sections:\n"
        + required_sections
        + "Keep it practical for agents doing real Rock work. Include specific source links inline.\n"
        "For facts that need verification in a live Rock instance, say what to inspect rather than pretending certainty.\n\n"
        "<source_pack_json>\n"
        + json.dumps(pack, ensure_ascii=False, indent=2)
        + "\n</source_pack_json>\n"
    )


def comprehensive_required_sections(concept: dict) -> str:
    title = str(concept["title"])
    subguides = concept.get("subguides") or []
    depends_on_topics = concept.get("depends_on_topics") or []
    sections = [
        "Executive Summary For Agents",
        "Scope And Terminology",
        f"{title} Mental Model",
        "Source Authority And How To Use This Guide",
        "Core Configuration And Data Model",
        "Primary Entities And Relationships",
        f"Common {title} Workflows",
    ]
    for subguide in subguides:
        sections.append(f"{subguide['title']} Deep Dive")
    if depends_on_topics:
        sections.append("Related Rock Areas: " + ", ".join(humanize_slug(topic) for topic in depends_on_topics))
    sections.extend(
        [
            "Administration And Operational Guardrails",
            "Developer, API, Lava, And Source-Code Landmarks",
            "Reporting, Analytics, And Model Map",
            "Version And Release Caveats",
            "Implementation Playbooks",
            "Troubleshooting Decision Tree",
            "Agent Task Recipes",
            "Source Map And Dependency Notes",
        ]
    )
    return "".join(f"{index}. {section}\n" for index, section in enumerate(sections, start=1)) + "\n"


def humanize_slug(value: str) -> str:
    return str(value).replace("-", " ").title()


def build_agent_pack_command() -> None:
    """Build generated agent navigation files."""
    ensure_generated_dirs()
    counts = build_agent_pack()
    console.print_json(json.dumps(counts))


def build_model_map_command(
    stable_path: Path = typer.Option(
        DEMO_MODEL_MAP_SCRAPE_PATH,
        "--stable-path",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Stable generic model-map raw artifact.",
    ),
    latest_path: Path = typer.Option(
        LATEST_MODEL_MAP_SCRAPE_PATH,
        "--latest-path",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Latest/upcoming generic model-map raw artifact.",
    ),
    skip_live_version_check: bool = typer.Option(
        False,
        "--skip-live-version-check",
        help="Allow rebuilding from local raw artifacts without comparing them to the live Rock version endpoints.",
    ),
) -> None:
    """Build generated public model-map resources from saved generic Rock Model Map artifacts."""
    ensure_generated_dirs()
    try:
        if not skip_live_version_check:
            freshness = model_map_scrape_freshness(stable_scrape_path=stable_path, latest_scrape_path=latest_path)
            if freshness.get("status") in {"stale", "missing"}:
                console.print_json(json.dumps(freshness))
                console.print(
                    "[red]ERROR[/red] Model-map raw artifacts are not current. "
                    "Run `uv run kb modelmap fetch --track both`, or use --skip-live-version-check for an explicit offline rebuild."
                )
                raise typer.Exit(code=1)
            if freshness.get("status") == "unknown":
                console.print_json(json.dumps(freshness))
                console.print("[yellow]WARNING[/yellow] Could not confirm live model-map versions; continuing with local raw artifacts.")
        result = build_model_map(stable_scrape_path=stable_path, latest_scrape_path=latest_path)
    except typer.Exit:
        raise
    except Exception as exc:
        console.print(f"[red]ERROR[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print_json(json.dumps(result))


def fetch_model_map_obsidian_command(
    stable_url: str = typer.Option(
        "https://rocksolidchurchdemo.com/admin/power-tools/model-map",
        "--stable-url",
        help="Stable/default Rock Model Map URL.",
    ),
    latest_url: str = typer.Option(
        "https://rockrmslatest.com/admin/power-tools/model-map",
        "--latest-url",
        help="Latest/pre-alpha Rock Model Map URL.",
    ),
    stable_output: Path = typer.Option(
        DEMO_MODEL_MAP_SCRAPE_PATH,
        "--stable-output",
        file_okay=True,
        dir_okay=False,
        help="Output path for the stable model-map raw artifact.",
    ),
    latest_output: Path = typer.Option(
        LATEST_MODEL_MAP_SCRAPE_PATH,
        "--latest-output",
        file_okay=True,
        dir_okay=False,
        help="Output path for the latest/pre-alpha model-map raw artifact.",
    ),
    username: str = typer.Option("admin", "--username", help="Rock login username for the generic demo sites."),
    password: str = typer.Option("admin", "--password", help="Rock login password for the generic demo sites."),
    concurrency: int = typer.Option(12, "--concurrency", min=1, max=64, help="Parallel GetModelDetails calls per track."),
    node_path: Optional[Path] = typer.Option(
        DEFAULT_MODEL_MAP_NODE_PATH,
        "--node-path",
        file_okay=False,
        dir_okay=True,
        help="Optional Node module directory containing Playwright.",
    ),
    track: str = typer.Option(
        "both",
        "--track",
        help="Which track to fetch: stable, latest, or both.",
    ),
) -> None:
    """Fetch model-map raw artifacts through authenticated Obsidian block-action calls."""
    selected = track.strip().lower()
    if selected not in {"stable", "latest", "both"}:
        console.print("[red]ERROR[/red] --track must be stable, latest, or both")
        raise typer.Exit(code=1)

    script_path = REPO_ROOT / "tools" / "model_map_obsidian_scrape.js"
    if not script_path.exists():
        console.print(f"[red]ERROR[/red] Missing model-map fetch script: {script_path}")
        raise typer.Exit(code=1)

    env = os.environ.copy()
    if node_path and node_path.exists():
        existing = env.get("NODE_PATH")
        env["NODE_PATH"] = f"{node_path}{os.pathsep}{existing}" if existing else str(node_path)

    jobs = []
    if selected in {"stable", "both"}:
        jobs.append(("stable", stable_url, stable_output))
    if selected in {"latest", "both"}:
        jobs.append(("latest", latest_url, latest_output))

    results = []
    for label, url, output in jobs:
        output.parent.mkdir(parents=True, exist_ok=True)
        command = [
            "node",
            str(script_path),
            "--url",
            url,
            "--output",
            str(output),
            "--track",
            label,
            "--username",
            username,
            "--password",
            password,
            "--concurrency",
            str(concurrency),
        ]
        proc = subprocess.run(command, cwd=REPO_ROOT, env=env, text=True, capture_output=True)
        if proc.returncode != 0:
            console.print(f"[red]ERROR[/red] Model-map fetch failed for {label}.")
            if proc.stdout.strip():
                console.print(proc.stdout.strip())
            if proc.stderr.strip():
                console.print(proc.stderr.strip())
            raise typer.Exit(code=proc.returncode)
        parsed = parse_trailing_json(proc.stdout)
        results.append(
            {
                "track": label,
                "url": url,
                "output": str(output),
                "models_jsonl": str(output.with_name(f"{output.stem}.models.jsonl")),
                "result": parsed,
            }
        )
    console.print_json(
        json.dumps(
            {
                "schema": "rock-kb-model-map-fetch-result-v1",
                "status": "ok",
                "collection_method": "obsidian_block_action",
                "tracks": results,
            }
        )
    )


def parse_trailing_json(output: str) -> Optional[dict[str, Any]]:
    text = output.strip()
    if not text:
        return None
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            parsed = json.loads(text[index:])
        except json.JSONDecodeError:
            continue
        return parsed if isinstance(parsed, dict) else None
    return None


def stamp_model_map_scrape_version_command(
    scrape_path: Path = typer.Option(
        DEMO_MODEL_MAP_SCRAPE_PATH,
        "--scrape-path",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Full demo model-map scrape artifact to stamp with Rock version metadata.",
    ),
    endpoint_url: str = typer.Option(
        DEMO_ROCK_VERSION_ENDPOINT,
        "--endpoint-url",
        help="Rock Utility endpoint that returns the semantic Rock version.",
    ),
    timeout_seconds: int = typer.Option(20, "--timeout-seconds", min=1, max=120),
) -> None:
    """Stamp a saved demo model-map scrape with the demo Rock version."""
    try:
        result = stamp_model_map_scrape_version(
            scrape_path=scrape_path,
            endpoint_url=endpoint_url,
            timeout_seconds=timeout_seconds,
        )
    except Exception as exc:
        console.print(f"[red]ERROR[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print_json(json.dumps(result))


def diff_model_map_scrapes_command(
    stable_path: Path = typer.Option(
        DEMO_MODEL_MAP_SCRAPE_PATH,
        "--stable-path",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Stable generic model-map scrape artifact.",
    ),
    latest_path: Path = typer.Option(
        LATEST_MODEL_MAP_SCRAPE_PATH,
        "--latest-path",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Latest/upcoming generic model-map scrape artifact.",
    ),
    output_path: Path = typer.Option(
        MODEL_MAP_VERSION_DIFF_PATH,
        "--output-path",
        file_okay=True,
        dir_okay=False,
        help="Summary diff JSON output path.",
    ),
    output_jsonl_path: Path = typer.Option(
        MODEL_MAP_VERSION_DIFF_JSONL_PATH,
        "--output-jsonl-path",
        file_okay=True,
        dir_okay=False,
        help="Per-change diff JSONL output path.",
    ),
) -> None:
    """Compare stable and latest generic Rock model-map scrapes."""
    try:
        result = build_model_map_version_diff(
            stable_path=stable_path,
            latest_path=latest_path,
            output_path=output_path,
            output_jsonl_path=output_jsonl_path,
        )
    except Exception as exc:
        console.print(f"[red]ERROR[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print_json(json.dumps(result))


def build_guide_intel_command(concept: str = typer.Option(..., "--concept", "-c")) -> None:
    """Build section maps, guide dependencies, task cards, release caveats, and guide quality metadata."""
    ensure_generated_dirs()
    result = build_guide_intelligence(concept)
    console.print_json(json.dumps(result))


def build_mobile_selector_audit_command() -> None:
    """Regenerate Rock Mobile selector audit resources from reviewed inventory and normalized sources."""
    ensure_generated_dirs()
    result = build_mobile_selector_audit()
    console.print_json(json.dumps(result))


def mobile_selector_audit_status_command() -> None:
    """Report whether Rock Mobile selector audit dependencies are current."""
    result = mobile_selector_audit_status()
    console.print_json(json.dumps(result))


def audit_guide_command(concept: str = typer.Option(..., "--concept", "-c")) -> None:
    """Fail if an authored concept guide is too shallow, under-cited, or missing required source families."""
    pack = read_latest_source_pack(concept)
    source_index = build_source_index(pack)
    guide_path = synthesis_output_path(concept)
    if not guide_path.exists():
        console.print(f"[red]No authored guide found at {guide_path}.[/red]")
        raise typer.Exit(code=1)
    guide_text = guide_path.read_text(encoding="utf-8")
    sections = parse_markdown_sections(guide_text)
    section_rows = section_source_map(concept, sections, source_index)
    task_cards = build_task_cards(concept, guide_text, section_rows, source_index)
    entity_rows = build_entity_rows(concept, guide_text, section_rows, task_cards, source_index)
    dependency = {
        "sources": [source for source in source_index.values() if any(source["source_key"] in row.get("source_keys", []) for row in section_rows)]
    }
    audit = audit_guide_quality(concept, guide_text, section_rows, dependency, task_cards, entity_rows)
    console.print_json(json.dumps(audit))
    if audit["status"] != "pass":
        raise typer.Exit(code=1)


def audit_licenses() -> None:
    """Fail if normalized records violate license/citation rules."""
    errors = audit_license_records()
    if errors:
        for error in errors:
            console.print(f"[red]ERROR[/red] {error}")
        raise typer.Exit(code=1)
    console.print("[green]License and citation audit passed.[/green]")


def audit_source_url_duplicates_command() -> None:
    """Fail if normalized sources duplicate URLs across unapproved source pairs."""
    errors = audit_duplicate_source_urls()
    if errors:
        for error in errors:
            console.print(f"[red]ERROR[/red] {error}")
        raise typer.Exit(code=1)
    console.print("[green]Source URL duplicate audit passed.[/green]")


def audit_rockumentation_api_coverage_command(
    probe_static: bool = typer.Option(False, "--probe-static", help="Live-probe static documentation/developer rows for Rockumentation API payloads."),
    max_static_probes: Optional[int] = typer.Option(None, "--max-static-probes", min=1, help="Limit live probes when using --probe-static."),
) -> None:
    """Fail if API-backed Rockumentation rows lack branch metadata."""
    result = audit_rockumentation_api_coverage(probe_static=probe_static, max_static_probes=max_static_probes)
    console.print_json(json.dumps(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)


def audit_source_policy_command() -> None:
    """Fail if source registry publish/private policy is inconsistent."""
    errors = audit_source_policy()
    if errors:
        for error in errors:
            console.print(f"[red]ERROR[/red] {error}")
        raise typer.Exit(code=1)
    console.print("[green]Source publish policy audit passed.[/green]")


def audit_public_export_command() -> None:
    """Fail if public export artifacts include raw/private data or disallowed fields."""
    errors = audit_source_policy()
    errors.extend(audit_public_export_manifest())
    if errors:
        for error in errors:
            console.print(f"[red]ERROR[/red] {error}")
        raise typer.Exit(code=1)
    console.print("[green]Public export audit passed.[/green]")


def audit_readiness(public_only: bool = typer.Option(False, "--public-only", help="Skip private-media corpus checks for CI environments without ignored private artifacts.")) -> None:
    """Report whether the KB meets the project goal and where evidence is still incomplete."""
    report = goal_readiness_report(include_private=not public_only)
    console.print_json(json.dumps(report))
    if report["status"] == "fail":
        raise typer.Exit(code=1)


def public_export(destination: Optional[Path] = typer.Option(None, "--destination", "-d", file_okay=False, dir_okay=True)) -> None:
    """Build a publishable distilled export that excludes private/raw working data."""
    ensure_generated_dirs()
    result = build_public_export(destination or PUBLIC_EXPORT_DIR)
    console.print_json(json.dumps(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)


def report_refresh() -> None:
    """Show source refresh status based on generated normalized records."""
    table = Table(title="Refresh Report")
    table.add_column("Source")
    table.add_column("Cadence")
    table.add_column("Records")
    table.add_column("Latest Retrieved")
    for source in load_sources():
        records = list(read_jsonl(source_output_path(source.id, "normalized")))
        latest = max([str(row.get("retrieved_at") or "") for row in records], default="")
        table.add_row(source.id, source.refresh_cadence, str(len(records)), latest)
    console.print(table)


def private_scan(
    repo: Path = typer.Option(..., "--repo", exists=True, file_okay=False, dir_okay=True),
    allowlist: Optional[Path] = typer.Option(None, "--allowlist", exists=True, file_okay=True, dir_okay=False),
    source_id: str = typer.Option("private_rock_repo_candidates", "--source-id"),
    org_id: str = typer.Option("local", "--org-id"),
) -> None:
    """Scan a private repo into a sanitized review queue."""
    ensure_generated_dirs()
    records = scan_private_repo(repo, allowlist, source_id=source_id, org_id=org_id)
    output = REVIEW_DIR / f"private-scan-{repo.name}.jsonl"
    count = write_jsonl(output, records)
    console.print(f"Wrote {count} private scan records to {output}")


def private_ingest(
    repo: Path = typer.Option(..., "--repo", exists=True, file_okay=False, dir_okay=True),
    allowlist: Optional[Path] = typer.Option(None, "--allowlist", exists=True, file_okay=True, dir_okay=False),
    source_id: str = typer.Option("private_rock_repo_candidates", "--source-id"),
    org_id: str = typer.Option("local", "--org-id"),
) -> None:
    """Ingest an approved private/local repo into the private review queue without public export."""
    ensure_generated_dirs()
    records = scan_private_repo(repo, allowlist, source_id=source_id, org_id=org_id)
    output = REVIEW_DIR / f"private-ingest-{repo.name}.jsonl"
    count = write_jsonl(output, records)
    blocked = sum(1 for record in records if str(record.get("publishability_status", "")).startswith("blocked"))
    console.print_json(json.dumps({"records": count, "blocked": blocked, "output": str(output)}))


def contribution_validate(path: Optional[Path] = typer.Option(None, "--path", exists=True, file_okay=True, dir_okay=True)) -> None:
    """Validate public outside-org contribution bundles for schema, traceability, and privacy."""
    if path is None:
        paths = contribution_paths()
    elif path.is_dir():
        paths = contribution_paths(path)
    else:
        paths = [path]
    errors = validate_contribution_paths(paths)
    if errors:
        for error in errors:
            console.print(f"[red]ERROR[/red] {error}")
        raise typer.Exit(code=1)
    console.print_json(json.dumps({"status": "ok", "files": len(paths)}))


def contribution_check(path: Optional[Path] = typer.Option(None, "--path", exists=True, file_okay=True, dir_okay=True)) -> None:
    """Run the contributor-facing bundle checks and summarize public contribution rows."""
    report = contribution_check_report(path)
    console.print_json(json.dumps(report))
    if report["status"] != "ok":
        raise typer.Exit(code=1)


def source_scan_command(
    output_dir: Path = typer.Option(DEFAULT_SOURCE_SCAN_DIR, "--output-dir", file_okay=False, dir_okay=True),
    baseline_snapshot: Optional[Path] = typer.Option(None, "--baseline-snapshot", exists=True, file_okay=True, dir_okay=False),
    snapshot_output: Optional[Path] = typer.Option(None, "--snapshot-output", file_okay=True, dir_okay=False),
    source_status: Optional[Path] = typer.Option(None, "--source-status", exists=True, file_okay=True, dir_okay=False),
) -> None:
    """Compare current registered source artifacts to a prior source snapshot and write scan reports."""
    report = build_source_scan_report(
        output_dir=output_dir,
        baseline_snapshot_path=baseline_snapshot,
        snapshot_output_path=snapshot_output,
        source_status_path=source_status,
    )
    console.print_json(json.dumps(report["summary"]))


def rebuild_plan_command(
    scan_report: Path = typer.Option(
        DEFAULT_SOURCE_SCAN_DIR / "source-scan-report.json",
        "--scan-report",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    output_dir: Path = typer.Option(DEFAULT_REBUILD_PLAN_DIR, "--output-dir", file_okay=False, dir_okay=True),
) -> None:
    """Create a deterministic/reviewer rebuild plan from a source-scan report."""
    plan = build_rebuild_plan(scan_report_path=scan_report, output_dir=output_dir)
    console.print_json(json.dumps(plan["summary"]))


def refresh_dashboard_command(
    scan_report: Path = typer.Option(
        DEFAULT_SOURCE_SCAN_DIR / "source-scan-report.json",
        "--scan-report",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    rebuild_plan: Path = typer.Option(
        DEFAULT_REBUILD_PLAN_DIR / "rebuild-plan-report.json",
        "--rebuild-plan",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    evaluation_report: Path = typer.Option(
        AGENT_DIR / "evaluation-report.json",
        "--evaluation-report",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    output_dir: Path = typer.Option(DEFAULT_REFRESH_DASHBOARD_DIR, "--output-dir", file_okay=False, dir_okay=True),
) -> None:
    """Build a maintainer dashboard from source scan, rebuild plan, and answer evaluation state."""
    dashboard = build_refresh_dashboard(
        scan_report_path=scan_report,
        rebuild_plan_path=rebuild_plan,
        evaluation_report_path=evaluation_report,
        output_dir=output_dir,
    )
    console.print_json(json.dumps(dashboard["summary"]))


def contribution_new(
    org_id: str = typer.Option(..., "--org-id"),
    org_display_name: Optional[str] = typer.Option(None, "--org-display-name"),
    root: Optional[Path] = typer.Option(None, "--root", file_okay=False, dir_okay=True),
    overwrite: bool = typer.Option(False, "--overwrite"),
) -> None:
    """Create a starter outside-org contribution folder with a non-public example bundle."""
    try:
        output = create_contribution_template(org_id, root=root, org_display_name=org_display_name, overwrite=overwrite)
    except ValueError as exc:
        console.print(f"[red]ERROR[/red] {exc}")
        raise typer.Exit(code=1) from exc
    except FileExistsError as exc:
        console.print(f"[red]ERROR[/red] {exc.filename} already exists. Use --overwrite to replace it.")
        raise typer.Exit(code=1) from exc
    console.print_json(json.dumps({"status": "created", "org_id": org_id, "output": str(output), "validated_by_default": False}))


def distill_private(
    scan_path: Path = typer.Option(..., "--scan-path", exists=True, file_okay=True, dir_okay=False),
    source_id: str = typer.Option(..., "--source-id"),
    concept: str = typer.Option(..., "--concept"),
    org_id: str = typer.Option("local", "--org-id"),
    limit: Optional[int] = typer.Option(None, "--limit"),
    output: Optional[Path] = typer.Option(None, "--output", file_okay=True, dir_okay=False),
    dependency_output: Optional[Path] = typer.Option(None, "--dependency-output", file_okay=True, dir_okay=False),
) -> None:
    """Create private draft contribution rows from reviewed generalizable private scan records."""
    ensure_generated_dirs()
    rows = distill_private_scan(
        scan_path,
        source_id=source_id,
        concept_id=concept,
        org_id=org_id,
        output_path=output,
        dependency_output_path=dependency_output,
        limit=limit,
    )
    output_path = output or private_distill_path(source_id, concept)
    dependency_path = dependency_output or private_dependency_path(source_id, concept)
    console.print_json(json.dumps({"records": len(rows), "output": str(output_path), "dependency_output": str(dependency_path), "status": "private_draft"}))


def private_review_report_command(
    scan_path: Path = typer.Option(..., "--scan-path", exists=True, file_okay=True, dir_okay=False),
    source_id: Optional[str] = typer.Option(None, "--source-id"),
    org_id: Optional[str] = typer.Option(None, "--org-id"),
) -> None:
    """Summarize a private scan manifest without exposing private paths or source text."""
    console.print_json(json.dumps(private_review_report(scan_path, source_id=source_id, org_id=org_id)))


def contribution_promote(
    draft_path: Path = typer.Option(..., "--draft-path", exists=True, file_okay=True, dir_okay=False),
    org_id: str = typer.Option(..., "--org-id"),
    output: Optional[Path] = typer.Option(None, "--output", file_okay=True, dir_okay=False),
    rewrite_file: Optional[Path] = typer.Option(None, "--rewrite-file", exists=True, file_okay=True, dir_okay=False),
    reviewed: bool = typer.Option(False, "--reviewed"),
    redaction_attestation: bool = typer.Option(False, "--redaction-attestation"),
    license_attestation: bool = typer.Option(False, "--license-attestation"),
    contribution_id: Optional[list[str]] = typer.Option(None, "--contribution-id"),
    concept: Optional[str] = typer.Option(None, "--concept"),
    limit: Optional[int] = typer.Option(None, "--limit"),
    append: bool = typer.Option(False, "--append"),
    review_status: str = typer.Option("redaction_reviewed", "--review-status"),
) -> None:
    """Promote private draft rows into a staging skeleton or reviewed public bundle."""
    ensure_generated_dirs()
    try:
        result = promote_private_contributions(
            draft_path,
            org_id=org_id,
            output_path=output,
            rewrite_path=rewrite_file,
            reviewed=reviewed,
            redaction_attestation=redaction_attestation,
            license_attestation=license_attestation,
            contribution_ids=contribution_id,
            concept_id=concept,
            limit=limit,
            append=append,
            review_status=review_status,
        )
    except ValueError as exc:
        console.print(f"[red]ERROR[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print_json(json.dumps(result))


def private_stale(
    scan_path: Path = typer.Option(..., "--scan-path", exists=True, file_okay=True, dir_okay=False),
    source_id: str = typer.Option(..., "--source-id"),
    concept: str = typer.Option(..., "--concept"),
    dependency_path: Optional[Path] = typer.Option(None, "--dependency-path", exists=True, file_okay=True, dir_okay=False),
) -> None:
    """Report private distilled rows whose private source hashes changed or disappeared."""
    path = dependency_path or private_dependency_path(source_id, concept)
    if not path.exists():
        console.print(f"[red]No private dependency file found at {path}.[/red]")
        raise typer.Exit(code=1)
    rows = report_private_staleness(scan_path, path)
    stale = sum(1 for row in rows if row.get("needs_rebuild"))
    console.print_json(json.dumps({"records": len(rows), "stale": stale, "dependency_path": str(path), "rows": rows}))


def private_impact(
    scan_path: Path = typer.Option(..., "--scan-path", exists=True, file_okay=True, dir_okay=False),
    dependency_path: Optional[Path] = typer.Option(None, "--dependency-path", exists=True, file_okay=True, dir_okay=True),
    source_id: Optional[str] = typer.Option(None, "--source-id"),
    org_id: Optional[str] = typer.Option(None, "--org-id"),
) -> None:
    """Report public concepts and artifacts affected by changed private source hashes."""
    console.print_json(json.dumps(report_private_impact(scan_path, dependency_path=dependency_path, source_id=source_id, org_id=org_id)))


def _fetch_github_repo_record(src):
    repo = src.raw.get("repo")
    if not repo:
        return normalize_raw_record(src, {"source_url": src.root_url, "source_title": src.name})
    api_url = f"https://api.github.com/repos/{repo}"
    with httpx.Client(timeout=30) as client:
        response = client.get(api_url, headers={"Accept": "application/vnd.github+json"})
    response.raise_for_status()
    return normalize_github_repo_metadata(src, response.json())


def _summarize_with_llm(llm_path: str, model: str, record: dict) -> str:
    prompt = (
        "Summarize this Rock RMS knowledge record in 2 concise sentences. "
        "Preserve version, module, risk, and source caveats when present.\n\n"
        + json.dumps(record, ensure_ascii=False)
    )
    result = subprocess.run(
        [llm_path, "-m", model, prompt],
        check=False,
        text=True,
        capture_output=True,
        timeout=120,
    )
    if result.returncode != 0:
        return record.get("summary") or ""
    return result.stdout.strip()
