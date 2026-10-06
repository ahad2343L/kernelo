from __future__ import annotations

import json
from collections.abc import AsyncIterator

import httpx

from .base import Backend, Message
from .errors import network_errors


class OllamaBackend(Backend):
    def __init__(self, model: str, host: str = "http://localhost:11434", read_timeout: float = 120.0) -> None:
        self.model = model
        self.host = host
        self.name = f"ollama:{model}"
        self._client = httpx.AsyncClient(
            base_url=host,
            timeout=httpx.Timeout(connect=5.0, read=read_timeout, write=10.0, pool=5.0),
        )

    async def stream(self, messages: list[Message]) -> AsyncIterator[str]:
        payload = {"model": self.model, "messages": messages, "stream": True}
        with network_errors(f"Ollama at {self.host} (try `ollama serve`)"):
            async with self._client.stream("POST", "/api/chat", json=payload) as resp:
                if resp.status_code != 200:
                    body = (await resp.aread()).decode(errors="replace").strip()
                    hint = f" (try `ollama pull {self.model}`)" if resp.status_code == 404 else ""
                    raise RuntimeError(f"ollama {resp.status_code}: {body}{hint}")
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    if err := chunk.get("error"):
                        raise RuntimeError(f"ollama error: {err}")
                    if content := chunk.get("message", {}).get("content"):
                        yield content
                    if chunk.get("done"):
                        return

    async def aclose(self) -> None:
        await self._client.aclose()
