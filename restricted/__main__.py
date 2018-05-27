"""
Main CLI Interface
"""
import sys
import argparse
import logging
import subprocess
from . import lib

def logging_level(level: str) -> int:
    try:
        return logging._nameToLevel[level.upper()]
    except KeyError:
        raise argparse.ArgumentTypeError(f'No such logging level: {level}')


def main(*args):
    parser = argparse.ArgumentParser(prog='restricted')

    parser.add_argument('-u', '--user', help='username of the process')
    parser.add_argument('-g', '--group', help='group of the user')

    parser.add_argument('-l', '--level', default='WARNING', type=logging_level, help='Logging level')

    parser.add_argument('command', nargs='+', help='commmand to launch')

    arguments = parser.parse_args(args)

    logging.getLogger().setLevel(arguments.level)

    kwargs = {key: getattr(arguments, key) for key in ('group', 'user') if getattr(arguments, key) is not None}
    user = lib.User(**kwargs)
    subprocess.run(['sudo', '-u', user.user] + arguments.command)

if __name__ == '__main__':
    main(*sys.argv[1:])
