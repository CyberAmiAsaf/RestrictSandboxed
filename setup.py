from pathlib import Path
from setuptools import setup, find_packages
from io import open

long_description = (Path(__file__).parent / 'README.md').read_text()


setup(
    name='restrictsandboxed',
    version='0.1',
    description='Sandboxed processes manager',
    long_description=long_description,

    url='https://github.com/CyberAmiAsaf/DekelYigal-RestrictSandboxed',
    author='Dekel Yigal',
    author_email='dekelyi@gmail.com',

    classifiers=[
        'Development Status :: 1 - Planning',

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

    install_requires=[],
    extras_require={
        'test': ['pylint', 'pytest'],
    },
)