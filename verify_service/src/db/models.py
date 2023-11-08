"""Модели."""
from pydantic import BaseModel


class VerificationResponse(BaseModel):
    """Модель сериализатора VerificationResponse."""

    verified: bool
