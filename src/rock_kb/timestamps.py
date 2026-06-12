from __future__ import annotations

import os
from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def generated_at_iso() -> str:
    fixed_value = os.environ.get("ROCK_KB_GENERATED_AT") or os.environ.get("SOURCE_DATE_EPOCH")
    if not fixed_value:
        return now_iso()
    if fixed_value.isdigit():
        return datetime.fromtimestamp(int(fixed_value), tz=timezone.utc).replace(microsecond=0).isoformat()
    return fixed_value.replace("Z", "+00:00")
