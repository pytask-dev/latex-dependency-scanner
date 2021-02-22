"""The name space for the package."""
from latex_dependency_scanner.compile import compile_pdf
from latex_dependency_scanner.scanner import scan

from ._version import get_versions


__all__ = ["compile_pdf", "scan"]

__version__ = get_versions()["version"]
del get_versions
