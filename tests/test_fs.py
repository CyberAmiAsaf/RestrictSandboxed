"""
Test the file-system premissions system
"""
import sys
import subprocess
import pytest
import py  # pylint: disable=unused-import
import restricted


@pytest.mark.parametrize('mode', ['r', 'w', 'x'])
def test_premission_denied_accessable_file(mode, tmpdir):
    """
    Test that the restircted user can't access a normal file if the required premission is not given

    :type tmpdir: py._path.local.LocalPath
    """
    # Create a 0o777 mode temp file
    fn = tmpdir.join('test_premission_denied_accessable_file.tmp')  # type: py._path.local.LocalPath
    fn.open('w').close()
    fn.chmod(511)
    # Create user
    user = restricted.User()
    user.set_fs_file_premission('/usr/bin/test')
    # test
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call(['sudo', '-u', user.user, 'test', '-' + mode, str(fn)])


@pytest.mark.parametrize('mode', ['r', 'w', 'x'])
def test_premission_permitted_accessable_file(mode, tmpdir):
    """
    Test that the restircted user can access a normal file if the required premission is given

    :type tmpdir: py._path.local.LocalPath
    """
    # Create a 0o777 mode temp file
    fn = tmpdir.join('test_premission_permitted_accessable_file.tmp')  # type: py._path.local.LocalPath
    fn.open('w').close()
    fn.chmod(511)
    # Create user
    user = restricted.User()
    user.set_fs_file_premission('/usr/bin/test', mode='rwx')
    user.set_fs_file_premission(str(fn), '--' + mode)

    # test
    subprocess.check_call(['sudo', '-u', user.user, 'test', '-' + mode, str(fn)])
