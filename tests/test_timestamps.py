from rock_kb.extract import generated_at_iso, now_iso


def test_generated_at_iso_defaults_to_current_clock(monkeypatch):
    monkeypatch.delenv("ROCK_KB_GENERATED_AT", raising=False)
    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)

    assert generated_at_iso().endswith("+00:00")
    assert len(generated_at_iso()) == len(now_iso())


def test_generated_at_iso_uses_explicit_build_timestamp(monkeypatch):
    monkeypatch.setenv("ROCK_KB_GENERATED_AT", "2026-06-10T00:00:00+00:00")
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "0")

    assert generated_at_iso() == "2026-06-10T00:00:00+00:00"


def test_generated_at_iso_supports_source_date_epoch(monkeypatch):
    monkeypatch.delenv("ROCK_KB_GENERATED_AT", raising=False)
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "0")

    assert generated_at_iso() == "1970-01-01T00:00:00+00:00"


def test_generated_at_iso_normalizes_z_suffix(monkeypatch):
    monkeypatch.setenv("ROCK_KB_GENERATED_AT", "2026-06-10T00:00:00Z")

    assert generated_at_iso() == "2026-06-10T00:00:00+00:00"
