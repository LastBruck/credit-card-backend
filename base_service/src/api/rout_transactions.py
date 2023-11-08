"""Операции."""
from decimal import Decimal

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

deposit = APIRouter()


@deposit.post('/', response_model=BalanceUser)
async def deposit_post(
    card_number: str,
    amount: Decimal,
    db: AsyncSession = Depends(get_session),
) -> BalanceUser:
    """Пополнение баланса.

    Args:
        card_number (str): номер карты
        amount (Decimal): сумма пополнения
        db (AsyncSession): сессия

    Raises:
        HTTPException: исключение

    Returns:
        BalanceUser: BalanceUser
    """
    try:
        await transactions.deposit(card_number, amount, db)
        balance = transactions.get_balance(card_number)
        return BalanceUser(card_number=card_number, balance=balance)
    except ValueError as ve:
        raise HTTPException(
            status_code=404, detail=str(ve),
        )

withdrawal = APIRouter()


@withdrawal.post('/', response_model=BalanceUser)
async def withdrawal_post(
    card_number: str,
    amount: Decimal,
    db: AsyncSession = Depends(get_session),
) -> BalanceUser:
    """Списание средств с баланса.

    Args:
        card_number (str): номер карты
        amount (Decimal): сумма списания
        db (AsyncSession): сессия

    Raises:
        HTTPException: исключение

    Returns:
        BalanceUser: BalanceUser
    """
    try:
        await transactions.withdrawal(card_number, amount, db)
        balance = transactions.get_balance(card_number)
        return BalanceUser(card_number=card_number, balance=balance)
    except ValueError as ve:
        raise HTTPException(
            status_code=404, detail=str(ve),
        )

change_limit = APIRouter()


@change_limit.post('/')
async def change_limit_after_verify(
    card_number: str,
    verified: bool,
    db: AsyncSession = Depends(get_session),
):
    """Изменение лимита после верификации.

    Args:
        card_number (str): номер карты
        verified (bool): результат верификации
        db (AsyncSession): сессия

    Raises:
        HTTPException: исключение
    """
    try:
        if verified:
            await transactions.change_limit(card_number, -100000, db)
        else:
            await transactions.change_limit(card_number, -20000, db)
    except ValueError as ve:
        raise HTTPException(
            status_code=404, detail=str(ve),
        )
