from __future__ import annotations

import typer

from . import (
    audit_cmds,
    claims_cmds,
    concepts_cmds,
    contribution_cmds,
    corpus_cmds,
    extract_cmds,
    lava_cmds,
    media_cmds,
    modelmap_cmds,
    private_cmds,
    publish_cmds,
    recipe_cmds,
    report_cmds,
    sources_cmds,
    tools_cmds,
    workflow_cmds,
)
from ._shared import candidate_ids_from_file, comprehensive_required_sections

app = typer.Typer(help="Rock RMS knowledge base tooling.")
workflow_cmds.register(app)
app.add_typer(sources_cmds.app, name="sources")
app.add_typer(extract_cmds.app, name="extract")
app.add_typer(lava_cmds.app, name="lava")
app.add_typer(media_cmds.app, name="media")
app.add_typer(claims_cmds.app, name="claims")
app.add_typer(corpus_cmds.app, name="corpus")
app.add_typer(private_cmds.app, name="private")
app.add_typer(contribution_cmds.app, name="contributions")
app.add_typer(concepts_cmds.app, name="concepts")
app.add_typer(modelmap_cmds.app, name="modelmap")
app.add_typer(recipe_cmds.app, name="recipes")
app.add_typer(audit_cmds.app, name="audit")
app.add_typer(publish_cmds.app, name="publish")
app.add_typer(report_cmds.app, name="report")
app.add_typer(tools_cmds.app, name="tools")

__all__ = ["app", "candidate_ids_from_file", "comprehensive_required_sections"]
