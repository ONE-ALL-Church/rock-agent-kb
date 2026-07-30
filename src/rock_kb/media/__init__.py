from __future__ import annotations

import functools
import inspect
from types import ModuleType
from typing import Any, Callable

from ._shared import *  # noqa: F401,F403
from .identity import *  # noqa: F401,F403
from .discover import *  # noqa: F401,F403
from .transcribe import *  # noqa: F401,F403
from .queue import *  # noqa: F401,F403
from .sidecars import *  # noqa: F401,F403
from .review import *  # noqa: F401,F403
from .promote import *  # noqa: F401,F403
from .understanding import *  # noqa: F401,F403
from .report import *  # noqa: F401,F403
from . import _shared, identity, discover, transcribe, queue, sidecars, review, promote, understanding, report

_MODULES: tuple[ModuleType, ...] = (
    _shared,
    identity,
    discover,
    transcribe,
    queue,
    sidecars,
    review,
    promote,
    understanding,
    report,
)

_OWNER_BY_NAME: dict[str, ModuleType] = {}
_RAW_BY_NAME: dict[str, Any] = {}
for _module in _MODULES:
    for _name, _value in vars(_module).items():
        if _name.startswith("_"):
            continue
        if inspect.ismodule(_value):
            continue
        _OWNER_BY_NAME.setdefault(_name, _module)
        _RAW_BY_NAME.setdefault(_name, _value)

_WRAPPER_BY_NAME: dict[str, Callable[..., Any]] = {}


def _make_wrapper(name: str, raw: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(raw)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        _sync_public_overrides()
        return raw(*args, **kwargs)

    wrapper.__module__ = __name__
    return wrapper


for _name, _value in list(_RAW_BY_NAME.items()):
    if callable(_value):
        _wrapper = _make_wrapper(_name, _value)
        _WRAPPER_BY_NAME[_name] = _wrapper
        globals()[_name] = _wrapper
    else:
        globals()[_name] = _value


def _sync_public_overrides() -> None:
    for name, raw in _RAW_BY_NAME.items():
        public_value = globals().get(name, raw)
        owner = _OWNER_BY_NAME[name]
        is_default_wrapper = callable(raw) and public_value is _WRAPPER_BY_NAME.get(name)
        for module in _MODULES:
            if module is owner and is_default_wrapper:
                module.__dict__[name] = raw
            else:
                module.__dict__[name] = public_value


_sync_public_overrides()

__all__ = sorted(_RAW_BY_NAME)
