"""
Utilitties
"""
import random
import string
import logging
import subprocess


def random_str(n):
    """
    Generate a {n} length random string from uppercase characters and digits
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def is_group_exists(group):
    with open('/etc/group') as fd:
        for line in fd:  # type: str
            if line.startswith(group + ':'):
                return True
    return False


def call_wrapper(*args, **kwargs):
    """
    A wrapper around the 'call' method of subprocess.
    Makes sure stdout and stderr are properly printed if necessary, even in a tested environment

    :return: the return code
    :rtype: int
    """
    # check whether to handle stdout
    if 'stdout' not in kwargs:
        kwargs['stdout'] = subprocess.PIPE
        handle_out = True
    else:
        handle_out = False

    # check whether to handle stderr
    if 'stderr' not in kwargs:
        kwargs['stderr'] = subprocess.PIPE
        handle_err = True
    else:
        handle_err = False

    # call the processes
    process = subprocess.Popen(*args, **kwargs)

    # handle stdout and stderr if necessary
    out, err = process.communicate()
    if out and handle_out:
        logging.info(out)
    if err and handle_err:
        logging.error(err)

    return process.returncode
