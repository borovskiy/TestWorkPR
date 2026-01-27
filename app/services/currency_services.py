import logging
from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TypeCurrency, Ticker
from app.repository.price_repo import PriceRepo
from app.schemas.currency_schema_response import CurrencyFiltersSchema
from app.schemas.paginate_schema import PaginationGetCurrencies, CurrenciesPage, PageMeta
from app.utils.derebit_connector import ConnectorDeribit


class PriceRepoService:
    def __init__(self, session: AsyncSession):  # Теперь синхронная сессия
        self.session = session
        self.price_repo = PriceRepo(self.session)
        self.connector = ConnectorDeribit()

    async def add_currency(self, data: dict):
        logging.info("add_currency")
        result = await self.price_repo.add_currency_value(data)
        logging.info("add_currency result {0}".format(result))
        return result

    async def get_expose_currency(self, type_currency: TypeCurrency):
        ## Получить значение валюты на внешнем сайте
        logging.info("get_currency")
        result = await self.connector.get_exchange_rate(type_currency)
        logging.info("get_currency result {0}".format(result))
        return result

    async def process_add_in_db_currency(self, type_currency: TypeCurrency):
        ## Процесс получания валюты и добавления в бд
        ## Коммит вынесен сюда по привычке юнит оф ворка
        logging.info("process_update_currency")
        result = await self.get_expose_currency(type_currency)
        new_price_obj = Ticker(ticker=type_currency.value, price=result)
        logging.info("new_price_obj {0}".format(new_price_obj))
        await self.add_currency(new_price_obj.to_dict())
        await self.session.commit()
        logging.info("commit")
        return result

    async def get_currency_db(self, pag_data: PaginationGetCurrencies, filters: CurrencyFiltersSchema) -> CurrenciesPage:
        ## Процесс получения валюты с фильтром и пагинацией
        logging.info("get_currency_db")
        prices, total = await self.price_repo.get_currency_filters(pag_data, filters)
        pages = ceil(total / pag_data.page_size) if pag_data.page_size else 1
        logging.info("total result {0}".format(total))
        return CurrenciesPage(
            meta=PageMeta(total=total, limit=pag_data.page_size, pages=pages),
            currencies=prices,
        )