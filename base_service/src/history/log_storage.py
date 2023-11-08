"""Log Storage."""
from collections import defaultdict
from datetime import datetime

from base_service.src.history.history import BalanceLog, CommonLog


class LogStorage:
    """Хранение логов."""

    _instance = None

    def __new__(cls):
        """Создание класса.

        Returns:
            _type_: _description_
        """
        if cls._instance is None:
            cls._instance = super(LogStorage, cls).__new__(cls)
            cls._instance.__balance_logs = defaultdict(list)
            cls._instance.__other_logs = []
        return cls._instance

    def save(self, log: CommonLog):
        """Сохранение в логи.

        Args:
            log (CommonLog): входящий лог

        Raises:
            ValueError: сообщение
        """
        if isinstance(log, CommonLog):
            self.__balance_logs[log.card_number].append(BalanceLog(log.before, log.after, log.changes))
            self.__other_logs.append(log)
        else:
            raise ValueError('Не подходящий тип лога.')

    def get_balance_history(self, card_number: str, from_date: datetime, to_date: datetime) -> list[BalanceLog]:
        """Получение списка по указанным параметрам.

        Args:
            card_number (str): номер карты
            from_date (datetime): дата от
            to_date (datetime): дата до

        Raises:
            ValueError: сообщение

        Returns:
            list[BalanceLog]: список логов баланса
        """
        if card_number in self.__balance_logs:
            return [log for log in self.__balance_logs.get(card_number, []) if from_date <= log.datetime_utc() <= to_date]
        raise ValueError('Пользователь не найден.')
