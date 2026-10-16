"""Deterministic visual formatting utilities for Shields.io badges and ASCII progress bars."""

import urllib.parse
from typing import Any, Union


def format_shield_badge(
    label: str,
    value: Any,
    color: str = "brightgreen",
) -> str:
    """Generate a Shields.io Markdown badge string.

    Format: ![label](https://img.shields.io/badge/<LABEL>-<VALUE>-<COLOR>)

    Args:
        label: Left-side badge label text (e.g. 'architecture')
        value: Right-side badge value text or score (e.g. '92%', 'v1.0')
        color: Badge color or hex code without hash (e.g. 'green', 'blue', 'orange', 'red')

    Returns:
        Markdown image link for the Shields.io badge.
    """
    clean_label = str(label) if label is not None else ""
    clean_value = str(value) if value is not None else ""
    clean_color = str(color).lstrip("#") if color else "lightgrey"

    # Shields.io escaping: '-' becomes '--', '_' becomes '__', space becomes '_'
    def _escape_badge_text(text: str) -> str:
        escaped = text.replace("-", "--").replace("_", "__").replace(" ", "_")
        return urllib.parse.quote(escaped, safe="@-_+/.")

    badge_label = _escape_badge_text(clean_label)
    badge_value = _escape_badge_text(clean_value)
    badge_color = urllib.parse.quote(clean_color, safe="")

    badge_url = f"https://img.shields.io/badge/{badge_label}-{badge_value}-{badge_color}"
    return f"![{clean_label}]({badge_url})"


def format_progress_bar(
    percentage: Union[int, float],
    total_blocks: int = 10,
    filled_char: str = "█",
    empty_char: str = "░",
) -> str:
    """Generate an ASCII progress bar string with clamped percentage display.

    Example:
        format_progress_bar(80) -> '████████░░ 80%'

    Args:
        percentage: Completion percentage (clamped to range [0.0, 100.0])
        total_blocks: Total block segments in the progress bar (default 10)
        filled_char: Glyph for filled segment (default '█')
        empty_char: Glyph for unfilled segment (default '░')

    Returns:
        String representing visual bar and percentage.
    """
    if total_blocks < 1:
        total_blocks = 10

    try:
        raw_val = float(percentage)
    except (TypeError, ValueError):
        raw_val = 0.0

    # Strict clamping to [0.0, 100.0]
    clamped = max(0.0, min(100.0, raw_val))
    filled_count = int(round((clamped / 100.0) * total_blocks))
    filled_count = max(0, min(total_blocks, filled_count))
    empty_count = total_blocks - filled_count

    bar_str = (filled_char * filled_count) + (empty_char * empty_count)
    return f"{bar_str} {int(round(clamped))}%"


class VisualFormatter:
    """Namespace class for formatting utilities."""

    @staticmethod
    def format_shield_badge(
        label: str,
        value: Any,
        color: str = "brightgreen",
    ) -> str:
        """Static wrapper for format_shield_badge."""
        return format_shield_badge(label=label, value=value, color=color)

    @staticmethod
    def format_progress_bar(
        percentage: Union[int, float],
        total_blocks: int = 10,
        filled_char: str = "█",
        empty_char: str = "░",
    ) -> str:
        """Static wrapper for format_progress_bar."""
        return format_progress_bar(
            percentage=percentage,
            total_blocks=total_blocks,
            filled_char=filled_char,
            empty_char=empty_char,
        )
