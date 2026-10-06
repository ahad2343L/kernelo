from __future__ import annotations

from collections.abc import AsyncIterator

Message = dict[str, str]


class Backend:
    name = "base"

    async def stream(self, messages: list[Message]) -> AsyncIterator[str]:
        raise NotImplementedError
        yield  # pragma: no cover  (makes this an async generator)

    async def aclose(self) -> None:
        return None
