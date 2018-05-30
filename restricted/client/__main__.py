"""
Main CLI Interface
"""
import os
import sys
import argparse
import logging
import subprocess
from pathlib import Path
from typing import Union, Callable

import pexpect

from restricted.__main__ import logging_level, PremissionDescriptor, PREMISSIONS
from restricted.server.__main__ import ADDR
from .user import User


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
        default=[], type=PremissionDescriptor.from_descriptor, help='add premission')
    for prem, char in PREMISSIONS.items():
        prem_group.add_argument(
            f'-{char}', f'--{prem}', dest='premissions',
            action='append', type=PremissionDescriptor.partial(mode=char), help=f'add {prem} premission')

    arguments = parser.parse_args(args)

    logging.getLogger().setLevel(arguments.level)

    kwargs = {key: getattr(arguments, key) for key in ('group', 'user') if getattr(arguments, key) is not None}
    user = User(ADDR, **kwargs)

    for path, mode in arguments.premissions:
        user.set_fs_file_premission(path, mode)

    command = user.run_as(*arguments.command)
    ps = pexpect.spawn(command[0], command[1:])
    ps.expect('(?i)password: ')
    ps.waitnoecho()
    ps.sendline(user.token)
    ps.expect('\n')
    ps.interact()
    ps.expect(pexpect.EOF)
    ps.close()

    if not arguments.keep_user:
        user.delete()

    return ps.exitstatus

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
