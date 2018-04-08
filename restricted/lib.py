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
            utils.call_wrapper(['groupadd', group])

        ret = utils.call_wrapper(['useradd', self.user, '-G', group])
        
        if ret == 9:
            raise errors.UserExistsError
        elif ret == 1:
            raise errors.PremissionError

        logging.info('Created user %s of group %s', self.user, self.group)
        self._executed = True

    def __del__(self):
        if not getattr(self, '_executed', False):
            return
        utils.call_wrapper(['userdel', self.user])

__all__ = ['User']
