import pytest
from decimal import Decimal

def test_user_creation_and_update(user_storage):
    card_number = '12345678900123456'
    user_info = {'first_name': 'Alex', 'last_name': 'Izek', 'info': 'NONE'}
    user_storage.add(card_number, user_info)
    user = user_storage.get_user(card_number)
    user.limit = -5000
    user.balance = -1000
    user_storage.update_user(user)
    updated_user = user_storage.get_user(card_number)  

    assert updated_user.balance == Decimal('-1000')
    assert updated_user.card_number == card_number
    assert updated_user.limit == Decimal('-5000')
    assert updated_user.info == user_info
    
    # Попытка обновить удалённого пользователя
    with pytest.raises(ValueError):
        user_storage.close(card_number)
        updated_user.info = {}
        user_storage.update_user(updated_user)


def test_balance_setter_with_valid_balance(user_storage, card_number_for_users):
    user_info = {'first_name': 'Alex', 'last_name': 'Izek', 'info': 'NONE'}
    user_storage.add(card_number_for_users, user_info)
    user = user_storage.get_user(card_number_for_users)
    user.limit = -5000
    user.balance = -1000
    user_storage.update_user(user)
    updated_user = user_storage.get_user(card_number_for_users) 
    updated_user.balance = Decimal('-2000')
    user_storage.update_user(updated_user)
    new_updated_user = user_storage.get_user(card_number_for_users)

    assert new_updated_user.balance == Decimal('-2000')
    
    #Попытка установить баланс меньше лимита
    with pytest.raises(ValueError):
        updated_user.balance = Decimal('-7000')

def test_user_storage_add_and_get_user(user_storage, card_number_for_users):
    info = {'first_name': 'Alex', 'last_name': 'Izek', 'info': 'NONE'}
    user = user_storage.get_user(card_number_for_users)

    assert user.info == info

    # Попытка сохранить дубликат пользователя
    with pytest.raises(ValueError):
        info = {'first_name': 'Alex', 'last_name': 'Izek', 'info': 'NONE'}
        user_storage.add(card_number_for_users, info)
    
    # Попытка получить не существующего пользователя
    with pytest.raises(ValueError):
        user_storage.get_user('7777777')


def test_user_storage_close(user_storage, card_number_for_users):
    user_storage.close(card_number_for_users)

    active_users = user_storage.get_active()
    closed_users = user_storage.get_closed()

    assert card_number_for_users not in active_users
    assert card_number_for_users in closed_users
    
    #Попытка удаления не существующего пользователя
    with pytest.raises(ValueError):
        user_storage.close('7777')
