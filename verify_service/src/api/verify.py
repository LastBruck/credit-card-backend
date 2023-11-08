"""Верификация по фото."""

from aiohttp import ClientSession
from deepface import DeepFace
from fastapi import APIRouter, BackgroundTasks, HTTPException

import settings
from verify_service.src.db.models import VerificationResponse

verify_rout = APIRouter()


async def check_user(card_number: str):
    """Проверка, есть ли пользователь с такой картой.

    Args:
        card_number (str): номер карты

    Returns:
        status, data: результат проверки
    """
    input_data = {'card_number': card_number}
    url = 'http://{host}:{port}/api/get_user/'.format(host=settings.APP_HOST, port=settings.APP_BASE_PORT)
    async with ClientSession(trust_env= True) as session:
        resp = await session.get(url, params=input_data)
        data = await resp.json()
        status = resp.status
    return status, data


async def verify_photos(selfie_path, document_path):
    """Верификация лиц на фото.

    Args:
        selfie_path (str): путь к фото селфи
        document_path (str): путь к фото документов

    Raises:
        ValueError: исключение

    Returns:
        Bool: результат верификации
    """
    try:
        return DeepFace.verify(selfie_path, document_path, model_name='Facenet')['verified']
    except Exception as ve:
        raise ValueError(str(ve))


async def chenge_limit_after_verify(card_number: str, verified: bool):
    """Отправка запроса на изменение лимита после верификации.

    Args:
        card_number (str): номер карты
        verified (bool): результат верификации
    """
    input_data = {'card_number': card_number, 'verified': str(verified)}
    url = 'http://{host}:{port}/api/change_limit/'.format(host=settings.APP_HOST, port=settings.APP_BASE_PORT)
    async with ClientSession() as session:
        await session.post(url, params=input_data)


@verify_rout.post('/')
async def verify_user_photo(
    card_number: str,
    selfie_name: str,
    document_name: str,
    backgroundtasks: BackgroundTasks,
) -> VerificationResponse:
    """Роутер верификации фото селфи и в паспорте.

    Args:
        card_number (str): Номер карты
        selfie_name (str): название фото клиента
        document_name (str): навзвание фото документа
        backgroundtasks (BackgroundTasks): init BackgroundTasks

    Raises:
        HTTPException: исключение
        HTTPException: исключение

    Returns:
        VerificationResponse: {'verified': true/false}
    """
    try:
        status, data = await check_user(card_number=card_number)
        if status != 200:
            raise HTTPException(status_code=status, detail=data['detail'])
        selfie_path = f'shared_photos/{selfie_name}'
        document_path = f'shared_photos/{document_name}'
        verified = await verify_photos(selfie_path, document_path)
        backgroundtasks.add_task(chenge_limit_after_verify, card_number=card_number, verified=verified)
        return VerificationResponse(verified=bool(verified))
    except ValueError as ve:
        raise HTTPException(
            status_code=404, detail=str(ve),
        )
