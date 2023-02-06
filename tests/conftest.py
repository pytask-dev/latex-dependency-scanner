"""Configuration file for pytest."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest


needs_latexmk = pytest.mark.skipif(
    shutil.which("latexmk") is None, reason="latexmk needs to be installed.",
)


TEST_RESOURCES = Path(__file__).parent / "resources"
