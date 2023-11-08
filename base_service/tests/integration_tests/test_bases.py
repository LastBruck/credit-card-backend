from fastapi.testclient import TestClient

from base_service.src.db.models import storage
from base_service.src.main import app

client = TestClient(app)


def test_get_balance(card_number_for_rout):
    #Создаём пользователя:
    storage.add(card_number=card_number_for_rout, info={})
    #Попытка получить баланс
    response = client.get(
        '/api/balance', params={'card_number': card_number_for_rout},
    )
    
    user = response.json()
    assert response.status_code == 200
    assert user['balance'] == 0


def test_get_balance_non_existent_card():
    #Попытка получить баланс не существующей карты.
    response = client.get(
        '/api/balance', params={'card_number': '77777'},
    )
    assert response.status_code == 404


def test_deposit_balance(card_number_for_rout):
    #Дополняем данные о пользователе
    user = storage.get_user(card_number=card_number_for_rout)
    user.limit = -2000
    user.balance = -500
    storage.update_user(user)
    
    #Попытка пополнить баланс
    response = client.post(
        '/api/deposit', params={'card_number': card_number_for_rout, 'amount': 100},
    )
    assert response.status_code == 200
    

def test_deposit_balance_non_existent_card():
    #Попытка пополнить баланс не существующего пользователя
    response = client.post(
        '/api/deposit', params={'card_number': '77777', 'amount': 100},
    )
    assert response.status_code == 404


def test_deposit_balance_negative_amount(card_number_for_rout):
    #Попытка пополнить баланс отрицательной суммой
    response = client.post(
        '/api/deposit', params={'card_number': card_number_for_rout, 'amount': -100},
    )
    assert response.status_code == 404


def test_withdrawal_balance(card_number_for_rout):
    #Попытка списать деньги с баланса
    response = client.post(
        '/api/withdrawal', params={'card_number': card_number_for_rout, 'amount': 200},
    )
    assert response.status_code == 200


def test_withdrawal_balance_non_existent_card():
    #Попытка списать деньги с баланса не существующего пользователя
    response = client.post(
        '/api/withdrawal', params={'card_number': '77777', 'amount': 200},
    )
    assert response.status_code == 404


def test_withdrawal_balance_negative_amount(card_number_for_rout):
    #Попытка списать деньги с баланса отрицательной суммой
    response = client.post(
        '/api/withdrawal', params={'card_number': card_number_for_rout, 'amount': -200},
    )
    assert response.status_code == 404


def test_get_balance_to_get_the_balance_below_the_limit(card_number_for_rout):
    #Попытка списать деньги с баланса чтобы баланс стал ниже лимита
    response = client.post(
        '/api/withdrawal', params={'card_number': card_number_for_rout, 'amount': 3000},
    )
    assert response.status_code == 404


def test_get_balance_history(card_number_for_rout):
    #Попытка получить историю баланса пользователя
    response = client.get(
        '/api/balance/history', 
        params={'card_number': card_number_for_rout, 'from_date': '2023-02-02T14:30:00', 'to_date': '2023-12-02T14:30:00'},
    )
    assert response.status_code == 200
    data = response.json()
    assert data[0]['after'] == -400
    assert data[1]['after'] == -600


def test_get_balance_history_non_existent_card():
    #Попытка получить историю баланса не существующей карты.
    response = client.get(
        '/api/balance/history', params={'card_number': '77777', 'from_date': '2023-02-02T14:30:00', 'to_date': '2023-10-02T14:30:00'},
    )
    assert response.status_code == 404


def test_get_balance_history_without_date(card_number_for_rout):
    #Попытка получить историю баланса без даты.
    response = client.get(
        '/api/balance/history', params={'card_number': card_number_for_rout, 'from_date': '', 'to_date': ''},
    )
    assert response.status_code == 422


def test_get_balance_history_without_date_to(card_number_for_rout):
        #Попытка получить историю баланса без даты ДО.
    response = client.get(
        '/api/balance/history', params={'card_number': card_number_for_rout, 'from_date': '2023-02-02T14:30:00', 'to_date': ''},
    )
    assert response.status_code == 422
    