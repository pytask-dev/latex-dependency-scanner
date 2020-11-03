import shutil
import textwrap

import pytest
from conftest import TEST_RESOURCES
from latex_dependency_scanner.compile import generate_pdf
from latex_dependency_scanner.scanner import scan


@pytest.mark.end_to_end
def test_normal_document(tmp_path):
    source = r"""
    \documentclass{article}
    \begin{document}
    Hello World!
    \end{document}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    generate_pdf(tmp_path.joinpath("document.tex"))

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [tmp_path.joinpath("document.tex")]


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

    generate_pdf(tmp_path.joinpath("document.tex"))

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [
        tmp_path.joinpath("document.tex"),
        tmp_path.joinpath("first.tex"),
        tmp_path.joinpath("sub", "second.tex"),
        tmp_path.joinpath("third.tex"),
    ]


@pytest.mark.end_to_end
@pytest.mark.parametrize("image_ext", [".eps", ".jpeg", ".pdf", ".png"])
def test_includegraphics(tmp_path, image_ext):
    source = """
    \\documentclass{article}
    \\usepackage{graphicx}
    \\begin{document}
    \\includegraphics{image}
    \\end{document}
    """
    tmp_path.joinpath("document.tex").write_text(textwrap.dedent(source))

    shutil.copy(TEST_RESOURCES / f"image{image_ext}", tmp_path / f"image{image_ext}")

    generate_pdf(tmp_path.joinpath("document.tex"))

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [
        tmp_path.joinpath("document.tex"),
        tmp_path.joinpath(f"image{image_ext}"),
    ]


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

    generate_pdf(tmp_path.joinpath("document.tex"))

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [
        tmp_path / "document.tex",
        tmp_path / "sections" / "section.tex",
        tmp_path / "sub" / "content.tex",
    ]


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

    generate_pdf(tmp_path.joinpath("document.tex"))

    nodes = scan(tmp_path.joinpath("document.tex"))

    assert nodes == [
        tmp_path / "document.tex",
        tmp_path / "sections" / "section.tex",
        tmp_path / "sections" / "sub" / "content.tex",
    ]


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

    generate_pdf(tmp_path / "document.tex")

    nodes = scan(tmp_path / "document.tex")

    assert nodes == [
        tmp_path / "document.tex",
        tmp_path / "part-a" / "section-1.tex",
        tmp_path / "part-a" / "section-2.tex",
        tmp_path / "part-b.tex",
        tmp_path / "misc" / "misc-1.tex",
    ]
