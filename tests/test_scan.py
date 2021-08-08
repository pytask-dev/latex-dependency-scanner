import shutil
import textwrap

import pytest
from conftest import needs_latexmk
from conftest import TEST_RESOURCES
from latex_dependency_scanner.compile import compile_pdf
from latex_dependency_scanner.scanner import COMMON_GRAPHICS_EXTENSIONS
from latex_dependency_scanner.scanner import scan


@needs_latexmk
@pytest.mark.end_to_end
def test_document_without_inclusions(tmp_path):
    source = r"""
    \documentclass{article}
    \begin{document}
    Hello World!
    \end{document}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    compile_pdf(tmp_path / "document.tex", tmp_path / "bld" / "document.pdf")

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [tmp_path.joinpath("document.tex")]


@needs_latexmk
@pytest.mark.end_to_end
@pytest.mark.parametrize("directive", ["include", "input"])
def test_input_or_include(tmp_path, directive):
    source = f"""
    \\documentclass{{article}}
    \\begin{{document}}
    \\{directive}{{first}}
    \\{directive}{{sub/second}}
    \\end{{document}}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    tmp_path.joinpath("first.tex").write_text("Hello World!")
    tmp_path.joinpath("sub").mkdir()
    # Include cannot be nested. Thus, only input
    tmp_path.joinpath("sub", "second.tex").write_text(r"\input{third}")
    tmp_path.joinpath("third.tex").write_text("More content.")

    compile_pdf(tmp_path / "document.tex", tmp_path / "bld" / "document.pdf")

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [
        tmp_path.joinpath("document.tex"),
        tmp_path.joinpath("first.tex"),
        tmp_path.joinpath("sub", "second.tex"),
        tmp_path.joinpath("third.tex"),
    ]


@pytest.mark.end_to_end
@pytest.mark.parametrize("directive", ["include", "input"])
def test_input_or_include_without_extension_and_file(tmp_path, directive):
    source = f"""
    \\documentclass{{article}}
    \\begin{{document}}
    \\{directive}{{first}}
    \\{directive}{{sub/second}}
    \\end{{document}}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [
        tmp_path.joinpath("document.tex"),
        tmp_path.joinpath("first.tex"),
        tmp_path.joinpath("sub", "second.tex"),
    ]


@needs_latexmk
@pytest.mark.end_to_end
@pytest.mark.parametrize("image_ext", COMMON_GRAPHICS_EXTENSIONS)
@pytest.mark.parametrize("has_extension", [True, False])
@pytest.mark.parametrize("file_exists", [True, False])
def test_includegraphics(tmp_path, image_ext, has_extension, file_exists):
    """Test includegraphics with/out extensions and if (not) the image file exists.

    Using post-script image files does not work with latexmk, since the .ps-file is
    converted to .pdf every run and latexmk will interpret it as a new file every time.
    Can be resolved by allowing pdflatex as the builder.

    """
    if image_ext == ".ps" and file_exists:
        pytest.xfail(
            ".ps does not work with latexmk: https://tex.stackexchange.com/a/67904."
        )
    if image_ext == ".eps" and file_exists:
        pytest.xfail(
            ".eps maybe needs \\graphicspath: https://tex.stackexchange.com/a/98886."
        )

    source = f"""
    \\documentclass{{article}}
    \\usepackage{{graphicx}}
    \\begin{{document}}
    \\includegraphics{{image{image_ext if has_extension else ''}}}
    \\end{{document}}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    # In case no extension is passed, we pick the pdf.
    _image_ext = image_ext if image_ext else ".pdf"

    if file_exists:
        shutil.copy(
            TEST_RESOURCES / f"image{_image_ext}", tmp_path / f"image{_image_ext}"
        )
        compile_pdf(tmp_path / "document.tex", tmp_path / "bld" / "document.pdf")

    nodes = scan(tmp_path.joinpath("document.tex"))

    expected = [tmp_path.joinpath("document.tex")]
    if has_extension or file_exists:
        expected.append(tmp_path.joinpath(f"image{_image_ext}"))
    else:
        expected.extend(
            [
                (tmp_path / "image").with_suffix(suffix)
                for suffix in COMMON_GRAPHICS_EXTENSIONS
            ]
        )

    assert nodes == expected


@pytest.mark.end_to_end
def test_includegraphics_with_beamer_overlay(tmp_path):
    source = """
    \\documentclass{{beamer}}
    \\usepackage{{graphicx}}
    \\begin{{document}}
    \\begin{{frame}}
    \\includegraphics<1>{{image.pdf}}
    \\end{{frame}}
    \\end{{document}}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [tmp_path.joinpath("document.tex"), tmp_path.joinpath("image.pdf")]


@needs_latexmk
@pytest.mark.end_to_end
def test_import(tmp_path):
    source = """
    \\documentclass{article}
    \\usepackage{import}
    \\begin{document}
    \\import{sections/}{section}
    \\end{document}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    tmp_path.joinpath("sections").mkdir()
    tmp_path.joinpath("sections", "section.tex").write_text("\\import{sub/}{content}")

    tmp_path.joinpath("sub").mkdir()
    tmp_path.joinpath("sub", "content.tex").write_text("More content.")

    compile_pdf(tmp_path / "document.tex", tmp_path / "bld" / "document.pdf")

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [
        tmp_path / "document.tex",
        tmp_path / "sections" / "section.tex",
        tmp_path / "sub" / "content.tex",
    ]


