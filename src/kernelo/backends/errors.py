from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

import httpx


@contextmanager
def network_errors(target: str) -> Iterator[None]:
    """Translate low-level httpx errors into readable RuntimeErrors."""
    try:
        yield
    except httpx.ConnectError as exc:
        raise RuntimeError(f"Cannot reach {target}. Is the server running?") from exc
    except httpx.ReadTimeout as exc:
        raise RuntimeError("The server stopped responding (read timeout).") from exc
    except httpx.RemoteProtocolError as exc:
        raise RuntimeError(f"Connection to {target} closed unexpectedly.") from exc
