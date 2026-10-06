from __future__ import annotations

from ..config import Settings
from .base import Backend, Message
from .echo import EchoBackend
from .ollama import OllamaBackend
from .openai_compat import OpenAICompatBackend

__all__ = ["Backend", "Message", "EchoBackend", "OllamaBackend", "OpenAICompatBackend", "build_backend"]


def build_backend(settings: Settings) -> Backend:
    if settings.backend == "echo":
        return EchoBackend()
    if settings.base_url:
        return OpenAICompatBackend(settings.base_url, settings.model, settings.api_key)
    return OllamaBackend(settings.model, settings.ollama_host)
