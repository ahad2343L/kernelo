"""Runtime settings, read from environment variables.

    CHAT_MODEL      model name (default: qwen2.5:3b)
    OLLAMA_HOST     Ollama URL (default: http://localhost:11434)
    CHAT_BASE_URL   if set, use an OpenAI-compatible server (e.g. http://localhost:8000/v1)
    CHAT_API_KEY    API key for the OpenAI-compatible server
    CHAT_BACKEND    set to "echo" to test the UI without a model
"""
from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_MODEL = "qwen2.5:3b"
DEFAULT_OLLAMA_HOST = "http://localhost:11434"
HISTORY_FILE = Path.home() / ".kernelo_history"


@dataclass(frozen=True)
class Settings:
    model: str = DEFAULT_MODEL
    ollama_host: str = DEFAULT_OLLAMA_HOST
    base_url: str | None = None
    api_key: str = "not-needed"
    backend: str = ""

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model=os.getenv("CHAT_MODEL", DEFAULT_MODEL),
            ollama_host=os.getenv("OLLAMA_HOST", DEFAULT_OLLAMA_HOST),
            base_url=os.getenv("CHAT_BASE_URL") or None,
            api_key=os.getenv("CHAT_API_KEY", "not-needed"),
            backend=os.getenv("CHAT_BACKEND", "").lower(),
        )

    @classmethod
    def from_cli_and_env(cls, argv: list[str] | None = None) -> "Settings":
        parser = argparse.ArgumentParser(
            prog="kernelo",
            description="Kernelo: A terminal chat UI in the style of Claude Code.",
        )
        parser.add_argument(
            "-m", "--model",
            default=os.getenv("CHAT_MODEL", DEFAULT_MODEL),
            help=f"Model name to use (default: {DEFAULT_MODEL} or CHAT_MODEL)",
        )
        parser.add_argument(
            "-b", "--backend",
            default=os.getenv("CHAT_BACKEND", "").lower(),
            choices=["ollama", "openai", "echo", ""],
            help="Backend type ('ollama', 'openai', or 'echo')",
        )
        parser.add_argument(
            "--ollama-host",
            default=os.getenv("OLLAMA_HOST", DEFAULT_OLLAMA_HOST),
            help=f"Ollama server host (default: {DEFAULT_OLLAMA_HOST} or OLLAMA_HOST)",
        )
        parser.add_argument(
            "--base-url",
            default=os.getenv("CHAT_BASE_URL"),
            help="OpenAI-compatible server base URL (e.g. http://localhost:8000/v1)",
        )
        parser.add_argument(
            "--api-key",
            default=os.getenv("CHAT_API_KEY", "not-needed"),
            help="API key for OpenAI-compatible server (default: CHAT_API_KEY or 'not-needed')",
        )
        args = parser.parse_args(argv)
        return cls(
            model=args.model,
            ollama_host=args.ollama_host,
            base_url=args.base_url or None,
            api_key=args.api_key,
            backend=args.backend,
        )
