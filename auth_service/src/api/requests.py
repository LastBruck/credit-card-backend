"""Запросы."""
import asyncio
import json
import uuid
from typing import Annotated

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile

import settings
from auth_service.src.api.auth import get_current_user_from_token
from auth_service.src.db.models import BalanceUser

request_balance = APIRouter()


@request_balance.get('/', response_model=BalanceUser)
async def get_balance(
    request: Request,
    card_number: str,
    current_user: Annotated[str, Depends(get_current_user_from_token)],
) -> BalanceUser:
    """Ручка получения баланса пользователя.

    Args:
        request (Request): _description_
        card_number (str): номер карты
        current_user (Annotated[str, Depends): авторизация.

    Raises:
        HTTPException: исключение
        HTTPException: исключение
        HTTPException: исключение

    Returns:
        BalanceUser: BalanceUser
    """
    input_params = {'card_number': card_number}
    url = 'http://{host}:{port}/api/balance/'.format(host=settings.APP_HOST, port=settings.APP_BASE_PORT)
    session = request.state.client_session
    async with session.get(url, params=input_params) as resp:
        data = await resp.json()
        status = resp.status
        balance = data.get('balance')
    if status != 200:
        raise HTTPException(status_code=status, detail=data['detail'])
    return BalanceUser(card_number=card_number, balance=balance)

request_history = APIRouter()


@request_history.get('/')
async def get_history(
    request: Request,
    card_number: str,
    from_date: str,
    to_date: str,
    current_user: Annotated[str, Depends(get_current_user_from_token)],
):
    """Ручка получения истории баланса пользователя.

    Args:
        request (Request): _description_
        card_number (str): номер карты
        from_date: (str): дата ОТ
        to_date: (str): дата ДО
        current_user (Annotated[str, Depends): авторизация.

    Raises:
        HTTPException: исключение
        HTTPException: исключение
        HTTPException: исключение
        HTTPException: исключение

    Returns:
        List: история баланса
    """
    input_params = {'card_number': card_number, 'from_date': from_date, 'to_date': to_date}
    url = 'http://{host}:{port}/api/balance/history'.format(host=settings.APP_HOST, port=settings.APP_BASE_PORT)
    session = request.state.client_session
    async with session.get(url, params=input_params) as resp:
        data = await resp.json()
        status = resp.status
    if bool(data) is False:
        raise HTTPException(status_code=404, detail='За указанный период история не найдена.')
    elif status != 200:
        if status == 404:
            raise HTTPException(status_code=status, detail=data['detail'])
        raise HTTPException(status_code=status, detail='Что-то пошло не так.')
    return data

request_deposit = APIRouter()


@request_deposit.post('/', response_model=BalanceUser)
async def deposit_post(
    request: Request,
    card_number: str,
    amount: str,
    current_user: Annotated[str, Depends(get_current_user_from_token)],
) -> BalanceUser:
    """Ручка пополнения баланса пользователя.

    Args:
        request (Request): _description_
        card_number (str): номер карты
        amount (str): сумма пополнения
        current_user (Annotated[str, Depends): авторизация.

    Raises:
        HTTPException: исключение
        HTTPException: исключение
        HTTPException: исключение

    Returns:
        BalanceUser: BalanceUser
    """
    input_data = {'card_number': card_number, 'amount': amount}
    url = 'http://{host}:{port}/api/deposit/'.format(host=settings.APP_HOST, port=settings.APP_BASE_PORT)
    session = request.state.client_session
    async with session.post(url, params=input_data) as resp:
        data = await resp.json()
        status = resp.status
        balance = data.get('balance')
    if status != 200:
        if status == 404:
            raise HTTPException(status_code=status, detail=data['detail'])
        raise HTTPException(status_code=status, detail='Что-то пошло не так.')
    return BalanceUser(card_number=card_number, balance=balance)

request_withdrawal = APIRouter()


@request_withdrawal.post('/', response_model=BalanceUser)
async def withdrawal_post(
    request: Request,
    card_number: str,
    amount: str,
    current_user: Annotated[str, Depends(get_current_user_from_token)],
) -> BalanceUser:
    """Ручка списания с баланса пользователя.

    Args:
        request (Request): _description_
        card_number (str): номер карты
        amount (str): сумма списания
        current_user (Annotated[str, Depends): авторизация.

    Raises:
        HTTPException: исключение
        HTTPException: исключение
        HTTPException: исключение

    Returns:
        BalanceUser: BalanceUser
    """
    input_data = {'card_number': card_number, 'amount': amount}
    url = 'http://{host}:{port}/api/withdrawal/'.format(host=settings.APP_HOST, port=settings.APP_BASE_PORT)
    session = request.state.client_session
    async with session.post(url, params=input_data) as resp:
        data = await resp.json()
        status = resp.status
        balance = data.get('balance')
    if status != 200:
        if status == 404:
            raise HTTPException(status_code=status, detail=data['detail'])
        raise HTTPException(status_code=status, detail='Что-то пошло не так.')
    return BalanceUser(card_number=card_number, balance=balance)

request_verify = APIRouter()


@request_verify.post('/')
async def verify_post(
    request: Request,
    card_number: str,
    current_user: Annotated[str, Depends(get_current_user_from_token)],
    selfie: UploadFile = File(...),
    document: UploadFile = File(...),
):
    """Ручка верификации фото пользователя.

    Args:
        request (Request): _description_
        card_number (str): Номер карты
        current_user (Annotated[str, Depends): аутентификация
        selfie (UploadFile): фото клиента. Defaults to File(...).
        document (UploadFile): фото документов. Defaults to File(...).

    Raises:
        HTTPException: исключение

    Returns:
        _type_: status
    """
    try:
        selfie_name = f'selfie_{uuid.uuid4()}.jpg'
        document_name = f'document_{uuid.uuid4()}.jpg'

        with open(f'shared_photos/{selfie_name}', 'wb') as selfie_file:
            selfie_file.write(selfie.file.read())

        with open(f'shared_photos/{document_name}', 'wb') as document_file:
            document_file.write(document.file.read())

        producer: AIOKafkaProducer = request.state.kafka_producer
        event = json.dumps({'card_number': card_number, 'selfie_name': selfie_name, 'document_name': document_name})
        await producer.send_and_wait(topic=settings.KAFKA_TOPIC_REQUEST, value=bytes(str(event), encoding='utf-8'))
        consumer: AIOKafkaConsumer = request.state.kafka_consumer_result
        while True:
            await asyncio.sleep(1)
            new_resp = await consumer.getone()
            new_resp = json.loads(new_resp.value.decode('utf-8').replace("'", '"'))
            status = new_resp.get('status')
            resoult = new_resp.get('resoult')
            if status != 200:
                raise HTTPException(status_code=status, detail=resoult['detail'])
            return resoult
    except TypeError:
        raise HTTPException(status=400, detail='Не поддерживаемые типы.')
