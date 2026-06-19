from __future__ import annotations

import typer

from . import _legacy as legacy

app = typer.Typer(help="Audit commands.")

app.command("guide")(legacy.audit_guide_command)
app.command("licenses")(legacy.audit_licenses)
app.command("source-url-duplicates")(legacy.audit_source_url_duplicates_command)
app.command("source-policy")(legacy.audit_source_policy_command)
app.command("public-export")(legacy.audit_public_export_command)
app.command("readiness")(legacy.audit_readiness)


@app.command("all")
def audit_all(
    public_only: bool = typer.Option(False, "--public-only", help="Pass --public-only through to readiness audit."),
) -> None:
    """Run licenses, source-policy, public-export, and readiness audits in sequence."""
    legacy.audit_licenses()
    legacy.audit_source_url_duplicates_command()
    legacy.audit_source_policy_command()
    legacy.audit_public_export_command()
    legacy.audit_readiness(public_only=public_only)
