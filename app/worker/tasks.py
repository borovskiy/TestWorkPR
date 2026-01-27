import asyncio
import logging

from app.core.db_connector import get_async_db
from app.models import TypeCurrency
from app.services.currency_services import PriceRepoService
from app.worker.celery import app


@app.task
def test_task(type_currency: str):
    """Синхронная обертка для асинхронной операции"""
    try:
        # Получаем текущий event loop или создаем новый
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # Если нет текущего loop (например, в отдельном потоке)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Запускаем асинхронную операцию
    logging.info("Start {0} currency worker".format(type_currency))
    result = loop.run_until_complete(async_process_currency(type_currency))
    return result


async def async_process_currency(type_currency_str: str):
    """Асинхронная логика обработки валюты"""
    async with get_async_db() as session:
        service = PriceRepoService(session)
        type_currency = TypeCurrency.parse(type_currency_str)
        data = await service.process_add_in_db_currency(type_currency)
        logging.info("Result {0} currency worker".format(data))
        return True
