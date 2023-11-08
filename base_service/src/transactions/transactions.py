"""Транзакции."""
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base_service.src.db.models import Card
from base_service.src.history.history import CommonLog
from base_service.src.history.log_storage import LogStorage
from base_service.src.users.storage import UserStorage


class Transactions:
    """Операции."""

    def __init__(self, user_storage: UserStorage, history: LogStorage):
        """Инициализация.

        Args:
            user_storage (UserStorage): хранилище пользователя
            history (LogStorage): хранилище логов
        """
        self.storage = user_storage
        self.history = history

    def get_balance(self, card_number: str) -> Decimal:
        """Получить баланс пользователя.

        Args:
            card_number (str): номер карты.

        Returns:
            Decimal: баланс пользователя
        """
        user = self.storage.get_user(card_number)
        return user.balance

    async def withdrawal(self, card_number: str, amount: Decimal, session: AsyncSession):
        """Списание с баланса.

        Args:
            card_number (str): номер карты
            amount (Decimal): число
            session (AsyncSession): сессия

        Raises:
            ValueError: исключение
        """
        if self.__check_amount(amount):
            user = self.storage.get_user(card_number)
            old_balance = user.balance
            new_balance = user.balance - amount
            await self.__change_balance(card_number, new_balance, session)
            log_entry = CommonLog(card_number, old_balance, new_balance, -amount)
            self.history.save(log_entry)
        else:
            raise ValueError('Списание невозможно. Сумма должна быть положительной.')

    async def deposit(self, card_number: str, amount: Decimal, session: AsyncSession):
        """Пополнение баланса.

        Args:
            card_number (str): номер карты
            amount (Decimal): число
            session (AsyncSession): сессия

        Raises:
            ValueError: исключение
        """
        if self.__check_amount(amount):
            user = self.storage.get_user(card_number)
            old_balance = user.balance
            new_balance = user.balance + amount
            await self.__change_balance(card_number, new_balance, session)
            log_entry = CommonLog(card_number, old_balance, new_balance, amount)
            self.history.save(log_entry)
        else:
            raise ValueError('Пополнение баланса невозможно. Сумма должна быть положительной.')

    def update_info(self, card_number: str, new_info: dict):
        """Обновление info пользователя.

        Args:
            card_number (str): номер карты
            new_info (dict): словарь
        """
        user = self.storage.get_user(card_number)
        user.info.update(new_info)

    async def change_limit(self, card_number: str, new_limit: Decimal, session: AsyncSession):
        """Изменение лимита.

        Args:
            card_number (str): номер карты
            new_limit (Decimal): новый лимит
            session (AsyncSession): сессия

        Raises:
            ValueError: исключение
        """
        user = self.storage.get_user(card_number)
        if new_limit < user.balance:
            user.limit = new_limit
            async with session.begin():
                card_to_update = await session.execute(select(Card).filter_by(number=card_number))
                card_to_update = card_to_update.scalar_one_or_none()
                if card_to_update:
                    card_to_update.limit = new_limit
                    await session.commit()
        else:
            raise ValueError('Изменение лимита невозможно. Лимит должен быть меньше баланса.')

    async def __change_balance(self, card_number: str, amount: Decimal, session: AsyncSession):
        """Изменение баланса пользователя.

        Args:
            card_number (str): номер карты
            amount (Decimal): число
            session (AsyncSession): сессия
        """
        user = self.storage.get_user(card_number)
        user.balance = amount
        self.storage.update_user(user)
        async with session.begin():
            card_to_update = await session.execute(select(Card).filter_by(number=card_number))
            card_to_update = card_to_update.scalar_one_or_none()
            if card_to_update:
                card_to_update.balance = amount
                await session.commit()

    @staticmethod
    def __check_amount(amount: Decimal) -> bool:
        """Проверка, что amount положительный.

        Args:
            amount (Decimal): число

        Returns:
            bool: True или False
        """
        return amount >= Decimal('0.00')
