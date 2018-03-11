"""
Test the user creation
"""
import pwd
import grp
from restricted.lib import User


def test_user_creation():
    """
    Test user creation
    """
    user = User()
    assert pwd.getpwnam(user.user), 'User was not created'


def test_user_group():
    """
    Test user's group creation
    """
    user = User()
    assert grp.getgrgid(pwd.getpwnam(user.user).pw_gid) == grp.getgrnam(user.group)
