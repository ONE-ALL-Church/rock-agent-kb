from __future__ import annotations

from typing import Any, Dict, get_args, get_origin

from pydantic import BaseModel, Field


def Private(**kwargs: Any) -> Any:
    """Marker for fields that must never appear in public artifacts."""
    extra = kwargs.pop("json_schema_extra", {}) or {}
    extra["visibility"] = "private"
    return Field(json_schema_extra=extra, **kwargs)


class KBRecord(BaseModel):
    """Base for all KB JSONL record types."""

    model_config = {"extra": "forbid"}

    def public_dump(self) -> Dict[str, Any]:
        """Serialize excluding every field marked Private."""
        return self.model_dump(exclude=_private_exclude_spec(type(self)), exclude_none=True, by_alias=True)


def _private_exclude_spec(model_type: type[BaseModel]) -> dict[str, Any]:
    spec: dict[str, Any] = {}
    for name, field in model_type.model_fields.items():
        if (field.json_schema_extra or {}).get("visibility") == "private":
            spec[name] = True
            continue
        nested = _nested_private_spec(field.annotation)
        if nested:
            spec[name] = nested
    return spec


def _nested_private_spec(annotation: Any) -> Any:
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin in (list, tuple, set, frozenset) and args:
        nested = _model_private_spec(args[0])
        if nested:
            return {"__all__": nested}
    candidates = args if origin is not None else (annotation,)
    for candidate in candidates:
        candidate_origin = get_origin(candidate)
        candidate_args = get_args(candidate)
        if candidate_origin in (list, tuple, set, frozenset) and candidate_args:
            nested = _model_private_spec(candidate_args[0])
            if nested:
                return {"__all__": nested}
        nested = _model_private_spec(candidate)
        if nested:
            return nested
    return None


def _model_private_spec(value: Any) -> dict[str, Any] | None:
    if isinstance(value, type) and issubclass(value, BaseModel):
        nested = _private_exclude_spec(value)
        return nested or None
    return None
