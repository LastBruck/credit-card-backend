"""создание токена."""
from datetime import datetime, timedelta

from jose import jwt

import settings


def create_access_token(input_data: dict):
    """Создание токена авторизации.

    Args:
        input_data (dict): словарь с логином

    Returns:
        _type_: Токен
    """
    to_encode = input_data.copy()
    expire_date = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire_date})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
