from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    gradient: tuple[str, ...]
    accent: str


PALETTE = Palette(
    ("#a5f3fc", "#67e8f9", "#22d3ee", "#06b6d4", "#0891b2", "#0e7490"),
    "#22d3ee",
)
