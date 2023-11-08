"""Авторизация."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from auth_service.src.controllers.security import create_access_token
from auth_service.src.db.models import Admin, TokenModel
from session import get_session

auth = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')


async def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)):
    """Геттер корректного пользователя по токену.

    Args:
        token (str): токен авторизации. Defaults to Depends(oauth2_scheme).
        db (AsyncSession): БД. Defaults to Depends(get_session).

    Raises:
        raise_exception: исключение
        raise_exception: исключение
        raise_exception: исключение

    Returns:
        _type_: user
    """
    raise_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось подтвердить учетные данные.',
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM],
        )
        username = payload.get('sub')
        if username is None:
            raise raise_exception
    except JWTError:
        raise raise_exception
    user = await get_user_by_username_for_auth(username=username, session=db)
    if user is None:
        raise raise_exception
    return user


async def get_user_by_username_for_auth(username: str, session: AsyncSession):
    """Проверка и получение данных пользователя в БД.

    Args:
        username (str): логин
        session : БД

    Returns:
        _type_: данные администратора
    """
    async with session.begin():
        query = select(Admin).where(Admin.username == username)
        res = await session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]


async def authenticate_user(username: str, password: str, db: AsyncSession):
    """Аутентификация пользователя.

    Args:
        username (str): логин
        password (str): пароль
        db (AsyncSession): БД

    Returns:
        _type_: данные администратора
    """
    user = await get_user_by_username_for_auth(username=username, session=db)
    if user is None:
        return None
    if password != user.password:
        return None
    return user


@auth.post('/token', response_model=TokenModel)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session),
):
    """Аутентификация, получение токена.

    Args:
        form_data (OAuth2PasswordRequestForm): данные из формы. Defaults to Depends().
        db (AsyncSession) : БД. Defaults to Depends().

    Raises:
        HTTPException: исключение

    Returns:
        dict: словарь с токеном
    """
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не верный логин или пароль.',
        )
    access_token = create_access_token(
        input_data={'sub': user.username, 'other_data': [1, 2, 3]},
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
