from __future__ import annotations

from rich.align import Align
from rich.console import Console, Group
from rich.padding import Padding
from rich.text import Text

from .theme import Palette

LOGO_LINES = [
    "██╗  ██╗███████╗██████╗ ███╗   ██╗███████╗██╗      ██████╗ ",
    "██║ ██╔╝██╔════╝██╔══██╗████╗  ██║██╔════╝██║     ██╔═══██╗",
    "█████╔╝ █████╗  ██████╔╝██╔██╗ ██║█████╗  ██║     ██║   ██║",
    "██╔═██╗ ██╔══╝  ██╔══██╗██║╚██╗██║██╔══╝  ██║     ██║   ██║",
    "██║  ██╗███████╗██║  ██║██║ ╚████║███████╗███████╗╚██████╔╝",
    "╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝ ",
]
LOGO_WIDTH = max(len(line) for line in LOGO_LINES)


def render_banner(console: Console, model: str, cwd: str, palette: Palette) -> Padding:
    title = Text("* Welcome to Kernelo", style=f"bold {palette.accent}")

    if console.width >= LOGO_WIDTH + 4:
        art = Text()
        for line, color in zip(LOGO_LINES, palette.gradient):
            art.append(line + "\n", style=f"bold {color}")
        art.rstrip()
    else:
        art = Text("KERNELO", style=f"bold {palette.accent}")

    info = Text.assemble(
        ("model  ", "dim"), (f"{model}\n", "bold"),
        ("cwd    ", "dim"), (cwd, "bold"),
    )
    return Padding(Group(Align.left(title), Text(""), Align.left(art), Text(""), info), (1, 2))
