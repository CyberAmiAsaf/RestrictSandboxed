"""
Test the file-system premissions system
"""
import subprocess
from pathlib import Path
import pytest
import restricted


@pytest.mark.parametrize('mode', ['r', 'w', 'x'])
def test_premission_denied(mode, user: restricted.User, tmpfile: Path):
    """
    Test that the restircted user can't access a normal file if the required premission is not given
    """
    user.set_fs_file_premission(tmpfile, '---')
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call(['sudo', '-u', user.user, 'test', '-' + mode, tmpfile])


@pytest.mark.parametrize('mode', ['r', 'w', 'x'])
def test_premission_permitted(mode, user: restricted.User, tmpfile: Path):
    """
    Test that the restircted user can access a normal file if the required premission is given
    """
    user.set_fs_file_premission(tmpfile, mode)
    subprocess.check_call(['sudo', '-u', user.user, 'test', '-' + mode, tmpfile])
