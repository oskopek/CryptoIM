#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

setup(
    name = "CryptoIM",
    version = "0.1.0dev",
    author = "CryptoIM Development Team",
    author_email = "",
    packages = find_packages(exclude=["Test*"]),
    url = "http://pypi.python.org/pypi/CryptoIM/",
    license = "LICENSE.txt",
    description = "Crypto Instant Messenger",
    long_description = open("README.adoc").read(),
    install_requires = [
        "docutils >= 0.3",
        "pygpgme >= 0.3",
	"nosetests >= 1.3.0",
    ],
)
