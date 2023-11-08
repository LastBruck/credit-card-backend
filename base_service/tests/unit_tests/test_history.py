import pytest
from datetime import datetime
from decimal import Decimal

from base_service.src.history.history import CommonLog, BalanceLog

#Тесты для класса CommonLog
def test_common_log_init():
    card_number = "1234-5678-9012-3456"
    before = Decimal("100.00")
    after = Decimal("150.00")
    changes = Decimal("50.00")
    log = CommonLog(card_number, before, after, changes)

    assert log.card_number == card_number
    assert log.before == before
    assert log.after == after
    assert log.changes == changes
    assert isinstance(log.datetime_utc(), datetime)

# Тесты для класса BalanceLog
def test_balance_log_init():
    card_number = "1234-5678-9012-3456"
    before = Decimal("100.00")
    after = Decimal("150.00")
    changes = Decimal("50.00")
    balance_log = CommonLog(card_number, before, after, changes)

    assert balance_log.card_number == card_number
    assert balance_log.before == before
    assert balance_log.after == after
    assert balance_log.changes == changes
    assert isinstance(balance_log.datetime_utc(), datetime)

#Тесты для класса LogStorage
def test_log_storage_save_balance_log(history):
    card_number = "1234-5678-9012-3456"
    before = Decimal("100.00")
    after = Decimal("150.00")
    changes = Decimal("50.00")
    balance_log = CommonLog(card_number, before, after, changes)
    history.save(balance_log)

    assert len(history._LogStorage__balance_logs[card_number]) == 1
    
    #Попытка сохранить лог с не подходящим типом.
    with pytest.raises(ValueError):
        history.save(['2', '2', '2', '2', ''])

def test_log_storage_get_balance_history(history):
    card_number = "1234-5678-9012-3456"
    before = Decimal("100.00")
    after = Decimal("150.00")
    changes = Decimal("50.00")
    balance_log = CommonLog(card_number, before, after, changes)
    history.save(balance_log)

    from_date = datetime(2023, 1, 1)
    to_date = datetime(2023, 12, 31)

    history_list = history.get_balance_history(card_number, from_date, to_date)
    
    assert len(history_list) == 2
    assert history_list[1].before == balance_log.before
    
    with pytest.raises(ValueError):
        history.get_balance_history('123321', from_date, to_date)
