"""The name space for the package."""
from latex_dependency_scanner.compile import compile_pdf
from latex_dependency_scanner.scanner import scan

try:
    from ._version import version as __version__
except ImportError:
    # broken installation, we don't even try unknown only works because we do poor mans
    # version compare
    __version__ = "unknown"


__all__ = ["__version__", "compile_pdf", "scan"]
