"""
Test to the sudo premissions
"""
import subprocess


def test_passwd_premission():
    """
    Test that the program has premissions to edit the PASSWD file
    """
    try:
        subprocess.call(['sudo', 'test', '-w', '/etc/passwd'])
    except Exception as err:
        raise err
