#!/usr/bin/env python

from setuptools import setup

setup(
    name="pantsmud",
    version="0.3.2",
    description="A simple MUD library built using the Pants networking framework.",
    author="ecdavis",
    author_email="me@ezdwt.com",
    url="http://github.com/ecdavis/pantsmud",
    download_url="https://github.com/ecdavis/pantsmud/tarball/master",
    packages=["pantsmud", "pantsmud.driver", "pantsmud.util"],
    install_requires=["pants >= 1.0"],
    tests_require=['mock'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English"
    ]
)
