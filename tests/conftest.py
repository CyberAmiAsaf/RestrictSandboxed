"""
Pytest configuration
"""
from pathlib import Path
import py
import _pytest
import pytest
import restricted

TempPath = py._path.local.LocalPath  # pylint: disable=protected-access
Request = _pytest.fixtures.FixtureRequest

@pytest.fixture
def user() -> restricted.User:
    """
    A User
    """
    return restricted.User()


@pytest.fixture
def tmpfile(request: Request, tmpdir: TempPath) -> Path:
    """
    A temporary file
    """
    fn = Path(str(tmpdir.join(request.function.__name__ + '.tmp')))
    fn.touch(0o777)
    return fn
