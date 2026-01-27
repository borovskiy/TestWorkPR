from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.db_connector import price_repo_services
from app.models import TypeCurrency
from app.schemas.currency_schema_response import CurrencyFiltersSchema
from app.schemas.paginate_schema import PaginationGetCurrencies, CurrenciesPage
from app.services.currency_services import PriceRepoService

router = APIRouter(
    prefix="/currencies",
    tags=["Сurrencies"],
)


@router.get("/",
            response_model=CurrenciesPage,
            status_code=200, )
async def get_all_currencies(
        price_serv: Annotated[PriceRepoService, Depends(price_repo_services)],
        pag_data: PaginationGetCurrencies = Depends(PaginationGetCurrencies),
        filters: CurrencyFiltersSchema = Depends(CurrencyFiltersSchema),

):
    """

    :param price_serv:
    :param pag_data:
    :param filters:
    :return:
    """
    return await price_serv.get_currency_db(pag_data, filters)


@router.get("/add_new_currency", status_code=200, )
async def add_new_currency(
        price_serv: Annotated[PriceRepoService, Depends(price_repo_services)],
):
    return await price_serv.process_add_in_db_currency(TypeCurrency.btc_usd)
