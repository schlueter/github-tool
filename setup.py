#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath('lib'))
from release import __version__, __author__ # pylint: disable=import-error
from setuptools import setup, find_packages


setup(
    name='GitHubCLI',
    version=__version__,
    description="Commandline interface to GitHub's API",
    author=__author__,
    author_email='githubcli@schlueter.blue',
    url='http://schlueter.github.io/github-cli',
    license='GPLv3',
    install_requires=['requests'],
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    scripts=[
        'bin/gh-copy-labels',
        'bin/gh-create-labels'
    ])
