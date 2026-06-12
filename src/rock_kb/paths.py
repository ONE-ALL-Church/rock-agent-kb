from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_DIR = REPO_ROOT / "sources"
CONCEPTS_DIR = REPO_ROOT / "concepts"
DATA_DIR = REPO_ROOT / "data"
CLAIMS_DIR = REPO_ROOT / "claims"
RAW_MANIFEST_DIR = DATA_DIR / "raw-manifests"
NORMALIZED_DIR = DATA_DIR / "normalized"
INDEX_DIR = DATA_DIR / "index"
REVIEW_DIR = DATA_DIR / "review"
MEDIA_DIR = DATA_DIR / "media"
PUBLIC_EXPORT_DIR = DATA_DIR / "public-export"
KNOWLEDGE_DIR = REPO_ROOT / "knowledge"
AGENT_DIR = REPO_ROOT / "agent"
DOCS_DIR = REPO_ROOT / "docs"


def ensure_generated_dirs() -> None:
    for path in [
        RAW_MANIFEST_DIR,
        CLAIMS_DIR,
        NORMALIZED_DIR,
        INDEX_DIR,
        REVIEW_DIR,
        MEDIA_DIR,
        PUBLIC_EXPORT_DIR,
        KNOWLEDGE_DIR,
        CONCEPTS_DIR,
        AGENT_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def source_output_path(source_id: str, kind: str) -> Path:
    base = RAW_MANIFEST_DIR if kind == "raw" else NORMALIZED_DIR
    return base / f"{source_id}.jsonl"
