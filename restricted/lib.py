"""
Main library file
"""
import logging
import subprocess
from . import utils
from . import consts
from . import errors

logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s', level=logging.DEBUG)


class User(object):
    """
    A resticrtable user
    """
    def __init__(self, user=None, group=consts.GROUP_DEFAULT):
        """
        :type user: str | None
        :type group: str
        """
        self.user = user or utils.random_str(10)
        self.group = group

        if not utils.is_group_exists(group):
            subprocess.run(['groupadd', group]).check_returncode()

        ret = subprocess.run(['useradd', self.user, '-G', group]).returncode

        if ret == 9:
            raise errors.UserExistsError
        elif ret == 1:
            raise errors.PremissionError

        logging.info('Created user %s of group %s', self.user, self.group)
        self._executed = True

    def __del__(self):
        if not getattr(self, '_executed', False):
            return
        subprocess.run(['userdel', self.user]).check_returncode()

__all__ = ['User']
