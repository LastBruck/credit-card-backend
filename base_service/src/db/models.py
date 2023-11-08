"""Base модели."""
from decimal import Decimal

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeMeta, declarative_base, relationship

Base: DeclarativeMeta = declarative_base()


class User(Base):
    """Модель юзера."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    cards = relationship('Card', back_populates='user')


class Card(Base):
    """Модель карты."""

    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    number = Column(String, unique=True, nullable=False)
    balance = Column(Numeric, nullable=False)
    limit = Column(Numeric, nullable=False)
    info = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='cards')


class BalanceUser(BaseModel):
    """Модель сериализатора BalanceUser."""

    card_number: str
    balance: Decimal
