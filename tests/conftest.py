"""Configuration file for pytest."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

needs_latexmk = pytest.mark.skipif(
    shutil.which("latexmk") is None, reason="latexmk needs to be installed."
)


def _has_tex_file(name: str) -> bool:
    kpsewhich = shutil.which("kpsewhich")
    if kpsewhich is None:
        return False
    result = subprocess.run(  # noqa: S603
        [kpsewhich, name],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and bool(result.stdout.strip())


needs_import_sty = pytest.mark.skipif(
    not _has_tex_file("import.sty"), reason="import.sty needs to be installed."
)

needs_biblatex_sty = pytest.mark.skipif(
    not _has_tex_file("biblatex.sty"), reason="biblatex.sty needs to be installed."
)


TEST_RESOURCES = Path(__file__).parent / "resources"
