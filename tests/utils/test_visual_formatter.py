"""Unit tests for VisualFormatter utility."""

import pytest
from src.utils.visual_formatter import (
    VisualFormatter,
    format_progress_bar,
    format_shield_badge,
)


class TestVisualFormatter:
    """Test suite for VisualFormatter."""

    def test_format_shield_badge_happy_path(self) -> None:
        """Verify standard Shields.io badge generation."""
        badge = format_shield_badge(
            label="architecture",
            value="95%",
            color="brightgreen",
        )
        assert badge == "![architecture](https://img.shields.io/badge/architecture-95%25-brightgreen)"

        badge_class = VisualFormatter.format_shield_badge("license", "MIT", "blue")
        assert badge_class == "![license](https://img.shields.io/badge/license-MIT-blue)"

    def test_format_shield_badge_spaces_and_special_chars(self) -> None:
        """Verify badge text escaping for spaces, dashes, and underscores."""
        badge = format_shield_badge(
            label="clean architecture",
            value="A-tier_grade",
            color="#2ecc71",
        )
        # spaces -> _, dashes -> --, underscores -> __, hash stripped
        assert "clean_architecture" in badge
        assert "A--tier__grade" in badge
        assert "2ecc71" in badge
        assert "#" not in badge.split("https://")[1]

    def test_format_shield_badge_none_and_edge_values(self) -> None:
        """Verify badge generation with None or numeric values."""
        badge_none = format_shield_badge(None, None, color="")  # type: ignore
        assert "![](" in badge_none
        assert "lightgrey" in badge_none

        badge_num = format_shield_badge("stars", 15000, "yellow")
        assert "stars-15000-yellow" in badge_num

    def test_format_progress_bar_happy_path(self) -> None:
        """Verify standard 10-block progress bar rendering."""
        assert format_progress_bar(80) == "████████░░ 80%"
        assert format_progress_bar(50) == "█████░░░░░ 50%"
        assert VisualFormatter.format_progress_bar(20) == "██░░░░░░░░ 20%"

    def test_format_progress_bar_boundaries(self) -> None:
        """Verify exact 0% and 100% boundary conditions."""
        assert format_progress_bar(0) == "░░░░░░░░░░ 0%"
        assert format_progress_bar(100) == "██████████ 100%"

    def test_format_progress_bar_clamping(self) -> None:
        """Verify clamping of negative or > 100% percentages."""
        assert format_progress_bar(-25) == "░░░░░░░░░░ 0%"
        assert format_progress_bar(-0.001) == "░░░░░░░░░░ 0%"
        assert format_progress_bar(125.5) == "██████████ 100%"
        assert format_progress_bar(999) == "██████████ 100%"

    def test_format_progress_bar_custom_blocks_and_chars(self) -> None:
        """Verify custom total blocks and custom glyphs."""
        # 5 blocks, 60% = 3 filled, 2 empty
        bar_5 = format_progress_bar(60, total_blocks=5, filled_char="#", empty_char="-")
        assert bar_5 == "###-- 60%"

        # Invalid total_blocks fallback to 10
        bar_invalid_blocks = format_progress_bar(70, total_blocks=-5)
        assert bar_invalid_blocks == "███████░░░ 70%"

    @pytest.mark.parametrize(
        "invalid_input",
        ["abc", None, [], {}],
    )
    def test_format_progress_bar_invalid_inputs_graceful(self, invalid_input) -> None:
        """Verify invalid non-numeric percentage falls back safely to 0%."""
        assert format_progress_bar(invalid_input) == "░░░░░░░░░░ 0%"  # type: ignore
