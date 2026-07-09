from __future__ import annotations

from typing import Any

from . import retrieval

SERVE_EXTRA_MESSAGE = "kb serve requires the serve extra: uv sync --extra serve"


class ServeDependencyError(RuntimeError):
    pass


def build_server(fastmcp_cls: type | None = None) -> Any:
    if fastmcp_cls is None:
        try:
            from mcp.server.fastmcp import FastMCP
        except ImportError as exc:
            raise ServeDependencyError(SERVE_EXTRA_MESSAGE) from exc
        fastmcp_cls = FastMCP

    mcp = fastmcp_cls("Rock KB")

    @mcp.tool(
        name="kb_search",
        description="Full-text search across the Rock RMS knowledge base. Start here for any Rock question; results cite public sources.",
    )
    def kb_search(query: str, limit: int = 10) -> list[dict[str, Any]]:
        return retrieval.search(query, limit=limit)

    @mcp.tool(
        name="kb_get_result",
        description="Return the full public record for one exact kb_search result ID.",
    )
    def kb_get_result(id: str) -> dict[str, Any]:
        return retrieval.get_result(id)

    @mcp.tool(
        name="kb_get_claim",
        description="Return one exact approved claim by claim_id, including all concept routes.",
    )
    def kb_get_claim(claim_id: str) -> dict[str, Any]:
        return retrieval.get_claim(claim_id)

    @mcp.tool(
        name="kb_list_models",
        description="List stable Rock Model Map models with slugs, categories, versions, and counts.",
    )
    def kb_list_models() -> dict[str, Any]:
        return retrieval.list_models()

    @mcp.tool(
        name="kb_get_model",
        description="Return an exact stable Model Map digest by slug or model name, optionally filtered by fields or property.",
    )
    def kb_get_model(model: str, fields: str | None = None, property: str | None = None) -> dict[str, Any] | None:
        return retrieval.get_model(model, fields=fields, property=property)

    @mcp.tool(
        name="kb_manifest",
        description="Return the public Rock KB manifest with available entrypoints and artifact metadata.",
    )
    def kb_manifest() -> dict[str, Any]:
        return retrieval.get_manifest()

    @mcp.tool(
        name="kb_list_concepts",
        description="List public Rock KB concepts with titles, guide paths, and dependency metadata.",
    )
    def kb_list_concepts() -> list[dict[str, Any]]:
        return retrieval.list_concepts()

    @mcp.tool(
        name="kb_get_concept",
        description="Return one concept package: quickstart, answers, task cards, and release caveats.",
    )
    def kb_get_concept(concept_id: str) -> dict[str, Any]:
        return retrieval.get_concept(concept_id)

    @mcp.tool(
        name="kb_get_claims",
        description="Return approved public claims for a concept, optionally filtered by claim tier.",
    )
    def kb_get_claims(concept_id: str, tier: str | None = None) -> list[dict[str, Any]]:
        return retrieval.get_claims(concept_id, tier=tier)

    return mcp


def run_stdio() -> None:
    build_server().run()
