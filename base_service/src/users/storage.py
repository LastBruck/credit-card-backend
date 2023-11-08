"""User storage."""
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from base_service.src.db.models import Card
from base_service.src.db.models import User as UserModel
from base_service.src.users.users import User


class UserStorage:
    """Хранение пользователей."""

    _instance = None

    def __new__(cls):
        """Создание класса.

        Returns:
            _type_: _description_
        """
        if cls._instance is None:
            cls._instance = super(UserStorage, cls).__new__(cls)
            cls._instance.__active = {}
            cls._instance.__closed = {}
        return cls._instance

    async def add(self, card_number: str, info: dict, session: AsyncSession):
        """Добавление пользователей в хранилища.

        Args:
            card_number (str): номер карты
            info (dict): словарь с информацией о пользователе
            session (AsyncSession): сессия

        Raises:
            ValueError: исключение
        """
        if card_number in (self.__active or self.__closed):
            raise ValueError('Такой пользователь уже существует.')
        user = User(
            _balance=info.get('balance', Decimal('0')),
            card_number=card_number,
            limit=info.get('limit', Decimal('0')),
            info=info.get('info', ''),
        )
        self.__active[card_number] = user
        async with session.begin():
            user = UserModel(
                first_name=info.get('first_name', ''),
                last_name=info.get('last_name', ''),
            )
            card = Card(
                number=card_number,
                balance=info.get('balance', Decimal('0')),
                limit=info.get('limit', Decimal('0')),
                info=info.get('info', ''),
            )
            user.cards.append(card)
            session.add(user)
            await session.commit()

    def get_active(self):
        """Получение хранилища активных пользователей.

        Returns:
            dict: хранилище активных пользователей
        """
        return self.__active

    def get_closed(self):
        """Получение хранилища удалённых пользователей.

        Returns:
            dict: хранилище удалённых пользователей
        """
        return self.__closed

    def get_user(self, card_number: str) -> User:
        """Получение пользователя из хранилища активных.

        Args:
            card_number (str): номер карты

        Raises:
            ValueError: исключение

        Returns:
            User: пользователь
        """
        if card_number in self.__active:
            return self.__active.get(card_number)
        raise ValueError('Пользователь не найден.')

    async def update_user(self, user: User):
        """Обновление пользователя.

        Args:
            user (User): пользователь

        Raises:
            ValueError: исключение
        """
        if user.card_number in self.__active:
            self.__active.update({user.card_number: user})
        else:
            raise ValueError('Пользователь не найден.')

    def close(self, card_number: str):
        """Удаление пользователя из хранилища активных и добавление в загрытые.

        Args:
            card_number (str): номер карты

        Raises:
            ValueError: исключение
        """
        if card_number in self.__active:
            user = self.__active.pop(card_number)
            self.__closed[card_number] = user
        else:
            raise ValueError('Пользователь не найден.')
