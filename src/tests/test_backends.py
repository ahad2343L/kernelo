import pytest

from kernelo.backends import build_backend
from kernelo.backends.base import Backend
from kernelo.backends.echo import EchoBackend
from kernelo.backends.ollama import OllamaBackend
from kernelo.backends.openai_compat import OpenAICompatBackend
from kernelo.config import Settings


def test_build_backend_ollama():
    backend = build_backend(Settings(model="llama3"))
    assert isinstance(backend, OllamaBackend)
    assert backend.name == "ollama:llama3"


def test_build_backend_openai():
    backend = build_backend(Settings(base_url="http://localhost:8000/v1", model="gpt-4o"))
    assert isinstance(backend, OpenAICompatBackend)
    assert backend.name == "openai-compat:gpt-4o"


def test_build_backend_echo():
    backend = build_backend(Settings(backend="echo"))
    assert isinstance(backend, EchoBackend)
    assert backend.name == "echo"


def test_settings_cli_args():
    s = Settings.from_cli_and_env(["--model", "mistral", "--backend", "echo"])
    assert s.model == "mistral"
    assert s.backend == "echo"

