from __future__ import annotations

import time

from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text


class StreamView:
    """Rich renderable rebuilt on every refresh: markdown + spinner/status."""

    def __init__(self, accent: str) -> None:
        self.accent = accent
        self.buffer = ""
        self.chunks = 0
        self.done = False
        self.interrupted = False
        self.error: str | None = None
        self.start = time.monotonic()
        self.spinner = Spinner("dots", style=accent)

    def __rich__(self) -> Table:
        body = Table.grid(padding=(0, 1))
        body.add_column(width=1)
        body.add_column(ratio=1)
        body.add_row(f"[bold {self.accent}]●[/]", Markdown(self.buffer) if self.buffer else "")
        if self.interrupted:
            body.add_row("", Text("[interrupted]", style="dim italic"))
        if self.error:
            body.add_row("", Text(f"Error: {self.error}", style="bold red"))
        if not self.done:
            elapsed = time.monotonic() - self.start
            label = "Generating" if self.chunks else "Thinking"
            self.spinner.update(
                text=Text(f" {label}… ({elapsed:.0f}s · {self.chunks} chunks · ctrl+c to interrupt)", style="dim")
            )
            body.add_row("", self.spinner)
        return body
