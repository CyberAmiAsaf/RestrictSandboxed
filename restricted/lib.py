"""
Main library file
"""
import os
import pwd
import logging
import subprocess
from pathlib import Path
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
            raise PermissionError

        logging.debug('Created user %s of group %s', self.user, self.group)

        for path in consts.RESTRICTED_BY_DEFAULT:
            self.set_fs_file_premission(Path(path), '---')

        self.set_password(self.user)

    def set_password(self, password: str):
        subprocess.run(['passwd', self.user], input=f'{password}\n{password}\n'.encode(), stdout=subprocess.DEVNULL).check_returncode()

    def delete(self):
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

    def set_fs_file_premission(self, path: Path, mode: str = 'xr'):
        """
        Set file premissions of {path} to be {mode}

        :param path: path to file or directory
        :param mode: file premission mode
        """
        try:
            subprocess.run(['setfacl', '-m', f'u:{self.user}:{mode}', path.resolve()]).check_returncode()
        except FileNotFoundError:
            raise RuntimeError('ACL Tools are not present in your host computer')
        logging.debug('Set file premissions of %s to %s', path, mode)

__all__ = ['User']
