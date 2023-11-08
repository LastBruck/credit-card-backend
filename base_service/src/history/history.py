"""История баланса."""
from datetime import datetime
from decimal import Decimal


class CommonLog:
    """Общий журнал."""

    def __init__(self, card_number: str, before: Decimal, after: Decimal, changes: Decimal):
        """Инициализация журнала.

        Args:
            card_number (str): номер карты
            before (Decimal): баланс ранее
            after (Decimal): баланс после
            changes (Decimal): изменение баланса
        """
        self.card_number = card_number
        self.before = before
        self.after = after
        self.changes = changes
        self.__datetime_utc: datetime = datetime.utcnow()

    def datetime_utc(self):
        """Получение информации об __datetime_utc.

        Returns:
            datetime: __datetime_utc
        """
        return self.__datetime_utc


class BalanceLog(CommonLog):
    """Журнал балансов."""

    def __init__(self, before: Decimal, after: Decimal, changes: Decimal):
        """Инициализация журнала.

        Args:
            before (Decimal): баланс ранее
            after (Decimal): баланс после
            changes (Decimal): изменение баланса
        """
        super().__init__('', before, after, changes)
