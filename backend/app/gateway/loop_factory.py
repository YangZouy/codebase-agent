"""Uvicorn loop factory that keeps asyncio subprocess support on Windows.

Problem
-------
uvicorn 0.54 picks the event loop class through ``Config.get_loop_factory``:

    Config.use_subprocess = bool(self.reload or self.workers > 1)
    asyncio_loop_factory(use_subprocess):
        win32 and not use_subprocess -> ProactorEventLoop  (subprocess OK)
        otherwise                    -> SelectorEventLoop  (subprocess NOT OK)

``make dev`` runs uvicorn with ``--reload``, so ``use_subprocess`` is True and
Windows gets ``SelectorEventLoop``. That loop has no
``_make_subprocess_transport`` implementation, so the ACP tool's
``asyncio.create_subprocess_exec`` raises a message-less ``NotImplementedError``
that surfaces as an empty error string.

Fix
---
Force ``ProactorEventLoop`` on Windows regardless of reload/workers. On POSIX
there is no change: keep uvicorn's normal auto behaviour (uvloop if installed,
otherwise the default selector loop, both of which support subprocesses).

Wiring: pass ``--loop app.gateway.loop_factory:gateway_loop_factory`` to uvicorn.
For a custom (non-builtin) loop string uvicorn imports the symbol and calls it
with no arguments, returning the loop instance — hence the no-arg signature.
"""

from __future__ import annotations

import asyncio
import sys
from collections.abc import Callable


def gateway_loop_factory() -> asyncio.AbstractEventLoop:
    """Build an event loop with subprocess support on every platform."""
    if sys.platform == "win32":
        # ProactorEventLoop implements _make_subprocess_transport; the selector
        # loop that uvicorn otherwise picks under --reload does not.
        policy = asyncio.WindowsProactorEventLoopPolicy()  # type: ignore[attr-defined]
        return policy.new_event_loop()

    # Non-Windows: mirror uvicorn's "auto" choice so behaviour is unchanged.
    loop_factory: Callable[[], asyncio.AbstractEventLoop] | None = None
    try:
        import uvloop  # type: ignore[import-not-found]

        loop_factory = uvloop.new_event_loop
    except ImportError:
        pass
    return loop_factory() if loop_factory is not None else asyncio.new_event_loop()
