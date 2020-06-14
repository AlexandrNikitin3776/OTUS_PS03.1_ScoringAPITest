#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scoringapi",  # Replace with your own username
    version="0.0.1",
    author="AlexandrNikitin3776",
    author_email="snegopad1@gmail.com",
    description="scoring API package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexandrNikitin3776/OTUS_PS03_ScoringAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
