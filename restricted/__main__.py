"""
Main CLI Interface
"""
import sys
import argparse
import logging
from pathlib import Path
import subprocess
from typing import Tuple, Callable
from . import lib

# types # pylint: disable=invalid-name
PremissionDescriptor = Tuple[str, Path]
# consts # pylint: enable=invalid-name
PREMISSIONS = {
    'read': 'r',
    'write': 'w',
    'execute': 'x'
}

def logging_level(level: str) -> int:
    """
    Return the numeric value of the logging level constant by the name {level}
    """
    try:
        return logging._nameToLevel[level.upper()]  # pylint: disable=protected-access
    except KeyError:
        raise argparse.ArgumentTypeError(f'No such logging level: {level}')


def premission(descriptor: str) -> PremissionDescriptor:
    """
    Parse a descriptor of the form '{mode}:{path}'
    """
    try:
        mode, path = descriptor.split(':')
        path = Path(path).expanduser().resolve()
    except ValueError:
        raise argparse.ArgumentTypeError("premission descriptor must be of form 'premission:path'")

    if any(c not in PREMISSIONS.values() for c in mode):
        raise argparse.ArgumentTypeError(f"premissions must be one or few of '{''.join(PREMISSIONS.values())}'")

    return (mode, path)


def premission_mode(mode: str) -> Callable[[str], PremissionDescriptor]:
    """
    Return a type function that get a path and return a PremissionDescriptor({mode}, {path})
    """
    def func(path: str) -> PremissionDescriptor:  # pylint: disable=missing-docstring
        return mode, Path(path).expanduser().resolve()
    return func


def main(*args):
    """
    Main CLI
    """
    parser = argparse.ArgumentParser(prog='restricted')

    parser.add_argument('-l', '--level', default='WARNING', type=logging_level, help='Logging level')
    parser.add_argument('command', nargs='+', help='commmand to launch')

    user_group = parser.add_argument_group('user options')
    user_group.add_argument('-u', '--user', help='username of the process')
    user_group.add_argument('-g', '--group', help='group of the user')
    user_group.add_argument('-k', '--keep-user', action='store_true', help="Don't delete the user after termination")

    prem_group = parser.add_argument_group('premissions')
    prem_group.add_argument(
        '-p', '--premission', action='append', dest='premissions',
        default=[], type=premission, help='add premission')
    for prem, char in PREMISSIONS.items():
        prem_group.add_argument(
            f'-{char}', f'--{prem}', dest='premissions',
            action='append', type=premission_mode(char), help=f'add {prem} premission')

    arguments = parser.parse_args(args)

    logging.getLogger().setLevel(arguments.level)

    kwargs = {key: getattr(arguments, key) for key in ('group', 'user') if getattr(arguments, key) is not None}
    user = lib.User(**kwargs)

    if arguments.keep_user:
        user.delete_user = False

    for mode, path in arguments.premissions:
        user.set_fs_file_premission(path, mode)

    subprocess.run(['sudo', '-u', user.user] + arguments.command)

if __name__ == '__main__':
    main(*sys.argv[1:])
