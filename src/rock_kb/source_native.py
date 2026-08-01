from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Iterable

import httpx
from markdownify import markdownify as html_to_markdown

from .community import (
    clean_rockumentation_markdown,
    fetch_rockumentation_payload,
    rockumentation_article_soup,
)
from .document_claims import build_document_claim_candidates
from .extract import USER_AGENT, now_iso, sha256_text
from .jsonl import read_jsonl, write_jsonl
from .paths import REPO_ROOT, REVIEW_DIR
from .schemas import (
    EvidenceLink,
    GenerationActivity,
    KnowledgeRelationship,
    KnowledgeUnit,
    ReviewedSourceNativeArtifact,
    SourceLocator,
    SourceNativeDistillationOutput,
    SourceNativePilotManifest,
    SourceNativeVerificationQueueItem,
    SourceSnapshot,
    SourceUnit,
)


SOURCE_NATIVE_PILOT_DIR = REPO_ROOT / "canonical" / "source-native" / "v1"
SOURCE_NATIVE_REVIEW_DIR = REVIEW_DIR / "source-native-pilot"
SOURCE_NATIVE_PROMPT_ID = "source-knowledge-distillation-v2.3"
SOURCE_NATIVE_PROMPT_VERSION = "2.3.1"
SOURCE_NATIVE_INPUT_HASH_VERSION = "2"
SOURCE_NATIVE_PROMPT_PATH = (
    REPO_ROOT
    / "docs"
    / "prompts"
    / "source-knowledge-distillation-v2.3.md"
)
SOURCE_NATIVE_SCHEMA_PATH = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "source-knowledge-distillation-v2.3.schema.json"
)
SOURCE_NATIVE_SPLIT_RULES_PATH = (
    REPO_ROOT / "canonical" / "source-native" / "v1" / "split-rules.jsonl"
)
SOURCE_NATIVE_PILOT_CONCEPTS = ("system-admin-ops", "check-in")
SOURCE_NATIVE_PILOT_LIMIT_PER_CONCEPT = 6
PILOT_FILE_NAMES = (
    "source-snapshots.jsonl",
    "source-units.jsonl",
    "generation-activities.jsonl",
    "reviewed-artifacts.jsonl",
    "relationships.jsonl",
    "evaluation-set.jsonl",
    "evaluation-holdout.jsonl",
    "verification-queue.jsonl",
    "split-rules.jsonl",
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
ORDERED_LIST_RE = re.compile(r"^\s*\d+[.)]\s+")
UNORDERED_LIST_RE = re.compile(r"^\s*[-*+]\s+")
TABLE_SEPARATOR_RE = re.compile(
    r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?\s*$"
)


def rockumentation_markdown(payload: Any) -> str:
    article = rockumentation_article_soup(payload)
    if not article:
        return ""
    for selector in (
        "script",
        "style",
        "noscript",
        "svg",
        ".js-menu-container",
        ".article-edit-panel",
    ):
        for node in article.select(selector):
            node.decompose()
    markdown = html_to_markdown(str(article), heading_style="ATX").strip()
    return normalize_markdown(clean_rockumentation_markdown(markdown))


def write_source_native_distillation_schema(
    destination: Path = SOURCE_NATIVE_SCHEMA_PATH,
) -> dict[str, Any]:
    schema = SourceNativeDistillationOutput.model_json_schema(by_alias=True)
    make_strict_response_schema(schema)
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "schema": "rock-kb-source-native-schema-build-v1",
        "status": "ok",
        "destination": str(destination),
        "sha256": sha256_file(destination),
    }


def make_strict_response_schema(node: Any) -> None:
    if isinstance(node, dict):
        node.pop("default", None)
        properties = node.get("properties")
        if isinstance(properties, dict):
            node["required"] = list(properties)
            node["additionalProperties"] = False
        for value in node.values():
            make_strict_response_schema(value)
    elif isinstance(node, list):
        for value in node:
            make_strict_response_schema(value)


