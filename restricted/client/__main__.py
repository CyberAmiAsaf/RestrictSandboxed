"""
Main CLI Interface
"""
import sys
import logging

import pexpect

from restricted.__main__ import adopts
from restricted.server.__main__ import ADDR
from .user import User


def main(*args):
    """
    Main CLI
    """
    parser = adopts()
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
