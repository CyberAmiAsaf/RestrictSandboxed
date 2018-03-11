"""
Main library file
"""
import logging
from . import utils
from . import consts

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

        logging.info('Created user %s of group %s', self.user, self.group)
