"""
Main CLI Interface
"""
import sys
import argparse
import logging
from pathlib import Path
import subprocess
from functools import partial
from typing import Union, Callable
from . import lib

# consts
PREMISSIONS = {
    'read': 'r',
    'write': 'w',
    'execute': 'x'
}

class PremissionDescriptor:
    """
    A descriptor of path and its desired premission mode
    """
    path: Path
    mode: str

    def __init__(self, path: Union[str, Path], mode: str):
        if any(c not in PREMISSIONS.values() for c in mode):
            raise ValueError(f"premissions must be one or few of '{''.join(PREMISSIONS.values())}'")
        self.path = Path(path).expanduser().resolve()
        self.mode = mode

    def __iter__(self):
        return iter((self.path, self.mode))

    def __repr__(self):
        return f'{{{self.mode}:{self.path}}}'

    @staticmethod
    def from_descriptor(descriptor: str) -> 'PremissionDescriptor':
        """
        Parse a descriptor of the form '{mode}:{path}'
        """
        try:
            mode, path = descriptor.split(':')
        except ValueError:
            raise ValueError("premission descriptor must be of form 'premission:path'")
        return PremissionDescriptor(path, mode)

    @staticmethod
    def partial(*args, **kwargs) -> Callable[..., 'PremissionDescriptor']:
        """
        Define a custom constructor of a descriptor
        """
        return partial(PremissionDescriptor, *args, **kwargs)


def logging_level(level: str) -> int:
    """
    Return the numeric value of the logging level constant by the name {level}
    """
    try:
        return logging._nameToLevel[level.upper()]  # pylint: disable=protected-access
    except KeyError:
        raise argparse.ArgumentTypeError(f'No such logging level: {level}')


def adopts() -> argparse.ArgumentParser:
    """
    Adopt arguments and return a parser
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
        default=[], type=PremissionDescriptor.from_descriptor, help='add premission')
    for prem, char in PREMISSIONS.items():
        prem_group.add_argument(
            f'-{char}', f'--{prem}', dest='premissions',
            action='append', type=PremissionDescriptor.partial(mode=char), help=f'add {prem} premission')
    return parser


def main(*args):
    """
    Main CLI
    """
    parser = adopts()
    arguments = parser.parse_args(args)

    logging.getLogger().setLevel(arguments.level)

    kwargs = {key: getattr(arguments, key) for key in ('group', 'user') if getattr(arguments, key) is not None}
    user = lib.User(**kwargs)

    for path, mode in arguments.premissions:
        user.set_fs_file_premission(path, mode)

    subprocess.run(['sudo', '-u', user.user] + arguments.command)

    if not arguments.keep_user:
        user.delete()

if __name__ == '__main__':
    main(*sys.argv[1:])
