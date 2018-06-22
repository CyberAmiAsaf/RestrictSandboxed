"""
Main CLI Interface
"""
import os
import sys
import logging

from restricted.__main__ import adopts
from restricted.server.__main__ import ADDR
from .user import User


def main(*args):
    """
    Main CLI
    """
    try:
        parser = adopts()
        arguments = parser.parse_args(args)

        logging.getLogger().setLevel(arguments.level)

        kwargs = {key: getattr(arguments, key) for key in ('group', 'user') if getattr(arguments, key) is not None}
        user = User(os.fspath(ADDR), **kwargs)

        for path, mode in arguments.premissions:
            user.set_fs_file_premission(path, mode)

        ret = user.run_as(*arguments.command)

        if not arguments.keep_user:
            user.delete()

        return ret
    except Exception as err:
        print(f'Error: {err}')
        return 1


def main_cmd():
    sys.exit(main(*sys.argv[1:]))

if __name__ == '__main__':
    main_cmd()
