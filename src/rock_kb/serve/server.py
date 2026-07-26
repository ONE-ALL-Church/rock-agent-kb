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
        name="kb_list_lava_contexts",
        description="List known Lava rendering surfaces with exact context IDs, coverage, versions, and root counts.",
    )
    def kb_list_lava_contexts(
        context_family: str | None = None,
        surface_type: str | None = None,
    ) -> dict[str, Any]:
        return retrieval.list_lava_contexts(context_family=context_family, surface_type=surface_type)

    @mcp.tool(
        name="kb_get_lava_context",
        description="Return one exact Lava rendering surface with all direct and inherited roots, conditions, model links, source pins, and completeness metadata.",
    )
    def kb_get_lava_context(context_id: str, root_key: str | None = None) -> dict[str, Any]:
        return retrieval.get_lava_context(context_id, root_key=root_key)

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

    @mcp.tool(
        name="kb_list_recipes",
        description="List reusable community Rock recipes, optionally filtered by concept.",
    )
    def kb_list_recipes(concept_id: str | None = None) -> dict[str, Any]:
        return retrieval.list_recipes(concept_id=concept_id)

    @mcp.tool(
        name="kb_get_recipe",
        description="Return one exact recipe with source pin, adaptation points, security, compatibility, validation, and reusable learnings.",
    )
    def kb_get_recipe(recipe_id: str) -> dict[str, Any]:
        return retrieval.get_recipe(recipe_id)

    @mcp.tool(
        name="kb_search_rock_issues",
        description="Search public Rock core and mobile issue routing metadata. Reports are leads, not proof of local impact.",
    )
    def kb_search_rock_issues(query: str, limit: int = 10) -> dict[str, Any]:
        return retrieval.search_rock_issues(query, limit=limit)

    @mcp.tool(
        name="kb_list_rock_issues",
        description="List Rock issues by repository, state, concept, or version evidence.",
    )
    def kb_list_rock_issues(
        repository: str | None = None,
        state: str | None = None,
        concept: str | None = None,
        version: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        return retrieval.list_rock_issues(repository, state, concept, version, limit, offset)

    @mcp.tool(
        name="kb_get_rock_issue",
        description="Get one exact Rock issue by GitHub URL, canonical ID, core number, or mobile:number.",
    )
    def kb_get_rock_issue(issue: str) -> dict[str, Any]:
        return retrieval.get_rock_issue(issue)

    @mcp.tool(
        name="kb_assess_rock_issues",
        description="Conservatively route an explicit open, historical-unresolved, or all-relevant issue population against a bounded profile. Never provide logs, identifiers, or person data.",
    )
    def kb_assess_rock_issues(
        profile: dict[str, Any],
        scope: str = "open",
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        return retrieval.assess_rock_issues(profile, scope=scope, limit=limit, offset=offset)

    @mcp.tool(
        name="kb_plan_rock_issue_investigation",
        description="Return a typed read-only multi-agent investigation plan. It never posts to GitHub.",
    )
    def kb_plan_rock_issue_investigation(issue: str, include_private_instance: bool = False) -> dict[str, Any]:
        return retrieval.plan_rock_issue_investigation(issue, include_private_instance=include_private_instance)

    return mcp


def run_stdio() -> None:
    build_server().run()
