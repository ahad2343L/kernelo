import asyncio

from kernelo.backends import EchoBackend, build_backend
from kernelo.config import Settings


def test_echo_streams_reply():
    async def collect():
        return "".join([t async for t in EchoBackend().stream([{"role": "user", "content": "hi"}])])

    assert "Echo:" in asyncio.run(collect())


def test_build_backend_selects_echo():
    assert build_backend(Settings(backend="echo")).name == "echo"


def test_build_backend_defaults_to_ollama():
    assert build_backend(Settings(model="x")).name == "ollama:x"
