from __future__ import annotations

import pytest

import markupsafe


def test_escape_inner_rejects_non_str() -> None:
    """``_escape_inner`` must reject a non-str argument with a clean,
    catchable error.

    The pure-Python fallback (``_native``) raises AttributeError/TypeError
    naturally. The C extension (``_speedups``) must behave the same way
    rather than returning NULL without setting a CPython exception, which
    surfaces as a SystemError (an interpreter-level error indicating a C-API
    contract violation).

    This test runs under both backends via the autouse ``_mod`` fixture in
    ``conftest.py``.
    """
    with pytest.raises((TypeError, AttributeError)) as excinfo:
        markupsafe._escape_inner(42)  # type: ignore[attr-defined,arg-type]
    assert not isinstance(excinfo.value, SystemError)
