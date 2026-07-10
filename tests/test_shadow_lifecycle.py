from __future__ import annotations

from datetime import date

from rock_kb.shadow_lifecycle import instance_lifecycle


INSTANCE = {
    "id": "shadow-dev",
    "owner": "maintainers",
    "purpose": "retrieval test",
    "production_routing": False,
    "review_by": "2026-07-24",
    "expires_at": "2026-08-10",
    "expiration_action": "delete",
}


def test_shadow_lifecycle_moves_from_active_to_review_due_to_expired():
    assert instance_lifecycle(INSTANCE, date(2026, 7, 10))["status"] == "active"
    assert instance_lifecycle(INSTANCE, date(2026, 7, 24))["status"] == "review_due"
    assert instance_lifecycle(INSTANCE, date(2026, 8, 10))["status"] == "expired"


def test_shadow_lifecycle_rejects_production_routing():
    row = {**INSTANCE, "production_routing": True}

    assert instance_lifecycle(row, date(2026, 7, 10))["status"] == "invalid_production_route"
