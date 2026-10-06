from __future__ import annotations

import json
from collections.abc import AsyncIterator

import httpx

from .base import Backend, Message
from .errors import network_errors


class OpenAICompatBackend(Backend):
    """Any server speaking the OpenAI /chat/completions SSE protocol (vLLM, llama.cpp, LM Studio...)."""

    def __init__(self, base_url: str, model: str, api_key: str = "not-needed", read_timeout: float = 120.0) -> None:
        self.model = model
        self.base_url = base_url
        self.name = f"openai-compat:{model}"
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/") + "/",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=httpx.Timeout(connect=5.0, read=read_timeout, write=10.0, pool=5.0),
        )

    async def stream(self, messages: list[Message]) -> AsyncIterator[str]:
        payload = {"model": self.model, "messages": messages, "stream": True}
        with network_errors(self.base_url):
            async with self._client.stream("POST", "chat/completions", json=payload) as resp:
                if resp.status_code != 200:
                    body = (await resp.aread()).decode(errors="replace").strip()
                    raise RuntimeError(f"server {resp.status_code}: {body}")
                async for line in resp.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        return
                    chunk = json.loads(data)
                    choices = chunk.get("choices") or []
                    if choices and (content := choices[0].get("delta", {}).get("content")):
                        yield content

    async def aclose(self) -> None:
        await self._client.aclose()
