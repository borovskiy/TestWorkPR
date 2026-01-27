from typing import Sequence

from pydantic import Field

from app.schemas.base_schema import BaseModelSchema
from app.schemas.currency_schema_response import CurrencySchema

## Схемы для пагинаций
class PaginationGetBase(BaseModelSchema):
    page: int = Field(default=0, ge=0)
    page_size: int = Field(default=10, ge=1)


class PageMeta(BaseModelSchema):
    total: int
    limit: int
    pages: int


class BasePage(BaseModelSchema):
    meta: PageMeta


class PaginationGetCurrencies(PaginationGetBase):
    ...


class CurrenciesPage(BasePage):
    currencies: Sequence[CurrencySchema]
