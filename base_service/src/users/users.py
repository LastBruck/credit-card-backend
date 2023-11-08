"""Пользователи."""
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class User:
    """Модель пользователя."""

    _balance: Decimal
    card_number: str
    limit: Decimal
    info: dict

    @property
    def balance(self):
        """Получение информации _balance.

        Returns:
            Decimal: _balance
        """
        return self._balance

    @balance.setter
    def balance(self, balance):
        """Редактирование _balance.

        Args:
            balance (Decimal): новый баланс

        Raises:
            ValueError: исключение
        """
        if balance < self.limit:
            raise ValueError('Баланс не может быть меньше лимита.')
        self._balance = balance
