from rock_kb.live_verification import PROBE_DEFINITIONS


def test_mobile_checkin_probe_uses_defined_values_for_device_type():
    probe = PROBE_DEFINITIONS["mobile_checkin"]

    assert "DeviceType" not in probe["tables"]
    assert "DefinedType" in probe["tables"]
    assert "DefinedValue" in probe["tables"]
    assert "DefinedType" in probe["sql"][0]
    assert "DefinedValue" in probe["sql"][0]
