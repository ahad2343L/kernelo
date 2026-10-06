from __future__ import annotations

import asyncio
import os
import signal
from dataclasses import dataclass, field

from prompt_toolkit import PromptSession
from rich.console import Console
from rich.live import Live
from rich.rule import Rule

from .backends import Backend, Message, build_backend
from .commands import Command, build_commands
from .config import Settings
from .ui import PALETTE, Palette, StreamView, build_session, render_banner


@dataclass
class ChatApp:
    backend: Backend
    palette: Palette = PALETTE
    console: Console = field(default_factory=Console)
    messages: list[Message] = field(default_factory=list)
    running: bool = True
    commands: dict[str, Command] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.commands = build_commands(self)
        self.session: PromptSession = build_session(self.commands, lambda: self.backend.name)

    # --- UI helpers ---
    def print_banner(self) -> None:
        self.console.print(render_banner(self.console, self.backend.name, os.getcwd(), self.palette))

    def _prompt_message(self) -> list[tuple[str, str]]:
        return [(f"fg:{self.palette.accent} bold", "> ")]

    # --- generation ---
    async def _consume(self, view: StreamView) -> None:
        async for token in self.backend.stream(self.messages):
            view.buffer += token
            view.chunks += 1

    async def respond(self) -> None:
        view = StreamView(self.palette.accent)
        loop = asyncio.get_running_loop()
        with Live(view, console=self.console, refresh_per_second=12, vertical_overflow="visible"):
            task = asyncio.create_task(self._consume(view))
            sigint_installed = False
            try:  # Ctrl+C cancels only the generation, not the app (Unix only)
                loop.add_signal_handler(signal.SIGINT, task.cancel)
                sigint_installed = True
            except (NotImplementedError, RuntimeError):
                pass
            try:
                await task
            except asyncio.CancelledError:
                view.interrupted = True
            except Exception as exc:  # surface backend errors without crashing
                view.error = str(exc)
            finally:
                if sigint_installed:
                    loop.remove_signal_handler(signal.SIGINT)
                view.done = True

        if view.buffer:
            self.messages.append({"role": "assistant", "content": view.buffer})
        elif self.messages:
            self.messages.pop()  # drop the unanswered user turn to keep history consistent

    # --- main loop ---
    async def run(self) -> None:
        self.print_banner()
        while self.running:
            self.console.print(Rule(style="dim"))
            try:
                text = (await self.session.prompt_async(self._prompt_message())).strip()
            except KeyboardInterrupt:
                self.console.print("[dim](ctrl+d or /exit to quit)[/]")
                continue
            except EOFError:
                break
            if not text:
                continue
            if text.startswith("/"):
                name, _, args = text.partition(" ")
                if cmd := self.commands.get(name):
                    cmd.handler(args)
                else:
                    self.console.print(f"[red]Unknown command:[/] {name}")
                continue
            self.messages.append({"role": "user", "content": text})
            await self.respond()


async def main() -> None:
    backend = build_backend(Settings.from_cli_and_env())
    try:
        await ChatApp(backend=backend).run()
    finally:
        await backend.aclose()
