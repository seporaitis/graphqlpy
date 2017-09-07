#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('graphqlpy')


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = []

test_requirements = []

setup(
    name='graphqlpy',
    version=version,
    description="A humble attempt at a library generating GraphQL queries programatically.",
    long_description=readme + '\n\n' + history,
    author="Julius Seporaitis",
    author_email='julius@seporaitis.net',
    url='https://github.com/seporaitis/graphqlpy',
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_dir={
        'graphqlpy': 'graphqlpy',
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='graphql',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
