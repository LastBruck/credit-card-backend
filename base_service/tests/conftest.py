import pytest
from decimal import Decimal
from fastapi.testclient import TestClient

from base_service.src.transactions.transactions import Transactions
from base_service.src.users.storage import UserStorage
from base_service.src.history.log_storage import LogStorage


@pytest.fixture
def test_admin():
    return {
        'username': 'bob',
        'password': '123',
    }

@pytest.fixture
def user_storage():
    return UserStorage()


@pytest.fixture
def history():
    return LogStorage()


@pytest.fixture
def transactions(user_storage, history):
    transactions = Transactions(user_storage, history)
    return transactions


@pytest.fixture
def card_number_for_users():
    return '1234567890123456'


@pytest.fixture
def card_number_for_transac():
    return '1234567890'


@pytest.fixture
def card_number_for_verify():
    return '555555'


@pytest.fixture
def card_number_for_rout():
    return '123000'


@pytest.fixture
def fake_selfie_image():
    return open('tests/images_for_test/fake_image_selfie.jpg', 'rb')


@pytest.fixture
def valid_selfie_image():
    return open('tests/images_for_test/image_selfie.png', 'rb')


@pytest.fixture
def valid_document_image():
    return open('tests/images_for_test/image_doc.png', 'rb')
