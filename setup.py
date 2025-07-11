#!/usr/bin/env python3
"""
Setup script for the PubMed Pharmaceutical Papers Fetcher.

This setup.py file provides an alternative installation method
for environments that don't support pyproject.toml.
"""

from setuptools import setup, find_packages
import pathlib

# Read the contents of README file
this_directory = pathlib.Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="pubmed-pharma-papers",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python program to fetch research papers from PubMed with pharmaceutical/biotech company affiliations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/navratra/pubmed-pharma-papers",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "xmltodict>=0.13.0",
        "click>=8.1.0",
        "pandas>=2.0.0",
        "email-validator>=2.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "types-requests>=2.31.0",
        ]
    },
    entry_points={
        "console_scripts": ["get-papers-list=pubmed_pharma_papers.cli:main"]
    },
    include_package_data=True,
    zip_safe=False,
)
