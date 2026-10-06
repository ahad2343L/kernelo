from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import ChatApp


@dataclass
class Command:
    name: str
    help: str
    handler: Callable[[str], None]


def build_commands(app: "ChatApp") -> dict[str, Command]:
    """Register slash commands. Add new ones here."""

    def help_(_args: str) -> None:
        for c in app.commands.values():
            app.console.print(f"  [{app.palette.accent}]{c.name:<8}[/] {c.help}")

    def clear(_args: str) -> None:
        app.messages.clear()
        app.console.clear()
        app.print_banner()

    def exit_(_args: str) -> None:
        app.running = False

    cmds = (
        Command("/help", "Show commands", help_),
        Command("/clear", "Clear conversation", clear),
        Command("/exit", "Quit", exit_),
    )
    return {c.name: c for c in cmds}
