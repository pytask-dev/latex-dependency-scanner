.. image:: https://img.shields.io/pypi/v/latex-dependency-scanner?color=blue
    :alt: PyPI
    :target: https://pypi.org/project/latex-dependency-scanner

.. image:: https://img.shields.io/pypi/pyversions/latex-dependency-scanner
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/latex-dependency-scanner

.. image:: https://img.shields.io/conda/vn/conda-forge/latex-dependency-scanner.svg
    :target: https://anaconda.org/conda-forge/latex-dependency-scanner

.. image:: https://img.shields.io/conda/pn/conda-forge/latex-dependency-scanner.svg
    :target: https://anaconda.org/conda-forge/latex-dependency-scanner

.. image:: https://img.shields.io/pypi/l/latex-dependency-scanner
    :alt: PyPI - License
    :target: https://pypi.org/project/latex-dependency-scanner

.. image:: https://img.shields.io/github/workflow/status/pytask-dev/latex-dependency-scanner/Continuous%20Integration%20Workflow/main
   :target: https://github.com/pytask-dev/latex-dependency-scanner/actions?query=branch%3Amain

.. image:: https://codecov.io/gh/pytask-dev/latex-dependency-scanner/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/pytask-dev/latex-dependency-scanner

.. image:: https://results.pre-commit.ci/badge/github/pytask-dev/latex-dependency-scanner/main.svg
    :target: https://results.pre-commit.ci/latest/github/pytask-dev/latex-dependency-scanner/main
    :alt: pre-commit.ci status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


Features
--------

latex-dependency-scanner is a package to detect all required files to compile a LaTeX
document.


Installation
------------

latex-dependency-scanner is available on `PyPI
<https://pypi.org/project/latex-dependency-scanner>`_ and `Anaconda.org
<https://anaconda.org/conda-forge/latex-dependency-scanner>`_. Install it with

.. code-block:: console

    $ pip install latex-dependency-scanner

    # or

    $ conda install -c conda-forge latex-dependency-scanner


Usage
-----

The package contains two functions.


Scan
~~~~

``scan()`` accepts a path-like object or a list of path-like objects which point to
``.tex`` documents. The return is a collection of paths related to this document.

.. code-block:: python

    import latex_dependency_scanner as lds


    paths = lds.scan("document.tex")

For dependencies which cannot be found and which have no file extension (like graphics
in ``\includegraphics``), all possible candidates are returned.


PDF
~~~

``generate_pdf()`` allows to conveniently generate PDFs with Python. The function is
mainly used for validating test cases.

.. code-block:: python

    import latex_dependency_scanner as lds


    lds.generate_pdf("document.tex", "document.pdf")


Changes
-------

Consult the `release notes <CHANGES.rst>`_ to find out about what is new.
