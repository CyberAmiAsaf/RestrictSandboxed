# Restricted Sandbox

Sandboxed processes manager

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for global use in your system.

### Prerequisites

* POSIX compatible operating system
* ACL-Enabled file system (btrfs/ext2-4)
* ACL POSIX Tools (`acl` package)
* [Python 3.6](https://www.python.org/downloads/)

### Installing

```sh
sudo pip3 install .
```

## Running the program

Use the `restricted` command or import the `restricted` python package.
Note that in order to run the program successfully, the user running the program must have sudo premissions.

One can use the networked framework of the program, via the `restricted-server` command and the `restricted-client` command, or with the `restricted.client` package.
Note that the server must be run as root as well.