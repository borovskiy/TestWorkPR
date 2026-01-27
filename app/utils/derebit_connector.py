import json
import logging

import aiohttp

from app.models import TypeCurrency
from app.schemas.deribit_price_schema_response import DeribitPriceSchemaResponseRPCResponse


class ConnectorDeribit:
    """
    Мини коннектор в бирже
    Но тут важно понимать что как только появится второй коннектор то надо будет делать интэрфейс, сейчас смысла нет делать
    """
    MAIN_API_LINK = "https://test.deribit.com/api/v2/public/"

    async def get_exchange_rate(self, type_currency: TypeCurrency) -> float:
        ## Просто запрашивает курс валюты
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    '{0}get_index_price?index_name={1}'.format(self.MAIN_API_LINK, type_currency.value)) as resp:
                if resp.status == 200:
                    resp = DeribitPriceSchemaResponseRPCResponse(**json.loads(await resp.text()))
                    return resp.result_data.index_price
                logging.error("Status {0}, text".format(resp.status, ))
                raise ErrorConnector("Request error status {0}".format(resp.status))


class ErrorConnector(Exception):
    def __init__(self, message):
        self.message = message
