from __future__ import annotations

import json
from pathlib import Path

import typer

from ..recipes import build_recipes, check_recipe_upstreams, load_recipes, promote_recipe_contribution


app = typer.Typer(help="Validate, build, inspect, and check community recipes.")


@app.command("validate")
def validate_recipes() -> None:
    rows = load_recipes()
    typer.echo(json.dumps({"status": "ok", "recipe_count": len(rows)}, indent=2))


@app.command("build")
def build_recipe_artifacts() -> None:
    typer.echo(json.dumps(build_recipes(), indent=2, sort_keys=True))


@app.command("list")
def list_recipes() -> None:
    rows = load_recipes()
    typer.echo(json.dumps([{"recipe_id": row["recipe_id"], "title": row["title"], "version": row["version"]} for row in rows], indent=2))


@app.command("get")
def get_recipe(recipe_id: str) -> None:
    row = next((row for row in load_recipes() if row["recipe_id"] == recipe_id), None)
    if row is None:
        raise typer.BadParameter(f"unknown recipe_id: {recipe_id}")
    typer.echo(json.dumps(row, indent=2, sort_keys=True))


@app.command("check-upstream")
def check_upstream() -> None:
    typer.echo(json.dumps(check_recipe_upstreams(), indent=2, sort_keys=True))


@app.command("promote")
def promote_recipe(bundle: Path, recipe_id: str, overwrite: bool = False) -> None:
    typer.echo(json.dumps(promote_recipe_contribution(bundle, recipe_id, overwrite=overwrite), indent=2, sort_keys=True))
