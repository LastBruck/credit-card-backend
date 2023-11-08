from datetime import datetime, timedelta
from decimal import Decimal

def test_integration_scenario(user_storage, history, transactions):
    card_number = "1234"
    info = {'name': 'Bob'}

    # Открытие карты
    user_storage.add(card_number, info)
    user_balance = transactions.get_balance(card_number)
    assert user_balance == Decimal('0.00')

    # Пополнение средств
    transactions.deposit(card_number, Decimal('100.00'))
    user_balance = transactions.get_balance(card_number)
    assert user_balance == Decimal('100.00')

    # Снятие средств
    transactions.withdrawal(card_number, Decimal('50.00'))
    user_balance = transactions.get_balance(card_number)
    assert user_balance == Decimal('50.00')

    # Запрос истории баланса
    logs = history.get_balance_history(card_number, datetime.utcnow() - timedelta(days=1), datetime.utcnow())
    assert len(logs) == 2  # Должно быть две записи
    