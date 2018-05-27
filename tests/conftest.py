"""
Pytest configuration
"""
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
def tmpfile(request: Request, tmpdir: TempPath) -> TempPath:
    """
    A temporary file
    """
    fn = tmpdir.join(request.function.__name__ + '.tmp')
    fn.open('w').close()
    fn.chmod(511)
    return fn
