from setuptools import find_packages
from setuptools import setup

setup(
    name="latex-dependency-scanner",
    version="0.0.1",
    description="Scan LaTeX documents for their dependencies.",
    author="Tobias Raabe",
    author_email="raabe@posteo.de",
    python_requires=">=3.6",
    license="MIT",
    keywords=["Build System"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    platforms="any",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    zip_safe=False,
)
