#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


CONTRIBUTION_TYPES = {
    "task_card",
    "troubleshooting_pattern",
    "release_caveat",
    "entity_note",
    "guide_section",
    "source_link",
    "open_question",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a public-safe community contribution JSONL row."
    )
    parser.add_argument("--org-id", required=True, help="Stable folder-safe org id, such as oneall or example-org.")
    parser.add_argument("--org-name", required=True, help="Public display name for the contributing org.")
    parser.add_argument("--concept", action="append", required=True, help="KB concept id. Repeat for multiple concepts.")
    parser.add_argument("--type", required=True, choices=sorted(CONTRIBUTION_TYPES), help="Contribution type.")
    parser.add_argument("--title", required=True, help="Short public-safe title.")
    parser.add_argument("--summary", required=True, help="Original public-safe distilled guidance.")
    parser.add_argument("--source-url", action="append", default=[], help="Public source URL. Repeat for multiple URLs.")
    parser.add_argument("--source-record-id", action="append", default=[], help="Existing KB source record id. Repeat for multiple ids.")
    parser.add_argument("--confidence", default="needs_review", choices=["low", "medium", "high", "needs_review"])
    parser.add_argument("--needs-live-verification", action="store_true", help="Use when local config, plugins, custom code, or versions may change behavior.")
    parser.add_argument("--redaction-reviewed", action="store_true", help="Confirms private details were removed.")
    parser.add_argument("--license-attested", action="store_true", help="Confirms you have rights to submit this original summary and sources.")
    parser.add_argument("--output", help="Optional output JSONL path. Defaults to community-contributions/<org-id>/bundle-<timestamp>.jsonl.")
    args = parser.parse_args()

    org_id = slug(args.org_id)
    if org_id != args.org_id:
        raise SystemExit(f"--org-id must already be folder-safe. Suggested value: {org_id}")
    if not args.source_url and not args.source_record_id:
        raise SystemExit("Add at least one --source-url or --source-record-id.")
    if not args.redaction_reviewed:
        raise SystemExit("Add --redaction-reviewed only after private details have been removed.")
    if not args.license_attested:
        raise SystemExit("Add --license-attested only when you have rights to submit this summary and sources.")

    created_at = datetime.now(timezone.utc).replace(microsecond=0)
    timestamp = created_at.strftime("%Y%m%dT%H%M%SZ")
    title_slug = slug(args.title)[:48].strip("-") or "contribution"
    output = Path(args.output) if args.output else Path("community-contributions") / org_id / f"bundle-{timestamp}.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)

    row = {
        "schema": "rock-kb-org-contribution-v1",
        "contribution_id": f"{org_id}:{title_slug}-{timestamp.lower().removesuffix('z')}",
        "org_id": org_id,
        "org_display_name": args.org_name,
        "contribution_type": args.type,
        "concept_ids": args.concept,
        "title": args.title,
        "distilled_summary": args.summary,
        "source_urls": args.source_url,
        "source_record_ids": args.source_record_id,
        "confidence": args.confidence,
        "review_status": "approved_for_public_distillation",
        "needs_live_verification": bool(args.needs_live_verification),
        "redaction_attestation": True,
        "license_attestation": True,
        "created_at": created_at.isoformat().replace("+00:00", "Z"),
    }

    mode = "a" if output.exists() else "w"
    with output.open(mode, encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"Wrote {output}")
    print(f"Validate with: python3 scripts/validate_bundle.py {output.parent}")
    return 0


def slug(value: str) -> str:
    lowered = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9_-]+", "-", lowered)
    normalized = re.sub(r"-+", "-", normalized)
    return normalized.strip("-")


if __name__ == "__main__":
    raise SystemExit(main())
