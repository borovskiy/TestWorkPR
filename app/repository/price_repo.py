import logging

from sqlalchemy import select, func, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Price
from app.schemas.currency_schema_response import CurrencyFiltersSchema
from app.schemas.paginate_schema import PaginationGetCurrencies


class PriceRepo:
    def __init__(self, session: AsyncSession):
        self.log = logging.LoggerAdapter(
            logging.getLogger(__name__),
            {"component": self.__class__.__name__}
        )
        self.session = session
        self.main_model = Price

    async def add_currency_value(self, data: dict):
        ## добавление валюты в БД
        self.log.info("add_currency_value {0}".format(data))
        model_fields = self.main_model.__table__.columns.keys()
        filtered_data = {k: v for k, v in data.items() if k in model_fields}
        self.log.info("filtered_data {0}".format(filtered_data))
        obj = self.main_model(**filtered_data)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_currency_filters(self, pag_data: PaginationGetCurrencies, filters: CurrencyFiltersSchema):
        ## Получаем валюты с фильтрами
        logging.info("get_currency_filters")
        page = pag_data.page
        page_size = pag_data.page_size

        stmt = select(self.main_model).where(
            self.main_model.type_currency == filters.type_currency
        ).order_by(desc(self.main_model.created_at))

        if filters.last_value:
            stmt_paginated = stmt.limit(1)
            total = 1
        else:
            if filters.start_timestamp and filters.end_timestamp:
                stmt = stmt.where(
                    and_(
                        self.main_model.created_at >= filters.start_timestamp,
                        self.main_model.created_at <= filters.end_timestamp
                    )
                )

            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = (await self.session.execute(count_stmt)).scalar() or 0

            stmt_paginated = (
                stmt.order_by(self.main_model.id.desc())
                .offset(page * page_size)
                .limit(page_size)
            )
        result = await self.session.execute(stmt_paginated)
        rows = result.scalars().all()

        return rows, total
