"""
Test to the sudo premissions
"""


def test_passwd_premission():
    """
    Test that the program has premissions to edit the PASSWD file
    """
    try:
        open('/etc/passwd').close()
    except Exception as err:
        raise err
