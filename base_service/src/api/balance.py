"""Баланс."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from base_service.src.db.models import BalanceUser
from base_service.src.history.log_storage import LogStorage
from base_service.src.transactions.transactions import Transactions
from base_service.src.users.storage import UserStorage
from session import get_session

storage = UserStorage()
history = LogStorage()
transactions = Transactions(storage, history)

get_user = APIRouter()


@get_user.get('/')
async def find_user(
    card_number: str,
):
    """Создание нового пользователя.

    Args:
        card_number (str): номер карты

    Raises:
        HTTPException: исключение

    Returns:
        User: User
    """
    try:
        return storage.get_user(card_number)
    except ValueError as ve:
        raise HTTPException(
            status_code=404, detail=str(ve),
        )


create_user = APIRouter()


@create_user.post('/')
async def new_user(
    card_number: str,
    info: dict,
    db: AsyncSession = Depends(get_session),
):
    """Создание нового пользователя.

    Args:
        card_number (str): номер карты
        info (dict): инфо
        db (AsyncSession): сессия

    Raises:
        HTTPException: исключение
    """
    try:
        await storage.add(card_number, info, db)
    except ValueError as ve:
        raise HTTPException(
            status_code=404, detail=str(ve),
        )

balance = APIRouter()


@balance.get('/', response_model=BalanceUser)
async def get_balance(
    card_number: str,
) -> BalanceUser:
    """Получение баланса пользователя.

    Args:
        card_number (str): номер карты

    Raises:
        HTTPException: исключение

    Returns:
        BalanceUser: BalanceUser
    """
    try:
        balance_user = transactions.get_balance(card_number)
        return BalanceUser(card_number=card_number, balance=balance_user)
    except ValueError as ve:
        raise HTTPException(
            status_code=404, detail=str(ve),
        )

get_history = APIRouter()


@get_history.get('/')
async def get_balance_history(
    card_number: str,
    from_date: datetime,
    to_date: datetime,
):
    """Получение истории баланса пользователя.

    Args:
        card_number (str): номер карты
        from_date (datetime): дата ОТ
        to_date (datetime): дата ДО

    Raises:
        HTTPException: исключение

    Returns:
        _type_: list[BalanceLog]
    """
    try:
        return history.get_balance_history(card_number, from_date, to_date)
    except ValueError as ve:
        raise HTTPException(
            status_code=404, detail=str(ve),
        )
