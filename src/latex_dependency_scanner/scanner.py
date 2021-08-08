"""Includes the ability to scan a LaTeX document."""
import re
from os.path import splitext
from pathlib import Path
from typing import List
from typing import Optional
from typing import Union

COMMON_TEX_EXTENSIONS = [".ltx", ".tex"]
"""List[str]: List of typical file extensions that contain latex"""


COMMON_GRAPHICS_EXTENSIONS = [
    # Image formats.
    ".eps",
    ".jpeg",
    ".pdf",
    ".png",
    ".ps",
]
"""List[str]: List of typical image extensions contained in LaTeX files."""


COMMON_EXTENSIONS_IN_TEX = (
    [
        # No extension if the extension is provided.
        "",
        # TeX formats.
        ".bib",
        ".sty",
    ]
    + COMMON_GRAPHICS_EXTENSIONS
    + COMMON_TEX_EXTENSIONS
)
"""List[str]: List of typical file extensions included in latex files"""


REGEX_TEX = re.compile(
    r"\\(?P<type>usepackage|RequirePackage|include|addbibresource|bibliography|putbib|"
    r"includegraphics|input|(sub)?import|lstinputlisting)"
    r"(<[^<>]*>)?"
    r"(\[[^\[\]]*\])?"
    r"({(?P<relative_to>[^{}]*)})?{(?P<file>[^{}]*)}",
    re.M,
)
"""re.Pattern: The regular expression pattern to extract included files from a LaTeX
document."""


def scan(paths: Union[Path, List[Path]]):
    """Scan the documents provided as paths for included files.

    Parameters
    ----------
    paths
        Paths to LaTeX files which are scanned for included files.

    """
    if isinstance(paths, (str, Path)):
        paths = [paths]
    paths = [Path(p) for p in paths]

    nodes = []
    for node in paths:
        for node_ in yield_nodes_from_node(node, nodes):
            nodes.append(node_)

    return nodes


def yield_nodes_from_node(
    node: Path,
    nodes: List[Path],
    relative_to: Optional[Path] = None,
):
    r"""Yield nodes from node.

    Nodes are references to other files inside a LaTeX document.

    This function goes through a LaTeX file and collects nodes such as images or
    bibliographies. When it encounters another ``.tex`` file, it recursively calls
    itself on the target.

    Depending on the inclusion instruction for another ``.tex`` file, we have to make
    some adjustments.

    In the beginning, there is the root file which will be compiled and all inclusion
    instructions define either absolute locations or relative locations based on the
    location of the root file.

    This is especially true for ``\input`` and ``\include`` which allow to use
    relative locations based on the root file.

    - If a file is included via ``\input`` or ``\include``, the paths inside the file
      still have to be relative to the root file.
    - If a file is imported via ``\import{}{}``, the first curly braces yield the
      location relative to the document which uses the import-statement. (Absolute paths
      are allowed as well, but provide not obstacle.)
    - If a document imports a file with ``\subimport{}{}``

    """
    if node not in nodes:
        yield node

    relative_to = node.parent if relative_to is None else relative_to

    text = node.read_text(encoding="utf-8")
    for match in REGEX_TEX.finditer(text):

        if match.group("type") in ["usepackage", "RequirePackage"]:
            continue

        for path in match.group("file").split(","):
            if path:

                if match.group("type") == "import":
                    path = relative_to.joinpath(match.group("relative_to"), path)
                elif match.group("type") == "subimport":
                    path = node.parent.joinpath(match.group("relative_to"), path)
                    relative_to = path.parent
                else:
                    pass

                if match.group("type") in ["usepackage", "RequirePackage"]:
                    common_extensions = [".sty"]
                elif match.group("type") in [
                    "addbibresource",
                    "bibliography",
                    "putbib",
                ]:
                    common_extensions = [".bib"]
                elif match.group("type") in ["input", "include", "import", "subimport"]:
                    common_extensions = [".tex"]
                elif match.group("type") == "includegraphics":
                    ext = splitext(path)[-1]
                    if ext in COMMON_GRAPHICS_EXTENSIONS:
                        common_extensions = [ext]
                    else:
                        common_extensions = COMMON_GRAPHICS_EXTENSIONS
                elif match.group("type") == "lstinputlistings":
                    common_extensions = [""]
                else:
                    common_extensions = [""]

                found_some_file = False

                for extension in common_extensions:
                    path_w_ext = relative_to.joinpath(path).resolve()

                    if extension:
                        path_w_ext = path_w_ext.with_suffix(extension)

                    if path_w_ext.exists():
                        found_some_file = True
                        if path_w_ext.suffix in COMMON_TEX_EXTENSIONS:
                            yield from yield_nodes_from_node(
                                path_w_ext, nodes, relative_to
                            )
                        else:
                            if path_w_ext not in nodes:
                                yield path_w_ext

                        # Stop loop, if a file has been found.
                        break

                if not found_some_file:
                    possible_paths = [
                        (relative_to / path).resolve().with_suffix(suffix)
                        if suffix
                        else (relative_to / path).resolve()
                        for suffix in common_extensions
                    ]
                    yield from possible_paths
