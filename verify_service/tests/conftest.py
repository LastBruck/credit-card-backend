import pytest


@pytest.fixture
def card_number_for_verify():
    return '555555'


@pytest.fixture
def fake_selfie_image():
    return 'verify_service/tests/images_for_test/fake_image_selfie.jpg'


@pytest.fixture
def valid_selfie_image():
    return 'verify_service/tests/images_for_test/image_selfie.png'


@pytest.fixture
def valid_document_image():
    return 'verify_service/tests/images_for_test/image_doc.png'
