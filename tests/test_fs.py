"""
Test the file-system premissions system
"""
import sys
import subprocess
import pytest
import py  # pylint: disable=unused-import
import restricted


@pytest.mark.parametrize('mode', ['r', 'w', 'x'])
def test_premission_denied(mode, user, tmpfile):
    """
    Test that the restircted user can't access a normal file if the required premission is not given

    :type tmpfile: py._path.local.LocalPath
    """
    user.set_fs_file_premission(str(tmpfile), '---')
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call(['sudo', '-u', user.user, 'test', '-' + mode, str(tmpfile)])


@pytest.mark.parametrize('mode', ['r', 'w', 'x'])
def test_premission_permitted(mode, user, tmpfile):
    """
    Test that the restircted user can access a normal file if the required premission is given

    :type tmpfile: py._path.local.LocalPath
    """
    user.set_fs_file_premission(str(tmpfile), mode)
    subprocess.check_call(['sudo', '-u', user.user, 'test', '-' + mode, str(tmpfile)])
