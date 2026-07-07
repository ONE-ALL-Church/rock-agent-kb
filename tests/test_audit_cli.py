from rock_kb.cli import audit_cmds


def test_audit_all_passes_plain_defaults_to_rockumentation_subcommand(monkeypatch):
    calls = {}

    monkeypatch.setattr(audit_cmds.legacy, "audit_licenses", lambda: None)
    monkeypatch.setattr(audit_cmds.legacy, "audit_source_url_duplicates_command", lambda: None)
    monkeypatch.setattr(audit_cmds.legacy, "audit_source_policy_command", lambda: None)
    monkeypatch.setattr(audit_cmds.legacy, "audit_public_export_command", lambda: None)
    monkeypatch.setattr(audit_cmds.legacy, "audit_readiness", lambda public_only=False: calls.setdefault("readiness", public_only))

    def fake_rockumentation_audit(probe_static=False, max_static_probes=None):
        calls["rockumentation"] = (probe_static, max_static_probes)

    monkeypatch.setattr(audit_cmds.legacy, "audit_rockumentation_api_coverage_command", fake_rockumentation_audit)

    audit_cmds.audit_all(public_only=True)

    assert calls["rockumentation"] == (False, None)
    assert calls["readiness"] is True
