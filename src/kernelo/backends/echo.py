from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

from .base import Backend, Message


class EchoBackend(Backend):
    """Offline backend for testing the UI."""

    name = "echo"

    async def stream(self, messages: list[Message]) -> AsyncIterator[str]:
        reply = f"**Echo:** {messages[-1]['content']}\n\n*(set CHAT_MODEL to talk to a real model)*"
        for word in reply.split(" "):
            await asyncio.sleep(0.03)
            yield word + " "
