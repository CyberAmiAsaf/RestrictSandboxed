import os
import subprocess


def test_passwd_premission():
    try:
        subprocess.call(['sudo', 'test', '-w', '/etc/passwd'])
    except Exception as err:
        raise err
