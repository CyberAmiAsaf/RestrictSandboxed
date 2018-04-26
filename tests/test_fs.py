"""
Test the file-system premissions system
"""
import sys
import subprocess
import pytest
import py  # pylint: disable=unused-import
import restricted


def test_premission_denied_readable_file(tmpdir):
    """
    Test that the restircted user can't access a normal file if the required premission is not given

    :type tmpdir: py._path.local.LocalPath
    """
    # Create a 0o777 mode temp file
    fn = tmpdir.join('test_premission_denied.tmp')  # type: py._path.local.LocalPath
    fn.open('w').close()
    fn.chmod(511)
    # Create user
    user = restricted.User()

    # test
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call(['sudo', '-u', user.user, 'test', '-r', str(fn)])
