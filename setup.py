#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

setup(
    name = "CryptoIM",
    version = "0.1.0dev",
    packages = find_packages(exclude=["Test*"]),
    install_requires = ["docutils >= 0.3"],
    license = "TODO license",
    long_description = open("README.adoc").read(),
)
