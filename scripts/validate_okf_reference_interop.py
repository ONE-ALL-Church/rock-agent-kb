#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath


UPSTREAM_REPOSITORY = "https://github.com/GoogleCloudPlatform/knowledge-catalog.git"
UPSTREAM_COMMIT = "3fcbb9f828c2f23d109c855ee403c3a4c81f3a96"
RESERVED = {"index.md", "log.md"}
CLIENT_SOURCE = Path(__file__).resolve().parents[1] / "clients" / "python" / "src"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the official OKF reference parser against a Rock KB bundle.")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--upstream-dir", type=Path)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="rock-kb-okf-interop-") as temporary:
        work = Path(temporary)
        bundle_root = materialize_bundle(args.bundle.resolve(), work / "bundle")
        upstream = args.upstream_dir.resolve() if args.upstream_dir else checkout_upstream(work / "upstream")
        report = validate_reference_interop(bundle_root, upstream)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["status"] == "ok" else 1


def validate_reference_interop(bundle_root: Path, upstream: Path) -> dict:
    reference_src = upstream / "okf" / "src"
    if not reference_src.exists():
        raise RuntimeError(f"Official OKF reference source not found: {reference_src}")
    sys.path.insert(0, str(reference_src))
    generator = importlib.import_module("reference_agent.viewer.generator")
    concepts = generator._walk_concepts(bundle_root)
    graph = generator._build_graph(concepts)

    expected = {
        path.relative_to(bundle_root).with_suffix("").as_posix()
        for path in bundle_root.rglob("*.md")
        if path.name not in RESERVED
    }
    parsed_concepts = [
        concept
        for concept in concepts
        if PurePosixPath(str(concept.id)).name not in {"index", "log"}
    ]
    parsed = {str(concept.id) for concept in parsed_concepts}
    missing = sorted(expected - parsed)
    edge_count = len(graph["edges"])
    generated_documents = sum(
        1
        for concept in parsed_concepts
        if isinstance(concept.generated, dict)
        and concept.generated.get("by")
        and concept.generated.get("at")
    )
    sourced_documents = sum(1 for concept in parsed_concepts if concept.sources)
    complete_v02_provenance = (
        generated_documents == len(expected)
        and sourced_documents == len(expected)
    )
    return {
        "schema": "rock-kb-okf-reference-interop-v1",
        "status": "ok" if not missing and edge_count and complete_v02_provenance else "failed",
        "upstream_commit": UPSTREAM_COMMIT,
        "expected_documents": len(expected),
        "parsed_documents": len(parsed),
        "graph_nodes": len(graph["nodes"]),
        "graph_edges": edge_count,
        "generated_documents": generated_documents,
        "sourced_documents": sourced_documents,
        "missing_documents": missing[:50],
    }


def materialize_bundle(source: Path, destination: Path) -> Path:
    if source.is_dir():
        return source
    sys.path.insert(0, str(CLIENT_SOURCE))
    from rock_kb_client.okf import read_bundle

    files = read_bundle(source)
    destination.mkdir(parents=True)
    for relative, content in files.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    return destination


def checkout_upstream(destination: Path) -> Path:
    subprocess.run(["git", "init", "--quiet", str(destination)], check=True)
    subprocess.run(["git", "-C", str(destination), "remote", "add", "origin", UPSTREAM_REPOSITORY], check=True)
    subprocess.run(
        ["git", "-C", str(destination), "fetch", "--quiet", "--depth", "1", "origin", UPSTREAM_COMMIT],
        check=True,
    )
    subprocess.run(["git", "-C", str(destination), "checkout", "--quiet", "FETCH_HEAD"], check=True)
    return destination


if __name__ == "__main__":
    raise SystemExit(main())
