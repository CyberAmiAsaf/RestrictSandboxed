"""
Utilitties
"""
import random
import string
import logging
import subprocess


def random_str(n: str) -> str:
    """
    Generate a {n} length random string from uppercase characters and digits
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def is_group_exists(group: str) -> bool:
    """
    Check if a certian user group is exist

    :param group: group name
    :return: whether or not the group exists
    """
    with open('/etc/group') as fd:
        for line in fd:  # type: str
            if line.startswith(group + ':'):
                return True
    return False
