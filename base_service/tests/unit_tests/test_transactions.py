import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from base_service.src.transactions.transactions import Transactions
from base_service.src.history.history import BalanceLog


def test_get_balance(transactions, user_storage, card_number_for_transac):
    # Добавляем тестовых пользователей
    user_info = {'name': 'Alex', 'email': 'alex@test.com'}
    user_storage.add(card_number_for_transac, user_info)
    user = user_storage.get_user(card_number_for_transac)
    user.balance = Decimal('1000.00')
    user_storage.update_user(user)
    # Проверяем метод get_balance
    balance = transactions.get_balance(card_number_for_transac)
    assert balance == Decimal('1000.00')

def test_withdrawal(transactions, history, card_number_for_transac):
    # Проверяем метод withdrawal
    amount = Decimal('500.00')
    transactions.withdrawal(card_number_for_transac, amount)
    
    # Проверяем, что баланс уменьшился
    assert transactions.get_balance(card_number_for_transac) == Decimal('500.00')
    
    # Проверяем, что в истории есть соответствующая запись
    logs = history.get_balance_history(card_number_for_transac, datetime.utcnow() - timedelta(days=1), datetime.utcnow())
    assert len(logs) == 1
    log_entry = logs[0]
    assert isinstance(log_entry, BalanceLog)
    assert log_entry.changes == -amount
    
    # Попытка списать отрицательную сумму
    with pytest.raises(ValueError):
        transactions.withdrawal(card_number_for_transac, Decimal('-1200.00'))


def test_deposit(transactions, history, card_number_for_transac):
    # Проверяем метод deposit
    amount = Decimal('200.00')
    transactions.deposit(card_number_for_transac, amount)
    
    # Проверяем, что баланс увеличился
    assert transactions.get_balance(card_number_for_transac) == Decimal('700.00')
    
    # Проверяем, что в истории есть соответствующая запись
    logs = history.get_balance_history(card_number_for_transac, datetime.utcnow() - timedelta(days=1), datetime.utcnow())
    assert len(logs) == 2
    log_entry = logs[1]
    assert isinstance(log_entry, BalanceLog)
    assert log_entry.changes == amount
    
    # Попытка положить отрицательную сумму
    with pytest.raises(ValueError):
        transactions.deposit(card_number_for_transac, Decimal('-1200.00'))

def test_update_info(transactions, user_storage, card_number_for_transac):
    # Проверяем метод update_info
    new_info = {'name': 'Bobby', 'email': 'BOBB@test.com'}
    transactions.update_info(card_number_for_transac, new_info)
    
    # Проверяем, что информация пользователя обновилась
    user = user_storage.get_user(card_number_for_transac)
    assert user.info == new_info


def test_change_limit(transactions, user_storage, card_number_for_transac):
    # Проверяем метод change_limit
    new_limit = Decimal('-800.00')
    transactions.change_limit(card_number_for_transac, new_limit)
    
    # Проверяем, что лимит изменился
    user = user_storage.get_user(card_number_for_transac)
    assert user.limit == new_limit

    # Попытка установить лимит больше баланса
    with pytest.raises(ValueError):
        transactions.change_limit(card_number_for_transac, Decimal('1200.00'))

def test_check_amount():
    # Проверяем статический метод __check_amount
    valid_amount = Decimal('100.00')
    assert Transactions._Transactions__check_amount(valid_amount) == True
    invalid_amount = Decimal('-100.00')
    assert Transactions._Transactions__check_amount(invalid_amount) == False