def write_source_native_generation_prompt(
    *,
    input_path: Path,
    destination: Path,
    concept_id: str | None = None,
    candidate_id: str | None = None,
    source_record_id: str | None = None,
    offset: int = 0,
    limit: int | None = None,
) -> dict[str, Any]:
    if candidate_id and source_record_id:
        raise ValueError("candidate_id and source_record_id are mutually exclusive")
    inputs = [
        row
        for row in read_jsonl(input_path)
        if not concept_id or concept_id in (row.get("concept_ids") or [])
    ]
    if candidate_id:
        inputs = [
            row
            for row in inputs
            if str(row.get("candidate_id") or "") == candidate_id
        ]
    if source_record_id:
        inputs = [
            row
            for row in inputs
            if str((row.get("source_snapshot") or {}).get("source_record_id") or "")
            == source_record_id
        ]
    if offset < 0:
        raise ValueError("offset must be non-negative")
    inputs = inputs[offset : offset + limit if limit is not None else None]
    if not inputs:
        raise ValueError("No source-native candidates matched the prompt filter")
    prompt = SOURCE_NATIVE_PROMPT_PATH.read_text(encoding="utf-8").rstrip()
    prompt += (
        "\n\n## Batch Requirement\n\n"
        f"Return exactly {len(inputs)} articles in the same order as the input. "
        "Review every supplied source unit.\n\n"
        "INPUT CANDIDATES\n"
        + json.dumps(inputs, ensure_ascii=False, separators=(",", ":"))
        + "\n"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(prompt, encoding="utf-8")
    return {
        "schema": "rock-kb-source-native-prompt-build-v1",
        "status": "ok",
        "concept_id": concept_id,
        "candidate_id": candidate_id,
        "source_record_id": source_record_id,
        "offset": offset,
        "limit": limit,
        "candidate_count": len(inputs),
        "destination": str(destination),
        "sha256": sha256_file(destination),
    }


def normalize_markdown(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n").replace("\u00a0", " ")
    lines = [line.rstrip() for line in value.splitlines()]
    output: list[str] = []
    blank = False
    for line in lines:
        if line.strip():
            output.append(line)
            blank = False
        elif output and not blank:
            output.append("")
            blank = True
    return "\n".join(output).strip()


def parse_markdown_source_units(
    *,
    markdown: str,
    source_snapshot_id: str,
    source_record_id: str,
    source_url: str,
    source_title: str,
    documentation_path: str | None = None,
    split_rules: Iterable[dict[str, Any]] | None = None,
) -> list[SourceUnit]:
    blocks = apply_source_unit_split_rules(
        markdown_blocks(markdown),
        source_record_id=source_record_id,
        split_rules=split_rules or [],
    )
    units: list[SourceUnit] = []
    duplicate_counts: Counter[tuple[str, str, str]] = Counter()
    locator_counts: Counter[tuple[str, str]] = Counter()
    unit_id_by_block_token: dict[str, str] = {}
    for block in blocks:
        text = normalize_block_text(str(block["text"]))
        if not text:
            continue
        ordinal = len(units) + 1
        heading_path = [str(value) for value in block["heading_path"]]
        context_label = str(block.get("context_label") or "").strip()
        unit_kind, locator_kind = source_unit_and_locator_kind(str(block["kind"]))
        block_hash = sha256_text(text)
        context_path = [*heading_path, *([context_label] if context_label else [])]
        heading_key = " > ".join(context_path) or "Overview"
        duplicate_key = (heading_key, unit_kind, block_hash)
        duplicate_counts[duplicate_key] += 1
        occurrence = duplicate_counts[duplicate_key]
        locator_counts[(heading_key, unit_kind)] += 1
        locator_ordinal = locator_counts[(heading_key, unit_kind)]
        stable_key = (
            f"{source_record_id}:{heading_key}:{unit_kind}:"
            f"{block_hash}:{occurrence}"
        )
        source_unit_id = "source-unit:" + sha256_text(stable_key)[:32]
        parent_source_unit_id = unit_id_by_block_token.get(
            str(block.get("parent_block_token") or "")
        )
        locator_value = (
            f"{heading_key} / {unit_kind}-{locator_ordinal}"
            if context_path
            else f"Overview / {unit_kind}-{locator_ordinal}"
        )
        units.append(
            SourceUnit(
                schema="rock-kb-source-unit-v2",
                source_unit_id=source_unit_id,
                source_snapshot_id=source_snapshot_id,
                unit_kind=unit_kind,
                locator=SourceLocator(
                    kind=locator_kind,
                    value=locator_value,
                    url=source_url,
                    path=documentation_path,
                    symbol=(
                        context_label
                        or (heading_path[-1] if heading_path else None)
                    ),
                ),
                parent_source_unit_id=parent_source_unit_id,
                ordinal=ordinal,
                heading_path=heading_path,
                contextual_prefix=" > ".join(
                    [source_title, *context_path]
                )[:1000],
                context=heading_key[:1000],
                text=text,
                normalized_content_hash=block_hash,
                required_public_handling="cite_and_summarize_only",
            )
        )
        block_token = str(block.get("block_token") or "")
        if block_token:
            unit_id_by_block_token[block_token] = source_unit_id
    canonical_text_units: dict[tuple[str, str], str] = {}
    for index, unit in enumerate(units):
        key = (unit.unit_kind, str(unit.normalized_content_hash or ""))
        canonical_id = canonical_text_units.get(key)
        if canonical_id:
            units[index] = unit.model_copy(
                update={"duplicate_text_of_source_unit_id": canonical_id}
            )
        else:
            canonical_text_units[key] = unit.source_unit_id
    return units


def markdown_blocks(markdown: str) -> list[dict[str, Any]]:
    lines = normalize_markdown(markdown).splitlines()
    headings: list[str] = []
    blocks: list[dict[str, Any]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            title = " ".join(heading.group(2).split())
            headings = [*headings[: level - 1], title]
            index += 1
            continue
        if line.lstrip().startswith("```"):
            chunk = [line]
            index += 1
            while index < len(lines):
                chunk.append(lines[index])
                if lines[index].lstrip().startswith("```"):
                    index += 1
                    break
                index += 1
            blocks.append(
                {"kind": "code_block", "heading_path": headings[:], "text": "\n".join(chunk)}
            )
            continue
        if is_table_start(lines, index):
            chunk = [line]
            index += 1
            while index < len(lines) and lines[index].strip() and "|" in lines[index]:
                chunk.append(lines[index])
                index += 1
            blocks.append(
                {"kind": "table", "heading_path": headings[:], "text": "\n".join(chunk)}
            )
            continue
        if ORDERED_LIST_RE.match(line) or UNORDERED_LIST_RE.match(line):
            list_blocks, index = consume_list_blocks(
                lines,
                index,
                headings,
            )
            blocks.extend(list_blocks)
            continue
        chunk = [line]
        index += 1
        while index < len(lines):
            candidate = lines[index]
            if not candidate.strip():
                break
            if (
                HEADING_RE.match(candidate)
                or candidate.lstrip().startswith("```")
                or ORDERED_LIST_RE.match(candidate)
                or UNORDERED_LIST_RE.match(candidate)
                or is_table_start(lines, index)
            ):
                break
            chunk.append(candidate)
            index += 1
        paragraph = "\n".join(chunk)
        for sentence in split_paragraph_sentences(paragraph):
            blocks.append(
                {
                    "kind": "paragraph",
                    "heading_path": headings[:],
                    "text": sentence,
                }
            )
    return blocks


def load_source_unit_split_rules(
    path: Path = SOURCE_NATIVE_SPLIT_RULES_PATH,
) -> list[dict[str, Any]]:
    rules = list(read_jsonl(path))
    seen: set[tuple[str, str]] = set()
    for line_number, rule in enumerate(rules, start=1):
        if rule.get("schema") != "rock-kb-source-unit-split-rule-v1":
            raise ValueError(f"{path}:{line_number} has an unsupported schema")
        if rule.get("strategy") != "sentence":
            raise ValueError(f"{path}:{line_number} has an unsupported strategy")
        if not str(rule.get("reviewed_by") or "").strip():
            raise ValueError(f"{path}:{line_number} is missing reviewed_by")
        if not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",
            str(rule.get("reviewed_at") or ""),
        ):
            raise ValueError(f"{path}:{line_number} has an invalid reviewed_at")
        if len(str(rule.get("review_reason") or "").strip()) < 20:
            raise ValueError(f"{path}:{line_number} has an invalid review_reason")
        content_hash = str(rule.get("source_unit_content_hash") or "")
        if not re.fullmatch(r"[0-9a-f]{64}", content_hash):
            raise ValueError(f"{path}:{line_number} has an invalid content hash")
        key = (str(rule.get("source_record_id") or ""), content_hash)
        if not key[0] or key in seen:
            raise ValueError(f"{path}:{line_number} has a duplicate or empty identity")
        seen.add(key)
    return rules


def apply_source_unit_split_rules(
    blocks: list[dict[str, Any]],
    *,
    source_record_id: str,
    split_rules: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    rules_by_hash = {
        str(rule["source_unit_content_hash"]): rule
        for rule in split_rules
        if str(rule.get("source_record_id") or "") == source_record_id
    }
    if not rules_by_hash:
        return blocks
    applied: set[str] = set()

    def expand(
        block: dict[str, Any],
        *,
        ancestor_rule_hashes: frozenset[str] = frozenset(),
    ) -> list[dict[str, Any]]:
        text = normalize_block_text(str(block.get("text") or ""))
        content_hash = sha256_text(text)
        rule = rules_by_hash.get(content_hash)
        if rule is None:
            return [block]
        if content_hash in ancestor_rule_hashes:
            raise ValueError(
                f"split rule {content_hash} created a recursive split cycle"
            )
        if block.get("kind") == "list_item":
            split_blocks = split_list_item_block(block)
        elif block.get("kind") == "paragraph":
            split_blocks = split_paragraph_block(block)
        else:
            raise ValueError(
                f"split rule {content_hash} expected a list_item or paragraph"
            )
        if len(split_blocks) < 2:
            raise ValueError(
                f"split rule {content_hash} no longer produces multiple units"
            )
        applied.add(content_hash)
        expanded: list[dict[str, Any]] = []
        for split_block in split_blocks:
            expanded.extend(
                expand(
                    split_block,
                    ancestor_rule_hashes=ancestor_rule_hashes | {content_hash},
                )
            )
        return expanded

    output = [child for block in blocks for child in expand(block)]
    missing = sorted(set(rules_by_hash) - applied)
    if missing:
        raise ValueError(
            f"source-unit split rules did not match current source text: {missing[:3]}"
        )
    return output


def split_list_item_block(block: dict[str, Any]) -> list[dict[str, Any]]:
    text = normalize_block_text(str(block.get("text") or ""))
    marker = re.match(r"^(\s*(?:\d+[.)]|[-*+])\s+)(.*)$", text, re.DOTALL)
    if marker is None:
        return [block]
    sentences = split_reviewed_block_sentences(marker.group(2).strip())
    if len(sentences) < 2:
        return [block]
    parent_token = str(block.get("block_token") or f"split:{sha256_text(text)[:16]}")
    first = {
        **block,
        "block_token": parent_token,
        "text": f"{marker.group(1)}{sentences[0]}",
    }
    children = [
        {
            "kind": "paragraph",
            "heading_path": list(block.get("heading_path") or []),
            "context_label": str(block.get("context_label") or ""),
            "parent_block_token": parent_token,
            "block_token": f"{parent_token}:sentence:{index}",
            "text": sentence,
        }
        for index, sentence in enumerate(sentences[1:], start=2)
    ]
    return [first, *children]


def split_paragraph_block(block: dict[str, Any]) -> list[dict[str, Any]]:
    text = normalize_block_text(str(block.get("text") or ""))
    sentences = split_reviewed_block_sentences(text)
    if len(sentences) < 2:
        return [block]
    parent_token = str(block.get("block_token") or f"split:{sha256_text(text)[:16]}")
    first = {
        **block,
        "block_token": parent_token,
        "text": sentences[0],
    }
    children = [
        {
            "kind": "paragraph",
            "heading_path": list(block.get("heading_path") or []),
            "context_label": str(block.get("context_label") or ""),
            "parent_block_token": parent_token,
            "block_token": f"{parent_token}:sentence:{index}",
            "text": sentence,
        }
        for index, sentence in enumerate(sentences[1:], start=2)
    ]
    return [first, *children]


def split_reviewed_block_sentences(value: str) -> list[str]:
    # Exact hash-gated rules may repair upstream punctuation that omitted a space.
    normalized = re.sub(
        r"(?<=[.!?])([*_`]{1,3})(?=[A-Z])",
        r"\1" + "\n",
        value,
    )
    normalized = re.sub(r"(?<=[.!?])(?=[A-Z])", " ", normalized)
    return [
        sentence
        for chunk in normalized.splitlines()
        for sentence in split_paragraph_sentences(chunk)
    ]


def is_table_start(lines: list[str], index: int) -> bool:
    return (
        index + 1 < len(lines)
        and "|" in lines[index]
        and bool(TABLE_SEPARATOR_RE.match(lines[index + 1]))
    )


def consume_list_blocks(
    lines: list[str],
    start: int,
    heading_path: list[str],
) -> tuple[list[dict[str, Any]], int]:
    ordered = bool(ORDERED_LIST_RE.match(lines[start]))
    matcher = ORDERED_LIST_RE if ordered else UNORDERED_LIST_RE
    base_indent = leading_indent(lines[start])
    blocks: list[dict[str, Any]] = []
    index = start
    item_number = 0

    def is_top_level(value: str) -> bool:
        return bool(matcher.match(value)) and leading_indent(value) == base_indent

    while index < len(lines) and is_top_level(lines[index]):
        item_number += 1
        chunk = [lines[index]]
        index += 1
        end_list = False
        while index < len(lines):
            candidate = lines[index]
            if not candidate.strip():
                lookahead = index + 1
                while lookahead < len(lines) and not lines[lookahead].strip():
                    lookahead += 1
                if lookahead < len(lines) and is_top_level(lines[lookahead]):
                    index = lookahead
                    break
                if (
                    lookahead < len(lines)
                    and leading_indent(lines[lookahead]) > base_indent
                ):
                    chunk.extend(lines[index:lookahead])
                    index = lookahead
                    continue
                index = lookahead
                end_list = True
                break
            if is_top_level(candidate):
                break
            if leading_indent(candidate) > base_indent:
                chunk.append(candidate)
                index += 1
                continue
            end_list = True
            break

        block_token = f"list:{start}:{item_number}"
        context_label = list_item_context(chunk[0])
        nested_start = next(
            (
                offset
                for offset, value in enumerate(chunk[1:], start=1)
                if (
                    leading_indent(value) > base_indent
                    and (
                        ORDERED_LIST_RE.match(value)
                        or UNORDERED_LIST_RE.match(value)
                    )
                )
            ),
            None,
        )
        primary_lines = chunk if nested_start is None else chunk[:nested_start]
        nested_lines = [] if nested_start is None else chunk[nested_start:]
        blocks.append(
            {
                "kind": "list_item",
                "heading_path": heading_path[:],
                "context_label": context_label,
                "block_token": block_token,
                "text": "\n".join(primary_lines),
            }
        )
        if nested_lines:
            blocks.append(
                {
                    "kind": "list_item",
                    "heading_path": heading_path[:],
                    "context_label": context_label,
                    "parent_block_token": block_token,
                    "text": "\n".join(nested_lines),
                }
            )
        if end_list:
            break
    return blocks, index


def leading_indent(value: str) -> int:
    expanded = value.expandtabs(4)
    return len(expanded) - len(expanded.lstrip())


def list_item_context(value: str) -> str:
    content = re.sub(r"^\s*(?:\d+[.)]|[-*+])\s+", "", value).strip()
    bold = re.match(r"^\*\*([^*]+?)\*\*(?:\s*[-:]|\s|$)", content)
    if bold:
        return bold.group(1).rstrip(":").strip()[:200]
    return re.sub(r"[`*_]", "", content).split(" - ", 1)[0].rstrip(":")[:200]


def normalize_block_text(value: str) -> str:
    lines = [line.rstrip() for line in value.strip().splitlines()]
    return "\n".join(lines).strip()


def split_paragraph_sentences(value: str) -> list[str]:
    normalized = " ".join(value.split())
    if not normalized:
        return []
    sentences = re.split(
        r"(?<=[.!?])\s+(?=(?:[`*_(]*[A-Z0-9]))",
        normalized,
    )
    units: list[str] = []
    for sentence in sentences:
        units.extend(split_top_level_contrast_clause(sentence.strip()))
    return [unit for unit in units if unit]


def split_top_level_contrast_clause(value: str) -> list[str]:
    """Split an explicit contrast only when it joins independently useful facts."""
    depth = 0
    lower = value.lower()
    marker = " but when "
    for index, character in enumerate(value):
        if character == "(":
            depth += 1
        elif character == ")":
            depth = max(0, depth - 1)
        if depth or not lower.startswith(marker, index):
            continue
        left = value[:index].rstrip(" ,;")
        right = value[index + len(marker) :].strip()
        if len(left) < 40 or len(right) < 40:
            continue
        return [
            f"{left.rstrip('.')}.",
            f"When {right[0].lower()}{right[1:]}",
        ]
    return [value]


def source_unit_and_locator_kind(block_kind: str) -> tuple[str, str]:
    if block_kind == "table":
        return "table", "table"
    if block_kind == "code_block":
        return "code_block", "code_block"
    if block_kind == "list_item":
        return "list_item", "list_item"
    return "paragraph", "paragraph"


def build_source_native_document_candidates(
    *,
    concept_ids: Iterable[str] = SOURCE_NATIVE_PILOT_CONCEPTS,
    limit_per_concept: int = SOURCE_NATIVE_PILOT_LIMIT_PER_CONCEPT,
    destination: Path = SOURCE_NATIVE_REVIEW_DIR,
    previous_dir: Path = SOURCE_NATIVE_PILOT_DIR,
    checked_at: str | None = None,
    records: list[dict[str, Any]] | None = None,
    payload_loader: Callable[[dict[str, Any]], dict[str, Any] | None] | None = None,
) -> dict[str, Any]:
    destination.mkdir(parents=True, exist_ok=True)
    candidate_path = destination / "document-candidates.jsonl"
    markdown_by_record: dict[str, str] = {}

    if payload_loader is None:
        with httpx.Client(
            follow_redirects=True,
            timeout=30,
            headers={"User-Agent": USER_AGENT},
        ) as client:
            return _build_source_native_document_candidates(
                concept_ids=list(concept_ids),
                limit_per_concept=limit_per_concept,
                destination=destination,
                candidate_path=candidate_path,
                previous_dir=previous_dir,
                checked_at=checked_at,
                records=records,
                payload_loader=lambda record: fetch_rockumentation_payload(
                    client,
                    str(record.get("source_url") or ""),
                ),
                markdown_by_record=markdown_by_record,
            )
    return _build_source_native_document_candidates(
        concept_ids=list(concept_ids),
        limit_per_concept=limit_per_concept,
        destination=destination,
        candidate_path=candidate_path,
        previous_dir=previous_dir,
        checked_at=checked_at,
        records=records,
        payload_loader=payload_loader,
        markdown_by_record=markdown_by_record,
    )


def _build_source_native_document_candidates(
    *,
    concept_ids: list[str],
    limit_per_concept: int,
    destination: Path,
    candidate_path: Path,
    previous_dir: Path,
    checked_at: str | None,
    records: list[dict[str, Any]] | None,
    payload_loader: Callable[[dict[str, Any]], dict[str, Any] | None],
    markdown_by_record: dict[str, str],
) -> dict[str, Any]:
    record_by_id = {
        str(row.get("id") or ""): row
        for row in (records or [])
        if row.get("id")
    }
    split_rules = load_source_unit_split_rules()
    previous_snapshots = {
        str(row.get("source_record_id") or ""): row
        for row in read_jsonl(
            previous_dir / "source-snapshots.jsonl"
        )
        if row.get("source_record_id")
    }

    def context_loader(record: dict[str, Any]) -> str:
        record_id = str(record.get("id") or "")
        record_by_id[record_id] = record
        payload = payload_loader(record)
        markdown = rockumentation_markdown(payload)
        markdown_by_record[record_id] = markdown
        return " ".join(markdown.split())

    build_result = build_document_claim_candidates(
        concept_ids=concept_ids,
        limit_per_concept=limit_per_concept,
        output_path=candidate_path,
        records=records,
        context_loader=context_loader,
        require_full_text=True,
    )
    snapshots: list[SourceSnapshot] = []
    units: list[SourceUnit] = []
    inputs: list[dict[str, Any]] = []
    observed_check_time = checked_at or now_iso()
    for candidate in read_jsonl(candidate_path):
        source_record_id = str(candidate["source_record_id"])
        article_split_rule_hashes = sorted(
            str(rule["source_unit_content_hash"])
            for rule in split_rules
            if str(rule.get("source_record_id") or "") == source_record_id
        )
        record = record_by_id.get(source_record_id, {})
        markdown = markdown_by_record.get(source_record_id, "")
        content_hash = sha256_text(normalize_markdown(markdown))
        snapshot_id = "source-snapshot:" + sha256_text(
            f"{source_record_id}:{content_hash}"
        )[:32]
        observation = source_observation_metadata(
            previous=previous_snapshots.get(source_record_id),
            checked_at=observed_check_time,
            content_hash=content_hash,
        )
        snapshot = SourceSnapshot(
            schema="rock-kb-source-snapshot-v2",
            source_snapshot_id=snapshot_id,
            source_id=str(candidate.get("source_id") or ""),
            source_record_id=source_record_id,
            source_work_id=f"documentation-article:{candidate.get('documentation_article_id')}",
            canonical_url=str(candidate.get("source_url") or ""),
            title=str(candidate.get("source_title") or ""),
            source_path=str(candidate.get("documentation_path") or "") or None,
            routing_paths=[
                str(value)
                for value in candidate.get("documentation_branches") or []
                if value
            ],
            observed_at=observation["observed_at"],
            last_checked_at=observed_check_time,
            content_changed_at=observation["content_changed_at"],
            content_hash=content_hash,
            normalized_content_hash=content_hash,
            upstream_revision=str(candidate.get("documentation_current_version") or "") or None,
            parser_id="rockumentation-markdown-blocks",
            parser_version="1.4.0",
            observation_status=observation["observation_status"],
            immutable=False,
            authority_tier="official",
            public_policy="cite_and_summarize_only",
            derivation={
                "extraction_tool": "rockumentation_block_action",
                "documentation_article_id": int(
                    candidate.get("documentation_article_id") or 0
                ),
                "source_unit_split_rule_count": len(article_split_rule_hashes),
                **(
                    {
                        "source_unit_split_rules_sha256": sha256_text(
                            ":".join(article_split_rule_hashes)
                        )
                    }
                    if article_split_rule_hashes
                    else {}
                ),
            },
        )
        article_units = parse_markdown_source_units(
            markdown=markdown,
            source_snapshot_id=snapshot_id,
            source_record_id=source_record_id,
            source_url=str(candidate.get("source_url") or ""),
            source_title=str(candidate.get("source_title") or ""),
            documentation_path=str(candidate.get("documentation_path") or "") or None,
            split_rules=split_rules,
        )
        concept_facets = sorted(
            str(value)
            for value in candidate.get("concept_ids") or []
            if value
        )
        existing_claims = sorted(
            [dict(row) for row in candidate.get("existing_claims") or []],
            key=lambda row: str(row.get("claim_id") or ""),
        )
        documentation_branches = sorted(
            str(value)
            for value in candidate.get("documentation_branches") or []
            if value
        )
        input_hash = source_native_model_input_hash(
            snapshot=snapshot,
            source_units=article_units,
            concept_ids=concept_facets,
            existing_claims=existing_claims,
            documentation_path=str(candidate.get("documentation_path") or "")
            or None,
            documentation_branches=documentation_branches,
            documentation_current_version=str(
                candidate.get("documentation_current_version") or ""
            )
            or None,
        )
        source_native_candidate_id = "source-native-candidate:" + sha256_text(
            f"{source_record_id}:{input_hash}"
        )[:24]
        snapshots.append(snapshot)
        units.extend(article_units)
        inputs.append(
            {
                "schema": "rock-kb-source-native-distillation-input-v1",
                "candidate_id": source_native_candidate_id,
                "source_input_hash": input_hash,
                "source_input_hash_version": SOURCE_NATIVE_INPUT_HASH_VERSION,
                "source_snapshot": snapshot.public_dump(),
                "source_units": [row.model_dump(by_alias=True) for row in article_units],
                "concept_ids": concept_facets,
                "existing_claims": existing_claims,
                "documentation_path": candidate.get("documentation_path"),
                "documentation_branches": documentation_branches,
                "documentation_current_version": candidate.get(
                    "documentation_current_version"
                ),
            }
        )
    snapshots.sort(key=lambda row: row.source_snapshot_id)
    units.sort(key=lambda row: (row.source_snapshot_id, row.ordinal or 0))
    inputs.sort(key=lambda row: str(row["candidate_id"]))
    write_jsonl(
        destination / "source-snapshots.jsonl",
        [row.public_dump() for row in snapshots],
    )
    write_jsonl(
        destination / "source-units.private.jsonl",
        [row.model_dump(by_alias=True, exclude_none=True) for row in units],
    )
    write_jsonl(destination / "distillation-input.jsonl", inputs)
    summary = {
        "schema": "rock-kb-source-native-candidate-build-v1",
        "status": "ok",
        "concept_ids": concept_ids,
        "article_count": len(inputs),
        "source_snapshot_count": len(snapshots),
        "source_unit_count": len(units),
        "source_input_hash_version": SOURCE_NATIVE_INPUT_HASH_VERSION,
        "source_unit_kind_counts": dict(
            sorted(Counter(row.unit_kind for row in units).items())
        ),
        "destination": str(destination),
        "document_candidate_build": build_result,
    }
    (destination / "candidate-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def source_observation_metadata(
    *,
    previous: dict[str, Any] | None,
    checked_at: str,
    content_hash: str,
) -> dict[str, str]:
    previous_hash = str(
        (previous or {}).get("normalized_content_hash")
        or (previous or {}).get("content_hash")
        or ""
    )
    if previous and previous_hash == content_hash:
        return {
            "observed_at": str(previous.get("observed_at") or checked_at),
            "content_changed_at": str(
                previous.get("content_changed_at")
                or previous.get("observed_at")
                or checked_at
            ),
            "observation_status": "unchanged",
        }
    return {
        "observed_at": checked_at,
        "content_changed_at": checked_at,
        "observation_status": "changed" if previous else "initial",
    }


def source_native_model_input_hash(
    *,
    snapshot: SourceSnapshot,
    source_units: Iterable[SourceUnit],
    concept_ids: Iterable[str],
    existing_claims: Iterable[dict[str, Any]],
    documentation_path: str | None,
    documentation_branches: Iterable[str],
    documentation_current_version: str | None,
) -> str:
    stable_snapshot = {
        "source_id": snapshot.source_id,
        "source_record_id": snapshot.source_record_id,
        "source_work_id": snapshot.source_work_id,
        "canonical_url": snapshot.canonical_url,
        "title": snapshot.title,
        "source_path": snapshot.source_path,
        "routing_paths": sorted(snapshot.routing_paths),
        "normalized_content_hash": snapshot.normalized_content_hash,
        "upstream_revision": snapshot.upstream_revision,
        "parser_id": snapshot.parser_id,
        "parser_version": snapshot.parser_version,
        "authority_tier": snapshot.authority_tier,
        "public_policy": snapshot.public_policy,
        "derivation": snapshot.derivation,
    }
    payload = {
        "source_input_hash_version": SOURCE_NATIVE_INPUT_HASH_VERSION,
        "source_snapshot": stable_snapshot,
        "source_units": [
            row.model_dump(by_alias=True, exclude_none=True)
            for row in source_units
        ],
        "concept_ids": sorted(set(concept_ids)),
        "existing_claims": sorted(
            [dict(row) for row in existing_claims],
            key=lambda row: str(row.get("claim_id") or ""),
        ),
        "documentation_path": documentation_path,
        "documentation_branches": sorted(set(documentation_branches)),
        "documentation_current_version": documentation_current_version,
    }
    return sha256_text(_canonical_json(payload))


def validate_source_native_distillation(
    output: SourceNativeDistillationOutput | dict[str, Any],
    *,
    inputs: Iterable[dict[str, Any]],
    require_promotable: bool = False,
) -> SourceNativeDistillationOutput:
    result = (
        output
        if isinstance(output, SourceNativeDistillationOutput)
        else SourceNativeDistillationOutput.model_validate(output)
    )
    inputs_by_id = {
        str(row.get("candidate_id") or ""): dict(row)
        for row in inputs
        if row.get("candidate_id")
    }
    if [row.candidate_id for row in result.articles] != [
        candidate_id for candidate_id in inputs_by_id
    ]:
        raise ValueError(
            "distillation articles must match input candidate IDs and order"
        )
    for article in result.articles:
        source_input = inputs_by_id.get(article.candidate_id)
        if source_input is None:
            raise ValueError(f"unknown candidate_id: {article.candidate_id}")
        if article.source_input_hash != source_input.get("source_input_hash"):
            raise ValueError(
                f"{article.candidate_id} source_input_hash does not match"
            )
        source_units = {
            str(row.get("source_unit_id") or ""): row
            for row in source_input.get("source_units") or []
        }
        decision_ids = {row.source_unit_id for row in article.unit_decisions}
        if decision_ids != set(source_units):
            missing = sorted(set(source_units) - decision_ids)
            unknown = sorted(decision_ids - set(source_units))
            raise ValueError(
                f"{article.candidate_id} unit decisions must cover the exact input "
                f"(missing={missing[:3]}, unknown={unknown[:3]})"
            )
        decision_by_id = {
            row.source_unit_id: row for row in article.unit_decisions
        }
        artifact_owners: dict[str, str] = {}
        allowed_concepts = set(source_input.get("concept_ids") or [])
        known_claim_ids = {
            str(row.get("claim_id") or "")
            for row in source_input.get("existing_claims") or []
        }
        verification_unit_ids: set[str] = set()
        for request in article.verification_requests:
            unknown_request_units = sorted(
                set(request.source_unit_ids) - set(source_units)
            )
            if unknown_request_units:
                raise ValueError(
                    f"{article.candidate_id} verification request references "
                    f"unknown source units: {unknown_request_units[:3]}"
                )
            verification_unit_ids.update(request.source_unit_ids)
        for artifact in article.artifacts:
            unknown_concepts = sorted(set(artifact.concept_ids) - allowed_concepts)
            if unknown_concepts:
                raise ValueError(
                    f"{article.candidate_id}/{artifact.artifact_key} has unknown "
                    f"concepts: {', '.join(unknown_concepts)}"
                )
            unknown_claims = sorted(
                set(artifact.related_existing_claim_ids) - known_claim_ids
            )
            if unknown_claims:
                raise ValueError(
                    f"{article.candidate_id}/{artifact.artifact_key} references "
                    f"unknown existing claims: {', '.join(unknown_claims)}"
                )
            for source_unit_id in artifact.source_unit_ids:
                decision = decision_by_id.get(source_unit_id)
                if decision is None:
                    raise ValueError(
                        f"{article.candidate_id}/{artifact.artifact_key} references "
                        f"unknown source unit {source_unit_id}"
                    )
                if decision.disposition != artifact.artifact_type:
                    raise ValueError(
                        f"{article.candidate_id}/{artifact.artifact_key} type does "
                        f"not match disposition for {source_unit_id}"
                    )
                existing_owner = artifact_owners.get(source_unit_id)
                if existing_owner:
                    raise ValueError(
                        f"{source_unit_id} is assigned to both {existing_owner} "
                        f"and {artifact.artifact_key}"
                    )
                artifact_owners[source_unit_id] = artifact.artifact_key
            for item in artifact.payload.reference_items:
                if item.value_status == "mutable_default" and not item.needs_verification:
                    raise ValueError(
                        f"{article.candidate_id}/{artifact.artifact_key} contains "
                        "a mutable default without verification status"
                    )
                if item.needs_verification and not artifact.needs_live_verification:
                    raise ValueError(
                        f"{article.candidate_id}/{artifact.artifact_key} contains "
                        "a verification-marked reference item without an "
                        "artifact verification requirement"
                    )
            has_verification_request = bool(
                set(artifact.source_unit_ids).intersection(
                    verification_unit_ids
                )
            )
            if artifact.needs_live_verification != has_verification_request:
                raise ValueError(
                    f"{article.candidate_id}/{artifact.artifact_key} verification "
                    "flag must match an explicit source-unit verification request"
                )
        material_ids = {
            row.source_unit_id
            for row in article.unit_decisions
            if row.disposition not in {"no_artifact", "split_required"}
        }
        no_artifact_ids = {
            row.source_unit_id
            for row in article.unit_decisions
            if row.disposition == "no_artifact"
        }
        split_required_ids = {
            row.source_unit_id
            for row in article.unit_decisions
            if row.disposition == "split_required"
        }
        if set(artifact_owners) != material_ids:
            raise ValueError(
                f"{article.candidate_id} useful source units must have exactly "
                "one typed artifact"
            )
        verification_without_artifact = sorted(
            verification_unit_ids - set(artifact_owners) - split_required_ids
        )
        if verification_without_artifact:
            raise ValueError(
                f"{article.candidate_id} verification requests must map to "
                f"reviewable artifacts: {verification_without_artifact[:3]}"
            )
        coverage = article.coverage_check
        if coverage.material_unit_count != len(material_ids):
            raise ValueError(
                f"{article.candidate_id} material_unit_count is incorrect"
            )
        if set(coverage.captured_source_unit_ids) != material_ids:
            raise ValueError(
                f"{article.candidate_id} captured_source_unit_ids are incorrect"
            )
        if set(coverage.no_artifact_source_unit_ids) != no_artifact_ids:
            raise ValueError(
                f"{article.candidate_id} no_artifact_source_unit_ids are incorrect"
            )
        omitted_ids = {
            row.source_unit_id for row in coverage.omitted_source_units
        }
        if omitted_ids != split_required_ids:
            raise ValueError(
                f"{article.candidate_id} omitted_source_units must match "
                "split_required decisions"
            )
        if require_promotable and split_required_ids:
            raise ValueError(
                f"{article.candidate_id} requires deterministic source-unit splits"
            )
    return result


def merge_source_native_distillation_outputs(
    *,
    input_path: Path,
    batch_paths: Iterable[Path],
    destination: Path,
    allow_review_blockers: bool = False,
) -> dict[str, Any]:
    inputs = list(read_jsonl(input_path))
    paths = list(batch_paths)
    articles_by_id: dict[str, dict[str, Any]] = {}
    for batch_path in paths:
        batch = SourceNativeDistillationOutput.model_validate(
            json.loads(batch_path.read_text(encoding="utf-8"))
        )
        for article in batch.articles:
            if article.candidate_id in articles_by_id:
                raise ValueError(
                    f"duplicate generated candidate_id: {article.candidate_id}"
                )
            articles_by_id[article.candidate_id] = article.public_dump()
    expected_ids = [str(row.get("candidate_id") or "") for row in inputs]
    missing = sorted(set(expected_ids) - set(articles_by_id))
    unknown = sorted(set(articles_by_id) - set(expected_ids))
    if missing or unknown:
        raise ValueError(
            "generated batches must cover the exact source-native input "
            f"(missing={missing[:3]}, unknown={unknown[:3]})"
        )
    merged = {
        "schema": "rock-kb-source-knowledge-distillation-v2.3",
        "variant_id": "source_knowledge_distillation_v2_3",
        "articles": [articles_by_id[candidate_id] for candidate_id in expected_ids],
    }
    validated = validate_source_native_distillation(
        merged,
        inputs=inputs,
        require_promotable=not allow_review_blockers,
    )
    split_required_count = sum(
        1
        for article in validated.articles
        for decision in article.unit_decisions
        if decision.disposition == "split_required"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(
            validated.public_dump(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "schema": "rock-kb-source-native-output-merge-v1",
        "status": "review_required" if split_required_count else "ok",
        "batch_count": len(paths),
        "article_count": len(validated.articles),
        "artifact_count": sum(
            len(article.artifacts)
            for article in validated.articles
        ),
        "source_unit_count": sum(
            len(article.unit_decisions)
            for article in validated.articles
        ),
        "split_required_count": split_required_count,
        "destination": str(destination),
        "sha256": sha256_file(destination),
    }


def promote_source_native_distillation(
    *,
    input_path: Path,
    output_path: Path,
    destination: Path = SOURCE_NATIVE_PILOT_DIR,
    reviewer: str,
    model: str,
    reviewed_at: str | None = None,
    generation_prompt_version: str | None = None,
    generated_at: str | None = None,
    base_dir: Path | None = None,
    generated_output_path: Path | None = None,
) -> dict[str, Any]:
    inputs = list(read_jsonl(input_path))
    output = SourceNativeDistillationOutput.model_validate(
        json.loads(output_path.read_text(encoding="utf-8"))
    )
    validated = validate_source_native_distillation(
        output,
        inputs=inputs,
        require_promotable=True,
    )
    generated_articles_by_id: dict[str, dict[str, Any]] = {}
    if generated_output_path is not None:
        generated_output = SourceNativeDistillationOutput.model_validate(
            json.loads(generated_output_path.read_text(encoding="utf-8"))
        )
        generated_articles_by_id = {
            article.candidate_id: article.public_dump()
            for article in generated_output.articles
        }
        if set(generated_articles_by_id) != {
            article.candidate_id for article in validated.articles
        }:
            raise ValueError(
                "generated output must cover the same source-native candidates "
                "as the reviewed output"
            )
    inputs_by_id = {
        str(row["candidate_id"]): row
        for row in inputs
    }
    reviewed_at = reviewed_at or now_iso()
    generated_at = generated_at or reviewed_at
    generated_with_prompt_version = (
        generation_prompt_version or SOURCE_NATIVE_PROMPT_VERSION
    )
    snapshots: dict[str, SourceSnapshot] = {}
    source_units: dict[str, SourceUnit] = {}
    activities: list[GenerationActivity] = []
    reviewed_artifacts: list[ReviewedSourceNativeArtifact] = []
    relationships: list[KnowledgeRelationship] = []
    verification_queue: list[SourceNativeVerificationQueueItem] = []
    for article in validated.articles:
        source_input = inputs_by_id[article.candidate_id]
        snapshot = SourceSnapshot.model_validate(source_input["source_snapshot"])
        snapshots[snapshot.source_snapshot_id] = snapshot
        input_units = {
            str(row["source_unit_id"]): SourceUnit.model_validate(row)
            for row in source_input.get("source_units") or []
        }
        decisions = {
            row.source_unit_id: row
            for row in article.unit_decisions
        }
        for source_unit_id, unit in input_units.items():
            decision = decisions[source_unit_id]
            public_unit = unit.model_copy(
                update={
                    "public_summary": (
                        decision.evidence_summary
                        or decision.decision_reason
                    )[:1500],
                    "text": None,
                }
            )
            source_units[source_unit_id] = SourceUnit.model_validate(
                public_unit.model_dump(by_alias=True)
            )
        activity_id = "generation:" + sha256_text(
            f"{article.candidate_id}:{article.source_input_hash}:"
            f"{generated_with_prompt_version}:{model}"
        )[:24]
        reviewed_article_payload = article.public_dump()
        generated_article_payload = generated_articles_by_id.get(
            article.candidate_id,
            reviewed_article_payload,
        )
        review_correction_count = json_change_count(
            generated_article_payload,
            reviewed_article_payload,
        )
        activities.append(
            GenerationActivity(
                schema="rock-kb-generation-activity-v1",
                generation_activity_id=activity_id,
                activity_type="source_distillation",
                model=model,
                prompt_id=SOURCE_NATIVE_PROMPT_ID,
                prompt_version=generated_with_prompt_version,
                source_snapshot_ids=[snapshot.source_snapshot_id],
                source_unit_ids=sorted(input_units),
                source_input_hash=article.source_input_hash,
                created_at=generated_at,
                review_method="model_generated_maintainer_reviewed",
                parameters={
                    "typed_artifact_contract": "v2.3",
                    "source_input_hash_version": str(
                        source_input.get("source_input_hash_version") or "1"
                    ),
                    "review_contract_version": SOURCE_NATIVE_PROMPT_VERSION,
                    "prompt_sha256": sha256_file(SOURCE_NATIVE_PROMPT_PATH),
                    "generated_article_sha256": sha256_text(
                        _canonical_json(generated_article_payload)
                    ),
                    "reviewed_article_sha256": sha256_text(
                        _canonical_json(reviewed_article_payload)
                    ),
                    "review_changed": bool(review_correction_count),
                    "review_correction_count": review_correction_count,
                    "public_retrieval_changed": False,
                },
            )
        )
        article_id = int(snapshot.derivation.get("documentation_article_id") or 0)
        artifact_ids_by_key = {
            artifact.artifact_key: (
                f"source-native:{artifact.artifact_type}:"
                f"{snapshot.source_id}:article-{article_id}:{artifact.artifact_key}"
            )
            for artifact in article.artifacts
        }
        for artifact in article.artifacts:
            artifact_id = artifact_ids_by_key[artifact.artifact_key]
            reviewed_artifacts.append(
                ReviewedSourceNativeArtifact(
                    schema="rock-kb-reviewed-source-native-artifact-v1",
                    artifact_id=artifact_id,
                    source_candidate_id=article.candidate_id,
                    generation_activity_id=activity_id,
                    artifact=artifact,
                    review_state="reviewer_approved",
                    reviewer=reviewer,
                    reviewed_at=reviewed_at,
                    review_notes=article.review_notes,
                    source_input_hash=article.source_input_hash,
                )
            )
            relation = {
                "adds_condition": "qualifies",
                "conflicts": "contradicts",
            }.get(artifact.relation_to_existing)
            if relation:
                for existing_claim_id in artifact.related_existing_claim_ids:
                    relationship_id = "relationship:" + sha256_text(
                        f"{artifact_id}:{relation}:{existing_claim_id}"
                    )[:24]
                    relationships.append(
                        KnowledgeRelationship(
                            schema="rock-kb-knowledge-relationship-v1",
                            relationship_id=relationship_id,
                            from_id=artifact_id,
                            to_id=existing_claim_id,
                            relation=relation,
                            decision="accept",
                            confidence=artifact.confidence,
                            rationale=artifact.rationale,
                            evidence_source_unit_ids=artifact.source_unit_ids,
                            reviewed_at=reviewed_at,
                        )
                    )

            for link in artifact.related_artifact_links:
                target_id = artifact_ids_by_key[link.target_artifact_key]
                relationship_id = "relationship:" + sha256_text(
                    f"{artifact_id}:{link.relation}:{target_id}"
                )[:24]
                relationships.append(
                    KnowledgeRelationship(
                        schema="rock-kb-knowledge-relationship-v1",
                        relationship_id=relationship_id,
                        from_id=artifact_id,
                        to_id=target_id,
                        relation=link.relation,
                        decision="accept",
                        confidence=artifact.confidence,
                        rationale=link.rationale,
                        evidence_source_unit_ids=link.evidence_source_unit_ids,
                        reviewed_at=reviewed_at,
                    )
                )

        for request in article.verification_requests:
            request_unit_ids = set(request.source_unit_ids)
            artifact_ids = sorted(
                artifact_ids_by_key[artifact.artifact_key]
                for artifact in article.artifacts
                if request_unit_ids.intersection(artifact.source_unit_ids)
            )
            verification_id = "source-native-verification:" + sha256_text(
                f"{article.candidate_id}:{request.verification_surface}:"
                f"{request.question}:{':'.join(sorted(request.source_unit_ids))}"
            )[:24]
            verification_queue.append(
                SourceNativeVerificationQueueItem(
                    schema="rock-kb-source-native-verification-request-v1",
                    verification_id=verification_id,
                    source_candidate_id=article.candidate_id,
                    artifact_ids=artifact_ids,
                    concept_ids=sorted(
                        {
                            concept_id
                            for artifact in article.artifacts
                            if request_unit_ids.intersection(
                                artifact.source_unit_ids
                            )
                            for concept_id in artifact.concept_ids
                        }
                        or set(source_input.get("concept_ids") or [])
                    ),
                    source_unit_ids=sorted(request.source_unit_ids),
                    verification_surface=request.verification_surface,
                    question=request.question,
                    why_material=request.why_material,
                )
            )

    evaluation_rows = [
        {
            "schema": "rock-kb-service-evaluation-case-v1",
            "id": "source-native-eval:"
            + sha256_text(
                f"{row.artifact_id}:"
                f"{row.artifact.independent_question}"
            )[:24],
            "question": row.artifact.independent_question,
            "concept_id": row.artifact.concept_ids[0],
            "source": "source_native_pilot_exact_question",
            "evaluation_mode": "retrieval",
            "expected_result_ids": [row.artifact_id],
            "expected_result_kinds": [row.artifact.artifact_type],
            "required_authority_tiers": ["official"],
            "max_rank": 3,
        }
        for row in reviewed_artifacts
    ]
    bundle_rows = {
        "source-snapshots.jsonl": [
            row.public_dump() for row in snapshots.values()
        ],
        "source-units.jsonl": [
            row.public_dump() for row in source_units.values()
        ],
        "generation-activities.jsonl": [
            row.public_dump() for row in activities
        ],
        "reviewed-artifacts.jsonl": [
            row.public_dump() for row in reviewed_artifacts
        ],
        "relationships.jsonl": [
            row.public_dump() for row in relationships
        ],
        "evaluation-set.jsonl": evaluation_rows,
        "verification-queue.jsonl": [
            row.public_dump() for row in verification_queue
        ],
    }
    if base_dir is not None:
        bundle_rows = merge_source_native_bundle_rows(
            base_dir=base_dir,
            incoming=bundle_rows,
        )
    destination.mkdir(parents=True, exist_ok=True)
    sort_keys = {
        "source-snapshots.jsonl": "source_snapshot_id",
        "source-units.jsonl": "source_unit_id",
        "generation-activities.jsonl": "generation_activity_id",
        "reviewed-artifacts.jsonl": "artifact_id",
        "relationships.jsonl": "relationship_id",
        "evaluation-set.jsonl": "id",
        "verification-queue.jsonl": "verification_id",
    }
    for name, rows in bundle_rows.items():
        write_jsonl(
            destination / name,
            sorted(rows, key=lambda row: str(row.get(sort_keys[name]) or "")),
        )
    if base_dir is not None:
        for preserved_name in (
            "evaluation-holdout.jsonl",
            "split-rules.jsonl",
        ):
            preserved_path = base_dir / preserved_name
            destination_path = destination / preserved_name
            if (
                preserved_path.exists()
                and preserved_path.resolve() != destination_path.resolve()
            ):
                write_jsonl(
                    destination_path,
                    list(read_jsonl(preserved_path)),
                )
    manifest = write_source_native_manifest(destination)
    return {
        "schema": "rock-kb-source-native-promotion-v1",
        "status": "ok",
        "destination": str(destination),
        "article_count": manifest.article_count,
        "refreshed_article_count": len(validated.articles),
        "reviewed_artifact_count": len(bundle_rows["reviewed-artifacts.jsonl"]),
        "source_unit_count": len(bundle_rows["source-units.jsonl"]),
        "verification_request_count": len(
            bundle_rows["verification-queue.jsonl"]
        ),
        "manifest": manifest.public_dump(),
    }


def merge_source_native_bundle_rows(
    *,
    base_dir: Path,
    incoming: dict[str, list[dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    """Append a reviewed batch while replacing prior rows for refreshed works."""

    key_by_file = {
        "source-snapshots.jsonl": "source_snapshot_id",
        "source-units.jsonl": "source_unit_id",
        "generation-activities.jsonl": "generation_activity_id",
        "reviewed-artifacts.jsonl": "artifact_id",
        "relationships.jsonl": "relationship_id",
        "evaluation-set.jsonl": "id",
        "verification-queue.jsonl": "verification_id",
    }
    prior = {
        name: list(read_jsonl(base_dir / name))
        for name in key_by_file
    }
    incoming_snapshots = incoming["source-snapshots.jsonl"]
    incoming_work_ids = {
        str(row.get("source_work_id") or "")
        for row in incoming_snapshots
        if row.get("source_work_id")
    }
    incoming_record_keys = {
        (
            str(row.get("source_id") or ""),
            str(row.get("source_record_id") or ""),
        )
        for row in incoming_snapshots
        if row.get("source_record_id")
    }
    replaced_snapshot_ids = {
        str(row.get("source_snapshot_id") or "")
        for row in prior["source-snapshots.jsonl"]
        if (
            str(row.get("source_work_id") or "") in incoming_work_ids
            or (
                str(row.get("source_id") or ""),
                str(row.get("source_record_id") or ""),
            )
            in incoming_record_keys
        )
    }
    replaced_unit_ids = {
        str(row.get("source_unit_id") or "")
        for row in prior["source-units.jsonl"]
        if str(row.get("source_snapshot_id") or "") in replaced_snapshot_ids
    }
    replaced_artifact_ids = {
        str(row.get("artifact_id") or "")
        for row in prior["reviewed-artifacts.jsonl"]
        if replaced_unit_ids.intersection(
            (row.get("artifact") or {}).get("source_unit_ids") or []
        )
    }
    replaced_activity_ids = {
        str(row.get("generation_activity_id") or "")
        for row in prior["generation-activities.jsonl"]
        if (
            replaced_snapshot_ids.intersection(row.get("source_snapshot_ids") or [])
            or replaced_unit_ids.intersection(row.get("source_unit_ids") or [])
        )
    }

    filtered = {
        "source-snapshots.jsonl": [
            row
            for row in prior["source-snapshots.jsonl"]
            if str(row.get("source_snapshot_id") or "")
            not in replaced_snapshot_ids
        ],
        "source-units.jsonl": [
            row
            for row in prior["source-units.jsonl"]
            if str(row.get("source_unit_id") or "") not in replaced_unit_ids
        ],
        "generation-activities.jsonl": [
            row
            for row in prior["generation-activities.jsonl"]
            if str(row.get("generation_activity_id") or "")
            not in replaced_activity_ids
        ],
        "reviewed-artifacts.jsonl": [
            row
            for row in prior["reviewed-artifacts.jsonl"]
            if str(row.get("artifact_id") or "") not in replaced_artifact_ids
        ],
        "relationships.jsonl": [
            row
            for row in prior["relationships.jsonl"]
            if str(row.get("from_id") or "") not in replaced_artifact_ids
            and str(row.get("to_id") or "") not in replaced_artifact_ids
            and not replaced_unit_ids.intersection(
                row.get("evidence_source_unit_ids") or []
            )
        ],
        "evaluation-set.jsonl": [
            row
            for row in prior["evaluation-set.jsonl"]
            if not replaced_artifact_ids.intersection(
                row.get("expected_result_ids") or []
            )
        ],
        "verification-queue.jsonl": [
            row
            for row in prior["verification-queue.jsonl"]
            if not replaced_unit_ids.intersection(row.get("source_unit_ids") or [])
            and not replaced_artifact_ids.intersection(row.get("artifact_ids") or [])
        ],
    }

    combined: dict[str, list[dict[str, Any]]] = {}
    for name, key in key_by_file.items():
        rows_by_id = {
            str(row.get(key) or ""): row
            for row in filtered[name]
            if row.get(key)
        }
        for row in incoming[name]:
            row_id = str(row.get(key) or "")
            if not row_id:
                raise ValueError(f"{name} row is missing {key}")
            rows_by_id[row_id] = row
        combined[name] = list(rows_by_id.values())
    return combined


def json_change_count(before: Any, after: Any) -> int:
    if isinstance(before, dict) and isinstance(after, dict):
        keys = set(before) | set(after)
        return sum(
            1
            if key not in before or key not in after
            else json_change_count(before[key], after[key])
            for key in keys
        )
    if isinstance(before, list) and isinstance(after, list):
        common = min(len(before), len(after))
        return sum(
            json_change_count(before[index], after[index])
            for index in range(common)
        ) + abs(len(before) - len(after))
    return int(before != after)


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def write_source_native_manifest(
    destination: Path = SOURCE_NATIVE_PILOT_DIR,
) -> SourceNativePilotManifest:
    file_hashes = {
        name: sha256_file(destination / name)
        for name in PILOT_FILE_NAMES
        if (destination / name).exists()
    }
    snapshots = list(read_jsonl(destination / "source-snapshots.jsonl"))
    source_units = list(read_jsonl(destination / "source-units.jsonl"))
    activities = list(read_jsonl(destination / "generation-activities.jsonl"))
    artifacts = list(read_jsonl(destination / "reviewed-artifacts.jsonl"))
    relationships = list(read_jsonl(destination / "relationships.jsonl"))
    verification_queue = list(
        read_jsonl(destination / "verification-queue.jsonl")
    )
    evaluations = [
        *read_jsonl(destination / "evaluation-set.jsonl"),
        *read_jsonl(destination / "evaluation-holdout.jsonl"),
    ]
    artifact_ids = {
        str(row.get("artifact_id") or "")
        for row in artifacts
        if row.get("artifact_id")
    }
    evaluation_ids: set[str] = set()
    missing_expected_ids: list[tuple[str, str]] = []
    for row in evaluations:
        evaluation_id = str(row.get("id") or "")
        if not evaluation_id or evaluation_id in evaluation_ids:
            raise ValueError(
                "source-native evaluations require unique non-empty IDs"
            )
        evaluation_ids.add(evaluation_id)
        for expected_id in row.get("expected_result_ids") or []:
            if str(expected_id) not in artifact_ids:
                missing_expected_ids.append((evaluation_id, str(expected_id)))
    if missing_expected_ids:
        raise ValueError(
            "source-native evaluations reference missing reviewed artifacts: "
            f"{missing_expected_ids[:3]}"
        )
    split_rules_path = destination / "split-rules.jsonl"
    if split_rules_path.exists():
        load_source_unit_split_rules(split_rules_path)
    concept_ids = sorted(
        {
            str(concept_id)
            for row in artifacts
            for concept_id in ((row.get("artifact") or {}).get("concept_ids") or [])
        }
    )
    manifest = SourceNativePilotManifest(
        schema="rock-kb-source-native-pilot-manifest-v1",
        prompt_id=SOURCE_NATIVE_PROMPT_ID,
        prompt_version=SOURCE_NATIVE_PROMPT_VERSION,
        concept_ids=concept_ids,
        article_count=len(
            {
                str(row.get("source_work_id") or row.get("source_record_id") or "")
                for row in snapshots
                if row.get("source_work_id") or row.get("source_record_id")
            }
        ),
        source_snapshot_count=len(snapshots),
        source_unit_count=len(source_units),
        generation_activity_count=len(activities),
        reviewed_artifact_count=len(artifacts),
        relationship_count=len(relationships),
        evaluation_case_count=len(evaluations),
        verification_request_count=len(verification_queue),
        artifact_type_counts=dict(
            sorted(
                Counter(
                    str((row.get("artifact") or {}).get("artifact_type") or "unknown")
                    for row in artifacts
                ).items()
            )
        ),
        generation_prompt_versions=dict(
            sorted(
                Counter(
                    str(row.get("prompt_version") or "unknown")
                    for row in activities
                ).items()
            )
        ),
        generation_models=dict(
            sorted(
                Counter(
                    str(row.get("model") or "unknown")
                    for row in activities
                ).items()
            )
        ),
        generation_input_hash_versions=dict(
            sorted(
                Counter(
                    str(
                        (row.get("parameters") or {}).get(
                            "source_input_hash_version"
                        )
                        or "1"
                    )
                    for row in activities
                ).items()
            )
        ),
        review_changed_article_count=sum(
            1
            for row in activities
            if bool((row.get("parameters") or {}).get("review_changed"))
        ),
        source_family_counts=dict(
            sorted(
                Counter(
                    str(row.get("source_id") or "unknown")
                    for row in snapshots
                ).items()
            )
        ),
        file_hashes=file_hashes,
        notes=[
            "The source-native bundle is canonical shadow input; default public retrieval remains legacy and any canary access requires a separate opt-in release.",
            "Tracked source units contain reviewed paraphrases and locators, never full Rockumentation text.",
            "Bounded factual catalogs may preserve reviewed field names, types, settings, and option matrices without reproducing expressive article prose.",
            "Unprocessed product-version scope is exposed separately from the observed documentation revision.",
        ],
    )
    (destination / "manifest.json").write_text(
        json.dumps(manifest.public_dump(), ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    return manifest


def load_source_native_pilot(
    repo_root: Path = REPO_ROOT,
) -> dict[str, list[Any]]:
    destination = repo_root / "canonical" / "source-native" / "v1"
    manifest_path = destination / "manifest.json"
    if not manifest_path.exists():
        return {
            "source_snapshots": [],
            "source_units": [],
            "generation_activities": [],
            "reviewed_artifacts": [],
            "relationships": [],
        }
    manifest = SourceNativePilotManifest.model_validate(
        json.loads(manifest_path.read_text(encoding="utf-8"))
    )
    for name, expected in manifest.file_hashes.items():
        actual = sha256_file(destination / name)
        if actual != expected:
            raise ValueError(
                f"source-native pilot hash mismatch for {name}: "
                f"expected {expected}, got {actual}"
            )
    return {
        "source_snapshots": [
            SourceSnapshot.model_validate(row)
            for row in read_jsonl(destination / "source-snapshots.jsonl")
        ],
        "source_units": [
            SourceUnit.model_validate(row)
            for row in read_jsonl(destination / "source-units.jsonl")
        ],
        "generation_activities": [
            GenerationActivity.model_validate(row)
            for row in read_jsonl(destination / "generation-activities.jsonl")
        ],
        "reviewed_artifacts": [
            ReviewedSourceNativeArtifact.model_validate(row)
            for row in read_jsonl(destination / "reviewed-artifacts.jsonl")
        ],
        "relationships": [
            KnowledgeRelationship.model_validate(row)
            for row in read_jsonl(destination / "relationships.jsonl")
        ],
    }


def source_native_evaluation_rows(
    repo_root: Path = REPO_ROOT,
) -> list[dict[str, Any]]:
    destination = repo_root / "canonical" / "source-native" / "v1"
    return [
        *read_jsonl(destination / "evaluation-set.jsonl"),
        *read_jsonl(destination / "evaluation-holdout.jsonl"),
    ]


def canonical_records_for_source_native_artifacts(
    reviewed_artifacts: Iterable[ReviewedSourceNativeArtifact],
) -> tuple[list[KnowledgeUnit], list[EvidenceLink]]:
    knowledge_units: list[KnowledgeUnit] = []
    evidence_links: list[EvidenceLink] = []
    for reviewed in reviewed_artifacts:
        artifact = reviewed.artifact
        payload = {
            "schema": "rock-kb-source-native-artifact-payload-v1",
            "source_candidate_id": reviewed.source_candidate_id,
            "artifact": artifact.public_dump(),
            "review": {
                "review_state": reviewed.review_state,
                "reviewed_at": reviewed.reviewed_at,
                "reviewer": reviewed.reviewer,
                "review_notes": reviewed.review_notes,
                "source_input_hash": reviewed.source_input_hash,
            },
        }
        knowledge_type = artifact.artifact_type
        content_hash = sha256_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        knowledge_units.append(
            KnowledgeUnit(
                schema="rock-kb-knowledge-unit-v1",
                knowledge_unit_id=reviewed.artifact_id,
                knowledge_type=knowledge_type,
                ingestion_mode="source_native_distillation",
                title=artifact.title,
                retrieval_text=artifact.retrieval_text,
                concept_facets=artifact.concept_ids,
                authority_tiers=["official"],
                claim_tier="source_backed",
                review_state=reviewed.review_state,
                rock_versions=artifact.rock_versions,
                version_scope_status=artifact.version_scope_status,
                source_unit_ids=artifact.source_unit_ids,
                generation_activity_ids=[reviewed.generation_activity_id],
                created_at=reviewed.reviewed_at,
                reviewed_at=reviewed.reviewed_at,
                content_changed_at=reviewed.reviewed_at,
                payload_schema="rock-kb-source-native-artifact-payload-v1",
                payload=payload,
                content_hash=content_hash,
            )
        )
        for source_unit_id in artifact.source_unit_ids:
            link_id = "evidence:" + sha256_text(
                f"{reviewed.artifact_id}:{source_unit_id}:supports"
            )[:24]
            evidence_links.append(
                EvidenceLink(
                    schema="rock-kb-evidence-link-v1",
                    evidence_link_id=link_id,
                    knowledge_unit_id=reviewed.artifact_id,
                    source_unit_id=source_unit_id,
                    relation="supports",
                    evidence_summary=artifact.rationale[:1500],
                    authority_tier="official",
                    confidence=artifact.confidence,
                    independence_group=reviewed.source_candidate_id,
                    needs_review=False,
                )
            )
    return knowledge_units, evidence_links


def build_source_native_impact_report(
    *,
    previous_dir: Path,
    current_dir: Path,
) -> dict[str, Any]:
    previous = source_native_dependency_state(previous_dir)
    current = source_native_dependency_state(current_dir)
    all_locators = sorted(set(previous["units"]) | set(current["units"]))
    added: list[str] = []
    removed: list[str] = []
    changed: list[str] = []
    relocated: list[str] = []
    unchanged: list[str] = []
    impacted_unit_ids: set[str] = set()
    for locator in all_locators:
        before = previous["units"].get(locator)
        after = current["units"].get(locator)
        if before is None:
            added.append(locator)
            impacted_unit_ids.add(str(after["source_unit_id"]))
        elif after is None:
            removed.append(locator)
            impacted_unit_ids.add(str(before["source_unit_id"]))
        elif before.get("normalized_content_hash") != after.get(
            "normalized_content_hash"
        ):
            changed.append(locator)
            impacted_unit_ids.update(
                {
                    str(before["source_unit_id"]),
                    str(after["source_unit_id"]),
                }
            )
        elif before.get("source_unit_id") != after.get("source_unit_id"):
            relocated.append(locator)
            impacted_unit_ids.update(
                {
                    str(before["source_unit_id"]),
                    str(after["source_unit_id"]),
                }
            )
        else:
            unchanged.append(locator)
    record_added: list[str] = []
    record_removed: list[str] = []
    routing_changed: list[str] = []
    revision_changed: list[str] = []
    for record_key in sorted(set(previous["records"]) | set(current["records"])):
        before = previous["records"].get(record_key)
        after = current["records"].get(record_key)
        if before is None:
            record_added.append(record_key)
            impacted_unit_ids.update(after["source_unit_ids"])
            continue
        if after is None:
            record_removed.append(record_key)
            impacted_unit_ids.update(before["source_unit_ids"])
            continue
        if before["routing_signature"] != after["routing_signature"]:
            routing_changed.append(record_key)
            impacted_unit_ids.update(before["source_unit_ids"])
            impacted_unit_ids.update(after["source_unit_ids"])
        if before["revision_signature"] != after["revision_signature"]:
            revision_changed.append(record_key)
            impacted_unit_ids.update(before["source_unit_ids"])
            impacted_unit_ids.update(after["source_unit_ids"])
    impacted_artifacts = sorted(
        artifact_id
        for artifact_id, source_ids in current["dependencies"].items()
        if set(source_ids) & impacted_unit_ids
    )
    removed_artifacts = sorted(
        artifact_id
        for artifact_id, source_ids in previous["dependencies"].items()
        if artifact_id not in current["dependencies"]
        or set(source_ids) & impacted_unit_ids
    )
    return {
        "schema": "rock-kb-source-native-impact-report-v1",
        "status": (
            "changed"
            if (
                added
                or removed
                or changed
                or relocated
                or record_added
                or record_removed
                or routing_changed
                or revision_changed
            )
            else "unchanged"
        ),
        "source_records": {
            "added": record_added,
            "removed": record_removed,
            "routing_changed": routing_changed,
            "revision_changed": revision_changed,
        },
        "source_units": {
            "added": added,
            "removed": removed,
            "changed": changed,
            "relocated": relocated,
            "unchanged_count": len(unchanged),
        },
        "revalidation_queue": {
            "knowledge_unit_ids": impacted_artifacts,
            "removed_or_prior_knowledge_unit_ids": removed_artifacts,
            "projection_targets": (
                ["canonical_search", "guides", "mcp", "cli", "okf"]
                if impacted_artifacts or removed_artifacts
                else []
            ),
        },
    }


def source_native_dependency_state(destination: Path) -> dict[str, Any]:
    snapshots = {
        str(row.get("source_snapshot_id") or ""): row
        for row in read_jsonl(destination / "source-snapshots.jsonl")
    }
    records: dict[str, dict[str, Any]] = {}
    units: dict[str, dict[str, Any]] = {}
    for row in read_jsonl(destination / "source-units.jsonl"):
        snapshot = snapshots.get(str(row.get("source_snapshot_id") or ""), {})
        record_key = "|".join(
            [
                str(snapshot.get("source_id") or ""),
                str(
                    snapshot.get("source_work_id")
                    or snapshot.get("source_record_id")
                    or snapshot.get("source_snapshot_id")
                    or ""
                ),
            ]
        )
        record = records.setdefault(
            record_key,
            {
                "routing_signature": [
                    str(snapshot.get("source_record_id") or ""),
                    str(snapshot.get("canonical_url") or ""),
                    str(snapshot.get("source_path") or ""),
                    sorted(str(value) for value in snapshot.get("routing_paths") or []),
                    sorted(str(value) for value in snapshot.get("location_aliases") or []),
                ],
                "revision_signature": [
                    str(snapshot.get("upstream_revision") or ""),
                    bool(snapshot.get("immutable")),
                ],
                "source_unit_ids": [],
            },
        )
        record["source_unit_ids"].append(str(row.get("source_unit_id") or ""))
        locator = row.get("locator") or {}
        key = "|".join(
            [
                record_key,
                str(locator.get("kind") or ""),
                str(locator.get("value") or ""),
            ]
        )
        units[key] = row
    dependencies = {
        str(row.get("artifact_id") or ""): list(
            ((row.get("artifact") or {}).get("source_unit_ids") or [])
        )
        for row in read_jsonl(destination / "reviewed-artifacts.jsonl")
        if row.get("artifact_id")
    }
    return {"records": records, "units": units, "dependencies": dependencies}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
