#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="custom_common_funcs",
    version="0.0.0",
    description="foobar",
    author="yi liu",
    author_email="",
    url="",
    install_requires=[],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
