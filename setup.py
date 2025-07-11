#!/usr/bin/env python3
"""
Setup script for PB&J Pipeline
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pbj-pipeline",
    version="1.0.0",
    author="Dylan Hubert",
    author_email="TBA",
    description="A Python RAG document processing pipeline that combines PDF parsing, markdown enhancement, JSON extraction, and format conversion",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dylanhubert/pbj-pipeline",
    project_urls={
        "Bug Tracker": "https://github.com/dylanhubert/pbj-pipeline/issues",
        "Documentation": "https://github.com/dylanhubert/pbj-pipeline#readme",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "pbj=pbj.sandwich:main",
        ],
    },
    include_package_data=True,
    package_data={
        "pbj": ["pantry/*.txt"],
    },
    keywords="pdf, rag, document-processing, llamaparse, openai, markdown, json",
    zip_safe=False,
) 