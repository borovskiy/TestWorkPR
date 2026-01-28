from datetime import datetime
from typing import Optional

from fastapi import Query, HTTPException
from pydantic import model_validator
from starlette import status

from app.models import TypeCurrency
from app.schemas.base_schema import BaseModelSchema


class CurrencySchema(BaseModelSchema):
    id: int
    ticker: str
    price: float
    created_at: int


class CurrencyFiltersSchema(BaseModelSchema):
    ## Схема для параметров с валидацией по логике определенной
    ticker: TypeCurrency
    last_value: Optional[bool] = Query(
        False,
        description="Получить только последние значения"
    )
    all_value: Optional[bool] = Query(
        False,
        description="Получить все значения"
    )
    start_timestamp: Optional[int] = Query(
        None,
        description="Начальный timestamp (Unix time в секундах)",
        examples=[1704067200]
    )
    end_timestamp: Optional[int] = Query(
        None,
        description="Конечный timestamp (Unix time в секундах)",
        examples=[1735689599]
    )

    @model_validator(mode='after')
    def validate_mutually_exclusive(self) -> 'CurrencyFiltersSchema':
        """Валидация взаимоисключающих параметров"""
        if self.last_value:
            # При last_value=True нельзя указывать другие параметры
            if self.all_value:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='last_value и all_value не могут быть True одновременно')

            if self.start_timestamp or self.end_timestamp:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='При last_value=True нельзя указывать start_date или end_date')

        # Проверка дат - должны быть указаны обе или ни одна
        if (self.start_timestamp and not self.end_timestamp) or (not self.start_timestamp and self.end_timestamp):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='start_date и end_date должны быть указаны вместе')
        # Проверка, что end_date не раньше start_date
        if self.start_timestamp and self.end_timestamp and self.end_timestamp < self.start_timestamp:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='end_date не может быть раньше start_date')

        return self

    class Config:
        from_attributes = True
