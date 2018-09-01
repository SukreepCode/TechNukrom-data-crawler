#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
]

test_requirements = [
]


setup(
    name='data_crawler',
    version='0.1.0',
    description="",
    long_description=readme + '\n\n',
    author="Thada Wangthammang",
    author_email='mildronize@gmail.com',
    url='',
    packages=[
        'data_crawler',
    ],
    package_dir={'data_crawler':
                 'data_crawler'},
    entry_points={
        'console_scripts': [
            'technukrom_start=data_crawler.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    test_suite='pytest',
    tests_require=test_requirements
)
