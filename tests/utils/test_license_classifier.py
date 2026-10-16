"""Unit tests for LicenseClassifier utility."""

import pytest
from src.utils.license_classifier import LicenseClassifier, classify_license


class TestLicenseClassifier:
    """Test suite for LicenseClassifier."""

    @pytest.mark.parametrize(
        "spdx_id,expected",
        [
            ("MIT", "PERMISSIVE"),
            ("Apache-2.0", "PERMISSIVE"),
            ("BSD-3-Clause", "PERMISSIVE"),
            ("BSD-2-Clause", "PERMISSIVE"),
            ("ISC", "PERMISSIVE"),
            ("Unlicense", "PERMISSIVE"),
            ("0BSD", "PERMISSIVE"),
            ("CC0-1.0", "PERMISSIVE"),
            ("GPL-3.0", "COPYLEFT_VIRAL"),
            ("GPL-2.0-only", "COPYLEFT_VIRAL"),
            ("AGPL-3.0", "COPYLEFT_VIRAL"),
            ("LGPL-2.1", "COPYLEFT_VIRAL"),
            ("MPL-2.0", "COPYLEFT_VIRAL"),
            ("EUPL-1.2", "COPYLEFT_VIRAL"),
            ("BSL-1.1", "COMMERCIAL_RESTRICTED"),
            ("SSPL-1.0", "COMMERCIAL_RESTRICTED"),
            ("Elastic-2.0", "COMMERCIAL_RESTRICTED"),
            ("CC-BY-NC-4.0", "COMMERCIAL_RESTRICTED"),
        ],
    )
    def test_happy_path_classifications(self, spdx_id: str, expected: str) -> None:
        """Verify accurate categorization of standard SPDX licenses."""
        assert classify_license(spdx_id) == expected
        assert LicenseClassifier.classify(spdx_id) == expected

    @pytest.mark.parametrize(
        "spdx_id,expected",
        [
            ("mit", "PERMISSIVE"),
            ("   APACHE-2.0  ", "PERMISSIVE"),
            ("gpl-3.0", "COPYLEFT_VIRAL"),
            ("GPL-3.0-with-GCC-exception", "COPYLEFT_VIRAL"),
            ("bsl-1.1-hashicorp", "COMMERCIAL_RESTRICTED"),
        ],
    )
    def test_edge_cases_casing_and_variants(self, spdx_id: str, expected: str) -> None:
        """Verify case insensitivity, whitespace trimming, and variant prefix matching."""
        assert classify_license(spdx_id) == expected

    @pytest.mark.parametrize(
        "invalid_or_unknown",
        [
            None,
            "",
            "   ",
            12345,
            [],
            "NOASSERTION",
            "CUSTOM_PROPRIETARY",
            "RandomFakeLicense-9.0",
        ],
    )
    def test_failure_unknown_and_invalid_inputs(self, invalid_or_unknown) -> None:
        """Verify unmapped, malformed, or null identifiers safely return UNKNOWN."""
        assert classify_license(invalid_or_unknown) == "UNKNOWN"
        assert LicenseClassifier.classify(invalid_or_unknown) == "UNKNOWN"
