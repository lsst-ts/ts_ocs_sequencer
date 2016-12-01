#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='ts_ocs_sequencer',
    version='0.1.0',
    description="LSST TS OCS Sequencer contains all the code for the OCS sequencer component",
    long_description=readme + '\n\n' + history,
    author="Philip N. Daly",
    author_email='pdaly@lsst.org',
    url='https://github.com/pndaly/ts_ocs_sequencer',
    packages=[
        'ts_ocs_sequencer',
    ],
    package_dir={'ts_ocs_sequencer':
                 'ts_ocs_sequencer'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='ts_ocs_sequencer',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
