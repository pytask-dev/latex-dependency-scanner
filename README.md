[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/latex-dependency-scanner)](https://pypi.org/project/latex-dependency-scanner)
[![image](https://img.shields.io/conda/vn/conda-forge/latex-dependency-scanner.svg)](https://anaconda.org/conda-forge/latex-dependency-scanner)
[![image](https://img.shields.io/conda/pn/conda-forge/latex-dependency-scanner.svg)](https://anaconda.org/conda-forge/latex-dependency-scanner)
[![PyPI - License](https://img.shields.io/pypi/l/latex-dependency-scanner)](https://pypi.org/project/latex-dependency-scanner)
[![image](https://img.shields.io/github/actions/workflow/status/pytask-dev/latex-dependency-scanner/main.yml?branch=main)](https://github.com/pytask-dev/latex-dependency-scanner/actions?query=branch%3Amain)
[![image](https://codecov.io/gh/pytask-dev/latex-dependency-scanner/branch/main/graph/badge.svg)](https://app.codecov.io/gh/pytask-dev/latex-dependency-scanner)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pytask-dev/latex-dependency-scanner/main.svg)](https://results.pre-commit.ci/latest/github/pytask-dev/latex-dependency-scanner/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Features

latex-dependency-scanner is a package to detect all required files to compile a LaTeX
document.

# Installation

latex-dependency-scanner is available on
[PyPI](https://pypi.org/project/latex-dependency-scanner) and
[Anaconda.org](https://anaconda.org/conda-forge/latex-dependency-scanner). Install it
with

```console
$ pip install latex-dependency-scanner

# or

$ conda install -c conda-forge latex-dependency-scanner
```

# Usage

The package contains two functions.

## Scan

`scan()` accepts a path-like object or a list of path-like objects which point to `.tex`
documents. The return is a collection of paths related to this document.

```python
import latex_dependency_scanner as lds


paths = lds.scan("document.tex")
```

For dependencies which cannot be found and which have no file extension (like graphics
in `\includegraphics`), all possible candidates are returned.

## PDF

`compile_pdf()` allows to conveniently generate PDFs with Python. The function is mainly
used for validating test cases.

```python
import latex_dependency_scanner as lds


lds.compile_pdf("document.tex", "document.pdf")
```

# Changes

Consult the [release notes](CHANGES.md) to find out about what is new.