@pytest.mark.end_to_end
def test_import_without_extension_and_file(tmp_path):
    source = """
    \\documentclass{article}
    \\usepackage{import}
    \\begin{document}
    \\import{sections/}{section}
    \\end{document}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [
        tmp_path / "document.tex",
        tmp_path / "sections" / "section.tex",
    ]


@needs_latexmk
@pytest.mark.end_to_end
def test_sub_import(tmp_path):
    source = """
    \\documentclass{article}
    \\usepackage{import}
    \\begin{document}
    \\import{sections/}{section}
    \\end{document}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    tmp_path.joinpath("sections").mkdir()
    tmp_path.joinpath("sections", "section.tex").write_text(
        "\\subimport{sub/}{content}"
    )

    tmp_path.joinpath("sections", "sub").mkdir()
    tmp_path.joinpath("sections", "sub", "content.tex").write_text("More content.")

    compile_pdf(tmp_path / "document.tex", tmp_path / "bld" / "document.pdf")

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [
        tmp_path / "document.tex",
        tmp_path / "sections" / "section.tex",
        tmp_path / "sections" / "sub" / "content.tex",
    ]


@pytest.mark.end_to_end
def test_sub_import_without_extension_and_file(tmp_path):
    source = """
    \\documentclass{article}
    \\usepackage{import}
    \\begin{document}
    \\import{sections/}{section}
    \\end{document}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    tmp_path.joinpath("sections").mkdir()
    tmp_path.joinpath("sections", "section.tex").write_text(
        "\\subimport{sub/}{content}"
    )

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [
        tmp_path / "document.tex",
        tmp_path / "sections" / "section.tex",
        tmp_path / "sections" / "sub" / "content.tex",
    ]


@needs_latexmk
@pytest.mark.end_to_end
def test_mixed_import_and_subimport(tmp_path):
    """Test document with mixed import and subimport directives.

    This is the folder structure:

    TREE
    │   document.tex
    │   part-b.tex
    │
    ├───misc
    │       misc-1.tex
    │
    └───part-a
            section-1.tex
            section-2.tex

    """
    source = """
    \\documentclass{book}
    \\usepackage{import}
    \\begin{document}
    \\part{Part A}
    \\subimport{part-a/}{section-1}
    \\end{document}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    tmp_path.joinpath("part-a").mkdir()
    tmp_path.joinpath("part-a", "section-1.tex").write_text(
        "\\section{Section 1}\n\\input{section-2}\n\\subimport{../}{part-b}"
    )
    tmp_path.joinpath("part-a", "section-2.tex").write_text("\\section{Section 2}")

    tmp_path.joinpath("part-b.tex").write_text("\\part{Part B}\n\\input{misc/misc-1}")

    tmp_path.joinpath("misc").mkdir()
    tmp_path.joinpath("misc", "misc-1.tex").write_text("\\section{Misc}")

    compile_pdf(tmp_path / "document.tex")

    nodes = scan(tmp_path / "document.tex")

    assert nodes == [
        tmp_path / "document.tex",
        tmp_path / "part-a" / "section-1.tex",
        tmp_path / "part-a" / "section-2.tex",
        tmp_path / "part-b.tex",
        tmp_path / "misc" / "misc-1.tex",
    ]


@needs_latexmk
@pytest.mark.end_to_end
def test_natbib_bibliography(tmp_path):
    source = """
    \\documentclass{article}
    \\usepackage{natbib}
    \\bibliographystyle{apalike}
    \\begin{document}
    \\cite{Einstein1935}
    \\bibliography{bibliography}
    \\end{document}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))
    shutil.copy(TEST_RESOURCES / "bibliography.bib", tmp_path / "bibliography.bib")

    compile_pdf(tmp_path / "document.tex", tmp_path / "bld" / "document.pdf")

    nodes = scan(tmp_path / "document.tex")

    assert nodes == [tmp_path / "document.tex", tmp_path / "bibliography.bib"]


@pytest.mark.end_to_end
def test_natbib_bibliography_without_extension_and_file(tmp_path):
    source = """
    \\documentclass{article}
    \\usepackage{natbib}
    \\bibliographystyle{apalike}
    \\begin{document}
    \\cite{Einstein1935}
    \\bibliography{bibliography}
    \\end{document}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    nodes = scan(tmp_path / "document.tex")

    assert nodes == [tmp_path / "document.tex", tmp_path / "bibliography.bib"]


@needs_latexmk
@pytest.mark.end_to_end
def test_biblatex_bibliography(tmp_path):
    """Test document with biblatex bibliography."""
    source = """
    \\documentclass{article}
    \\usepackage{biblatex}
    \\addbibresource{bibliography.bib}
    \\begin{document}
    \\cite{Einstein1935}
    \\printbibliography
    \\end{document}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))
    shutil.copy(TEST_RESOURCES / "bibliography.bib", tmp_path / "bibliography.bib")

    compile_pdf(tmp_path / "document.tex", tmp_path / "bld" / "document.pdf")

    nodes = scan(tmp_path / "document.tex")

    assert nodes == [tmp_path / "document.tex", tmp_path / "bibliography.bib"]


@pytest.mark.end_to_end
def test_biblatex_bibliography_without_extension_and_file(tmp_path):
    """Test document without biblatex bibliography file and extension."""
    source = """
    \\documentclass{article}
    \\usepackage{biblatex}
    \\addbibresource{bibliography.bib}
    \\begin{document}
    \\cite{Einstein1935}
    \\printbibliography
    \\end{document}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    nodes = scan(tmp_path / "document.tex")

    assert nodes == [tmp_path / "document.tex", tmp_path / "bibliography.bib"]
