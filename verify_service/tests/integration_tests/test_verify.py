import io
import pytest
from fastapi.testclient import TestClient

from verify_service.src.main import app
from base_service.src.db.models import storage

client = TestClient(app)

def test_verify_valid_photo(card_number_for_verify, valid_selfie_image, valid_document_image):
    #Создаём пользователя:
    storage.add(card_number=card_number_for_verify, info={})    
    # На обоих фотографиях один человек
    response = client.post(
        '/api/verify',
        params={
            'card_number': card_number_for_verify,
            'selfie_path': valid_selfie_image,
            'document_path': valid_document_image,
            },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verified"] == True

    
def test_verify_invalid_photo(card_number_for_verify, valid_document_image, fake_selfie_image):
    # На фотографиях разные люди
    response = client.post(
        '/api/verify',
        params={
            'card_number': card_number_for_verify,
            'selfie_path': fake_selfie_image,
            'document_path': valid_document_image,
            },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["verified"] == False
    
    
def test_verify_one_photo(card_number_for_verify, valid_selfie_image):
    # Ошибка: Не загружено изображение документа
    response = client.post(
        '/api/verify',
        params={
            'card_number': card_number_for_verify,
            'selfie_path': valid_selfie_image,
            },
    )
    
    assert response.status_code == 422

def test_verify_invalid_card_number(valid_selfie_image, valid_document_image):
    # Ошибка: Некорректный номер карты
    response = client.post(
        "/api/verify/",
        params={
            'card_number': '0000',
            'selfie_path': valid_selfie_image,
            'document_path': valid_document_image,
            },
    )
    assert response.status_code == 404

def test_verify_uncorrect_input_photo(card_number_for_verify):
    # Ошибка: Некорректные изображения (например, не изображения в формате JPEG)
    response = client.post(
        "/api/verify/",
        params={
            'card_number': card_number_for_verify,
            'selfie_path': ("selfie.png", io.BytesIO(b"invalid_image_data"), "image/png"),
            'document_path': ("document.jpg", io.BytesIO(b"invalid_image_data"), "image/jpeg"),
            },
    )
    assert response.status_code == 404

def test_verify_no_photo(card_number_for_verify):
    # Ошибка: Нет входящих изображений.
    response = client.post(
        "/api/verify/",
        params={
            'card_number': card_number_for_verify,
            },
    )
    assert response.status_code == 422
