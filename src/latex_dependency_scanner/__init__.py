"""The name space for the package."""
from latex_dependency_scanner.compile import compile_pdf
from latex_dependency_scanner.scanner import scan

__version__ = "0.0.1"
__all__ = ["compile_pdf", "scan"]
