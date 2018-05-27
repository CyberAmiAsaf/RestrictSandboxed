# Restrcit
[![Build Status](https://img.shields.io/travis/CyberAmiAsaf/DekelYigal-RestrictSandboxed/master.svg?style=for-the-badge)](https://travis-ci.org/CyberAmiAsaf/DekelYigal-RestrictSandboxed)

Sandboxed processes manager

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Linux
* [Python 3.6](https://www.python.org/downloads/)

### Installing

```sh
pip install -e .
chmod -R +x scripts
```

## Running the tests

```sh
pip install -e .[test]
./scripts/lint
sudo ./scripts/test
```

## Authors

* Dekel Yigal <dekelyi@gmail.com>
