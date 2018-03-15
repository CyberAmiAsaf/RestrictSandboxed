"""
Test the user creation
"""
import pwd
import grp
import pytest
import restricted


def test_user_creation():
    """
    Test user creation
    """
    user = restricted.User()
    assert pwd.getpwnam(user.user), 'User was not created'


def test_user_deletion():
    user = restricted.User()
    uname = user.user
    
    try:
        pwd.getpwnam(uname)
    except KeyError:
        pytest.skip('User was not created')

    del user
    with pytest.raises(KeyError):
        pwd.getpwnam(uname)


def test_user_group():
    """
    Test user's group creation
    """
    user = restricted.User()
    assert grp.getgrgid(pwd.getpwnam(user.user).pw_gid) == grp.getgrnam(user.group)


def test_error_user_exists():
    """
    Test that user creation fails when an exsisting user name is trying to be created
    """
    with pytest.raises(restricted.UserExistsError):
        restricted.User('root')
