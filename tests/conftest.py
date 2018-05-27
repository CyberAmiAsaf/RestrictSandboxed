import py
import pytest
import restricted


@pytest.fixture
def user():
    return restricted.User()


@pytest.fixture
def tmpfile(request, tmpdir):
    fn = tmpdir.join(request.function.__name__ + '.tmp')
    fn.open('w').close()
    fn.chmod(511)
    return fn
