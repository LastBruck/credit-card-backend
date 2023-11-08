"""models auth."""
from decimal import Decimal

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class Admin(Base):
    """Модель администратора.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)


class TokenModel(BaseModel):
    """Модель сериализатора TokenModel."""

    access_token: str
    token_type: str


class BalanceUser(BaseModel):
    """Модель сериализатора BalanceUser."""

    card_number: str
    balance: Decimal
