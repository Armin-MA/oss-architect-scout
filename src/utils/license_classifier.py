"""Deterministic SPDX license classification utility."""

from typing import Dict, Optional, Set

PERMISSIVE_LICENSES: Set[str] = {
    "mit",
    "apache-2.0",
    "bsd-2-clause",
    "bsd-3-clause",
    "isc",
    "unlicense",
    "cc0-1.0",
    "0bsd",
    "wtfpl",
    "zlib",
    "bsl-1.0",
    "postgresql",
    "x11",
    "mit-0",
}

COPYLEFT_VIRAL_LICENSES: Set[str] = {
    "gpl-2.0",
    "gpl-3.0",
    "gpl-2.0-only",
    "gpl-2.0-or-later",
    "gpl-3.0-only",
    "gpl-3.0-or-later",
    "agpl-1.0",
    "agpl-3.0",
    "agpl-3.0-only",
    "agpl-3.0-or-later",
    "lgpl-2.0",
    "lgpl-2.1",
    "lgpl-3.0",
    "lgpl-2.1-only",
    "lgpl-2.1-or-later",
    "lgpl-3.0-only",
    "lgpl-3.0-or-later",
    "mpl-1.1",
    "mpl-2.0",
    "epl-1.0",
    "epl-2.0",
    "eupl-1.1",
    "eupl-1.2",
    "osl-3.0",
}

COMMERCIAL_RESTRICTED_LICENSES: Set[str] = {
    "bsl-1.1",
    "busl-1.1",
    "sspl-1.0",
    "commons-clause",
    "cc-by-nc-4.0",
    "cc-by-nc-sa-4.0",
    "rsal-2.0",
    "elastic-2.0",
    "polyform-noncommercial-1.0.0",
}


def classify_license(spdx_id: Optional[str]) -> str:
    """Classify an SPDX license identifier into standard licensing categories.

    Categories:
        - PERMISSIVE: Highly permissive licenses (MIT, Apache-2.0, BSD, etc.)
        - COPYLEFT_VIRAL: Viral or reciprocal copyleft (GPL, AGPL, LGPL, MPL, etc.)
        - COMMERCIAL_RESTRICTED: Source-available or non-commercial restrictions (BSL-1.1, SSPL, etc.)
        - UNKNOWN: Unmapped, proprietary, null, or invalid licenses.

    Args:
        spdx_id: SPDX license identifier (e.g. 'MIT', 'Apache-2.0', 'GPL-3.0')

    Returns:
        One of 'PERMISSIVE', 'COPYLEFT_VIRAL', 'COMMERCIAL_RESTRICTED', 'UNKNOWN'
    """
    if not spdx_id or not isinstance(spdx_id, str):
        return "UNKNOWN"

    normalized = spdx_id.strip().lower()
    if not normalized:
        return "UNKNOWN"

    if normalized in PERMISSIVE_LICENSES:
        return "PERMISSIVE"
    if normalized in COPYLEFT_VIRAL_LICENSES:
        return "COPYLEFT_VIRAL"
    if normalized in COMMERCIAL_RESTRICTED_LICENSES:
        return "COMMERCIAL_RESTRICTED"

    # Heuristic prefix matching for version variants (e.g., GPL-3.0-with-GCC-exception)
    if normalized.startswith(("gpl", "agpl", "lgpl")):
        return "COPYLEFT_VIRAL"
    if normalized.startswith(("bsl-1.1", "busl", "elastic", "sspl")):
        return "COMMERCIAL_RESTRICTED"
    if normalized.startswith(("mit", "apache", "bsd")):
        return "PERMISSIVE"

    return "UNKNOWN"


class LicenseClassifier:
    """Namespace class for license classification operations."""

    @staticmethod
    def classify(spdx_id: Optional[str]) -> str:
        """Classify SPDX identifier using static method."""
        return classify_license(spdx_id)
