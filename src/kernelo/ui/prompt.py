from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Protocol

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings

from ..config import HISTORY_FILE


class _HasHelp(Protocol):
    help: str


class SlashCompleter(Completer):
    def __init__(self, commands: Mapping[str, _HasHelp]) -> None:
        self.commands = commands

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if text.startswith("/") and " " not in text:
            for name, cmd in self.commands.items():
                if name.startswith(text):
                    yield Completion(name, start_position=-len(text), display_meta=cmd.help)


def build_keybindings() -> KeyBindings:
    """Enter submits (or accepts a highlighted completion); Alt+Enter inserts a newline."""
    kb = KeyBindings()

    @kb.add("enter")
    def _submit(event):
        buf = event.current_buffer
        state = buf.complete_state
        if state and state.current_completion:
            buf.apply_completion(state.current_completion)
        else:
            buf.validate_and_handle()

    @kb.add("escape", "enter")
    def _newline(event):
        event.current_buffer.insert_text("\n")

    return kb


def build_session(commands: Mapping[str, _HasHelp], backend_name: Callable[[], str]) -> PromptSession:
    return PromptSession(
        history=FileHistory(str(HISTORY_FILE)),
        completer=SlashCompleter(commands),
        complete_while_typing=True,
        multiline=True,
        key_bindings=build_keybindings(),
        bottom_toolbar=lambda: [("", f" {backend_name()} · enter: send · alt+enter: newline · /help")],
    )
