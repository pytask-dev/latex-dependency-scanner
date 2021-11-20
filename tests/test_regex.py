"""Test regular expressions."""
import pytest
from latex_dependency_scanner.scanner import REGEX_TEX


@pytest.mark.unit
@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "\\usepackage{geometry}",
            {"type": "usepackage", "file": "geometry", "relative_to": None},
        ),
        ("\\usepackage{}", {"type": "usepackage", "file": "", "relative_to": None}),
        ("\\usepackages{geometry}", None),
        ("\\usepackage", None),
        (
            "\\RequirePackage{geometry}",
            {"type": "RequirePackage", "file": "geometry", "relative_to": None},
        ),
        (
            "\\RequirePackage{}",
            {"type": "RequirePackage", "file": "", "relative_to": None},
        ),
        ("\\RequirePackages{geometry}", None),
        ("\\RequirePackage", None),
        (
            "\\input{document}",
            {"type": "input", "file": "document", "relative_to": None},
        ),
        (
            "\\import{./}{document}",
            {"type": "import", "file": "document", "relative_to": "./"},
        ),
        (
            "\\subimport{sub/}{document}",
            {"type": "subimport", "file": "document", "relative_to": "sub/"},
        ),
        (
            "\\includegraphics{image}",
            {"type": "includegraphics", "file": "image", "relative_to": None},
        ),
        (
            "\\includegraphics{image.pdf}",
            {"type": "includegraphics", "file": "image.pdf", "relative_to": None},
        ),
        (
            "\\includegraphics{image.eps}",
            {"type": "includegraphics", "file": "image.eps", "relative_to": None},
        ),
        (
            "\\bibliography{bibfile}",
            {"type": "bibliography", "file": "bibfile", "relative_to": None},
        ),
        ("\\bibliographystyle{plain}", None),
        (
            "\\addbibresource{bibfile}",
            {"type": "addbibresource", "file": "bibfile", "relative_to": None},
        ),
        (
            "\\glsxtrresourcefile{glsfile}",
            {"type": "glsxtrresourcefile", "file": "glsfile", "relative_to": None},
        ),
        (
            "\\GlsXtrLoadResources[src={glsfile}, selection={all}]",
            {"type": "GlsXtrLoadResources", "file": "glsfile", "relative_to": None},
        ),
    ],
)
def test_regex_tex(text, expected):
    """Test that regexes capture relevant information."""
    match = REGEX_TEX.match(text)
    if expected is None:
        assert match is expected
    else:
        assert match.groupdict() == expected
