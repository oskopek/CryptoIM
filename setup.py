#!/usr/bin/env python
# encoding: utf-8

"""
    Copyright 2013,2014 CryptoIM Development Team

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from setuptools import setup, find_packages

setup(
    name = "CryptoIM",
    version = "0.1.0dev",
    author = "CryptoIM Development Team",
    author_email = "skopekondrej@gmail.com",
    packages = find_packages(exclude=["tests"]),
    url = "http://pypi.python.org/pypi/CryptoIM/",
    license = "Apache License 2.0",
    description = "Crypto Instant Messenger",
    keywords = "crypto instant messenger",
    classifiers = [
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Communications :: Chat",
        "Topic :: Security :: Cryptography",
    ],
    long_description = open("README").read(),
    install_requires = [
        "docutils >= 0.3",
        "pygpgme >= 0.3",
        "nose >= 1.3.0",
    ],
)
