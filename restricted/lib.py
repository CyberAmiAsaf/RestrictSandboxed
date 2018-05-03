"""
Main library file
"""
import os
import pwd
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
            utils.call_wrapper(['groupadd', group])

        ret = utils.call_wrapper(['useradd', self.user, '-G', group])

        if ret == 9:
            raise errors.UserExistsError
        elif ret == 1:
            raise errors.PremissionError
        
        self.set_fs_file_premission('/', '---')

        logging.info('Created restricted user %s of group %s', self.user, self.group)
        self._executed = True

    def __del__(self):
        if not getattr(self, '_executed', False):
            return
        utils.call_wrapper(['userdel', self.user])

    @property
    def uid(self):
        """
        Get the UID of the user

        :rtype: int
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
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file_ in files:
                    self.set_fs_file_premission(os.path.join(root, file_), mode)
        else:
            subprocess.check_call(['setfacl', '-m', '{}:{}'.format(self.user, mode), path])

__all__ = ['User']
