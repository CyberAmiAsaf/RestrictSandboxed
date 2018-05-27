"""
Test the user creation
"""
import pwd
import grp
import pytest
import restricted


def test_user_creation(user):
    """
    Test user creation
    """
    try:
        pwd.getpwnam(user.user)
    except KeyError:
        pytest.fail('User was not created')


def test_user_deletion():
    """
    Test user deletion
    """
    user = restricted.User()
    uname = user.user

    try:
        pwd.getpwnam(uname)
    except KeyError:
        pytest.skip('User was not created')

    del user
    with pytest.raises(KeyError):
        pwd.getpwnam(uname)


def test_user_group(user):
    """
    Test user's group creation
    """
    assert user.user in grp.getgrnam(user.group).gr_mem


def test_error_user_exists():
    """
    Test that user creation fails when an exsisting user name is trying to be created
    """
    with pytest.raises(restricted.UserExistsError):
        restricted.User('root')
