# Reviewed Rock Issue Intelligence

The generated upstream catalog lives in `agent/rock-issues.jsonl`. This directory is reserved for reviewed public-safe enrichments that add evidence-backed diagnosis, applicability, or workaround knowledge.

Do not copy issue bodies, comments, screenshots, attachments, private instance evidence, or agent transcripts here. A reviewed enrichment must use `rock-kb-rock-issue-enrichment-v1`, cite public evidence, distinguish hypothesis from confirmed cause, include redaction and license attestations, and pass the normal public export audit.

Private church evidence stays in a permission-scoped overlay and is never merged into this public directory.

Only `approved_for_public_distillation` JSON records belong here. Drafts, worker outputs, screenshots, and investigation packets stay under ignored `data/review/rock-issues/`. Run `uv run kb issues sync --timeline-backfill-limit 0` to validate and project approved records into `agent/rock-issue-enrichments.jsonl`.
