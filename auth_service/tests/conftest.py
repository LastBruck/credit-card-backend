import pytest


@pytest.fixture
def test_admin():
    return {
        'username': 'bob',
        'password': '123',
    }
