#!/usr/bin/env python3
from os import fspath
from pathlib import Path
from setuptools import setup, find_packages
from io import open

DIR = Path(__file__).parent
long_description = (DIR / 'README.md').read_text()


setup(
    name='restricted',
    version='0.1',
    description='Sandboxed processes manager',
    long_description=long_description,

    url='https://github.com/CyberAmiAsaf/DekelYigal-RestrictSandboxed',
    author='Dekel Yigal',
    author_email='dekelyi@gmail.com',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: System'
        'Topic :: Security',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules'

        'Programming Language :: Unix Shell',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',

        'Environment :: Console',
        'Operating System :: POSIX',
    ],
    keywords='sandbox restricted jail',
    platforms=['posix'],

    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'restricted=restricted.__main__:main_cmd',
            'restricted-client=restricted.client.__main__:main_cmd',
            'restricted-server=restricted.server.__main__:main'
        ]
    },

    install_requires=['pexpect'],
    extras_require={
        'test': ['pylint', 'pytest'],
    },
)