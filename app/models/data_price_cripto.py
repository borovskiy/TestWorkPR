import enum
from typing import Union

from sqlalchemy import Enum, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class TypeCurrency(enum.Enum):
    btc_usd = "btc_usd"
    eth_usd = "eth_usd"

    @classmethod
    def parse(cls, value: Union[str, 'TypeCurrency']) -> 'TypeCurrency':
        """Принимает строку или TypeCurrency, возвращает TypeCurrency"""
        if isinstance(value, cls):
            return value
        return cls(value)


class Price(BaseModel):
    """
    Модель с данными о валютах
    """
    __tablename__ = "cur_price"
    type_currency: Mapped[TypeCurrency] = mapped_column(Enum(TypeCurrency), nullable=False)
    price: Mapped[float] = mapped_column(Float(), nullable=False)
