from pathlib import Path

from setuptools import find_packages
from setuptools import setup

import versioneer

README = Path("README.rst").read_text()

PROJECT_URLS = {
    "Documentation": "https://github.com/pytask-dev/latex-dependency-scanner",
    "Github": "https://github.com/pytask-dev/latex-dependency-scanner",
    "Tracker": "https://github.com/pytask-dev/latex-dependency-scanner/issues",
    "Changelog": "https://github.com/pytask-dev/latex-dependency-scanner/blob/main/"
    "CHANGES.rst",
}


setup(
    name="latex-dependency-scanner",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Scan LaTeX documents for their dependencies.",
    long_description=README,
    long_description_content_type="text/x-rst",
    author="Tobias Raabe",
    author_email="raabe@posteo.de",
    python_requires=">=3.6",
    url=PROJECT_URLS["Github"],
    project_urls=PROJECT_URLS,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    platforms="any",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    zip_safe=False,
)
