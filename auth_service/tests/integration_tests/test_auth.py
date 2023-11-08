import pytest
from fastapi.testclient import TestClient
from jose import jwt

import settings
from auth_service.src.main import app

client = TestClient(app)

def test_auth(test_admin):
    res = client.post('/api/auth/token', data=test_admin)
    response = res.json()
    assert res.status_code == 200
    assert 'access_token' in response
    assert 'token_type' in response
    assert response['token_type'] == 'bearer'
    payload = jwt.decode(response['access_token'], settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    assert payload['sub'] == test_admin['username']


@pytest.mark.parametrize(
    'username, password, status_code',
    [
        ('wrongelogin', '123', 401),
        ('bob', 'wrongpassword', 401),
        ('wrongelogin', 'wrongpassword', 401),
        (None, '123', 422),
        ('bob', None, 422),
        (None, None, 422),
    ],
)
def test_incorrect_login(username, password, status_code):
    res = client.post('/api/auth/token', data={'username': username, 'password': password})
    assert res.status_code == status_code
