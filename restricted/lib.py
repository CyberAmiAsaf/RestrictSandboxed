"""
Main library file
"""
import os
import pwd
import logging
import subprocess
from typing import Optional
from . import utils
from . import consts
from . import errors

class User(object):
    """
    A resticrtable user
    """
    def __init__(self, user: Optional[str] = None, group: str = consts.GROUP_DEFAULT):
        self.user = user or utils.random_str(10)
        self.group = group

        if not utils.is_group_exists(group):
            subprocess.run(['groupadd', group]).check_returncode()

        ret = subprocess.run(['useradd', self.user, '-G', group]).returncode

        if ret == 9:
            raise errors.UserExistsError
        elif ret == 1:
            raise errors.PremissionError

        for path in consts.RESTRICTED_BY_DEFAULT:
            self.set_fs_file_premission(path, '---')

        logging.info('Created restricted user %s of group %s', self.user, self.group)
        self._executed = True

    def __del__(self):
        if not getattr(self, '_executed', False):
            return
        try:
            subprocess.run(['userdel', self.user]).check_returncode()
        except subprocess.CalledProcessError:
            logging.warning('User %s could not be deleted', self.user)

    @property
    def uid(self) -> int:
        """
        Get the UID of the user
        """
        return pwd.getpwnam(self.user)[2]

    def setuid(self):
        """
        Set the process' UID to the user's UID
        """
        os.setuid(self.uid)

    def set_fs_file_premission(self, path, mode='-xr'):
        """
        Set file premissions of {path} to be {mode}

        :param str path: path to file or directory
        :param str mode: file premission mode
        """
        subprocess.check_call(['setfacl', '-m', '{}:{}'.format(self.user, mode), path])

__all__ = ['User']
