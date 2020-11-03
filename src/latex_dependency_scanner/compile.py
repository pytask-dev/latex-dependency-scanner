"""This module provides the means to compile a LaTeX document to a desired location.

The function is mainly used in testing to validate the provided examples, but can also
be used by users to compile their documents.

"""
import os
import shutil
import subprocess
from pathlib import Path
from typing import List
from typing import Optional


DEFAULT_OPTIONS = ["--pdf", "--interaction=nonstopmode", "--synctex=1", "--cd"]


def compile_pdf(
    latex_document: Path,
    compiled_document: Optional[Path] = None,
    args: Optional[List[str]] = None,
):
    """Generate a PDF from LaTeX document."""
    if shutil.which("latexmk") is None:
        raise RuntimeError("'latexmk' must be on PATH to compile a LaTeX document.")

    cmd = _prepare_cmd_options(latex_document, compiled_document, args)
    return subprocess.run(cmd, check=True)


def _prepare_cmd_options(
    latex_document: Path,
    compiled_document: Optional[Path] = None,
    args: Optional[List[str]] = None,
):
    """Prepare the command line arguments to compile the LaTeX document.

    The output folder needs to be declared as a relative path to the directory where the
    latex source lies.

    1. It must be relative because bibtex / biber, which is necessary for
       bibliographies, does not accept full paths as a safety measure.
    2. Due to the ``--cd`` flag, latexmk will change the directory to the one where the
       source files are. Thus, relative to the latex sources.

    See this `discussion on Github
    <https://github.com/James-Yu/LaTeX-Workshop/issues/1932#issuecomment-582416434>`_
    for additional information.

    """
    if compiled_document is None:
        compiled_document = latex_document.with_suffix(".pdf")

    if args is None:
        args = DEFAULT_OPTIONS.copy()

    # Jobname controls the name of the compiled document. No suffix!
    if latex_document.stem != compiled_document.stem:
        jobname = [f"--jobname={compiled_document.stem}"]
    else:
        jobname = []

    # The path to the output directory must be relative from the location of the source
    # file. See docstring for more information.
    out_relative_to_latex_source = Path(
        os.path.relpath(compiled_document.parent, latex_document.parent)
    ).as_posix()

    return (
        [
            "latexmk",
            *args,
        ]
        + jobname
        + [
            f"--output-directory={out_relative_to_latex_source}",
            latex_document.as_posix(),
        ]
    )
