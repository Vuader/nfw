import os
import sys
from setuptools import find_packages

config = {
        "name": "nfw",
        "author": "Christiaan Frans Rademan",
        "author_email": "christiaan.rademan@gmail.com",
        "description": "Neutrino Framework - WSGI Applications",
        "license": "BSD 3-Clause",
        "include_package_data": True,
        "keywords": "web development and restapi framework",
        "url": "http://neutrino.fwiw.co.za",
        "packages": find_packages(),
        "scripts": [
            'neutrino.py'
            ],
        "classifiers": [
            "Topic :: Software Development :: Libraries :: Application Frameworks",
            "Environment :: Other Environment",
            "Intended Audience :: Information Technology",
            "Intended Audience :: System Administrators",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7"
            ]
        }
