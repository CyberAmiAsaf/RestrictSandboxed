# Restrcited Sandbox
[![Build Status](https://img.shields.io/travis/CyberAmiAsaf/DekelYigal-RestricedSandbox/master.svg?style=for-the-badge)](https://travis-ci.org/CyberAmiAsaf/DekelYigal-RestricedSandbox)

Sandboxed processes manager

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes, or for global use in your system.

### Prerequisites

* POSIX compatible operating system
* ACL-Enabled file system (btrfs/ext2-4)
* ACL POSIX Tools (`acl` package)
* [Python 3.6](https://www.python.org/downloads/)

### Installing

```sh
# for global use
sudo pip3 install .
# for development use
pip3 install -e .
```

## Running the program

Use the `restricted` command or import the `restricted` python package.
Note that in order to run the program successfully, the user running the program must have sudo premissions.

## Running the tests

```sh
pip3 install -e .[test]
chmod +x ./scripts
./scripts/lint
sudo ./scripts/test
```

## Authors

* Dekel Yigal <dekelyi@gmail.com>
